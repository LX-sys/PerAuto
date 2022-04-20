# -*- coding:utf-8 -*-
# @time:2022/4/1916:47
# @author:LX
# @file:record.py
# @software:PyCharm

from __future__ import print_function
from commonlyfunctions import currentTime, error_display
from color import PrintColor
from header import (
    wraps,
    sys,
    json
)


# 参数格式化
def argc_format(argc):
    if not argc:
        return ""

    temp = list()
    for c in argc:
        if isinstance(c, int):
            temp.append(str(c) + ",")
        elif isinstance(c, str):
            temp.append("\"{}\",".format(c))
        elif c is None:
            temp.append("None,")
        else:
            temp.append(json.dumps(c) + ",")
    return "".join(temp)


# 参数格式化
def argc_format_dict(argc_dict):
    if not argc_dict:
        return ""

    temp = list()
    f = "{}={},"
    for k, v in argc_dict.items():
        if isinstance(v, int):
            temp.append(f.format(k, str(v)))
        elif isinstance(v, str):
            temp.append(f.format(k, "\"{}\"".format(v)))
        elif v is None:
            temp.append(f.format(k, "None"))
        else:
            temp.append(f.format(k, json.dumps(v)))

    return "".join(temp)


# 显示记录
def show_record(func_name, args_=None, func_err=True, is_show=True):
    '''

    :param func_name: 函数名称
    :param args_: 参数
    :param func_err: True:函数名显示 绿色,False:红色
    :param is_show: 是否显示记录
    :return:
    '''
    if is_show:
        print(PrintColor.defaultColor(currentTime()), end="")
        PrintColor.printCColor(func_err, "  <{}>  ".format(func_name), ("green", "red"), end="")
        # 格式显示参数
        if args_:
            argc_str = argc_format(args_["args"])
            del args_["args"]
            argc_str += argc_format_dict(args_)
            # 移除最后一个逗号
            args_ = argc_str.rstrip(",")
        print(PrintColor.defaultColor("Argc: {}".format(args_)))


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

    # 对每个函数处理异常
    def try_func(self, func, func_name, *args, **kwargs):
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
                    "func_result": None,
                    "error_info": e
                }
        else:
            func_result["func_result"] = func(*args, **kwargs)

        # 打印记录
        args_dict = kwargs
        args_dict["args"] = args[1:]
        show_record(func_name, args_=args_dict, func_err=True if func_result["func_result"] else False,
                    is_show=self.is_show_record)
        error_display(func_result["error_info"])

        return func_result["func_result"]

    def __call__(self, func):
        print(func)
        func_name = func.__name__
        if not self.record_date.in_(func_name):
            self.record_date.add_func_name(func.__name__)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # 调用者的self
            _self = args[0]

            func_result = self.try_func(func, func_name, *args, **kwargs)
            return func_result
        return wrapper

    @staticmethod
    def pp(func):
        print("a")

# @Record()
# def sss(s):
#     print("sd")


# class A:
#     @Record("ss")
#     def hello(self, a, e=None):
#
#         print(self.__dict__)
#         return self
#
    # @Record()
    # def world(self):
    #     # print("dd")
    #     return self
#
#
# a = A()
# a.hello("das", [1, 23])
# a.world()
