# -*- coding:utf-8 -*-
# @time:2022/4/1916:49
# @author:LX
# @file:utils.py
# @software:PyCharm
from __future__ import print_function

from selenium.common.exceptions import JavascriptException
from color import PrintColor
from compat import (
    sys,
    datetime,
    urlparse,
    is_system_win,
    is_system_linux,
    is_system_mac,
)
'''
    实用方法
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
def error_display(e, end=""):
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
        print(PrintColor.red('  File "%s", line %d, in <%s>' % (filename, lineno, name)))
        exc_traceback_obj = exc_traceback_obj.tb_next
        n += 1
    if not (e is None):  # 显示具体报错信息
        print(PrintColor.red(e), end=end)


# 返回可用url
def url(url_str):
    # 解析
    _url = urlparse(url_str)

    if _url.scheme in ["http", "https"]:
        return url_str

    if "file" not in url_str:
        if is_system_win:
            url_str = r"file://" + url_str

        if is_system_mac or is_system_linux:
            url_str = r"file://" + _url.path

    return url_str.replace("\\", r"/")


# 返回可用驱动路径
def to_driver_path(driver_path):
    if is_system_win:
        if u".exe" in driver_path:
            return driver_path
        else:
            return driver_path + ".exe"

    if is_system_mac:
        if u".exe" in driver_path:
            return driver_path.replace(".exe", "")
        else:
            return driver_path
    return driver_path


# 返回HTML常用标签
def get_html_label():
    html = ["a", "p", "div", "select", "button", "span", "img", "form", "input","iframe","ins", "table",
            "tr", "th", "td", "title", "ul", "li", "ol"]
    h = ["h" + str(i) for i in range(1, 7)]
    html.extend(h)

    return html


# xpath路径解释器
def node_to_xpath(driver,node):
    js = '''
    var s = document.getElementsByTagName("select")
    // 获取兄弟元素名称
    function getSameLevelName(node){
        // 如果存在兄弟元素
        if(node.previousSibling) {
            let name = '',   // 返回的兄弟元素名称字符串
            count = 1,    // 紧邻兄弟元素中相同名称元素个数
            nodeName = node.nodeName,
            sibling = node.previousSibling;
            while(sibling){
                if(sibling.nodeType == 1 && sibling.nodeType === node.nodeType && sibling.nodeName){
                    if(nodeName == sibling.nodeName){
                        // name
                        // name += ++count;
                        num_ = ++count
                        name = "["+num_+"]"
                    }else {
                        // 重制相同紧邻节点名称节点个数
                        count = 1;
                        // 追加新的节点名称
                        // name += '|' + sibling.nodeName.toUpperCase()
                    }
                }
                sibling = sibling.previousSibling;
            }
            return name
        }else {
            // 不存在兄弟元素返回''
            return ''
        }
    }

    // XPath解释器
    let Interpreter = (function(){
        return function(node, wrap){
            // 路径数组
            let path = [],
            // 如果不存在容器节点，默认为document
            wrap_ = wrap || document;
            // 如果当前节点等于容器节点
            if(node === wrap_) {
                if(wrap_.nodeType == 1) {
                    path.push(wrap_.nodeName.toLowerCase())
                }
                return path
            }
            // 如果当前节点的父节点不等于容器节点
            if(node.parentNode !== wrap_){
                // 对当前节点的父节点执行遍历操作
                path = arguments.callee(node.parentNode, wrap_)
            }
            // 如果当前节点的父元素节点与容器节点相同
            else {
                wrap_.nodeType == 1 && path.push(wrap_.nodeName.toLowerCase())
            }
            // 获取元素的兄弟元素的名称统计
            let siblingsNames = getSameLevelName(node)
            if(node.nodeType == 1){
                path.push(node.nodeName.toLowerCase() + siblingsNames)
            }
            // 返回最终的路径数组结果
            return path
        }
    })()
    function xpath(node){
        let path = Interpreter(document.querySelector(node))
        return path.join('/')
    }
    return xpath(\"<node>\")
    '''
    js = js.replace("<node>",node)
    try:
        return driver.execute_script(js)
    except JavascriptException:
        return None

# 在JS中使用查找元素
'''
    这个方法与原生selenium的find_elemnts("xpath","xx")效果差不多,
    但是这个方法可以自动忽略,不显示的元素
'''
def js_xpath_find_eles(driver,path):
    js ='''
        var arr = [];
        nodes=document.evaluate(\"<path>\", document);

        var v = nodes.iterateNext();
        while(v){
            if(v.scrollHeight !=0 && v.scrollWidth !=0){
                arr.push(v);
            }
            v = nodes.iterateNext();
        }
        return arr;
    '''
    js = js.replace("<path>", path)
    try:
        return driver.execute_script(js)
    except JavascriptException:
        return None

# def js_xpath_find_eles_up(driver,path):


if __name__ == '__main__':
    pass
    # try:
    #     # 1/0
    #     pass
    # except Exception as e:
    #     error_display(e)
