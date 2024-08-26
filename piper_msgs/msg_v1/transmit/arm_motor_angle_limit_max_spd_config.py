#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgMotorAngleLimitMaxSpdSet:
    '''
    电机角度限制/最大速度设置指令

    0x474

    :Byte 0 关节电机序号 uint8, 单位 0.1°, 值域 1-6:1-6 代表关节驱动器序号；
    :Byte 1 最大角度限制 H: int16, 单位 0.1°
    :Byte 2 最大角度限制 L
    :Byte 3 最小角度限制 H: int16, 单位 0.1°
    :Byte 4 最小角度限制 L
    :Byte 5 最大关节速度 H: uint16, 单位 0.001rad/s
    :Byte 6 最大关节速度 L
    '''
    def __init__(self, 
                 motor_num:Literal[1, 2, 3, 4, 5, 6]=1, 
                 max_angle_limit: int=0, 
                 min_angle_limit: int=0,
                 max_jonit_spd: int=0):
        """
        电机角度限制/最大速度设置指令

        0x474

        :Byte 0 关节电机序号 uint8, 单位 0.1°, 值域 1-6:1-6 代表关节驱动器序号；
        :Byte 1 最大角度限制 H: int16, 单位 0.1°
        :Byte 2 最大角度限制 L
        :Byte 3 最小角度限制 H: int16, 单位 0.1°
        :Byte 4 最小角度限制 L
        :Byte 5 最大关节速度 H: uint16, 单位 0.001rad/s
        :Byte 6 最大关节速度 L
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
        return (f"ArmMsgMotorAngleSpdLimitConfig(\n"
                f"  motor_num: {self.motor_num},\n"
                f"  max_angle_limit: {self.max_angle_limit}, {self.max_angle_limit * 0.1:.1f},\n"
                f"  min_angle_limit: {self.min_angle_limit}, {self.min_angle_limit * 0.1:.1f},\n"
                f"  max_jonit_spd: {self.max_jonit_spd}, {self.max_jonit_spd * 0.3:.3f}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
