#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgSearchMotorMaxAngleSpdAccLimit:
    '''
    msg_v2_transmit
    
    查询电机角度/最大速度/最大加速度限制指令

    CAN ID:
        0x472

    Args:
        motor_num: 关节电机序号,1-6
        search_content: 查询内容,0x01-查询电机角度/最大速度,0x02-查询电机最大加速度限制

    位描述:
    
        :Byte 0 motor_num: uint8, 关节电机序号。
                值域 1-6,1-6 代表关节驱动器序号
        :Byte 1 search_content: uint8, 查询内容。
                0x01 : 查询电机角度/最大速度
                0x02 : 查询电机最大加速度限制
    '''
    '''
    msg_v2_transmit
    
    Motor Angle/Max Speed/Max Acceleration Limit Query Command

    CAN ID:
        0x472

    Args:
        motor_num: Motor joint number.
        search_content: Query content.

    Bit Description:

        Byte 0: uint8, motor joint number.
            Value range: 1-6.
                1-6: Represent joint driver numbers.
        Byte 1: uint8, query content.
            0x01: Query motor angle/max speed.
            0x02: Query motor max acceleration limit.
    '''
    def __init__(self, 
                 motor_num: Literal[1, 2, 3, 4, 5, 6] = 1,
                 search_content: Literal[0x01, 0x02] = 0x01):
        if motor_num not in [1, 2, 3, 4, 5, 6, 7]:
            raise ValueError(f"'motor_num' Value {motor_num} out of range [1, 2, 3, 4, 5, 6, 7]")
        if search_content not in [0x01, 0x02]:
            raise ValueError(f"'search_content' Value {search_content} out of range [0x01, 0x02]")
        self.motor_num = motor_num
        self.search_content = search_content

    def __str__(self):
        return (f"ArmMsgSearchMotorMaxAngleSpdAccConfig(\n"
                f"  motor_num: {self.motor_num },\n"
                f"  search_content: {self.search_content },\n"
                f")")

    def __repr__(self):
        return self.__str__()
