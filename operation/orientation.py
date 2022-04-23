# -*- coding:utf-8 -*-
# @time:2022/4/2018:01
# @author:LX
# @file:orientation.py
# @software:PyCharm
'''
    元素定位
'''

from drive.drive import Options,Drive
from compat import time,random
from record import Record
from utils import node_to_xpath
from htmlanalyse import HTMLAnalyse



# 镜像网页驱动(具体实现)
class MirrorWebDriver(Drive):
    '''
        这个类主要是避免的一个带装饰器的方法去调用另一个带装饰器的方法,从而触发多次装饰器
    '''
    def __init__(self,driver_or_path=None, **kwargs):
        super(MirrorWebDriver, self).__init__(driver_or_path, **kwargs)

    def title(self):
        return self.driver.title

    def url(self):
        return self.driver.current_url

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

    @Record()
    def quit(self):
        self.driver.quit()
        return self


op = Options()
op.win_max = True
dri = Driver("chromedriver",options=op)
dri.doc()
# https://www.baidu.com/
dri.create_browser(r"file:///D:/code/my_html/automationCode.html")
s = HTMLAnalyse(dri.driver)
print s.is_page_contrast(interval_time=1)
dri.wait(1,2)
dri.quit()