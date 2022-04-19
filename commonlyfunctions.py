# -*- coding:utf-8 -*-
# @time:2022/4/1916:49
# @author:LX
# @file:commonlyfunctions.py
# @software:PyCharm
from __future__ import print_function
from color import PrintColor
from header import (
    datetime,
    sys
)

'''
    常用方法
'''

# 返回当前时间
def currentTime(connector_before=":", connector_after=":", custom=None):
    '''
    返回当前时间
    Return current time
    :connector_before: 年月日之间连接符
    :connector_after:时分秒之间连接符
    :custom:自定义
    :return: str
    '''
    _time = '%Y@1%m@1%d %H@%M@%S'.replace("@1", connector_before)
    _time = _time.replace("@", connector_after)
    if custom:
        _time = custom
    return datetime.datetime.now().strftime(_time)


# 递归显示信息
def error_display(e):
    exc_type, exc_value, exc_traceback_obj = sys.exc_info()
    # 获取递归的最大程度
    limit = sys.tracebacklimit if hasattr(sys, 'tracebacklimit') else None
    n = 0
    while exc_traceback_obj is not None and (limit is None or n < limit):
        lineno = exc_traceback_obj.tb_lineno
        co = exc_traceback_obj.tb_frame.f_code
        filename = co.co_filename
        name = co.co_name
        # 这句话格式可以实现报错后,在pycharm中点击跳转
        print(PrintColor.red('  File "%s", line %d, in <%s>'% (filename, lineno, name)))
        exc_traceback_obj = exc_traceback_obj.tb_next
        n += 1
    if e:  # 显示具体报错信息
        print(e, end="")


if __name__ == '__main__':
    try:
        1/0
    except Exception as e:
        error_display(e)