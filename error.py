# -*- coding:utf-8 -*-
# @time:2022/4/229:49
# @author:LX
# @file:error.py
# @software:PyCharm

'''
    自定义异常文件
'''


# 异常基类
class ABCError(Exception):
    def __init__(self, v):
        self.v = v

    def __str__(self):
        return self.v


# 驱动异常
class DriveError(ABCError):
    def __init__(self, v):
        super(DriveError, self).__init__(v)

    def __str__(self):
        return super(DriveError, self).__str__()


# 驱动路径异常
class ExecutablePathError(ABCError):

    def __init__(self, *args):
        super(ExecutablePathError, self).__init__(*args)

    def __str__(self):
        return super(ExecutablePathError, self).__str__()


# options设置异常
class OptionsError(ABCError):
    def __init__(self, *args):
        super(OptionsError, self).__init__(*args)

    def __str__(self):
        return super(OptionsError, self).__str__()


# 父类转子类异常
class ParentToChildError(ABCError):
    def __init__(self, *args):
        super(ParentToChildError, self).__init__(*args)

    def __str__(self):
        return super(ParentToChildError, self).__str__()