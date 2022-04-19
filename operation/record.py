# -*- coding:utf-8 -*-
# @time:2022/4/1916:47
# @author:LX
# @file:record.py
# @software:PyCharm

from __future__ import print_function
from commonlyfunctions import currentTime,error_display
from header import wraps,sys
from color import PrintColor


# 显示记录
def show_record(func_name, args=None, func_err=True, is_show=True):
    '''

    :param func_name: 函数名称
    :param args: 参数
    :param func_err: True:函数名显示 绿色,False:红色
    :param is_show: 是否显示记录
    :return:
    '''
    if is_show:
        print(PrintColor.defaultColor(currentTime()), end="")
        PrintColor.printCColor(func_err, "  <{}>  ".format(func_name), ("green", "red"), end="")
        print(PrintColor.defaultColor("argc: {}".format(args)))



# 存储记录(单例模式)
class RecordDate(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, u'_instance'):
            cls._instance = super(RecordDate, cls).__new__(cls, *args, **kwargs)
            cls.__func_name = list()
        return cls._instance

    def __init__(self):
        pass

    @classmethod
    def add_func_name(cls, name):
        cls.__func_name.append(name)

    @classmethod
    def func_names(cls):
        return cls.__func_name

    @classmethod
    def in_(cls, item):
        return item in cls.__func_name


# 记录
class Record(object):

    def __init__(self, *args, **kwargs):

        self.record_date = RecordDate()
        # 异常拦截
        self.abnormal_intercept = kwargs.get("abnormal_intercept", True)
        # 显示记录
        self.is_show_record = kwargs.get("is_show_record", True)

    def func_names(self):
        if hasattr(self, "func_name"):
            return self.func_name
        return None

    # 对每个函数处理异常
    def try_func(self, func, *args, **kwargs):
        func_result = {
            "func_result": None,
            "error_info": None
        }
        if self.abnormal_intercept:
            try:
                func_result["func_result"] = func(*args, **kwargs)
            except Exception as e:
                # 返回结果,错误信息
                func_result = {
                    "func_result":None,
                    "error_info":e
                }
                error_display(e)
        else:
            func_result["func_result"] = func(*args, **kwargs)
        return func_result

    def __call__(self, func):
        func_name = func.__name__
        if not self.record_date.in_(func_name):
            self.record_date.add_func_name(func.__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用者的self
            _self = args[0]
            func_result = self.try_func(func, *args, **kwargs)
            # 打印记录
            show_record(func_name, args[1:],
                        func_err=True if func_result["func_result"] else False,
                        is_show=self.is_show_record
                        )
            # if not func_result["func_result"]:
            #     error_display(func_result["error_info"])
            return func_result["func_result"]

        # print(self.record_date.func_names())
        return wrapper

    @staticmethod
    def pp(func):
        print("a")


class A:
    @Record(is_show_record=True)
    def hello(self, a):
        1/0
        # print("ss", a)
        # raise TypeError("djasiokldjaskldjaksdl")
        return self


#
#     @Record()
#     def world(self):
#         print("dd")
a = A()
a.hello("dsad")
