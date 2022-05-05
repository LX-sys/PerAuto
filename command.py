# -*- coding:utf-8 -*-
# @time:2022/5/412:50
# @author:LX
# @file:command.py
# @software:PyCharm
'''
    命令模式
'''

from abc import ABCMeta,abstractmethod

class CommandABC(object):
    __metaclass__ = ABCMeta
    GET = "get"

    @abstractmethod
    def execute(self,*args,**kwargs):
        pass


# get命令
class CommandGET(CommandABC):
    def __init__(self,obj,*args,**kwargs):
        self.__obj = obj
        self.__args = args

    def execute(self,*args,**kwargs):
        self.__obj.get(*self.__args)


# 调用者
class Invoker(object):
    def get(self,*args,**kwargs):
        print "---get",args


# 代理
class Proxy(object):
    def __init__(self):
        # 伪队列
        self.__pseudo_queue = []

    def isQueue(self):
        if self.__pseudo_queue:
            return False
        return True

    def isNotQueue(self):
        if self.__pseudo_queue:
            return True
        return False

    # 添加命令
    def add_execute_cmd(self,cmd):
        self.__pseudo_queue.append(cmd)

    def pop_head(self):
        if self.isNotQueue():
            del self.__pseudo_queue[0]

    def pop_end(self):
        if self.isNotQueue():
            del self.__pseudo_queue[-1]

    # 执行单个命令
    def execute_cmd(self,cmd):
        self.add_execute_cmd(cmd)
        # 执行成功的弹出
        try:
            cmd.execute()
            self.pop_head()
        except Exception:
            pass

    # 执行所有的命令
    def executes(self):
        if self.isQueue():
            return None

        for cmd in self.__pseudo_queue:
            self.execute_cmd(cmd)

test = Invoker()
cmd = CommandGET(test,"url")
proxy = Proxy()
proxy.execute_cmd(cmd)