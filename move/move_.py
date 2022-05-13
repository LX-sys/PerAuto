# -*- coding:utf-8 -*-
# @time:2022/5/1118:40
# @author:LX
# @file:move_.py
# @software:PyCharm
from compat import (
    math,
    time,
    numpy,
    random,
    webdriver,
    pyautogui
)

driver = webdriver.Chrome(executable_path="chromedriver.exe")

# url = 'file:///D:/code/my_html/automationCode.html'

url = 'https://www.baidu.com/'

driver.get(url)

driver.maximize_window()

be = driver.find_element("id",'su')
af = driver.find_element("id","kw")


# 人类鼠标移动轨迹
class HumanMoveTrajectory(object):
    '''
        青年人
        中年人
        老年人
    '''
    YOUTH = (0.01, 0.018)
    MIDDLE_AGED = (0.019, 0.03)
    ELDERLY = (0.02, 0.035)

    # 获取元素的x,y,w,h
    @staticmethod
    def get_ele_rect(ele=None, note=""):
        ele_w, ele_h, ele_x, ele_y = 0, 0, 0, 0
        try:
            # 如果网页刷新找不到前元素,则用鼠标当前位置代替
            if ele.is_displayed():
                before = ele.rect
                ele_x, ele_y = before["x"], before["y"]
                ele_w, ele_h = before["width"], before["height"]
            else:
                ele = None
        except:
            ele = None

        # 获取鼠标位置给前元素
        if ele is None:
            pos = pyautogui.position()
            ele_w, ele_h = 0, 0
            ele_x, ele_y = pos.x, pos.y

        return ele_x, ele_y, ele_w, ele_h

    # 获取拟人移动轨迹
    @staticmethod
    def get_move_trajectory(before_ele=None, after_ele=None):
        '''
            贝塞尔曲线一次公式: p0+(p1-p0)*t
            贝塞尔曲线二次公式: (1-t)^2*p0+2*t(1-t)+t^2*p2
            如果前一个元素位置/获取鼠标位置 在 后元素的左边,则鼠标移动后的位置靠近后元素整个大小的左侧(左侧~中心)，反正...
            元素位置情况一:
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

        # 前元素
        before_e_x, before_e_y, before_e_w, before_e_h = HumanMoveTrajectory.get_ele_rect(before_ele)
        # 后元素
        after_e_x, after_e_y, after_e_w, after_e_h = HumanMoveTrajectory.get_ele_rect(after_ele)

        print "原始前元素:", before_e_x, before_e_y, before_e_w, before_e_h
        print "原始后元素:", after_e_x, after_e_y, after_e_w, after_e_h

        # 后元素的落脚点
        if after_e_x >= before_e_x:
            # 鼠标落在元素中间分开靠左部分
            after_arrival_x = (after_e_x * 1.1, after_e_x + after_e_w // 2)
        if after_e_x <= before_e_x:
            # 鼠标落在元素中间分开靠右部分
            after_arrival_x = ((after_e_x + after_e_w // 2) * 1.1, after_e_x + after_e_w // 2 - after_e_w // 6)
        after_arrival_x = random.uniform(*after_arrival_x)

        after_arrival_y = random.uniform(after_e_y + after_e_h + 2, after_e_y + after_e_h + after_e_h - 2)
        # +40+11    +40+22
        before_arrival_pos = {"x": before_e_x, "y": before_e_y, "w": before_e_w, "h": before_e_h}
        after_arrival_pos = {"x": after_arrival_x, "y": after_arrival_y, "w": after_e_w, "h": after_e_h}
        print "前元素:", before_arrival_pos

        print "后元素:", after_arrival_pos
        return {"be": before_arrival_pos, "af": after_arrival_pos}

    # 贝塞尔鼠标移动
    @staticmethod
    def Bessel_move(before_pos=(200, 700, 80, 50), after_pos=(500, 200, 80, 50), duration=(0.01, 0.018), radian=None,
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
        # 弧度随机
        if radian is None:
            radian = {"up_arc": (0.51, 0.54), "down_arc": (0.8, 0.9), "random": True}
            radian_ = random.choice([radian["up_arc"], radian["down_arc"]]) if radian["random"] else radian["up_arc"]
        else:
            radian_ = (radian, radian + 0.1)
        # print before_pos[0],bw,after_pos[0]
        # print math.fabs(before_pos[0]+bw-after_pos[0])
        # 如果两者距离小于12px
        # if before_pos[0] >= after_pos[0]:
        #     b,a = before_pos[0],after_pos[0]
        #     w = after_pos[2]
        # if before_pos[0] <= after_pos[0]:
        #     b,a = after_pos[0],before_pos[0]
        #     w = before_pos[2]
        # print b,a,w
        # print b-(a+w)
        # if math.fabs(b-(a+w)) <= 12:
        #     print "------------"
        #     radian_ = (0.6,0.6)

        middle_pos = (math.fabs(before_pos[0] + bw + (after_pos[0] - before_pos[0] + bw) // 2),
                      math.fabs(after_pos[1] + bh + (before_pos[1] - after_pos[1] + bh) // 2))

        middle_pos = [i * random.uniform(*radian_) for i in middle_pos]
        # print middle_pos
        P0, P1, P2 = numpy.array([before_pos[:2], middle_pos, after_pos[:2]])

        # 二次贝塞尔曲线公式
        P = lambda t: (1 - t) ** 2 * P0 + 2 * t * (1 - t) * P1 + t ** 2 * P2
        # 生成坐标点
        points = numpy.array([P(t) for t in numpy.linspace(0, 1, 30)])
        # 两端位置,0,1表示维度
        x, y = points[:, 0], points[:, 1]
        zip_xy = zip(list(x), list(y))

        if move_drive_f is None:
            move_drive_f = pyautogui.moveTo

        for pos in zip_xy:
            move_drive_f(pos[0], pos[1])
            time.sleep(random.uniform(*duration))

    # 贝塞尔鼠标移动 - 使用大漠驱动(变量名必须是dm)
    @staticmethod
    def dm_Bessel_move(before_pos=(200, 700, 80, 50), after_pos=(500, 200, 80, 50), duration=(0.01, 0.018),
                       radian=None):
        HumanMoveTrajectory.Bessel_move(before_pos, after_pos, duration, radian, move_drive_f=dm.moveto)

    # 光滑曲线公式
    @staticmethod
    def Smoothcurve_move(self):
        '''
        # 光滑曲线弧长公式：L=n(圆心角度数)×π(1)×r
        :param self:
        :return:
        '''

    # 将移动轨迹的返回格式转换成贝塞尔移动需要的格式
    @staticmethod
    def to_bessel(move_trajectory):
        be_, af_ = move_trajectory["be"], move_trajectory["af"]

        return (
            (be_["x"], be_["y"], be_["w"], be_["h"]),
            (af_["x"], af_["y"], af_["w"], af_["h"])
        )


import numpy
import math

from DM import DM

dm = DM()


class HMT(HumanMoveTrajectory):
    pass


t = HMT.get_move_trajectory(before_ele=be, after_ele=af)

# HMT.dm_Bessel_move((be_["x"], be_["y"], 57, 30), (af_["x"], af_["y"], 177, 21), duration=HMT.YOUTH)
HMT.dm_Bessel_move(*HMT.to_bessel(t), duration=HMT.YOUTH)
# pyautogui.moveTo(8,92.875)
# time.sleep(4)
# pyautogui.moveTo(1033.796875,128)
#  (500, 200),(200, 700),
# HMT.Bessel_move(duration=HMT.YOUTH,move_drive_f=dm.moveto)
# HMT.dm_Bessel_move((8, 90, 80, 50), (1200, 144, 80, 50), duration=HMT.YOUTH)
