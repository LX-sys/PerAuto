# -*- coding:utf-8 -*-
# @time:2022/5/1118:40
# @author:LX
# @file:move_.py
# @software:PyCharm
from selenium import webdriver
import random
import pyautogui
driver = webdriver.Chrome(executable_path="chromedriver.exe")

url = 'file:///D:/code/my_html/automationCode.html'


driver.get(url)

driver.maximize_window()
# 拟人移动轨迹
def personification_move_trajectory(before_ele=None, after_ele=None):
    # 前元素
    try:
        # 如果网页刷新找不到前元素,则用鼠标当前位置代替
        if before_ele.is_displayed():
            before = before_ele.rect
            before_e_w, before_e_h = before["width"], before["height"]
            before_e_x, before_e_y = before["x"], before["y"]
        else:
            before_ele = None
    except:
        before_ele = None

    # 获取鼠标位置
    if before_ele is None:
        pos = pyautogui.position()
        before_e_w, before_e_h = 0, 0
        before_e_x, before_e_y = pos.x, pos.y

    # 后元素
    after = after_ele.rect
    after_e_w, after_e_h = after["width"], after["height"]
    after_e_x, after_e_y = after["x"], after["y"]
    # 后元素的落脚点
    if after_e_x <= before_e_x:
        after_arrival_x = (after_e_x, after_e_x + after_e_w // 2)
    if after_e_x >= before_e_x:
        after_arrival_x = (after_e_x + after_e_w // 2, after_e_x + after_e_w)
    after_arrival_x = random.uniform(*after_arrival_x)
    after_arrival_y = random.uniform(after_e_y + 2, after_e_y + after_e_h - 2)
    before_arrival_pos = {"x":before_e_x,"y":before_e_y,"w":before_e_w,"h":before_e_h}
    after_arrival_pos = {"x": after_arrival_x, "y": after_arrival_y,"w":after_e_w,"h":after_e_h}
    print "前元素:",before_arrival_pos
    print "后元素:",after_arrival_pos
    return {"be":before_arrival_pos,"af":after_arrival_pos}
    '''
            贝塞尔曲线一次公式: p0+(p1-p0)*t
            贝塞尔曲线二次公式: (1-t)^2*p0+2*t(1-t)+t^2*p2
            如果前一个元素位置/获取鼠标位置 在 后元素的左边,则鼠标移动后的位置靠近后元素整个大小的左侧(左侧~中心)，反正...
            元素位置情况一(需要数学公式:贝塞尔曲线):
              ^^              ^^                
                      @
              ^^              ^^
              # -------------------------
            元素位置情况二:
                    ^^
               ^^    @    ^^
                    ^^

            在情况一下使用:

                                点二(中心点)
                                                    点三(后元素)


                    点一(前元素)
                贝塞尔曲线二次公式,二次贝塞尔曲线由三个点组成,点一和点三由前元素和后元素组成,
                点二(中心点)由两个元素形成的矩形高度中心偏上位置(大约十分之六的位置)
        '''


def to(t):
    be_ = t["be"]
    af_ = t["af"]
    return (be_["x"], be_["y"],be_["w"],be_["h"],
            af_["x"], af_["x"],af_["w"],af_["h"])


be = driver.find_element("id","myselect")
af = driver.find_element("id","myinput")
t = personification_move_trajectory(before_ele=be,after_ele=af)
be_ = t["be"]
af_ = t["af"]

import numpy
import math

# from DM import DM

# dm = DM()


# 人类鼠标移动轨迹
class HumanMoveTrajectory(object):
    '''
        青年人
        中年人
        老年人
    '''
    YOUTH = 0.03
    MIDDLE_AGED = 0.04
    ELDERLY = 0.05

    # 贝塞尔鼠标移动
    @staticmethod
    def Bessel_move(before_pos=(200, 700, 80, 50), after_pos=(500, 200, 80, 50), duration=0.03, radian=None,
                    move_drive_f=None):
        '''

        :param before_pos: 前元素(x, y, w, h)
        :param after_pos: 后元素(x, y, w, h)
        :param duration:持续时间(移动在几秒内完成)
        :param radian: 弧度，基本格式 {"up_arc":(0.51,0.54),"down_arc":(0.8,0.9),"random":True}
                up_arc:上弧
                down_arc: 下弧
                random: True表示在两个弧里面随机选择一个,False默认使用上弧
        :param move_drive_f:鼠标移动的驱动函数 格式: f(x,y)
                不同的移动驱动,实现的效果不一样
                如果不设置移动驱动,者默认使用python自带的pyautogui.moveTo
        :return:
        '''
        bw, bh = before_pos[2], before_pos[3]
        aw, ah = after_pos[2], after_pos[3]
        middle_pos = (math.fabs(before_pos[0] + 80 + (after_pos[0] - before_pos[0] + 80) // 2),
                      math.fabs(after_pos[1] + 50 + (before_pos[1] - after_pos[1] + 50) // 2))
        # 弧度随机
        if radian is None:
            radian = {"up_arc": (0.51, 0.54), "down_arc": (0.8, 0.9), "random": True}
        if radian["random"]:
            radian_ = random.choice([radian["up_arc"], radian["down_arc"]])
        else:
            radian_ = radian["up_arc"]

        middle_pos = [i * random.uniform(*radian_) for i in middle_pos]
        # print middle_pos
        P0, P1, P2 = numpy.array([before_pos[:2], middle_pos, after_pos[:2]])

        # 二次贝塞尔曲线公式
        P = lambda t: (1 - t) ** 2 * P0 + 2 * t * (1 - t) * P1 + t ** 2 * P2
        # 生成坐标点
        points = numpy.array([P(t) for t in numpy.linspace(0, 1, 10)])
        # 两端位置,0,1表示维度
        x, y = points[:, 0], points[:, 1]
        zip_xy = zip(list(x), list(y))

        if move_drive_f is None:
            move_drive_f = pyautogui.moveTo

        for pos in zip_xy:
            move_drive_f(pos[0], pos[1])
            time.sleep(duration)

    # 贝塞尔鼠标移动 - 使用大漠驱动(变量名必须是dm)
    @staticmethod
    def dm_Bessel_move(before_pos=(200, 700, 80, 50), after_pos=(500, 200, 80, 50), duration=0.03, radian=None):
        HumanMoveTrajectory.Bessel_move(before_pos, after_pos, duration, radian, move_drive_f=dm.moveto)


class HMT(HumanMoveTrajectory):
    pass


HMT.dm_Bessel_move((be_["x"], be_["y"], 57, 30), (af_["x"], af_["x"], 177, 21), duration=HMT.YOUTH)
#  (500, 200),(200, 700),
# HMT.Bessel_move(duration=HMT.YOUTH,move_drive_f=dm.moveto)
# HMT.dm_Bessel_move((200, 300, 80, 50), (200, 700, 80, 50), duration=HMT.YOUTH)
