#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author  : wuyinan02@playcrab.com
# @Desc    :
from poco.drivers.std import StdPoco


class CommonUI:
    def __init__(self, poco):
        self.poco = poco

    def drag(self, direction="left", duration_time=0.3):
        # 左右滑动主界面
        '''
        direction传入left表示滑动到主界面左侧
        direction传入right表示滑动到主界面右侧
        '''
        pos_center = self.poco(name="chouka")
        pos_left = self.poco(name="iconColor")
        pos_right = self.poco(name="chargeBtn")
        if direction == "left":
            return (pos_center).drag_to(pos_right, duration=duration_time)
        else:
            return (pos_center).drag_to(pos_left, duration=duration_time)

    def close_btn(self,btnName=False):
        # 通用点击关闭、返回按钮
        '''
        游戏中关闭和返回按钮有三种，检查任意一种是否存在后点击
        该方法适用于heros里面所有需要点击返回或者关闭按钮
        btnName为空，判断哪个关闭按钮存在，然后点击
        butName不为空，直接点击该关闭按钮
        '''
        btnList = [self.poco(name="closeBtn"), self.poco(name="closeBtn2"), self.poco(name="btn_return")]
        if btnName:
            return self.poco(name=btnName).click()
        else:
            for x in btnList:
                if x.exists():
                    return x.click()
                else:
                    print("not find closeBtn")
