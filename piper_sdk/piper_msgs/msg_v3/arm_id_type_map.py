#!/usr/bin/env python3
# -*-coding:utf8-*-

from typing import (
    Optional,
)
from .arm_msg_type import ArmMsgType_V3
from .can_id import CanIDPiper_V3
from ..msg_v2 import ArmMessageMapping

_ARM_MSG_TYPE = ArmMsgType_V3
_CAN_ID = CanIDPiper_V3

class ArmMessageMapping_V3(ArmMessageMapping):
    '''
    msg_v3
    
    机械臂消息类型和CAN ID的映射
    '''
    '''
    msg_v3
    
    Mapping of Robotic Arm Message Types and CAN IDs
    '''
    ArmMsgType = _ARM_MSG_TYPE
    CanIDPiper = _CAN_ID

    # 从父版本映射中删除的 CAN ID。
    # 适用场景：新协议版本废弃了某条旧报文，或者某个旧 CAN ID 在新版本中不应再被解析。
    # 示例：
    #   removed_mapping_ids = {0x15A}
    removed_mapping_ids = set()

    # 已有功能的 CAN ID 发生变化时使用。
    # changed_mapping 会先删除父版本中同名消息类型对应的旧 CAN ID，再写入新的 CAN ID。
    # 适用场景：例如 V5 将 PiperMsgJointMitCtrl_1 从 0x15A 改到 0x16A。
    # 示例：
    #   changed_mapping = {
    #       CanIDPiper_V5.ARM_JOINT_MIT_CTRL_1.value: ArmMsgType.PiperMsgJointMitCtrl_1,
    #   }
    changed_mapping = {

    }

    # 新增的 CAN ID 到消息类型映射。
    # 适用场景：新协议版本增加了父版本没有的新报文。
    # 如果只是新增报文，不会删除父版本中的任何旧映射。
    # 示例：
    #   additional_mapping = {
    #       CanIDPiper_V4.NEW_FRAME.value: ArmMsgType.PiperMsgNewFrame,
    #   }
    additional_mapping = {
        CanIDPiper.ARM_IK_JOINT_FEEDBACK_12.value : ArmMsgType.PiperMsgIKJointFeedBack_12,
        CanIDPiper.ARM_IK_JOINT_FEEDBACK_34.value : ArmMsgType.PiperMsgIKJointFeedBack_34,
        CanIDPiper.ARM_IK_JOINT_FEEDBACK_56.value : ArmMsgType.PiperMsgIKJointFeedBack_56,
    }
