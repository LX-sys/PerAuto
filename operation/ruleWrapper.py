# -*- coding:utf-8 -*-
# @time:2022/4/1819:51
# @author:LX
# @file:ruleWrapper.py
# @software:PyCharm

# 基础规则列表
'''
[
    {btn:""xxxxx"} -> 这种普通字符串就是页面只有按钮,随机点一个

    {"select":"xxxx"} --> 这种格式,页面只有下拉框,选择一项
    {"select_s":"xxx"} --> 这种格式表示页面有多个下拉框,每个下拉框选择一个
    {"select":"xxxx","btn":"xxx"} --> 这种格式页面有下拉框和按钮(执行顺序,先执行下拉框,在执行按钮)
    {"select_s":"xxx","btn":"xxx"} --> 这种格式表示页面有多个下拉框和按钮(执行顺序,先执行下拉框,在执行按钮)

    {"radio":"xxx"}  --> 这种格式表示页面只有一个单选按钮
    {"radio_s":"xxx"}    -->这种格式表示页面只有多个单选按钮
    {"radio":"xxx","btn":"xxx"}  --> 这种格式表示页面只有一个单选按钮和按钮
    {"radio_s":"xxx","btn":"xxx"} -->这种格式表示页面只有多个单选按钮和按钮(执行顺序,先执行单选按钮,在执行按钮)

    {"check":"xxx"}  --> 这种格式表示页面只有复选框
    {"check_s":"xxx"}   -->这种格式表示页面只有多个复选按钮
    {"check":"xxx","btn":"xxx"}  -->这种格式表示页面只有复选框和按钮
    {"check_s":"xxx","btn":"xxx"}    -->这种格式表示页面只有多个复选按钮和按钮(执行顺序,先执行复选按钮,在执行按钮)

    {"input":"xxx",argc:[xxx]}  -->页面只有一个输入框,argc表示对应的信息列表
    {"input_s":"xxx" argc:[xxx]}  -->页面只有多个输入框,在每个输入框中输入信息
    {"input":"xxx","argc":[xxx],"btn":"xxxxx"}  -->页面只有一个输入框和按钮,argc表示对应的信息列表
    {"input_s":"xxx","argc":[xxx],"btn":"xxxxx"}  -->页面有多个输入框和按钮,argc表示对应的信息列表

    ......
]
# 给文字的匹配规则,需要在父子节点反复搜索
# 给id,xpath,...的匹配规则
'''
# -------------------------------------------------
'''

解决随机广告个数,随机按钮个数模型
while True:
    flag = True
    [try:
        for 单条规则 in 规则列表:
            具体操作(单条规则)
            flag=False
        [新打开的网页,则关闭,返回原来的网页]
        [定位元素位置]
    except:
        pass]
    if flag:
        break
# 常见按钮的规则
["No","1","0","Continue", "Yes","Skip"]
'''

import copy
from bridge import MyThread
from utils import get_html_label
from compat import (
    WebDriverWait,
    threading,
    webdriver
)


# 规则包装器伪抽象类
class RuleWrapperABC(object):
    '''

        这是一个伪抽象类,为了兼容python2,python3
        python3 与python2
    '''
    def __init__(self,driver,*agrs):
        '''

        :param args:匹配元素的方式
        '''
        self.__driver = driver
        self.__rule = list()
        self.__rule.extend(agrs)
        self.__rule_len = self.ruleLength()

    def setDriver(self,dri):
        self.__driver = dri

    @property
    def driver(self):
        return self.__driver

    # 判断是否有匹配规则
    def is_rule(self):
        if self.__rule:
            return True
        return False

    # 规则长度
    def ruleLength(self):
        return len(self.__rule)

    # 返回单个规则(默认返回首个)
    def rule(self):
        if not self.is_rule():
            return None
        if self.ruleLength() == 1:
            return self.__rule[0]

    # 返回单多个规则
    def rules(self):
        if not self.is_rule():
            return None
        return self.__rule


    # 返回规则与路径
    # 伪抽象方法
    def rule_path(self):
        pass

    # 返回类型
    # 伪抽象方法
    def rule_type(self):
        pass

    # 元素定位器,抽象方法
    def locators(self, path,poll_number=5,interval=1):
        pass


