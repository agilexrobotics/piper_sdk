#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgCircularPatternCoordNumUpdateCtrl:
    '''
    圆弧模式坐标序号更新指令

    :Byte 0 instruction_num: uint8, 指令点序号,以整数表示。
                            0x00 无效
                            0x01 起点
                            0x02 中点
                            0x03 终点
    '''
    def __init__(self, instruction_num:Literal[0x00, 0x01, 0x02, 0x03]=0x00):
        """
        初始化 ArmMsgCircularPatternCoordNumUpdateCtrl 实例。

        :Byte 0 instruction_num: uint8, 指令点序号,以整数表示。
                                0x00 无效
                                0x01 起点
                                0x02 中点
                                0x03 终点
        """
        if instruction_num not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"instruction_num 值 {instruction_num} 超出范围 [0x00, 0x01, 0x02, 0x03]")
        self.instruction_num = instruction_num

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。

        :return: 格式化的字符串
        """
        return (f"ArmMsgCircularPatternCoordNumUpdateCtrl(\n"
                f"  instruction_num: {self.instruction_num},\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
