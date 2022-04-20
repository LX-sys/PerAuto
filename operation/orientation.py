# -*- coding:utf-8 -*-
# @time:2022/4/2018:01
# @author:LX
# @file:orientation.py
# @software:PyCharm
'''
    元素定位
'''

from drive.drive import Options,Drive
from header import time,random
from record import Record

# 镜像网页驱动
class MirrorWebDriver(Drive):
    def __init__(self,driver_or_path=None, **kwargs):
        super(MirrorWebDriver, self).__init__(driver_or_path, **kwargs)


    def _get(self, url):
        self.driver.get(url)
        return self

    def _wait(self, s=0, e=0):
        time.sleep(random.randint(s, e))
        return self

    def _quit(self):
        self.driver.quit()
        return self


# 网页驱动(用于操作网页)
class Driver(MirrorWebDriver):
    def __init__(self,driver_or_path=None, **kwargs):
        super(Driver, self).__init__(driver_or_path,**kwargs)

    @Record()
    def create_browser(self, url=None):
        return super(Driver, self).create_browser(url)

    @Record()
    def get(self, url):
        super(Driver, self)._get(url)
        return self

    @Record()
    def wait(self, s=0, e=0):
        super(Driver, self)._wait(s,e)
        return self
    #
    @Record()
    def quit(self):
        self.driver.quit()
        return self

# "chromedriver.exe"
op = Options()
op.headless = True
dri = Driver("chromedriver")
dri.create_browser()
dri.get("https://www.baidu.com/")
# dri.create_browser("file:///Users/lx/Documents/PersonificationAuto/test.html")
dri.wait(3,4)
dri.quit()