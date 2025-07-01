#!/usr/bin/env python3
# -*-coding:utf8-*-
import math
from typing_extensions import (
    Literal,
)
class ArmMsgFeedbackHighSpd:
    '''
    msg_v2_feedback
    
    驱动器信息高速反馈 0x5

    节点 ID:
        0x1~0x06
    
    CAN ID:
        0X251~0x256

    Args:
        can_id: 当前canid,用来代表关节序号
        motor_speed: 电机当前转速
        current: 电机当前电流
        pos: 电机当前位置
        effort: 经过固定系数转换的力矩,单位0.001N/m
    
    位描述:

        Byte 0: 转速高八位, int16, 电机当前转速 单位: 0.001rad/s
        Byte 1: 转速低八位
        Byte 2: 电流高八位, uint16, 电机当前电流 单位: 0.001A
        Byte 3: 电流低八位
        Byte 4: 位置最高位, int32, 电机当前位置 单位: rad
        Byte 5: 位置次高位
        Byte 6: 位置次低位
        Byte 7: 位置最低位
    '''
    '''
    msg_v2_feedback
    
    High-Speed Feedback of Drive Information 0x5

    Node ID:
        0x1~0x06

    CAN ID:
        0x251~0x256

    Args:
        can_id: Current CAN ID, used to represent the joint number.
        motor_speed: Motor Speed.
        current: Motor Current.
        pos: Motor Position.
        effort: Torque converted using a fixed coefficient, with a unit of 0.001 N/m.

    
    Bit Description:

        Byte 0: Motor Speed (High Byte), int16, unit: 0.001rad/s
        Byte 1: Motor Speed (Low Byte)
        Byte 2: Motor Current (High Byte), uint16, unit: 0.001A
        Byte 3: Motor Current (Low Byte)
        Byte 4: Motor Position (Most Significant Byte), int32, unit: rad
        Byte 5: Motor Position (Second Most Significant Byte)
        Byte 6: Motor Position (Second Least Significant Byte)
        Byte 7: Motor Position (Least Significant Byte)
    '''
    def __init__(self, 
                 can_id: Literal[0x000, 0x251, 0x252, 0x253, 0x254, 0x255, 0x256] = 0,
                 motor_speed: int = 0, 
                 current: int = 0, 
                 pos: int = 0,
                 effort: float = 0
                 ):
        if can_id not in [0x000, 0x251, 0x252, 0x253, 0x254, 0x255, 0x256]:
            raise ValueError(f"'can_id' Value {can_id} out of range [0x000, 0x251, 0x252, 0x253, 0x254, 0x255, 0x256]")
        self._COEFFICIENT_1_3 = 1.18125
        self._COEFFICIENT_4_6 = 0.95844
        self.can_id = can_id
        self.motor_speed = motor_speed
        self.current = current
        self.pos = pos
        self.effort = effort
    
    def cal_effort(self, current: int = None)-> float:
        current_ = 0
        if(current is None):
            current_ = self.current
        elif(isinstance(current, (int, float))):
            current_ = current
        else:
            raise TypeError(f"current {current} is not 'int' or 'float'.")
        if(self.can_id in [0x251, 0x252, 0x253]):
            self.effort = current_ * self._COEFFICIENT_1_3
        elif(self.can_id in [0x254, 0x255, 0x256]):
            self.effort = current_ * self._COEFFICIENT_4_6
        return self.effort

    def __str__(self):
        return (f"ArmMsgFeedbackHighSpd(\n"
                f"  can_id: {hex(self.can_id)}\n"
                f"  motor_speed: {self.motor_speed}\n"
                f"  current: {self.current}\n"
                f"  pos: {self.pos}\n"
                f"  effort: {self.effort}\n"
                f")")

    def __repr__(self):
        return self.__str__()