# 包装器
class RuleWrapper(RuleWrapperABC):

    def __init__(self,driver, path_type=None, *args):
        # 转换
        if not self.is_child() and type(path_type) not in [str, list, tuple]:
            child = self.__chirldToparent(path_type)
            path_type, args = child[0], child[1]
        super(RuleWrapper, self).__init__(driver,*args)
        self.__path_type = path_type
        # print self.__path_type
        # 规则对应元素字典:
        self.__rule_to_ele_dict = dict()
        # 创建线程池
        # self._th_pool = ThreadPoolBridge(3)
        # 从当前元素向外探索的层数
        # self._explore = 2

    # 判断当前创建实例是否为子类
    def is_child(self):
        if isinstance(self, ID) \
                or isinstance(self, CSS) \
                or isinstance(self, XPATH) \
                or isinstance(self, TagName) \
                or isinstance(self, LinkText) \
                or isinstance(self, ClassName) \
                or isinstance(self, CssSelector) \
                or isinstance(self, PartialLinkText):
            return True
        return False

    # 子类转父类
    def __chirldToparent(self, child_class):
        # webdriver.Chrome().find_element().is_displayed()
        # 子转父
        path_type, args = child_class.rule_path()[0], child_class.rule_path()[1]
        return [path_type], args if isinstance(args, list) else [args]

    # 元素定位器
    def locators(self, path, timeout=5, poll_frequency=0.5,is_reuse=True):
        '''

        :param path: 元素的匹配路径
        :param timeout: 反复查找元素的次数
        :param poll_frequency: 每次查找的时间间隔
        :param is_reuse: 使用被相同的路径找到的元素
        :return:
        '''
        if is_reuse and path in self.__rule_to_ele_dict:
            return self.__rule_to_ele_dict[path]
        # until这个方法参数是一个函数(这个函数必须有一个驱动参数)
        element_list = WebDriverWait(self.driver,timeout=timeout,poll_frequency=poll_frequency).until(
            lambda d:d.find_elements(self.rule_type(), path)
        )
        # for _ in range(poll_number):
        #     eles.extend(
        #         self.driver.find_elements(self.rule_type(), path)
        #     )
        #     if eles:
        #         break
        if len(element_list) == 1:
            self.__rule_to_ele_dict[path] = element_list[0]
        else:
            #去除不显示的元素
            copy_element_list = copy.copy(element_list)
            for e in copy_element_list:
                if e.is_displayed():
                    element_list.remove(e)
            del copy_element_list
        return element_list

    def rule_path(self):
        if not self.is_rule():
            return None
        if self.ruleLength() == 1:
            return self.rule_type(), self.rule()
        else:
            return self.rule_type(), self.rules()

    def rule_type(self):
        if isinstance(self.__path_type, str):
            return self.__path_type
        elif isinstance(self.__path_type, list):
            return self.__path_type
        else:
            return ""

    def __add__(self, other):
        '''
            实现规则相加
            myid = ID("abc")
            myxpath = XPATH("bb")
            myid + myxpath =  ["id","xpath"],["abc","bb"]
        :param other:
        :return:
        '''
        # 匹配类型列表,匹配规则列表
        type_list, argc_list = [], []
        temp_list = [type_list, argc_list]

        oneself = [self, other]

        for temp_self in oneself:
            for i in range(len(temp_list)):
                type_or_path = temp_self.rule_path()[i]
                if isinstance(type_or_path, str) and type_or_path not in type_list:
                    temp_list[i].append(type_or_path)
                if isinstance(type_or_path, list) and type_or_path not in argc_list:
                    temp_list[i].extend(type_or_path)

        return RuleWrapper(self.driver,
            type_list[0] if len(type_list) == 1 else type_list,
            *argc_list)


# id定位
class ID(RuleWrapper):

    def __init__(self,driver=None, *args):
        super(ID, self).__init__(driver,self.rule_type(), *args)

    def rule_type(self):
        return "id"


# xpath定位
class XPATH(RuleWrapper):

    def __init__(self,driver=None, *args):
        super(XPATH, self).__init__(driver,self.rule_type(), *args)

    def rule_type(self):
        return "xpath"


# css定位
class CSS(RuleWrapper):

    def __init__(self,driver=None, *args):
        super(CSS, self).__init__(driver,self.rule_type(), *args)

    def rule_type(self):
        return "css"


# tag name定位
class TagName(RuleWrapper):
    def __init__(self,driver=None, *args):
        super(TagName, self).__init__(driver,self.rule_type(), *args)

    def rule_type(self):
        return "tag name"


# class name定位
class ClassName(RuleWrapper):
    def __init__(self,driver=None, *args):
        super(ClassName, self).__init__(driver,self.rule_type(), *args)

    def rule_type(self):
        return "class name"


# css selector定位
class CssSelector(RuleWrapper):
    def __init__(self,driver=None, *args):
        super(CssSelector, self).__init__(driver,self.rule_type(), *args)

    def rule_type(self):
        return "css selector"


# link text 定位
class LinkText(RuleWrapper):
    def __init__(self,driver=None, *args):
        super(LinkText, self).__init__(driver,self.rule_type(), *args)

    def rule_type(self):
        return "link text"


# partial link text定位
class PartialLinkText(RuleWrapper):
    def __init__(self,driver=None, *args):
        super(PartialLinkText, self).__init__(driver,self.rule_type(), *args)

    def rule_type(self):
        return "partial link text"


def see(driver,path_type, path):
    if path_type.lower():
        if path_type == "id":
            e = ID(driver,path)
        elif path_type == "xpath":
            e = XPATH(driver,path)
        elif path_type == "css":
            e = CSS(driver,path)
        elif path_type == "tag name":
            e = TagName(driver,path)
        elif path_type == "class name":
            e = ClassName(driver,path)
        elif path_type == "css selector":
            e = CssSelector(driver,path)
        elif path_type == "link text":
            e = LinkText(driver,path)
        elif path_type == "partial link text":
            e = PartialLinkText(driver,path)
        else:
            raise TypeError("There is no such match!")
        return e


# 元素定位
class ElementLocalization(object):
    def __init__(self,driver):
        self.__driver = driver

    @property
    def driver(self):
        return self.__driver

    def id(self,path):
        id_ = ID(path)



s = ID("dir","abc")

# print s.rule_path()
# print s
# pp = RuleWrapper("dri",s)
# print pp.rule_path()
s_to = RuleWrapper("driver","id", ["text", "s"])
x = RuleWrapper("driver","id", "ppp")
yy = x+s_to
print yy.rule_path()

# print s_to.rule_type()
# cc = ID(s_to)
# print cc.rule_path()

# 线程池
# from concurrent.futures import ThreadPoolExecutor
#
# ths = ThreadPoolExecutor(max_workers=10)
# print ths
# print ths.submit()
