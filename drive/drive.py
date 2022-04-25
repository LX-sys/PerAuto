# -*- coding:utf-8 -*-
# @time:2022/4/1423:49
# @author:LX
# @file:drive.py
# @software:PyCharm
from __future__ import print_function
from color import PrintColor
from utils import to_driver_path
from error import DriveError, ExecutablePathError
from compat import (
    sys,
    WebDriver,
    webdriver
)

# 处理编码问题
try:
    reload(sys)
    sys.setdefaultencoding(r"utf-8")
except:
    pass


# ORM驱动映射
class DriveVerification(object):
    '''
        驱动验证,并创建驱动
    '''

    def __init__(self, *paths):
        self.path_list = set(paths) if paths else ["chromedriver.exe"]
        # 真正的驱动
        self.drive = None  # type:webdriver
        # 外部传入的路径
        self.external_path = ""

    def __set__(self, instance, value):
        if self.verification(value):
            self.creative()

    def __get__(self, instance, owner):
        return self.drive  # type:webdriver

    def verification(self, value):
        '''
            验证
        :param value:
        :return:
        '''
        if value is None:
            return False

        temp_error = {
            "WebDriver": False,
            "str": False
        }
        if isinstance(value, WebDriver):
            print("The driver added successfully!")
            self.drive = value
            return False
        else:
            temp_error["WebDriver"] = True

        if isinstance(value, str):
            for v in self.path_list:
                if v in value:
                    self.external_path = value
                    print("The driver path is added successfully!")
                    return True
            temp_error["str"] = True

        # 如果外部驱动 和 驱动路径一样都没有,则报错
        if temp_error["WebDriver"]:
            raise DriveError("Driver error!:{}".format(value))

        if temp_error["str"]:
            raise ExecutablePathError("There is no such path:{}!".format(value))

    def creative(self):
        self.drive = (webdriver.Chrome, self.external_path)
        # self.drive = webdriver.Chrome(executable_path=self.external_path)


# ORM配置映射
class OptionVerification(object):

    def __init__(self, *args):
        self.__chromeOptions = webdriver.ChromeOptions()
        self._args = args
        self._args_len = len(self._args)
        self._type = ""  # 类型

    @staticmethod
    def doc_():
        return {
            u"headless": u"无头(无界面)模式",
            u"win_max": u"浏览器最大化",
            u"zh_cn_utf8": u"设置utf8编码",
            u"prefs": u"去除网页通知",
            u"disable_info_bar": u"禁止浏览器正被自动化程序控制的提示"
        }

    def __set__(self, instance, value):
        if value is True:
            self.add()
        elif value is False:
            self.delete()
        elif value is None:
            pass
        else:
            raise ValueError("The argument can only be True or False!:{}".format(value))

    # 返回配置格式的空客
    def ghost(self):
        return self.__chromeOptions.to_capabilities()

    # 判断该项是否激活
    def is_activate(self):
        if self.__chromeOptions.arguments or self.__chromeOptions.experimental_options:
            return True
        return False

    def get_option(self):
        if self._args_len == 1:
            return self._args[0]
        elif self._args_len == 2:
            return {self._args[0]: self._args[1]}

    # 添加配置
    def add(self):
        if not self.__chromeOptions.arguments and self._args_len == 1:
            self.__chromeOptions.add_argument(*self._args)
        elif not self.__chromeOptions.experimental_options and self._args_len == 2:
            self.__chromeOptions.add_experimental_option(*self._args)

    def delete(self):
        if self.__chromeOptions.arguments:
            del self.__chromeOptions.arguments[-1]
        elif self.__chromeOptions.experimental_options:
            del self.__chromeOptions.experimental_options[self._args[0]]

    def __get__(self, instance, owner):
        if self._args_len == 1 and self.__chromeOptions.arguments:
            return {self._args[0]: None}
        elif self._args_len == 2 and self.__chromeOptions.experimental_options:
            return {self._args[0]: self._args[1]}
        return None


