# -*- coding:utf-8 -*-
# @time:2022/4/2111:34
# @author:LX
# @file:compat.py
# @software:PyCharm

'''
    兼容python2,3

'''


import re
import os
import sys
import copy
import json
import time
import socket
import base64
import requests
import platform
from requests import ConnectionError, ReadTimeout
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.command import Command
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote import remote_connection

try:
    import win32com.client
except ImportError:
    pass

try:
    import simplejson as json
except ImportError:
    import json


_version = sys.version_info

is_py2 = _version[0] == 2

is_py3 = _version[0] == 3

# 操作系统
__system= platform.system().lower()

is_system_win = __system == "windows"

is_system_linux = __system == "linux"

is_system_mac = __system == "darwin"

if is_py2:
    from urlparse import urlparse
    # 这个模块需要单独下载 pip install threadpool
    from threadpool import ThreadPool, makeRequests


if is_py3:
    import asyncio
    from urllib.parse import urlparse
    # 这个方法是python3内置方法
    from concurrent.futures import ThreadPoolExecutor

