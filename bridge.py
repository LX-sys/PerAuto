# -*- coding:utf-8 -*-
# @time:2022/4/2211:47
# @author:LX
# @file:bridge.py
# @software:PyCharm

'''
    桥接器文件
'''

from compat import (
    is_py2,
    is_py3,
)

try:
    from compat import (
        ThreadPool,
        makeRequests
    )
except ImportError:
    pass

try:
    from compat import ThreadPoolExecutor
except ImportError:
    pass


# 线程池
class ThreadPoolBridge(object):
    '''
        线程池,支持python2,python3

    '''

    def __init__(self, max_workers=7):
        self.__max_workers = max_workers
        self.__th_obj = self._create_thread_obj()
        self.__args = list()

    def thobj(self):
        return self.__th_obj

    def _create_thread_obj(self):
        if is_py2:
            return ThreadPool(self.__max_workers)
        if is_py3:
            return ThreadPoolExecutor(max_workers=self.__max_workers)

    # 添加单个参数
    def addarg(self, arg):
        '''
            传入单个参数,这个参数只作用与第一个线程
            # 参数支持格式
            str,
            list,
            tuple
            ex:
                xx.addarg("aa")
                xx.addarg(["bb","b"])
        :param arg:
        :return:
        '''
        if is_py2:
            if isinstance(arg, str):
                self.__args.append(([arg],None))
            if isinstance(arg, tuple) or isinstance(arg, list):
                self.__args.append((arg, None))
        if is_py3:
            self.__args.append(arg)

    # 添加多个参数
    def addargs(self, args):

        '''
            ["xx",["ss","sad"],("das","das")]
            ex:
                xx.addargs(["aa",["bb","b"]])
            优先添加参数,
            参数可以是单个,也可以是一个列表,
            注意:这个方法只有在使用 addfunc(),不传第二个参数时生效
        :param args:
        :return:
        '''
        for ar in args:
            self.addarg(ar)

    def args(self):
        return self.__args

    # 添加线程
    def addfunc(self, callable_, args_list=None,timeout=10):
        '''

        :param callable_: 可调函数
        :param args_list: 参数列表
        :return:
        '''
        if args_list is None:
            args_list = self.args()

        if is_py2:
            requests = makeRequests(callable_, args_list)
            for ts in requests:
                self.thobj().putRequest(ts, timeout=timeout)

        if is_py3:
            for d in args_list:
                self.thobj().submit(callable_, *d)

    def wait(self):
        if is_py2:
            self.thobj().wait()
        if is_py3:
            self.thobj().shutdown(True)


from time import sleep


def hello(c=None, b=None):
    i = 0
    print("{}->{}->{}".format(i, c, b))
    sleep(1)
    i += 1
    return c


data = [(["aa","sda"],None), "b", "c", "d", "e"]
t = ThreadPoolBridge(10)
# t.addarg("aa")
# t.addarg(["bb","b"])
# print t.args()
t.addargs(["aa",["bb","b"]])
t.addfunc(hello)
t.wait()
