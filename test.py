# -*- coding:utf-8 -*-
# @time:2022/4/2510:39
# @author:LX
# @file:test.py
# @software:PyCharm

import requests

# import subprocess
# subprocess.Popen("chromedriver.exe")
# from time import sleep
# sleep(2)

# 请求地址(打开浏览器)
driver_url = 'http://localhost:9515/session'
# 打开浏览器的请求参数
driver_value = {"capabilities":
                    {"firstMatch": [{}],
                     "alwaysMatch":
                         {"browserName":
                              "chrome",
                          "platformName": "any",
                          "goog:chromeOptions":
                              {"extensions": [], "args": []}}},
                "desiredCapabilities":
                    {"browserName":
                         "chrome",
                     "version": "",
                     "platform": "ANY",
                     "goog:chromeOptions": {"extensions": [],
                                            "args": []}}}
# 发送求清
# response_session = requests.post(driver_url, json = driver_value)
# print(response_session.json())
#
response_session= {u'value': {u'sessionId': u'5a8a6e5d4c73d8e60af4f3ab3f50859b', u'capabilities': {u'goog:chromeOptions': {u'debuggerAddress': u'localhost:54789'}, u'browserVersion': u'100.0.4896.88', u'timeouts': {u'pageLoad': 300000, u'implicit': 0, u'script': 30000}, u'strictFileInteractability': False, u'acceptInsecureCerts': False, u'webauthn:virtualAuthenticators': True, u'networkConnectionEnabled': False, u'chrome': {u'chromedriverVersion': u'100.0.4896.60 (6a5d10861ce8de5fce22564658033b43cb7de047-refs/branch-heads/4896@{#875})', u'userDataDir': u'C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\scoped_dir13544_868852836'}, u'browserName': u'chrome', u'setWindowRect': True, u'proxy': {}, u'pageLoadStrategy': u'normal', u'webauthn:extension:largeBlob': True, u'platformName': u'windows', u'unhandledPromptBehavior': u'dismiss and notify', u'webauthn:extension:credBlob': True}}}
# # 访问我的博客的请求地址 （这个地址是我们上面记录的地址）
# # url = u'http://localhost:9515/session/'+response_session["value"]['sessionId']+u'/url'
url = u'http://localhost:52355/session/'+response_session["value"]['sessionId']+u'/url'
# 访问我的博客的请求参数
# https://www.baidu.com/
# D:\code\my_html\automationCode.html
# value = {"url": r"https://www.baidu.com/", "sessionId": response_session["value"]['sessionId']}
# response_blog = requests.post(url = url,json = value)
# print(response_blog.json())


# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
# from selenium.webdriver.remote.webdriver import WebDriver

# s = Service("chromedriver.exe",0)
# s.start()
# print s.service_url
# print s.is_connectable()
# cr = ChromeRemoteConnection(remote_server_addr=s.service_url,
#                             keep_alive=True)
#
# c = WebDriver(command_executor=cr,desired_capabilities=None)
# print c.__dict__

import os,socket

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect(("127.0.0.1",int("64389")))
    s.shutdown(2)
    print "占用"
except:
    print "不占用"