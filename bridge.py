# -*- coding:utf-8 -*-
# @time:2022/4/2211:47
# @author:LX
# @file:bridge.py
# @software:PyCharm

'''
    桥接器文件
    线程池,兼容python2,python3
'''
import Queue
import threading


from compat import (
    is_py2,
    is_py3,
    time,
    re
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
        线程池,兼容python2,python3
        def hello(c=None, b=None):
            i = 0
            print("{}->{}->{}".format(i, c, b))
            sleep(1)
            i += 1
            return c

        __t = ThreadPoolBridge(10)
        __t.addarg("aa")
        __t.addarg(["bb","b"])
        __t.addfunc(hello)
        __t.wait()
    '''

    def __init__(self, max_workers=7):
        '''

        :param max_workers: 最大线程数量
        '''
        self.__max_workers = max_workers
        self.__th_obj = self._create_thread_obj()
        self.__args = list()

    # 返回线程对象
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


# 自定义线程类
class MyThread(threading.Thread):
    def __init__(self,target=None,*argc):
        super(MyThread, self).__init__()
        number_str = "".join(
            re.findall(r"[0-9].*", self.getName())
        )
        # 重新定义线程名称,与函数名称一致
        self.setName(target.__name__+"-"+number_str)
        # 函数，参数，结果
        self._target = target
        self._argc = argc
        self.__result = None

    def run(self):
        self.__result = self._target(*self._argc)

    # 返回线程执行的结果
    def get_result(self):
        return self.__result


# 自定义线程池(基于 生产者消费者模型)
class Threads(object):

    def __init__(self,max_workers=7):
        self.__max = max_workers
        # 线程队列
        self.__thread_que = Queue.Queue(self.__max)
        # 无限大小的队列
        self.__advantage_que = Queue.Queue(-1)
        # 返回值列表
        self._result_list = []

    # 返回每个线程的结果
    def result(self):
        temp = []
        for th in self._result_list:
            v = th.get_result()
            if v:
                temp.append(v)
        return temp

    def add_work(self,f_,argc=None):
        '''

        :param f_: 可调用函数
        :param argc: 参数列表,参数个数等于线程数量
        :return:
        '''
        for ar in argc:
            # 判断队列是否已满,如果满了,就将溢出的线程转移到无限大小队列中
            if self.__thread_que.full():
                self.__advantage_que.put(MyThread(f_,ar))
            else:
                self.__thread_que.put(MyThread(f_,ar))

    def start(self):
        while True:

            while self.__thread_que.qsize():
                self._result_list.append(self.__thread_que.get())
                self._result_list[-1].start()

            # 等待
            for th in self._result_list:
                th.join()

            if self.__advantage_que.empty():
                break

            for _ in range(self.__thread_que.maxsize):
                if self.__advantage_que.qsize():
                    self.__thread_que.put(self.__advantage_que.get())
                else:
                    break


import random

def test(a):
    i=0
    # while i<5:
    print ("->",i,a)
    i+=1
    time.sleep(1)
    return i+random.randint(1,7)

def test2():
    i=0
    while i<5:
        print ("<-",i)
        i+=1
        time.sleep(1)
    return i

t = Threads(2)
t.add_work(test,["a","b","c","d","e"])
t.start()
print t.result()
