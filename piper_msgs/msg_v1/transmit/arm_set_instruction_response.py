#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgInstructionResponseConfig:
    '''
    设置指令应答

    0x476

    :Byte 0 uint8, 应答指令索引
                        取设置指令 id 最后一个字节
                        例如：应答 0x471 设置指令时此位填充 0x71
    :Byte 1 uint8, 零点是否设置成功
                        零点成功设置 : 0x01
                        设置失败/未设置: 0x00
                        仅在关节设置指令--成功设置 N 号电机当前位置为零点时应答 0x01
    '''
    def __init__(self,
                 instruction_index:int=0,
                 zero_config_success_flag:Literal[0x00, 0x01]=0):
        """
        初始化 ArmMsgSearchMotorMaxAngleSpdAccConfig 实例。

        设置指令应答

        0x476

        :Byte 0 uint8, 应答指令索引
                            取设置指令 id 最后一个字节
                            例如：应答 0x471 设置指令时此位填充 0x71
        :Byte 1 uint8, 零点是否设置成功
                            零点成功设置 : 0x01
                            设置失败/未设置: 0x00
                            仅在关节设置指令--成功设置 N 号电机当前位置为零点时应答 0x01
        """
        if zero_config_success_flag not in [0x00, 0x01]:
            raise ValueError(f"zero_config_success_flag 值 {zero_config_success_flag} 超出范围 [0x01, 0x02]")
        self.instruction_index = instruction_index
        self.zero_config_success_flag = zero_config_success_flag

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。

        :return: 格式化的字符串
        """
        return (f"ArmMsgInstructionResponseConfig(\n"
                f"  instruction_index: {self.instruction_index },\n"
                f"  zero_config_success_flag: {self.zero_config_success_flag },\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
