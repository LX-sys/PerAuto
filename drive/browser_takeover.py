# -*- coding:utf-8 -*-
# @time:2022/4/2510:57
# @author:LX
# @file:browser_takeover.py
# @software:PyCharm
'''

    浏览器中断后继续执行(类似接管)
    但是在操作上比接管更加方便
    w3c万位网协议网址: https://w3c.github.io/webdriver/webdriver-spec.html#sessions
    检查反爬的网址: https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html
'''
import time

from compat import (
    os,
    copy,
    json,
    socket,
    base64,
    platform,
    requests,
    ConnectionError, ReadTimeout,
    InvalidArgumentException,
    ChromeRemoteConnection,
    Service,
    Command,
    WebDriver
)
from utils import to_driver_path
from color import PrintColor
# 这个不是报错
from selenium import __version__




# 原生selenium3的变量
_W3C_CAPABILITY_NAMES = frozenset([
    'acceptInsecureCerts',
    'browserName',
    'browserVersion',
    'platformName',
    'pageLoadStrategy',
    'proxy',
    'setWindowRect',
    'timeouts',
    'unhandledPromptBehavior',
])

# 原生selenium3的变量
_OSS_W3C_CONVERSION = {
    'acceptSslCerts': 'acceptInsecureCerts',
    'version': 'browserVersion',
    'platform': 'platformName'
}

# 原生selenium3的方法
def _make_w3c_caps(caps):
    """Makes a W3C alwaysMatch capabilities object.

    Filters out capability names that are not in the W3C spec. Spec-compliant
    drivers will reject requests containing unknown capability names.

    Moves the Firefox profile, if present, from the old location to the new Firefox
    options object.

    :Args:
     - caps - A dictionary of capabilities requested by the caller.
    """
    caps = copy.deepcopy(caps)
    profile = caps.get('firefox_profile')
    always_match = {}
    if caps.get('proxy') and caps['proxy'].get('proxyType'):
        caps['proxy']['proxyType'] = caps['proxy']['proxyType'].lower()
    for k, v in caps.items():
        if v and k in _OSS_W3C_CONVERSION:
            always_match[_OSS_W3C_CONVERSION[k]] = v.lower() if k == 'platform' else v
        if k in _W3C_CAPABILITY_NAMES or ':' in k:
            always_match[k] = v
    if profile:
        moz_opts = always_match.get('moz:firefoxOptions', {})
        # If it's already present, assume the caller did that intentionally.
        if 'profile' not in moz_opts:
            # Don't mutate the original capabilities.
            new_opts = copy.deepcopy(moz_opts)
            new_opts['profile'] = profile
            always_match['moz:firefoxOptions'] = new_opts
    return {"firstMatch": [{}], "alwaysMatch": always_match}


# 判断一个端口是否占用
def is_port_use(ip,port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        s.shutdown(2)
        return True
    except:
        return False


class MyChromeRemoteConnection(ChromeRemoteConnection):

    headers_ = None  # 请求头

    def __init__(self,*args,**kwargs):

        super(MyChromeRemoteConnection, self).__init__(*args,**kwargs)

    @classmethod
    def get_remote_connection_headers(cls, parsed_url, keep_alive=False):
        """
        Get headers for remote request.

        :Args:
         - parsed_url - The parsed url
         - keep_alive (Boolean) - Is this a keep-alive connection (default: False)
        """

        system = platform.system().lower()
        if system == "darwin":
            system = "mac"

        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'selenium/{} (python {})'.format(__version__, system)
        }

        if parsed_url.username:
            base64string = base64.b64encode('{0.username}:{0.password}'.format(parsed_url).encode())
            headers.update({
                'Authorization': 'Basic {}'.format(base64string.decode())
            })

        if keep_alive:
            headers.update({
                'Connection': 'keep-alive'
            })
        #
        cls.headers_ = headers
        return headers


