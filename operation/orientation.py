# -*- coding:utf-8 -*-
# @time:2022/4/2018:01
# @author:LX
# @file:orientation.py
# @software:PyCharm
'''
    定位
'''

from drive.drive import Options,Drive
from header import time,random
from record import Record

# 操作网页
class Driver(Drive):
    def __init__(self,driver_or_path=None, **kwargs):
        super(Driver, self).__init__(driver_or_path,**kwargs)

    @Record()
    def create_browser(self, url=None):
        return super(Driver, self).create_browser(url)

    @Record()
    def get(self, url):
        self.driver.get(url)
        return self

    @Record()
    def wait(self, s=0, e=0):
        time.sleep(random.randint(s, e))
        return self

    @Record()
    def quit(self):
        self.driver.quit()
        return self

# "chromedriver.exe"
op = Options()
op.headless = True
dri = Driver("chromedriver.exe")
dri.create_browser("https://www.baiu.com/")
dri.wait(3,4)
dri.quit()