# 启动配置类(可以继承它,添加自己的方法)
class Options(object):
    '''
        仿写原生Options
        启动配置类
        这个类必须在浏览器驱动创建之前创建
        这个类可以被继承,自定义点击方法和下面一样
        # 启动方法:
            op = Options()
            op.zh_cn_utf8 = True   # True启动,False关闭
            op.prefs = True
    '''
    # 配置
    zh_cn_utf8 = OptionVerification("lang=zh_CN.UTF-8")
    win_max = OptionVerification("--start-maximized")
    headless = OptionVerification("--headless")
    disable_info_bar = OptionVerification("--disable-infobars")
    prefs = OptionVerification("prefs", {
        'profile.default_content_setting_values': {
            'notifications': 2
        }
    })

    # 返回所有的配置变量(包括用户继承的子类变量)
    def options(self):
        # 首先获取父类
        superclass = self.__class__.__bases__[0]
        # 获取配置信息字典
        __op = self.__class__.__dict__
        #  这个循环是获取当前类所定义的配置加上未来子类的配置
        while superclass is not object:
            # 这里会因为这个dictproxy(字典代理)而报错
            # 直接使用拷贝绕过去
            try:
                __op.update(superclass.__dict__)
            except (TypeError, AttributeError):
                __op = __op.copy()
                __op.update(superclass.__dict__)
            superclass = superclass.__bases__[0]
        copy_op = __op.copy()
        for k in __op.keys():  # 如果不是OptionVerification类型直接删除
            if not isinstance(copy_op[k], OptionVerification):
                del copy_op[k]
        return copy_op

    # 返回所有激活的配置
    def all_activate_options(self):
        av_options = dict()
        for op_key, op_value in self.options().items():
            if op_value.is_activate():
                av_options[op_key] = op_value
        return av_options

    def to_capabilities(self):
        '''
            模拟原selenium的to_capabilities
        :return:
        '''

        __to_capabilities = webdriver.ChromeOptions().to_capabilities()
        # print(__to_capabilities)
        # 寻找args值所对应的key
        key = ""
        for k, v in __to_capabilities.items():
            if 'args' in v:
                key = k
                break
        # 将值填充进去
        for op_key, op_value in self.all_activate_options().items():
            value = op_value.get_option()
            if isinstance(value, str):
                __to_capabilities[key]['args'].append(value)
            if isinstance(value, dict):
                __to_capabilities[key].update(value)
        return __to_capabilities

    # 显示可用的配置变量名称文档
    def doc(self):
        print("---Available configuration names---")
        for op_key, op_value in self.options().items():
            activate = op_value.is_activate()
            doc = op_value.doc_().get(op_key, "")
            print("       ", end=u"")
            PrintColor.printCColor(activate, op_key, (u"green", u"defaultColor"), end=u"")
            print(PrintColor.defaultColor(u"  -->"), end=u"")
            PrintColor.printCColor(activate, doc, (u"blue", u"defaultColor"))
        print(PrintColor.defaultColor("--------------doc------------------"))

    def argument(self, var_str):
        '''
            获取类变量所对应的配置信息,如果已激活则返回,反之返回None
        :param var_str:类变量名称
        :return:
        '''
        if self.options()[var_str].is_activate():
            return self.options()[var_str].get_option()
        return None


# 驱动类
class Drive(Options):
    # 这个括号里表示可以适配的驱动
    driver_or_path = DriveVerification("chromedriver")

    def __init__(self, driver_or_path=None, **kwargs):
        '''
        :param driver_path: 这里给出驱动路径,直接得到驱动,获取接收外部传入的驱动
        '''
        self.driver_or_path = to_driver_path(driver_or_path)
        self.__true_driver = None  # 真实的驱动对象
        self._options = kwargs.get("options").to_capabilities() if kwargs else None

    # 创建浏览器
    def create_browser(self, url=None):
        browser = self.driver_or_path[0]  # 浏览器函数
        executable_path = self.driver_or_path[1]  # 参数
        # desired_capabilities这个参数selenium真实需要的(也是options)
        # print(executable_path)
        self.__true_driver = browser(executable_path=executable_path,
                                     desired_capabilities=self._options
                                     )
        if url:
            self._get(url)
        return self

    @property
    def driver(self):
        return self.__true_driver

    def _get(self, url):
        pass
