#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgMotorAngleLimitMaxSpdSet:
    '''
    电机角度限制/最大速度设置指令

    CAN ID:
        0x474

    Args:
        motor_num: 关节电机序号
        max_angle_limit: 最大角度限制,单位 0.1°,0x7FFF为设定无效数值
        min_angle_limit: 最小角度限制,单位 0.1°,0x7FFF为设定无效数值
        max_joint_spd: 最大关节速度,单位 0.001rad/s,0x7FFF为设定无效数值
    
    位描述:
    
        Byte 0: 关节电机序号 uint8, 值域 1-6:1-6 代表关节驱动器序号
        Byte 1: 最大角度限制 H: int16, 单位 0.1°(基于V1.5-2版本后增加无效数值0x7FFF)
        Byte 2: 最大角度限制 L
        Byte 3: 最小角度限制 H: int16, 单位 0.1°(基于V1.5-2版本后增加无效数值0x7FFF)
        Byte 4: 最小角度限制 L
        Byte 5: 最大关节速度 H: uint16, 单位 0.001rad/s(基于V1.5-2版本后增加无效数值0x7FFF)
        Byte 6: 最大关节速度 L
    '''
    '''
    Motor Angle Limits/Maximum Speed Setting Command

    CAN ID:
        0x474

    Args:
        motor_num: Joint motor index.
        max_angle_limit: Maximum angle limit, unit 0.1°,0x7FFF is defined as the invalid value.
        min_angle_limit: Minimum angle limit, unit 0.1°,0x7FFF is defined as the invalid value.
        max_joint_spd: Maximum joint speed, unit 0.001 rad/s,0x7FFF is defined as the invalid value.

    Bit Description:

        Byte 0: Joint motor index, uint8, range 1-6.
        Byte 1: Maximum angle limit (high byte), int16, unit 0.1°.(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
        Byte 2: Maximum angle limit (low byte).
        Byte 3: Minimum angle limit (high byte), int16, unit 0.1°.(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
        Byte 4: Minimum angle limit (low byte).
        Byte 5: Maximum joint speed (high byte), uint16, unit 0.001 rad/s.(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
        Byte 6: Maximum joint speed (low byte).
    '''
    def __init__(self, 
                 motor_num:Literal[1, 2, 3, 4, 5, 6]=1, 
                 max_angle_limit: int=0, 
                 min_angle_limit: int=0,
                 max_joint_spd: int=0):
        if motor_num not in [1, 2, 3, 4, 5, 6]:
            raise ValueError(f"motor_num 值 {motor_num} 超出范围 [1, 2, 3, 4, 5, 6]")
        self.motor_num = motor_num
        self.max_angle_limit = max_angle_limit
        self.min_angle_limit = min_angle_limit
        self.max_joint_spd = max_joint_spd

    def __str__(self):
        return (f"ArmMsgMotorAngleSpdLimitConfig(\n"
                f"  motor_num: {self.motor_num},\n"
                f"  max_angle_limit: {self.max_angle_limit}, {self.max_angle_limit * 0.1:.1f},\n"
                f"  min_angle_limit: {self.min_angle_limit}, {self.min_angle_limit * 0.1:.1f},\n"
                f"  max_joint_spd: {self.max_joint_spd}, {self.max_joint_spd * 0.3:.3f}\n"
                f")")

    def __repr__(self):
        return self.__str__()
