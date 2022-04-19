# -*- coding:utf-8 -*-
# @time:2022/4/1819:51
# @author:LX
# @file:ruleWrapper.py
# @software:PyCharm

from abc import ABCMeta,abstractmethod


# 规则包装器python2.7
class RuleWrapperABC(object):
    # 抽象方法
    __metaclass__ = ABCMeta

    def __init__(self, *args):
        self.__rule = list(args)
        self.__rule_len = len(self.__rule)

    # 判断是否有匹配规则
    def isRule(self):
        if self.__rule:
            return True
        return False

    # 规则长度
    def ruleLength(self):
        return self.__rule_len

    def rule(self):
        if not self.isRule():
            return None
        if self.ruleLength() == 1:
            return self.__rule[0]

    def rules(self):
        if not self.isRule():
            return None
        return self.__rule

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