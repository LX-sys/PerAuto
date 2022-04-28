# -*- coding:utf-8 -*-
# @time:2022/4/2510:57
# @author:LX
# @file:browser_takeover.py
# @software:PyCharm
'''

    浏览器中断后继续执行(类似接管)
    但是在操作上比接管更加方便

'''
import os
import copy
import json
import socket
import time

from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver
import sys


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

class MyWebDriver(WebDriver):

    def __init__(self,command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None, browser_profile=None, proxy=None,
                 keep_alive=False, file_detector=None, options=None,take_over=None,take_over_path=None):

        with open(take_over_path,"r") as f:
            self.__take_over = json.load(f)
        print "---------->",self.__take_over
        self.__take_over_path=take_over_path
        self._parameters = None

        super(MyWebDriver, self).__init__(command_executor, desired_capabilities, browser_profile, proxy, keep_alive,
                                          file_detector, options)


    def get_parameters(self):
        return self._parameters

    def take_over(self):
        return self.__take_over["take_over"]

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
            with open(self.__take_over_path,"r") as f:
                c = json.load(f)
                with open(self.__take_over_path,"w") as f2:
                    c["take_over"] = response
                    json.dump(c,f2)
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



# s = Service("chromedriver.exe",0)
# s.start()
# # print s.command_line_args()
# print s.service_url
# # print s.is_connectable()
# cr = ChromeRemoteConnection(remote_server_addr=s.service_url,
#                             keep_alive=True)
#
# # s.service_url 需要写入文件
#
# # {'capabilities': {'alwaysMatch': {}, 'firstMatch': [{}]}, 'desiredCapabilities': {}}
# c = MyWebDriver(command_executor=cr,desired_capabilities=None)
# c.get("https://www.baidu.com/")
# sessionId = c.session_id
# print sessionId

class Dri(object):
    def __init__(self,executable_path="chromedriver.exe"):
        # 创建文件
        if os.path.isfile(r"D:\code\PerAuto\port_session.json") is False:
            with open(r"D:\code\PerAuto\port_session.json", "w") as f:
                json.dump({"port":None,"take_over":None},f)

        # 读取
        with open(r"D:\code\PerAuto\port_session.json","r") as f:
            try:
                self.conf = json.load(f)
            except ValueError:
                self.conf = {"port": None, "take_over": None}

        # 存储接管的必须信息
        if not self.conf:
            self.conf = {"port":None,"take_over":None}

        if self.conf["port"] is None:
            self.service = Service(executable_path=executable_path,port=0)
            self.service.start()
            self.conf["port"]=self.service.service_url
            with open(r"D:\code\PerAuto\port_session.json","w") as f:
                json.dump(self.conf,f)
        # print self.conf["port"]
        self.cr = ChromeRemoteConnection(remote_server_addr=self.conf["port"],
                                    keep_alive=True)
        self.__driver = MyWebDriver(command_executor=self.cr,take_over=self.conf["take_over"],
                                    take_over_path=r"D:\code\PerAuto\port_session.json")

    def get(self,url):
        self.__driver.get(url)

    def quit(self):
        self.__driver.quit()

d = Dri()
d.get("https://www.baidu.com/")
# time.sleep(2)
# d.quit()