#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd:
    '''
    反馈当前电机限制角度/最大速度
    '''
    def __init__(self, 
                 motor_num:Literal[1, 2, 3, 4, 5, 6]=1, 
                 max_angle_limit: int=0, 
                 min_angle_limit: int=0,
                 max_jonit_spd: int=0):
        """
        初始化 ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd 实例。

        :Byte 0: 关节电机序号, uint8, 最大角度限制 H
        :Byte 1: 最大角度限制,uint16, 单位 0.1度
        :Byte 2: 最大角度限制
        :Byte 3: 最小角度限制, uint16, 单位 0.1度
        :Byte 4: 最小角度限制
        :Byte 5: 最大关节速度， uint16, 单位 0.001rad/s
        :Byte 6: 最大关节速度
        :Byte 7:
        """
        if motor_num not in [1, 2, 3, 4, 5, 6]:
            raise ValueError(f"motor_num 值 {motor_num} 超出范围 [1, 2, 3, 4, 5, 6]")
        self.motor_num = motor_num
        self.max_angle_limit = max_angle_limit
        self.min_angle_limit = min_angle_limit
        self.max_jonit_spd = max_jonit_spd

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(\n"
                f"  motor_num: {self.motor_num},\n"
                f"  max_angle_limit: {self.max_angle_limit}, {self.max_angle_limit * 0.1:.1f},\n"
                f"  min_angle_limit: {self.min_angle_limit}, {self.min_angle_limit * 0.1:.1f},\n"
                f"  max_jonit_spd: {self.max_jonit_spd}, {self.max_jonit_spd * 0.001:.3f}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
