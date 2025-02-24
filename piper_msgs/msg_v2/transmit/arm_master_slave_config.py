#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgMasterSlaveModeConfig:
    '''
    msg_v2_transmit
    
    随动主从模式设置指令
    
    CAN ID:
        0x470
    
    Args:
        linkage_config: 联动设置指令
        feedback_offset: 反馈指令偏移值
        ctrl_offset: 控制指令偏移值
        linkage_offset: 联动模式控制目标地址偏移值
    
    位描述:
    
        Byte 0 linkage_config: uint8, 联动设置指令。
                                0x00 无效
                                0xFA 设置为示教输入臂
                                0xFC 设置为运动输出臂
        Byte 1 feedback_offset: uint8, 反馈指令偏移值。
                                0x00 : 不偏移/恢复默认
                                0x10 ：反馈指令基 ID 由 2Ax偏移为 2Bx
                                0x20 ：反馈指令基 ID 由 2Ax偏移为 2Cx
        Byte 2 ctrl_offset: uint8, 控制指令偏移值。
                                0x00 : 不偏移/恢复默认
                                0x10 ：控制指令基 ID 由 15x偏移为 16x
                                0x20 ：控制指令基 ID 由 15x偏移为 17x
        Byte 3 linkage_offset: uint8, 联动模式控制目标地址偏移值。
                                0x00 : 不偏移/恢复默认
                                0x10 : 控制目标地址基 ID由 15x 偏移为 16x
                                0x20 : 控制目标地址基 ID由 15x 偏移为 17x
    '''
    '''
    msg_v2_transmit
    
    Follow Master-Slave Mode Setting Command

    CAN ID:
        0x470

    Args:
        linkage_config: Linkage setting command.
        feedback_offset: Offset value for feedback instructions.
        ctrl_offset: Offset value for control instructions.
        linkage_offset: Offset value for linkage mode control target address.

    Bit Descriptions:

        Byte 0 linkage_config: uint8, linkage setting command.
            0x00: Invalid.
            0xFA: Set as teaching input arm.
            0xFC: Set as motion output arm.

        Byte 1 feedback_offset: uint8, feedback instruction offset value.
            0x00: No offset/restore default.
            0x10: Feedback instruction base ID shifted from 2Ax to 2Bx.
            0x20: Feedback instruction base ID shifted from 2Ax to 2Cx.

        Byte 2 ctrl_offset: uint8, control instruction offset value.
            0x00: No offset/restore default.
            0x10: Control instruction base ID shifted from 15x to 16x.
            0x20: Control instruction base ID shifted from 15x to 17x.

        Byte 3 linkage_offset: uint8, offset value for the linkage mode control target address.
            0x00: No offset/restore default.
            0x10: Control target address base ID shifted from 15x to 16x.
            0x20: Control target address base ID shifted from 15x to 17x.
    '''
    def __init__(self, 
                 linkage_config: Literal[0x00, 0xFA, 0xFC] = 0x00,
                 feedback_offset: Literal[0x00, 0x10, 0x20] = 0x00,
                 ctrl_offset: Literal[0x00, 0x10, 0x20] = 0x00,
                 linkage_offset: Literal[0x00, 0x10, 0x20] = 0x00):
        if linkage_config not in [0x00, 0xFA, 0xFC]:
            raise ValueError(f"'linkage_config' Value {linkage_config} out of range [0x00, 0xFA, 0xFC]")
        if feedback_offset not in [0x00, 0x10, 0x20]:
            raise ValueError(f"'feedback_offset' Value {feedback_offset} out of range [0x00, 0x10, 0x20]")
        if ctrl_offset not in [0x00, 0x10, 0x20]:
            raise ValueError(f"'ctrl_offset' Value {ctrl_offset} out of range [0x00, 0x10, 0x20]")
        if linkage_offset not in [0x00, 0x10, 0x20]:
            raise ValueError(f"'linkage_offset' Value {linkage_offset} out of range [0x00, 0x10, 0x20]")
        self.linkage_config = linkage_config
        self.feedback_offset = feedback_offset
        self.ctrl_offset = ctrl_offset
        self.linkage_offset = linkage_offset

    def __str__(self):
        return (f"ArmMsgMasterSlaveModeConfig(\n"
                f"  linkage_config: {self.linkage_config },\n"
                f"  feedback_offset: {self.feedback_offset },\n"
                f"  ctrl_offset: {self.ctrl_offset },\n"
                f"  linkage_offset: {self.linkage_offset}\n"
                f")")

    def __repr__(self):
        return self.__str__()
