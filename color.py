# -*- coding:utf-8 -*-
# @time:2022/4/4 16:20
# Author:LX
# @File:color.py
# @Software:PyCharm
from __future__ import print_function

'''

    输出颜色类
'''


class PrintColor(object):

    def __init__(self):
        print(PrintColor.__dict__)

    @staticmethod
    def __template(a=u"[0;0;", b=u"0m", c=u"hello world", d=u"0m", underline=False):
        if underline:
            return u"\033{}4m{}\033[0m".format(a, c)
        return u"\033{}{}{}\033{}".format(a, b, c, d)

    @staticmethod
    def color(color_code, text, underline=False):
        '''

        :param color_code: 颜色代码
        :param text: 输出文本
        :param underline: 是否需要下划线
        :return:str
        '''
        if underline:
            return PrintColor.__template(a="[1;{};".format(color_code), c=text, underline=True)
        return PrintColor.__template("[1;{};".format(color_code), "1m", text, "[8m")

    @staticmethod
    def red(text, underline=False):
        '''

        :param text: 输出文本
        :param underline: 是否需要下划线
        :return:str
        '''
        return PrintColor.color(u"31", text, underline)

    @staticmethod
    def blue(text, underline=False):
        return PrintColor.color(u"34", text.encode('utf-8'), underline)

    @staticmethod
    def green(text, underline=False):
        return PrintColor.color(u"32", text.encode('utf-8'), underline)

    @staticmethod
    def defaultColor(text, underline=False):
        if underline:
            return u"\033[0;0;4m{}\033[0m".format(text.encode('utf-8'))
        return u"\033[0;0;0m{}\033[0m".format(text.encode('utf-8'))

    @staticmethod
    def availableColor():
        '''
        显示可用颜色
        :return:
        '''
        temp = [u"red", u"blue", u"green"]
        for c in temp:
            print(c)

    @staticmethod
    def __getFunction(color):
        '''
            通过字符串函数获取真正可调用的函数对象
        :param color: 颜色方法名称
        :return:str
        '''
        return PrintColor.__dict__[color].__func__

    @staticmethod
    def printColor(text_colors, interval=u" ", end=u"\n"):
        '''
            彩色输出
        :param text_colors: 多个文本和颜色  格式 [(文本,颜色),(文本,颜色),...]
        :param interval: 每个文本直之间的间隔
        :param end:结尾
        :return:
        '''
        for combination in text_colors:
            if len(combination) == 2:
                text, color = combination[0], combination[1]
                print(PrintColor.__getFunction(color)(text) + "{}".format(interval), end="")
            elif len(combination) == 3:
                text, color, line = combination[0], combination[1], combination[2]
                print(PrintColor.__getFunction(color)(text, line) + "{}".format(interval), end="")
            else:
                raise IndexError("The maximum index is 2")
        print(end=end)

    @staticmethod
    def printCColor(is_com, text, colors, underline=False, end=u"\n"):
        '''
            比较输出颜色
            根据is_com 来决定输出那个颜色的文本
        :param is_com:True/False
        :param text: 文本
        :param colors: 颜色 格式("xx","xx")
        :return:
        '''
        if is_com:
            print(PrintColor.__getFunction(colors[0])(text, underline), end=end)
        else:
            print(PrintColor.__getFunction(colors[1])(text, underline), end=end)


if __name__ == '__main__':
    PrintColor.printColor([(u"hdhasd", u"defaultColor")])
    PrintColor.printCColor(False, u"helllo", (u"red", u"blue"), underline=True)
