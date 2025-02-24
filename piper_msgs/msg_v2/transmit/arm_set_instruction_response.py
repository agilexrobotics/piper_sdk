#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgInstructionResponseConfig:
    '''
    msg_v2_transmit
    
    设置指令应答

    CAN ID:
        0x476

    Args:
        instruction_index: 应答指令索引
        zero_config_success_flag: 零点是否设置成功
    
    位描述:
    
        Byte 0: uint8, 应答指令索引
                取设置指令 id 最后一个字节
                例如：应答 0x471 设置指令时此位填充0x71
        Byte 1: uint8, 零点是否设置成功
                零点成功设置 : 0x01
                设置失败/未设置: 0x00
                仅在关节设置指令--成功设置 N 号电机当前位置为零点时应答 0x01
    '''
    '''
    msg_v2_transmit
    
    Set Command Response

    CAN ID:
        0x476

    Args:
        instruction_index: Response instruction index.
        zero_config_success_flag: Whether the zero-point configuration was successful.

    Bit Description:

        Byte 0: uint8, response instruction index.
            Fill in the last byte of the set command ID.
                Example: Responding to the 0x471 set command, this byte will be 0x71.
        Byte 1: uint8, zero-point configuration success flag.
            0x01: Zero-point successfully set.
            0x00: Failed to set/Not set.
    '''
    def __init__(self,
                 instruction_index: int = 0,
                 zero_config_success_flag: Literal[0x00, 0x01] =0 ):
        if zero_config_success_flag not in [0x00, 0x01]:
            raise ValueError(f"'zero_config_success_flag' Value {zero_config_success_flag} out of range [0x01, 0x02]")
        self.instruction_index = instruction_index
        self.zero_config_success_flag = zero_config_success_flag

    def __str__(self):
        return (f"ArmMsgInstructionResponseConfig(\n"
                f"  instruction_index: {self.instruction_index },\n"
                f"  zero_config_success_flag: {self.zero_config_success_flag },\n"
                f")")

    def __repr__(self):
        return self.__str__()
