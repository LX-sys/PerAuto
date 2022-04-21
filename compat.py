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
import chardet
import random
import datetime
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

is_py2 = (_version[0] == 2)

is_py3 = (_version[0] == 3)



if is_py2:
    print("当前python2")
    import threading



if is_py3:
    print("当前python2")
    import asyncio
