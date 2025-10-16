#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgFeedbackRespSetInstruction:
    '''
    msg_v2_feedback
    
    发送设置指令后的应答帧, 0x4XX开头为设置指令id

    CAN ID:
        0x476

    Args:
        instruction_index: 应答指令索引
            取设置指令 id 最后一个字节
            例如,应答 0x471 设置指令时此位填充0x71
        is_set_zero_successfully: 零点是否设置成功
            零点成功设置-0x01
            设置失败/未设置-0x00
            仅在关节设置指令--成功设置 N 号电机当前位置为零点时应答-0x01
    
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
    
    Set Command ResponseThe response frame after sending the setting command, starting with 0x4XX is the setting command ID

    CAN ID:
        0x476

    Args:
        instruction_index (int): The response instruction index.
            This is derived from the last byte of the set instruction ID.
            For example, when responding to the 0x471 set instruction, this would be 0x71.
        
        is_zero_config_success (int): Flag indicating whether the zero point was successfully set.
            0x01: Zero point successfully set.
            0x00: Zero point set failed/not set.
            This is only applicable when responding to a joint setting instruction that successfully sets 
            motor N's current position as the zero point.

    Bit Description:

        Byte 0: uint8, response instruction index.
            Fill in the last byte of the set command ID.
                Example: Responding to the 0x471 set command, this byte will be 0x71.
        Byte 1: uint8, zero-point configuration success flag.
            0x01: Zero-point successfully set.
            0x00: Failed to set/Not set.
    '''
    def __init__(self,
                 instruction_index: int = -1,
                 is_set_zero_successfully: int = -1):
        self.instruction_index = instruction_index
        self.is_set_zero_successfully = is_set_zero_successfully

    def __str__(self):
        return (f"ArmMsgFeedbackRespSetInstruction(\n"
                f"  instruction_index: {hex(self.instruction_index) },\n"
                f"  is_set_zero_successfully: {self.is_set_zero_successfully },\n"
                f")")

    def __repr__(self):
        return self.__str__()
