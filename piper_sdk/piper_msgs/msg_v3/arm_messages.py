#!/usr/bin/env python3
# -*-coding:utf8-*-

from abc import ABC, abstractmethod
import time
from enum import Enum, auto
import can
from can.message import Message

from typing import (
    Optional,
)
from .arm_msg_type import ArmMsgType_V3 as ArmMsgType
from ..msg_v2 import PiperMessage
# 导入 feedback 子模块的类
from .feedback import *
# 导入 transmit 子模块的类
from .transmit import *

class PiperMessage_V3(PiperMessage):
    '''
    msg_v3
    
    Piper机械臂全部消息,为所有消息的汇总
    '''
    '''
    msg_v3
    
    Piper Robotic Arm Complete Message Summary
    '''
    def __init__(self, 
                #  反馈
                 type_: ArmMsgType = None,
                 time_stamp: float = 0.0,
                 arm_status_msgs: ArmMsgFeedbackStatus = None,
                 arm_joint_feedback: ArmMsgFeedBackJointStates = None,
                 gripper_feedback: ArmMsgFeedBackGripper = None,
                 arm_end_pose: ArmMsgFeedBackEndPose=None,
                 arm_feedback_current_motor_angle_limit_max_spd:ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd=None,
                 arm_feedback_current_end_vel_acc_param:ArmMsgFeedbackCurrentEndVelAccParam=None,
                 arm_feedback_current_motor_max_acc_limit:ArmMsgFeedbackCurrentMotorMaxAccLimit=None,
                 arm_crash_protection_rating_feedback:ArmMsgFeedbackCrashProtectionRating=None,
                 # arm_feedback_joint_vel_acc:ArmMsgFeedbackJointVelAcc=None
                 # arm_feedback_all_current_motor_angle_limit_max_spd:ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd=None,
                 # arm_feedback_all_motor_max_acc_limit:ArmMsgFeedbackAllCurrentMotorMaxAccLimit=None,
                 arm_high_spd_feedback:ArmMsgFeedbackHighSpd=None,
                 arm_low_spd_feedback:ArmMsgFeedbackLowSpd=None,
                 arm_gripper_teaching_param_feedback:ArmMsgFeedbackGripperTeachingPendantParam=None,
                 arm_feedback_resp_set_instruction:ArmMsgFeedbackRespSetInstruction=None,
                #  发送
                 arm_motion_ctrl_1: ArmMsgMotionCtrl_1=None,
                 arm_motion_ctrl_2: ArmMsgMotionCtrl_2=None,
                 arm_motion_ctrl_cartesian: ArmMsgMotionCtrlCartesian=None,
                 arm_joint_ctrl: ArmMsgJointCtrl=None,
                 arm_circular_ctrl: ArmMsgCircularPatternCoordNumUpdateCtrl=None,
                 arm_gripper_ctrl: ArmMsgGripperCtrl=None,
                 arm_joint_mit_ctrl: ArmMsgJointMitCtrl=None,
                 arm_ms_config: ArmMsgMasterSlaveModeConfig=None,
                 arm_motor_enable: ArmMsgMotorEnableDisableConfig=None,
                 arm_search_motor_max_angle_spd_acc_limit:ArmMsgSearchMotorMaxAngleSpdAccLimit=None,
                 arm_motor_angle_limit_max_spd_set:ArmMsgMotorAngleLimitMaxSpdSet=None,
                 arm_joint_config:ArmMsgJointConfig=None,
                 arm_set_instruction_response:ArmMsgInstructionResponseConfig=None,
                 arm_param_enquiry_and_config:ArmMsgParamEnquiryAndConfig=None,
                 arm_end_vel_acc_param_config:ArmMsgEndVelAccParamConfig=None,
                 arm_crash_protection_rating_config:ArmMsgCrashProtectionRatingConfig=None,
                 arm_gripper_teaching_param_config:ArmMsgGripperTeachingPendantParamConfig=None
                 ):
        super().__init__(
                        type_, 
                        time_stamp, 
                        arm_status_msgs, 
                        arm_joint_feedback, 
                        gripper_feedback, 
                        arm_end_pose, 
                        arm_feedback_current_motor_angle_limit_max_spd, 
                        arm_feedback_current_end_vel_acc_param, 
                        arm_feedback_current_motor_max_acc_limit, 
                        arm_crash_protection_rating_feedback, 
                        arm_high_spd_feedback, 
                        arm_low_spd_feedback, 
                        arm_gripper_teaching_param_feedback, 
                        arm_feedback_resp_set_instruction, 
                        arm_motion_ctrl_1, 
                        arm_motion_ctrl_2, 
                        arm_motion_ctrl_cartesian, 
                        arm_joint_ctrl, 
                        arm_circular_ctrl, 
                        arm_gripper_ctrl, 
                        arm_joint_mit_ctrl, 
                        arm_ms_config, 
                        arm_motor_enable, 
                        arm_search_motor_max_angle_spd_acc_limit, 
                        arm_motor_angle_limit_max_spd_set, 
                        arm_joint_config, 
                        arm_set_instruction_response, 
                        arm_param_enquiry_and_config, 
                        arm_end_vel_acc_param_config, 
                        arm_crash_protection_rating_config, 
                        arm_gripper_teaching_param_config
                        )
        self.arm_motion_ctrl_2 = arm_motion_ctrl_2 if arm_motion_ctrl_2 else ArmMsgMotionCtrl_2()
        # 初始化机械臂状态消息
        self.arm_status_msgs = arm_status_msgs if arm_status_msgs else ArmMsgFeedbackStatus()
        # 关节mit控制
        self.arm_joint_mit_ctrl = arm_joint_mit_ctrl if arm_joint_mit_ctrl else ArmMsgJointMitCtrl()