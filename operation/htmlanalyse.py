# -*- coding:utf-8 -*-
# @time:2022/4/2310:39
# @author:LX
# @file:htmlanalyse.py
# @software:PyCharm
'''

    HTML网页分析
'''
import difflib
import matplotlib.pyplot as plt
import numpy as np
from compat import (
    is_py2,
    webdriver,
    time
)


# 网页分析
class HTMLAnalyse(object):

    def __init__(self,driver):
        self.__driver = driver
        # self.__driver = webdriver.Chrome()

    # 返回网页的64编码
    def get_html_64(self):
        html_text = self.__driver.page_source
        old_64 = ""
        if is_py2 and type(html_text) == unicode:
            # old_64 = html_text.encode("base64")
            old_64 = html_text
        if type(html_text) == bytes or type(html_text) == str:
            old_utf8 = html_text.decode("utf-8")
            # old_64 = old_utf8.encode("base64")
            old_64 = old_utf8
        return old_64

    # 页面对比
    def is_page_contrast(self, poll_number=5,interval_time=1,similarity=85,is_line_chart=True):
        '''

        :param poll_number: 检测网页的次数
        :param interval_time: 网页多久比较一次
        :param similarity: 相识值(大于等于这个值时,判断为相识)
        :param is_line_chart:是否绘制网页整体变化的折线图
        :return:
        '''
        # 差异值列表
        diff_list = []
        # 获取一次原始网页
        old_html = self.get_html_64()
        for _ in range(poll_number):
            time.sleep(interval_time)
            new_html = self.get_html_64()
            diff_list.append(
                int(difflib.SequenceMatcher(None, old_html, new_html).ratio() * 100)
            )
        # 绘制网页波动折线图
        if is_line_chart:
            x = [i*10 for i in range(1,poll_number+1)]
            plt.figure()
            plt.plot(x,diff_list)
            plt.show()
            plt.clf()
            plt.close()
        return diff_list[-1] >= similarity

# import difflib
#
# s="hello"
# w="hello"
# print