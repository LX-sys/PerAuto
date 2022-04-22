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
import time
import math
import random
import chardet
import datetime
import platform
import threading
import pyautogui
import traceback
from functools import wraps
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver


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
