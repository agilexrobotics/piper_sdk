#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgMotorEnableDisableConfig:
    '''
    电机使能/失能设置指令
    '''
    def __init__(self, 
                 motor_num:Literal[1, 2, 3, 4, 5, 6, 7, 0xFF]=0xFF,
                 enable_flag:Literal[0x01, 0x02]=0x01):
        """
        初始化 ArmMsgMotorEnableDisableConfig 实例。

        :Byte 0 motor_num: uint8, 关节电机序号。
                            值域 1-7:
                                1-6 代表关节驱动器序号
                                
                                7代表夹爪电机

                                FF代表全部关节电机(包含夹爪)
        :Byte 1 enable_flag: uint8, 使能/失能。
                            0x01 : 失能
                            0x02 : 使能
        """
        if motor_num not in [1, 2, 3, 4, 5, 6, 7, 0xFF]:
            raise ValueError(f"motor_num 值 {motor_num} 超出范围 [1, 2, 3, 4, 5, 6, 7, 0xFF]")
        if enable_flag not in [0x01, 0x02]:
            raise ValueError(f"enable_flag 值 {enable_flag} 超出范围 [0x01, 0x02]")
        self.motor_num = motor_num
        self.enable_flag = enable_flag

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。

        :return: 格式化的字符串
        """
        return (f"ArmMsgMotorEnableDisableConfig(\n"
                f"  motor_num: {self.motor_num },\n"
                f"  enable_flag: {self.enable_flag },\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
