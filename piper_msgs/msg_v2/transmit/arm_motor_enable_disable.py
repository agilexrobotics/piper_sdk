#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgMotorEnableDisableConfig:
    '''
    msg_v2_transmit
    
    电机使能/失能设置指令
    
    CAN ID:
        0x471
    
    Args:
        motor_num: 电机序号[1,7],7代表所有电机
        enable_flag: 使能标志位,0x01-失能;0x02-使能
    
    位描述:
    
        Byte 0: uint8, 关节电机序号。
                值域 1-7:1-6 代表关节驱动器序号,7代表夹爪电机,FF代表全部关节电机(包含夹爪)
        Byte 1: uint8, 使能/失能。
                0x01 : 失能
                0x02 : 使能
    '''
    '''
    msg_v2_transmit
    
    Motor Enable/Disable Command

    CAN ID:
        0x471

    Args:
        motor_num: Motor index [1, 7], where 7 represents all motors.
        enable_flag: Enable flag, 0x01 for disable, 0x02 for enable.

    Bit Description:

        Byte 0:
            motor_num, uint8, motor index.
            Range 1-7:
                1-6: Represents joint motor index.
                7: Represents gripper motor.
                0xFF: Represents all joint motors (including gripper).
        Byte 1:
            enable_flag, uint8, enable/disable.
            0x01: Disable.
            0x02: Enable.
    '''
    def __init__(self, 
                 motor_num: Literal[1, 2, 3, 4, 5, 6, 7, 0xFF] = 0xFF,
                 enable_flag: Literal[0x01, 0x02] = 0x01):
        if motor_num not in [1, 2, 3, 4, 5, 6, 7, 0xFF]:
            raise ValueError(f"'motor_num' Value {motor_num} out of range [1, 2, 3, 4, 5, 6, 7, 0xFF]")
        if enable_flag not in [0x01, 0x02]:
            raise ValueError(f"'enable_flag' Value {enable_flag} out of range [0x01, 0x02]")
        self.motor_num = motor_num
        self.enable_flag = enable_flag

    def __str__(self):
        return (f"ArmMsgMotorEnableDisableConfig(\n"
                f"  motor_num: {self.motor_num },\n"
                f"  enable_flag: {self.enable_flag },\n"
                f")")

    def __repr__(self):
        return self.__str__()