class MyWebDriver(WebDriver):

    def __init__(self,command_executor='http://127.0.0.1:4444/wd/hub',browser_handle=0,
                 desired_capabilities=None, browser_profile=None, proxy=None,
                 keep_alive=False, file_detector=None, options=None,take_over_path=None):

        # 浏览器句柄
        self.__browser_handle = browser_handle

        with open(take_over_path,"r") as f:
            self.__take_over = json.load(f)
        self.__take_over_path=take_over_path
        self._parameters = None

        super(MyWebDriver, self).__init__(command_executor, desired_capabilities, browser_profile, proxy, keep_alive,
                                          file_detector, options)

    # 句柄
    def handle(self):
        return str(self.__browser_handle)

    def get_parameters(self):
        return self._parameters

    def take_over(self):
        return self.__take_over[self.handle()]["take_over"]

    def start_session(self, capabilities, browser_profile=None):

        """
        Creates a new session with the desired capabilities.

        :Args:
         - browser_name - The name of the browser to request.
         - version - Which browser version to request.
         - platform - Which platform to request the browser on.
         - javascript_enabled - Whether the new session should support JavaScript.
         - browser_profile - A selenium.webdriver.firefox.firefox_profile.FirefoxProfile object. Only used if Firefox is requested.
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})
        w3c_caps = _make_w3c_caps(capabilities)
        parameters = {"capabilities": w3c_caps,
                      "desiredCapabilities": capabilities}

        if not self.take_over():
            response = self.execute(Command.NEW_SESSION, parameters)
            self._parameters = response
            self.__take_over[self.handle()]["take_over"] = response
            with open(self.__take_over_path, "w") as f2:
                json.dump(self.__take_over, f2)
        else:
            response = self.take_over()

        if 'sessionId' not in response:
            response = response['value']
        self.session_id = response['sessionId']
        self.capabilities = response.get('value')
        # if capabilities is none we are probably speaking to
        # a W3C endpoint
        if self.capabilities is None:
            self.capabilities = response.get('capabilities')

        # Double check to see if we have a W3C Compliant browser
        self.w3c = response.get('status') is None
        self.command_executor.w3c = self.w3c


class Dri(object):
    def __init__(self,executable_path="chromedriver",is_take_over=False,browser_handle=None,options=None):
        '''

        :param executable_path: 浏览器驱动路径
        :param is_take_over: 浏览器是否需要接管
        :param browser_handle: 浏览器句柄(当is_take_over为False时,设置将失效)
        实现浏览器接管的流程
        [{"browser_handle":session},{"browser_handle":session},{"browser_handle":session},...]
                    启动程序
                      |
                读取session文件(获取到浏览器session列表)
                      |
           使用句柄从session列表获取真实存在的浏览器
                 |                |          |
                 |浏览器不存在      |句柄不存在   |浏览器存在
                 |               |           |
            重新生成新的浏览器session
                            |                   |
                            |                   |
                            \                  |
                              \              |
                                 打开浏览器
        '''
        # 浏览器句柄
        self.__browser_handle = 0 if browser_handle is None else browser_handle
        self.__json_path = "session.json"
        # 测试浏览器是否连接的页面
        self.__test_session_html = 'session_test.html'
        # 接管
        self.set_take_over = is_take_over
        #
        self.options = options
        # 初始文件
        init_file = False

        if os.path.isfile(self.session_path()) is False:
            init_file = True
        else:
            # 读取
            with open(self.session_path(),"r") as f:
                try:
                    self.conf = json.load(f)
                except ValueError:
                    init_file = True
        # 创建文件
        if init_file:
            with open(self.session_path(),'w') as f:
                self.conf = self.new_session_struct(self.handle())
                json.dump(self.conf, f)
        else:
            # 检测所有句柄的可连接性
            self.inspect_browsers_connection()

        addr = self.conf.get(self.handle(), None)

        # 如果是启用接管,而且是第一次创建浏览器则为 False
        if self.set_take_over:
            is_b_connection = False if (addr is None) or (self.conf == self.new_session_struct(self.handle())) \
                else True
        else:
            is_b_connection = False

        # 是否需要创建新的服务
        if not is_b_connection:
            self.create_new_browser()
            self.service = Service(executable_path=to_driver_path(executable_path),port=0)
            self.service.start()
            self.conf[self.handle()]["port"] = self.service.service_url
            with open(self.session_path(),"w") as f:
                json.dump(self.conf,f)

        # 打开浏览器
        self.switch_handle(self.handle())
        # self.cr = MyChromeRemoteConnection(remote_server_addr=self.conf[self.handle()]["port"],
        #                             keep_alive=True)
        # self.__driver = MyWebDriver(command_executor=self.cr,browser_handle=int(self.handle()),
        #                             take_over_path=self.session_path())

    # 切换句柄
    def switch_handle(self,browser_handle=None):
        '''
            在浏览器运行期间切换句柄(当前浏览器失去控制权)
        :param browser_handle: 浏览器句柄
        :return:
        '''
        self.cr = MyChromeRemoteConnection(remote_server_addr=self.conf[str(browser_handle)]["port"],
                                           keep_alive=True)
        self.__driver = MyWebDriver(command_executor=self.cr, browser_handle=int(str(browser_handle)),
                                    take_over_path=self.session_path(),options=self.options)

    def session_path(self):
        return self.__json_path

    # 新的存session结构
    def new_session_struct(self,handle=0):
        # {"port": None, "take_over": None}
        return {str(handle):{"port": None, "take_over": None}}

    # 句柄
    def handle(self):
        return str(self.__browser_handle)

    # 检测当前浏览器是否处于连接状态
    def __is_connection(self,local_url_port,sessionId):
        '''
            测试原理:
                浏览器处于打开状态,则get返回200
                如果浏览器只有进程存在,返回404
                如果过浏览器进程不存在,返回500
        :param local_url_port:
        :param sessionId:
        :return:
        '''
        url = local_url_port + "/session/" + sessionId + u'/url'
        value = {"url": self.__test_session_html, "sessionId": sessionId}
        try:
            response = requests.get(url=url, json=value, timeout=5)
            if response.status_code == 200:
                return True
            if response.status_code in [404, 500]:
                return False
        except (ConnectionError, ReadTimeout):
            return False
        return False

    # 判断所有浏览器浏览是否处于连接状态
    def inspect_browsers_connection(self):
        '''
            检查浏览器的连接状态,
            移除无效连接
        :return:
        '''
        print u"正在检测浏览器是否可以连接..."
        copy_conf = copy.deepcopy(self.conf)
        # 懒检测,只检测当前句柄的连接状态
        if self.set_take_over:
            local_url_port_, sessionId = copy_conf[self.handle()]["port"],copy_conf[self.handle()]["take_over"]["value"]["sessionId"]
            if self.__is_connection(local_url_port_, sessionId) is False:
                del self.conf[self.handle()]
                print PrintColor.red(u"Browser [{}] failed to connect --> remove".format(self.handle()))
        else:
            # 删除无法连接的句柄
            for i, info in copy_conf.items():
                local_url_port_,take_over = info.get("port",None),info.get("take_over")
                if local_url_port_ and take_over:
                    sessionId = take_over["value"]["sessionId"]
                    if self.__is_connection(local_url_port_,sessionId) is False:
                        del self.conf[i]
                        print PrintColor.red(u"Browser [{}] failed to connect --> remove".format(i))

        if self.conf:
            pass
            # 重新排序
            # copy_conf = copy.deepcopy(self.conf)
            # self.conf.clear()
            # index = 0
            # for info in copy_conf.values():
            #     self.conf[str(index)] = info
            #     index += 1
        else:
            self.conf = self.new_session_struct(self.handle()) if self.set_take_over else self.new_session_struct(0)
        with open(self.session_path(), 'w') as f:
            json.dump(self.conf, f)

    def create_new_browser(self):
        # 获取句柄最大的数字
        conf_int_list = [int(i) for i in self.conf.keys()]
        max_handle = max(conf_int_list)
        # 接管
        if self.set_take_over:
            max_handle = int(self.handle())
        else: # 句柄由系统自己决定
            if self.conf[str(max_handle)] != self.new_session_struct(max_handle)[str(max_handle)]:
                max_handle += 1
                print "============"
            self.__browser_handle = max_handle
        self.conf.update(self.new_session_struct(max_handle))
        print PrintColor.green(u"Creating a New browser [{}]".format(str(max_handle)))

    def headers(self):
        return self.cr.headers_

    def get(self,url):
        self.__driver.get(url)

    def quit(self):
        self.__driver.quit()




d = Dri(is_take_over=False,browser_handle=1)
# d.get("https://www.baidu.com/")
# d.get("https://www.cnblogs.com/wwwwtt/p/15892233.html")
# d.get(r"D:\code\my_html\automationCode.html")
# time.sleep(3)
# time.sleep(2)
# d.quit()