#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)

class ArmMsgMasterSlaveModeConfig:
    '''
    随动主从模式设置指令
    '''
    def __init__(self, 
                 linkage_config:Literal[0x00, 0xFA, 0xFC]=0x00,
                 feedback_offset:Literal[0x00, 0x10, 0x20]=0x00,
                 ctrl_offset:Literal[0x00, 0x10, 0x20]=0x00,
                 linkage_offset:Literal[0x00, 0x10, 0x20]=0x00):
        """
        初始化 ArmMsgMasterSlaveModeConfig 实例。

        :Byte 0 linkage_config: uint8, 联动设置指令。
                                0x00 无效
                                0xFA 设置为示教输入臂
                                0xFC 设置为运动输出臂
        :Byte 1 feedback_offset: uint8, 反馈指令偏移值。
                                0x00 : 不偏移/恢复默认
                                0x10 ：反馈指令基 ID 由 2Ax偏移为 2Bx
                                0x20 ：反馈指令基 ID 由 2Ax偏移为 2Cx
        :Byte 2 ctrl_offset: uint8, 控制指令偏移值。
                                0x00 : 不偏移/恢复默认
                                0x10 ：控制指令基 ID 由 15x偏移为 16x
                                0x20 ：控制指令基 ID 由 15x偏移为 17x
        :Byte 3 linkage_offset: uint8, 联动模式控制目标地址偏移值。
                                0x00 : 不偏移/恢复默认
                                0x10 : 控制目标地址基 ID由 15x 偏移为 16x
                                0x20 : 控制目标地址基 ID由 15x 偏移为 17x
        """
        if linkage_config not in [0x00, 0xFA, 0xFC]:
            raise ValueError(f"linkage_config 值 {linkage_config} 超出范围 [0x00, 0xFA, 0xFC]")
        if feedback_offset not in [0x00, 0x10, 0x20]:
            raise ValueError(f"feedback_offset 值 {feedback_offset} 超出范围 [0x00, 0x10, 0x20]")
        if ctrl_offset not in [0x00, 0x10, 0x20]:
            raise ValueError(f"ctrl_offset 值 {ctrl_offset} 超出范围 [0x00, 0x10, 0x20]")
        if linkage_offset not in [0x00, 0x10, 0x20]:
            raise ValueError(f"linkage_offset 值 {linkage_offset} 超出范围 [0x00, 0x10, 0x20]")
        self.linkage_config = linkage_config
        self.feedback_offset = feedback_offset
        self.ctrl_offset = ctrl_offset
        self.linkage_offset = linkage_offset

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。

        :return: 格式化的字符串
        """
        return (f"ArmMsgMasterSlaveModeConfig(\n"
                f"  linkage_config: {self.linkage_config },\n"
                f"  feedback_offset: {self.feedback_offset },\n"
                f"  ctrl_offset: {self.ctrl_offset },\n"
                f"  linkage_offset: {self.linkage_offset}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
