# -*- coding:utf-8 -*-
# @time:2022/4/1819:51
# @author:LX
# @file:ruleWrapper.py
# @software:PyCharm

# 基础规则列表
'''
[
    {btn:""xxxxx"} -> 这种普通字符串就是页面只有按钮,随机点一个

    {"select":"xxxx"} --> 这种格式,页面只有下拉框,选择一项
    {"select_s":"xxx"} --> 这种格式表示页面有多个下拉框,每个下拉框选择一个
    {"select":"xxxx","btn":"xxx"} --> 这种格式页面有下拉框和按钮(执行顺序,先执行下拉框,在执行按钮)
    {"select_s":"xxx","btn":"xxx"} --> 这种格式表示页面有多个下拉框和按钮(执行顺序,先执行下拉框,在执行按钮)

    {"radio":"xxx"}  --> 这种格式表示页面只有一个单选按钮
    {"radio_s":"xxx"}    -->这种格式表示页面只有多个单选按钮
    {"radio":"xxx","btn":"xxx"}  --> 这种格式表示页面只有一个单选按钮和按钮
    {"radio_s":"xxx","btn":"xxx"} -->这种格式表示页面只有多个单选按钮和按钮(执行顺序,先执行单选按钮,在执行按钮)

    {"check":"xxx"}  --> 这种格式表示页面只有复选框
    {"check_s":"xxx"}   -->这种格式表示页面只有多个复选按钮
    {"check":"xxx","btn":"xxx"}  -->这种格式表示页面只有复选框和按钮
    {"check_s":"xxx","btn":"xxx"}    -->这种格式表示页面只有多个复选按钮和按钮(执行顺序,先执行复选按钮,在执行按钮)

    {"sendkey":"xxx",argc:[xxx]}  -->页面只有一个输入框,argc表示对应的信息列表
    {"sendkey_s":"xxx" argc:[xxx]}  -->页面只有多个输入框,在每个输入框中输入信息
    {"sendkey":"xxx","argc":[xxx],"btn":"xxxxx"}  -->页面只有一个输入框和按钮,argc表示对应的信息列表
    {"sendkey_s":"xxx","argc":[xxx],"btn":"xxxxx"}  -->页面有多个输入框和按钮,argc表示对应的信息列表

    ......
]

# 给文字的匹配规则,需要在父子节点反复搜索
# 给id,xpath,...的匹配规则
'''

from abc import ABCMeta, abstractmethod


# 规则包装器python2.7
class RuleWrapperABC(object):
    # 抽象方法
    __metaclass__ = ABCMeta

    def __init__(self, args_list):
        '''

        :param args:匹配元素的方式
        '''
        self.__rule = args_list
        print("===",self.__rule)
        if isinstance(args_list,list) or isinstance(args_list,tuple):
            self.__rule_len = len(self.__rule)
        else:
            self.__rule_len = 1

    # 判断是否有匹配规则
    def isRule(self):
        if self.__rule:
            return True
        return False

    # 规则长度
    def ruleLength(self):
        return self.__rule_len

    # 返回单个规则(默认返回首个)
    def rule(self):
        if not self.isRule():
            return None
        if self.ruleLength() == 1:
            return self.__rule

    # 返回单多个规则
    def rules(self):
        if not self.isRule():
            return None
        return self.__rule

    # 返回规则与路径
    def rule_path(self):
        if not self.isRule():
            return None
        if self.ruleLength() == 1:
            return self.ruleType(),self.rule()
        else:
            return self.ruleType(),self.rules()

    @abstractmethod
    def ruleType(self):
        pass


# id定位
class ID(RuleWrapperABC):

    def ruleType(self):
        return "id"


# xpath定位
class XPATH(RuleWrapperABC):

    def ruleType(self):
        return "xpath"


# css定位
class CSS(RuleWrapperABC):

    def ruleType(self):
        return "css"


# tag name定位
class TagName(RuleWrapperABC):
    def ruleType(self):
        return "tag name"


# class name定位
class ClassName(RuleWrapperABC):
    def ruleType(self):
        return "class name"


# css selector定位
class CssSelector(RuleWrapperABC):
    def ruleType(self):
        return "css selector"


# link text 定位
class LinkText(RuleWrapperABC):
    def ruleType(self):
        return "link text"


# partial link text定位
class PartialLinkText(RuleWrapperABC):
    def ruleType(self):
        return "partial link text"


def see(path_type, path):
    if path_type.lower():
        if path_type == "id":
            e = ID(path)
        elif path_type == "xpath":
            e = XPATH(path)
        elif path_type == "css":
            e = CSS(path)
        elif path_type == "tag name":
            e = TagName(path)
        elif path_type == "class name":
            e = ClassName(path)
        elif path_type == "css selector":
            e = CssSelector(path)
        elif path_type == "link text":
            e = LinkText(path)
        elif path_type == "partial link text":
            e = PartialLinkText(path)
        else:
            raise TypeError("There is no such match!")
        return e

print(see("id","pas").rule_path())