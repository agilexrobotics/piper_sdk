#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgMotorAngleLimitMaxSpdSet:
    '''
    msg_v1_transmit
    
    电机角度限制/最大速度设置指令

    CAN ID:
        0x474

    Args:
        motor_num: 关节电机序号
        max_angle_limit: 最大角度限制,单位 0.1°
        min_angle_limit: 最小角度限制,单位 0.1°
        max_joint_spd: 最大关节速度,单位 0.001rad/s,范围[0,3000]
    
    |joint_name|     limit(rad)       |    limit(angle)    |     limit(rad/s)   |
    |----------|     ----------       |     ----------     |     ----------     |
    |joint1    |   [-2.6179, 2.6179]  |    [-150.0, 150.0] |      [0, 3.0]      |
    |joint2    |   [0, 3.14]          |    [0, 180.0]      |      [0, 3.0]      |
    |joint3    |   [-2.967, 0]        |    [-170, 0]       |      [0, 3.0]      |
    |joint4    |   [-1.745, 1.745]    |    [-100.0, 100.0] |      [0, 3.0]      |
    |joint5    |   [-1.22, 1.22]      |    [-70.0, 70.0]   |      [0, 3.0]      |
    |joint6    |   [-2.09439, 2.09439]|    [-120.0, 120.0] |      [0, 3.0]      |
    
    位描述:
    
        Byte 0: 关节电机序号 uint8, 值域 1-6:1-6 代表关节驱动器序号
        Byte 1: 最大角度限制 H: int16, 单位 0.1°
        Byte 2: 最大角度限制 L
        Byte 3: 最小角度限制 H: int16, 单位 0.1°
        Byte 4: 最小角度限制 L
        Byte 5: 最大关节速度 H: uint16, 单位 0.001rad/s
        Byte 6: 最大关节速度 L
    '''
    '''
    msg_v1_transmit
    
    Motor Angle Limits/Maximum Speed Setting Command

    CAN ID:
        0x474

    Args:
        motor_num: Joint motor index.
        max_angle_limit: Maximum angle limit, unit 0.1°.
        min_angle_limit: Minimum angle limit, unit 0.1°.
        max_joint_spd: Maximum joint speed, unit 0.001 rad/s,Range [0, 3000].
    
    |joint_name|     limit(rad)       |    limit(angle)    |     limit(rad/s)   |
    |----------|     ----------       |     ----------     |     ----------     |
    |joint1    |   [-2.6179, 2.6179]  |    [-150.0, 150.0] |      [0, 3.0]      |
    |joint2    |   [0, 3.14]          |    [0, 180.0]      |      [0, 3.0]      |
    |joint3    |   [-2.967, 0]        |    [-170, 0]       |      [0, 3.0]      |
    |joint4    |   [-1.745, 1.745]    |    [-100.0, 100.0] |      [0, 3.0]      |
    |joint5    |   [-1.22, 1.22]      |    [-70.0, 70.0]   |      [0, 3.0]      |
    |joint6    |   [-2.09439, 2.09439]|    [-120.0, 120.0] |      [0, 3.0]      |
    
    Bit Description:

        Byte 0: Joint motor index, uint8, range 1-6.
        Byte 1: Maximum angle limit (high byte), int16, unit 0.1°.
        Byte 2: Maximum angle limit (low byte).
        Byte 3: Minimum angle limit (high byte), int16, unit 0.1°.
        Byte 4: Minimum angle limit (low byte).
        Byte 5: Maximum joint speed (high byte), uint16, unit 0.001 rad/s.
        Byte 6: Maximum joint speed (low byte).
    '''
    def __init__(self, 
                 motor_num: Literal[1, 2, 3, 4, 5, 6] = 1, 
                 max_angle_limit: int = 0, 
                 min_angle_limit: int = 0,
                 max_joint_spd: int = 3000):
        if motor_num not in [1, 2, 3, 4, 5, 6]:
            raise ValueError(f"'motor_num' Value {motor_num} out of range [1, 2, 3, 4, 5, 6]")
        if not (0 <= max_joint_spd <= 3000):
            raise ValueError(f"'max_joint_spd' Value {max_joint_spd} out of range 0-3000")
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
