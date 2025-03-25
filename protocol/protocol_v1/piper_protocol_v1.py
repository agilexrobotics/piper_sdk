#!/usr/bin/env python3
# -*-coding:utf8-*-
#机械臂协议V1版本，为方便后续修改协议升级，继承自base

from abc import ABC, abstractmethod
import time
from threading import Timer
from enum import Enum, auto
import can
from can.message import Message

from typing import (
    Optional,
)

# import sys,os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from ..piper_protocol_base import C_PiperParserBase
from ...piper_msgs.msg_v1 import (
    ArmMsgType, 
    PiperMessage, 
    ArmMessageMapping
)
from ..can_id_type_map import ProtocolMapping

class C_PiperParserV1(C_PiperParserBase):
    '''
    Piper机械臂解析数据类V1版本
    '''
    '''
    Piper Robotic Arm Data Parsing Class V1 Version
    '''
    def __init__(self) -> None:
        pass

    def GetParserProtocolVersion(self):
        '''
        获取当前协议版本,当前为V1
        '''
        '''
        Get the current protocol version, currently V1.
        '''
        return self.ProtocolVersion.ARM_PROROCOL_V1

    def parse_can_message(self, can_id, can_data, msg):
        """根据 can_id 查找并执行相应的函数"""
        handler = ProtocolMapping.decodemsg_get_handler(can_id, "V1")  # 通过 ProtocolMapping 获取
        if handler:
            # print(handler)
            handler(self, can_id, can_data, msg, "V1")  # 执行解析函数
            return True
        else:
            # print(f"未找到 can_id: {can_id:#x} 的处理函数")
            return False
    
    def process_message(self, can_id, data, msg):
        """解析并处理 CAN 消息"""
        return self.parse_can_message(can_id, data, msg)
    
    def DecodeMessage(self, rx_can_frame: Optional[can.Message], msg:PiperMessage):
        '''解码消息,将can数据帧转为设定的类型

        Args:
            rx_can_frame (Optional[can.Message]): can 数据帧, 为输入
            msg (PiperMessage): 自定义中间层数据, 为输出

        Returns:
            bool:
                can消息的id如果存在, 反馈True

                can消息的id若不存在, 反馈False
        '''
        '''Decode the message, convert the CAN data frame to the specified type.

        Args:

            rx_can_frame (Optional[can.Message]): CAN data frame, input.
            msg (PiperMessage): Custom intermediate data, output.

        Returns:

            bool:
                If the CAN message ID exists, return True.
                If the CAN message ID does not exist, return False.
        '''
        ret:bool = True
        can_id:int = rx_can_frame.arbitration_id
        can_data:bytearray = rx_can_frame.data
        
        if not self.process_message(can_id, can_data, msg):
            ret = False
        return ret

    def parse_msg_type(self, msg_type_, msg, tx_can_frame):
        handler = ProtocolMapping.encodemsg_get_handler(msg_type_, "V1")  # 通过 ProtocolMapping 获取
        # print(msg_type_)
        if handler:
            handler(self, msg_type_, msg, tx_can_frame, "V1")  # 执行解析函数
            return True
        else:
            # print(f"未找到 msg_type: {msg_type} 的处理函数")
            return False
    
    def process_msg(self, msg_type_, msg, tx_can_frame):
        """解析并处理消息"""
        return self.parse_msg_type(msg_type_, msg, tx_can_frame)

    def EncodeMessage(self, msg:PiperMessage, tx_can_frame: Optional[can.Message]):
        '''将消息转为can数据帧

        Args:
            msg (PiperMessage): 自定义数据
            tx_can_frame (Optional[can.Message]): can要发送的数据

        Returns:
            bool:
                msg消息的type如果存在, 反馈True

                msg消息的type若不存在, 反馈False
        '''
        '''Convert the message to CAN data frame

        Args:
            msg (PiperMessage): Custom data
            tx_can_frame (Optional[can.Message]): CAN data to be sent

        Returns:
            bool:
                Returns True if the msg message type exists
                Returns False if the msg message type does not exist
        '''
        ret:bool = True
        msg_type_ = msg.type_
        if not self.process_msg(msg_type_, msg, tx_can_frame):
            ret = False
        return ret
            

