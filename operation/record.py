# -*- coding:utf-8 -*-
# @time:2022/4/1916:47
# @author:LX
# @file:record.py
# @software:PyCharm

from __future__ import print_function
from commonlyfunctions import currentTime
from header import wraps
from color import PrintColor

def show_record(func_name,args):
    print
    currentTime() + "  <{}>  argc:{}".format(func_name, args[1:])



# 存储记录(单例模式)
class RecordDate(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,u'_instance'):
            cls._instance = super(RecordDate, cls).__new__(cls,*args,**kwargs)
            cls.__func_name = list()
        return cls._instance

    def __init__(self):
        pass

    @classmethod
    def add_func_name(cls,name):
        cls.__func_name.append(name)

    @classmethod
    def func_names(cls):
        return cls.__func_name

    @classmethod
    def in_(cls,item):
        return item in cls.__func_name


# 记录
class Record(object):

    def __init__(self,*args,**kwargs):

        self.record_date = RecordDate()
        # 异常拦截
        self.abnormal_intercept = kwargs.get("abnormal_intercept",True)

    def func_names(self):
        if hasattr(self,"func_name"):
            return self.func_name
        return None

    # 对每个函数处理异常
    def try_func(self,func,*args,**kwargs):
        if self.abnormal_intercept:
            try:
                func_result = func(*args, **kwargs)
            except Exception:
                func_result = None
        else:
            func_result = func(*args, **kwargs)
        return func_result

    def __call__(self, func):
        func_name = func.__name__
        if not self.record_date.in_(func_name):
            self.record_date.add_func_name(func.__name__)

        @wraps(func)
        def wrapper(*args,**kwargs):
            # 调用者的self
            _self=args[0]
            # 组合打印记录
            # zu = currentTime()+"  <{}>  argc:{}".format(func_name,args[1:])
            # print(zu)
            func_result = self.try_func(func,*args,**kwargs)
            return func_result
        # print(self.record_date.func_names())
        return wrapper

    @staticmethod
    def pp(func):
        print("a")


# class A:
#     @Record()
#     def hello(self,a):
#         print("ss",a)
#         return self
#
#     @Record()
#     def world(self):
#         print("dd")
# a = A()
# a.hello("dsad")

