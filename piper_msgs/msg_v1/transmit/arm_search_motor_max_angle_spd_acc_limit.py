#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgSearchMotorMaxAngleSpdAccLimit:
    '''
    查询电机角度/最大速度/最大加速度限制指令

    0x472

    :Byte 0 motor_num: uint8, 关节电机序号。
                        值域 1-6:
                            1-6 代表关节驱动器序号
    :Byte 1 search_content: uint8, 查询内容。
                        0x01 : 查询电机角度/最大速度
                        0x02 : 查询电机最大加速度限制
    '''
    def __init__(self, 
                 motor_num:Literal[1, 2, 3, 4, 5, 6]=1,
                 search_content:Literal[0x01, 0x02]=0x01):
        """
        查询电机角度/最大速度/最大加速度限制指令

        初始化 ArmMsgSearchMotorMaxAngleSpdAccConfig 实例。

        0x472

        :Byte 0 motor_num: uint8, 关节电机序号。
                            值域 1-6:
                                1-6 代表关节驱动器序号
        :Byte 1 search_content: uint8, 查询内容。
                            0x01 : 查询电机角度/最大速度
                            0x02 : 查询电机最大加速度限制
        """
        if motor_num not in [1, 2, 3, 4, 5, 6, 7]:
            raise ValueError(f"motor_num 值 {motor_num} 超出范围 [1, 2, 3, 4, 5, 6, 7]")
        if search_content not in [0x01, 0x02]:
            raise ValueError(f"search_content 值 {search_content} 超出范围 [0x01, 0x02]")
        self.motor_num = motor_num
        self.search_content = search_content

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。

        :return: 格式化的字符串
        """
        return (f"ArmMsgSearchMotorMaxAngleSpdAccConfig(\n"
                f"  motor_num: {self.motor_num },\n"
                f"  search_content: {self.search_content },\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
