#!/usr/bin/env python3
# -*-coding:utf8-*-
import math
from typing_extensions import (
    Literal,
)
class ArmHighSpdFeedback:
    '''
    驱动器信息高速反馈 0x5

    节点 ID: 0x1~0x06
    帧 ID :  0X251~0x256

    :Byte 0: 转速高八位, int16, 电机当前转速 单位: RPM
    :Byte 1: 转速低八位
    :Byte 2: 电流高八位, uint16, 电机当前电流 单位: 0.1A
    :Byte 3: 电流低八位
    :Byte 4: 位置最高位, int32, 电机当前位置 单位: rad
    :Byte 5: 位置次高位
    :Byte 6: 位置次低位
    :Byte 7: 位置最低位
    '''
    def __init__(self, 
                 can_id:Literal[0x000,0x251,0x252,0x253,0x254,0x254,0x255,0x256]=0,
                 motor_speed:int=0, 
                 current:int=0, 
                 pos: int=0,
                 ):
        """
        初始化 ArmHighSpdFeedback 实例。
        """
        if can_id not in [0x000,0x251,0x252,0x253,0x254,0x254,0x255,0x256]:
            raise ValueError(f"can_id 值 {can_id} 不在范围 [0x000,0x251,0x252,0x253,0x254,0x254,0x255,0x256]")
        self.can_id = can_id
        self.motor_speed = motor_speed
        self.current = current
        self.pos = pos

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmHighSpdFeedback(\n"
                f"  can_id: {hex(self.can_id)},\n"
                f"  motor_speed: {self.motor_speed} RPM,\n"
                f"  current: {self.current}, {self.current*0.1}A\n"
                f"  pos: {self.pos} rad\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
