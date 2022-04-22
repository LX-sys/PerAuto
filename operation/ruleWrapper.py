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

    {"input":"xxx",argc:[xxx]}  -->页面只有一个输入框,argc表示对应的信息列表
    {"input_s":"xxx" argc:[xxx]}  -->页面只有多个输入框,在每个输入框中输入信息
    {"input":"xxx","argc":[xxx],"btn":"xxxxx"}  -->页面只有一个输入框和按钮,argc表示对应的信息列表
    {"input_s":"xxx","argc":[xxx],"btn":"xxxxx"}  -->页面有多个输入框和按钮,argc表示对应的信息列表

    ......
]

# 给文字的匹配规则,需要在父子节点反复搜索
# 给id,xpath,...的匹配规则
'''

from compat import threading

# 规则包装器
class RuleWrapperABC(object):
    '''

        这是一个伪抽象类,为了兼容python2,python3
        python3 与python2
    '''
    def __init__(self, *agrs):
        '''

        :param args:匹配元素的方式
        '''
        self.__rule = list()
        self.__rule.extend(agrs)
        self.__rule_len = self.ruleLength()


    # 判断是否有匹配规则
    def is_rule(self):
        if self.__rule:
            return True
        return False


    # 规则长度
    def ruleLength(self):
        return len(self.__rule)


    # 返回单个规则(默认返回首个)
    def rule(self):
        if not self.is_rule():
            return None
        if self.ruleLength() == 1:
            return self.__rule[0]


    # 返回单多个规则
    def rules(self):
        if not self.is_rule():
            return None
        return self.__rule


    # 返回规则与路径
    # 伪抽象方法
    def rule_path(self):
        pass
        # if not self.is_rule():
        #     return None
        # if self.ruleLength() == 1:
        #     return self.rule_type(),self.rule()
        # else:
        #     return self.rule_type(),self.rules()


    # 返回类型
    # 伪抽象方法
    def rule_type(self):
        pass

    # 单个匹配,运行多个规则
    # def run(self):
        # threading.Thread


class RuleWrapper(RuleWrapperABC):

    def __init__(self, path_type=None, *args):
        child = self.__chirldToparent(path_type)
        if not isinstance(child, str):
            path_type, args = child[0], child[1]
        super(RuleWrapper, self).__init__(*args)
        self.__path_type = path_type


    # 子类转父类
    def __chirldToparent(self, child_class):

        # 处理子类自己
        if isinstance(child_class, str):
            return child_class

        # 子转父
        if isinstance(child_class, ID) \
                or isinstance(child_class, CSS) \
                or isinstance(child_class, XPATH) \
                or isinstance(child_class, TagName) \
                or isinstance(child_class, LinkText) \
                or isinstance(child_class, ClassName) \
                or isinstance(child_class, CssSelector) \
                or isinstance(child_class, PartialLinkText):
            path_type, args = child_class.rule_path()[0], child_class.rule_path()[1]
            return [path_type], args if isinstance(args, list) else [args]
        return None

    def rule_path(self):
        if not self.is_rule():
            return None
        if self.ruleLength() == 1:
            return self.rule_type(), self.rule()
        else:
            return self.rule_type(), self.rules()

    def rule_type(self):
        if isinstance(self.__path_type, str):
            return self.__path_type
        elif isinstance(self.__path_type, list):
            return self.__path_type
        else:
            return ""

    def __add__(self, other):
        '''
            实现规则相加
            myid = ID("abc")
            myxpath = XPATH("bb")
            myid + myxpath =  ["id","xpath"],["abc","bb"]
        :param other:
        :return:
        '''
        # 匹配类型列表,匹配规则列表
        type_list, argc_list = [], []
        temp_list = [type_list, argc_list]

        oneself = [self, other]

        for temp_self in oneself:
            for i in range(len(temp_list)):
                type_or_path = temp_self.rule_path()[i]
                if isinstance(type_or_path, str) and type_or_path not in type_list:
                    temp_list[i].append(type_or_path)
                if isinstance(type_or_path, list) and type_or_path not in argc_list:
                    temp_list[i].extend(type_or_path)

        return RuleWrapper(
            type_list[0] if len(type_list) == 1 else type_list,
            *argc_list)


# id定位
class ID(RuleWrapper):

    def __init__(self, *args):
        super(ID, self).__init__(self.rule_type(), *args)

    def rule_type(self):
        return "id"


# xpath定位
class XPATH(RuleWrapper):

    def __init__(self, *args):
        super(XPATH, self).__init__(self.rule_type(), *args)

    def rule_type(self):
        return "xpath"


# css定位
class CSS(RuleWrapper):

    def __init__(self, *args):
        super(CSS, self).__init__(self.rule_type(), *args)

    def rule_type(self):
        return "css"


# tag name定位
class TagName(RuleWrapper):
    def __init__(self, *args):
        super(TagName, self).__init__(self.rule_type(), *args)

    def rule_type(self):
        return "tag name"


# class name定位
class ClassName(RuleWrapper):
    def __init__(self, *args):
        super(ClassName, self).__init__(self.rule_type(), *args)

    def rule_type(self):
        return "class name"


# css selector定位
class CssSelector(RuleWrapper):
    def __init__(self, *args):
        super(CssSelector, self).__init__(self.rule_type(), *args)

    def rule_type(self):
        return "css selector"


# link text 定位
class LinkText(RuleWrapper):
    def __init__(self, *args):
        super(LinkText, self).__init__(self.rule_type(), *args)

    def rule_type(self):
        return "link text"


# partial link text定位
class PartialLinkText(RuleWrapper):
    def __init__(self, *args):
        super(PartialLinkText, self).__init__(self.rule_type(), *args)

    def rule_type(self):
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


# s = LinkText("abc")
# # print s.rule_path()
# s_to = RuleWrapper("id", ["text", "s"])
# cc = ID(s_to)
# print cc.rule_path()

# 线程池
# from concurrent.futures import ThreadPoolExecutor
#
# ths = ThreadPoolExecutor(max_workers=10)
# print ths
# print ths.submit()
from time import sleep

# python2 的线程
def hello(c=None):
    i=0
    print "{}->{}".format(i,c)
    sleep(1)
    i+=1
from threadpool import ThreadPool,makeRequests
data = ["a","b","c","d","e"]

pool = ThreadPool(10)
requests=makeRequests(hello,data)
[pool.putRequest(req) for req in requests]
pool.wait()