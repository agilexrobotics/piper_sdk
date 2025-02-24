#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgCircularPatternCoordNumUpdateCtrl:
    '''
    msg_v2_transmit
    
    圆弧模式坐标序号更新指令
    
    CAN ID:
        0x158
    
    Args:
        instruction_num: 指令点序号
    
    位描述:

        Byte 0: uint8, 指令点序号,以整数表示。
                0x00 无效
                0x01 起点
                0x02 中点
                0x03 终点
    '''
    '''
    msg_v2_transmit
    
    Arc Mode Coordinate Index Update Command

    CAN ID:
        0x158

    Args:
        instruction_num: Instruction point index.

    Bit Description:

        Byte 0 instruction_num: uint8, Instruction point index, represented as an integer.
                        0x00 Invalid
                        0x01 Start point
                        0x02 Midpoint
                        0x03 Endpoint
    '''
    def __init__(self, instruction_num: Literal[0x00, 0x01, 0x02, 0x03] = 0x00):
        if instruction_num not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"'instruction_num' Value {instruction_num} out of range [0x00, 0x01, 0x02, 0x03]")
        self.instruction_num = instruction_num

    def __str__(self):
        return (f"ArmMsgCircularPatternCoordNumUpdateCtrl(\n"
                f"  instruction_num: {self.instruction_num},\n"
                f")")

    def __repr__(self):
        return self.__str__()
