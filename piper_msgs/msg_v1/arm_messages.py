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
from .arm_msg_type import ArmMsgType
from .feedback.arm_end_pose import ArmMsgEndPoseFeedBack
from .feedback.arm_joint_feedback import ArmMsgJointFeedBack
from .feedback.arm_status import ArmMsgStatus
from .feedback.gripper_feedback import ArmMsgGripperFeedBack
from .feedback.arm_feedback_current_end_vel_acc_param import (
    ArmMsgFeedbackCurrentEndVelAccParam,
)
from .feedback.arm_feedback_current_motor_angle_limit_max_spd import (
    ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd,
    ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd,
)
from .feedback.arm_feedback_current_motor_max_acc_limit import (
    ArmMsgFeedbackCurrentMotorMaxAccLimit,
    ArmMsgFeedbackAllCurrentMotorMaxAccLimit,
)
from .feedback.arm_feedback_joint_vel_acc import (
    ArmMsgFeedbackJointVelAcc,
    ArmMsgFeedbackAllJointVelAcc,
)
from .feedback.arm_high_spd_feedback import ArmHighSpdFeedback
from .feedback.arm_low_spd_feedback import ArmLowSpdFeedback

from .transmit.arm_motion_ctrl_1 import ArmMsgMotionCtrl_1
from .transmit.arm_motion_ctrl_2 import ArmMsgMotionCtrl_2
from .transmit.arm_motion_ctrl_cartesian import ArmMsgMotionCtrlCartesian
from .transmit.arm_joint_ctrl import ArmMsgJointCtrl
from .transmit.arm_circular_pattern import ArmMsgCircularPatternCoordNumUpdateCtrl
from .transmit.arm_gripper_ctrl import ArmMsgGripperCtrl
from .transmit.arm_master_slave_config import ArmMsgMasterSlaveModeConfig
from .transmit.arm_motor_enable_disable import ArmMsgMotorEnableDisableConfig
from .transmit.arm_search_motor_max_angle_spd_acc_limit import (
    ArmMsgSearchMotorMaxAngleSpdAccLimit,
)
from .transmit.arm_motor_angle_limit_max_spd_config import (
    ArmMsgMotorAngleLimitMaxSpdSet,
)
from .transmit.arm_joint_config import ArmMsgJointConfig
from .transmit.arm_set_instruction_response import ArmMsgInstructionResponseConfig
from .transmit.arm_param_enquiry_and_config import ArmMsgParamEnquiryAndConfig
from .transmit.arm_end_vel_acc_param_config import ArmMsgEndVelAccParamConfig
from .transmit.arm_crash_protection_rating_config import (
    ArmMsgCrashProtectionRatingConfig,
)
from .feedback.arm_crash_protection_rating_feedback import (
    ArmMsgCrashProtectionRatingFeedback,
)


class PiperMessage:
    """
    Piper机械臂全部消息,为所有消息的汇总
    """

    def __init__(
        self,
        #  反馈
        type_: "ArmMsgType" = None,
        arm_status_msgs: "ArmMsgStatus" = None,
        arm_joint_feedback: "ArmMsgJointFeedBack" = None,
        gripper_feedback: "ArmMsgGripperFeedBack" = None,
        arm_end_pose: "ArmMsgEndPoseFeedBack" = None,
        arm_feedback_current_motor_angle_limit_max_spd: "ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd" = None,
        arm_feedback_current_end_vel_acc_param: "ArmMsgFeedbackCurrentEndVelAccParam" = None,
        arm_feedback_current_motor_max_acc_limit: "ArmMsgFeedbackCurrentMotorMaxAccLimit" = None,
        arm_crash_protection_rating_feedback: "ArmMsgCrashProtectionRatingFeedback" = None,
        #  arm_feedback_joint_vel_acc:'ArmMsgFeedbackJointVelAcc'=None
        #  arm_feedback_all_current_motor_angle_limit_max_spd:'ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd'=None,
        #  arm_feedback_all_motor_max_acc_limit:'ArmMsgFeedbackAllCurrentMotorMaxAccLimit'=None,
        arm_high_spd_feedback: "ArmHighSpdFeedback" = None,
        arm_low_spd_feedback: "ArmLowSpdFeedback" = None,
        #  发送
        arm_motion_ctrl_1: "ArmMsgMotionCtrl_1" = None,
        arm_motion_ctrl_2: "ArmMsgMotionCtrl_2" = None,
        arm_motion_ctrl_cartesian: "ArmMsgMotionCtrlCartesian" = None,
        arm_joint_ctrl: "ArmMsgJointCtrl" = None,
        arm_circular_ctrl: "ArmMsgCircularPatternCoordNumUpdateCtrl" = None,
        arm_gripper_ctrl: "ArmMsgGripperCtrl" = None,
        arm_ms_config: "ArmMsgMasterSlaveModeConfig" = None,
        arm_motor_enable: "ArmMsgMotorEnableDisableConfig" = None,
        arm_search_motor_max_angle_spd_acc_limit: "ArmMsgSearchMotorMaxAngleSpdAccLimit" = None,
        arm_motor_angle_limit_max_spd_set: "ArmMsgMotorAngleLimitMaxSpdSet" = None,
        arm_joint_config: "ArmMsgJointConfig" = None,
        arm_set_instruction_response: "ArmMsgInstructionResponseConfig" = None,
        arm_param_enquiry_and_config: "ArmMsgParamEnquiryAndConfig" = None,
        arm_end_vel_acc_param_config: "ArmMsgEndVelAccParamConfig" = None,
        arm_crash_protection_rating_config: "ArmMsgCrashProtectionRatingConfig" = None,
    ):
        # -------------------------------反馈-------------------------------------------
        # 初始化数据帧类型
        self.type_ = type_
        # 初始化机械臂状态消息
        self.arm_status_msgs = arm_status_msgs if arm_status_msgs else ArmMsgStatus()
        # 初始化机械臂关节反馈
        self.arm_joint_feedback = (
            arm_joint_feedback if arm_joint_feedback else ArmMsgJointFeedBack()
        )
        # 初始化夹爪反馈
        self.gripper_feedback = (
            gripper_feedback if gripper_feedback else ArmMsgGripperFeedBack()
        )
        # 初始化末端姿态反馈
        self.arm_end_pose = arm_end_pose if arm_end_pose else ArmMsgEndPoseFeedBack()
        # 驱动器信息高速反馈
        self.arm_high_spd_feedback_1 = (
            arm_high_spd_feedback if arm_high_spd_feedback else ArmHighSpdFeedback()
        )
        self.arm_high_spd_feedback_2 = (
            arm_high_spd_feedback if arm_high_spd_feedback else ArmHighSpdFeedback()
        )
        self.arm_high_spd_feedback_3 = (
            arm_high_spd_feedback if arm_high_spd_feedback else ArmHighSpdFeedback()
        )
        self.arm_high_spd_feedback_4 = (
            arm_high_spd_feedback if arm_high_spd_feedback else ArmHighSpdFeedback()
        )
        self.arm_high_spd_feedback_5 = (
            arm_high_spd_feedback if arm_high_spd_feedback else ArmHighSpdFeedback()
        )
        self.arm_high_spd_feedback_6 = (
            arm_high_spd_feedback if arm_high_spd_feedback else ArmHighSpdFeedback()
        )
        # 驱动器信息低速反馈
        self.arm_low_spd_feedback_1 = (
            arm_low_spd_feedback if arm_low_spd_feedback else ArmLowSpdFeedback()
        )
        self.arm_low_spd_feedback_2 = (
            arm_low_spd_feedback if arm_low_spd_feedback else ArmLowSpdFeedback()
        )
        self.arm_low_spd_feedback_3 = (
            arm_low_spd_feedback if arm_low_spd_feedback else ArmLowSpdFeedback()
        )
        self.arm_low_spd_feedback_4 = (
            arm_low_spd_feedback if arm_low_spd_feedback else ArmLowSpdFeedback()
        )
        self.arm_low_spd_feedback_5 = (
            arm_low_spd_feedback if arm_low_spd_feedback else ArmLowSpdFeedback()
        )
        self.arm_low_spd_feedback_6 = (
            arm_low_spd_feedback if arm_low_spd_feedback else ArmLowSpdFeedback()
        )
        # -------------------------------发送-------------------------------------------
        self.arm_motion_ctrl_1 = (
            arm_motion_ctrl_1 if arm_motion_ctrl_1 else ArmMsgMotionCtrl_1()
        )
        self.arm_motion_ctrl_2 = (
            arm_motion_ctrl_2 if arm_motion_ctrl_2 else ArmMsgMotionCtrl_2()
        )
        self.arm_motion_ctrl_cartesian = (
            arm_motion_ctrl_cartesian
            if arm_motion_ctrl_cartesian
            else ArmMsgMotionCtrlCartesian()
        )
        self.arm_joint_ctrl = arm_joint_ctrl if arm_joint_ctrl else ArmMsgJointCtrl()
        self.arm_circular_ctrl = (
            arm_circular_ctrl
            if arm_circular_ctrl
            else ArmMsgCircularPatternCoordNumUpdateCtrl()
        )
        self.arm_gripper_ctrl = (
            arm_gripper_ctrl if arm_gripper_ctrl else ArmMsgGripperCtrl()
        )
        self.arm_ms_config = (
            arm_ms_config if arm_ms_config else ArmMsgMasterSlaveModeConfig()
        )
        # 电机使能/失能设置指令
        self.arm_motor_enable = (
            arm_motor_enable if arm_motor_enable else ArmMsgMotorEnableDisableConfig()
        )
        # 查询电机角度/最大速度/最大加速度限制指令
        self.arm_search_motor_max_angle_spd_acc_limit = (
            arm_search_motor_max_angle_spd_acc_limit
            if arm_search_motor_max_angle_spd_acc_limit
            else ArmMsgSearchMotorMaxAngleSpdAccLimit()
        )
        # 反馈当前电机限制角度/最大速度
        self.arm_feedback_current_motor_angle_limit_max_spd = (
            arm_feedback_current_motor_angle_limit_max_spd
            if arm_feedback_current_motor_angle_limit_max_spd
            else ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd()
        )
        # 电机角度限制/最大速度设置指令
        self.arm_motor_angle_limit_max_spd_set = (
            arm_motor_angle_limit_max_spd_set
            if arm_motor_angle_limit_max_spd_set
            else ArmMsgMotorAngleLimitMaxSpdSet()
        )
        # 关节设置指令
        self.arm_joint_config = (
            arm_joint_config if arm_joint_config else ArmMsgJointConfig()
        )
        # 设置指令应答
        self.arm_set_instruction_response = (
            arm_set_instruction_response
            if arm_set_instruction_response
            else ArmMsgInstructionResponseConfig()
        )
        # 机械臂参数查询与设置指令
        self.arm_param_enquiry_and_config = (
            arm_param_enquiry_and_config
            if arm_param_enquiry_and_config
            else ArmMsgParamEnquiryAndConfig()
        )
        # 反馈当前末端速度/加速度参数
        self.arm_feedback_current_end_vel_acc_param = (
            arm_feedback_current_end_vel_acc_param
            if arm_feedback_current_end_vel_acc_param
            else ArmMsgFeedbackCurrentEndVelAccParam()
        )
        # 末端速度/加速度参数设置指令
        self.arm_end_vel_acc_param_config = (
            arm_end_vel_acc_param_config
            if arm_end_vel_acc_param_config
            else ArmMsgEndVelAccParamConfig()
        )
        # 碰撞防护等级设置指令
        self.arm_crash_protection_rating_config = (
            arm_crash_protection_rating_config
            if arm_crash_protection_rating_config
            else ArmMsgCrashProtectionRatingConfig()
        )
        # 碰撞防护等级设置反馈指令
        self.arm_crash_protection_rating_feedback = (
            arm_crash_protection_rating_feedback
            if arm_crash_protection_rating_feedback
            else ArmMsgCrashProtectionRatingFeedback()
        )
        # 反馈当前电机最大加速度限制
        self.arm_feedback_current_motor_max_acc_limit = (
            arm_feedback_current_motor_max_acc_limit
            if arm_feedback_current_motor_max_acc_limit
            else ArmMsgFeedbackCurrentMotorMaxAccLimit()
        )
        # 反馈各个关节当前末端速度/加速度
        # self.arm_feedback_joint_vel_acc = arm_feedback_joint_vel_acc \
        #     if arm_feedback_joint_vel_acc else ArmMsgFeedbackJointVelAcc()
        # 全部的电机当前限制角度/最大速度
        # self.arm_feedback_all_current_motor_angle_limit_max_spd = arm_feedback_all_current_motor_angle_limit_max_spd \
        #     if arm_feedback_all_current_motor_angle_limit_max_spd else ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd()
        # # 全部的电机最大加速度限制
        # self.arm_feedback_all_motor_max_acc_limit = arm_feedback_all_motor_max_acc_limit \
        #     if arm_feedback_all_motor_max_acc_limit else ArmMsgFeedbackAllCurrentMotorMaxAccLimit()

    def __str__(self):
        if self.type_ == ArmMsgType.PiperMsgStatusFeedback:
            return f"Type: {self.type_}\n" f"Arm Status: {self.arm_status_msgs}\n"
        elif self.type_ == ArmMsgType.PiperMsgJointFeedBack_12:
            return f"Type: {self.type_}\n" f"Joint Feed: {self.arm_joint_feedback}\n"
        elif self.type_ == ArmMsgType.PiperMsgJointFeedBack_34:
            return f"Type: {self.type_}\n" f"Joint Feed: {self.arm_joint_feedback}\n"
        elif self.type_ == ArmMsgType.PiperMsgJointFeedBack_56:
            return f"Type: {self.type_}\n" f"Joint Feed: {self.arm_joint_feedback}\n"
        elif self.type_ == ArmMsgType.PiperMsgGripperFeedBack:
            return f"Type: {self.type_}\n" f"Gripper Feed: {self.gripper_feedback}\n"
        elif self.type_ == ArmMsgType.PiperMsgEndPoseFeedback_1:
            return f"Type: {self.type_}\n" f"End Pose Feed: {self.arm_end_pose}\n"
        elif self.type_ == ArmMsgType.PiperMsgEndPoseFeedback_2:
            return f"Type: {self.type_}\n" f"End Pose Feed: {self.arm_end_pose}\n"
        elif self.type_ == ArmMsgType.PiperMsgEndPoseFeedback_3:
            return f"Type: {self.type_}\n" f"End Pose Feed: {self.arm_end_pose}\n"
        elif self.type_ == ArmMsgType.PiperMsgHighSpdFeed_1:
            return (
                f"Type: {self.type_}\n"
                f"High Spd Feedback: {self.arm_high_spd_feedback_1}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgHighSpdFeed_2:
            return (
                f"Type: {self.type_}\n"
                f"High Spd Feedback: {self.arm_high_spd_feedback_2}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgHighSpdFeed_3:
            return (
                f"Type: {self.type_}\n"
                f"High Spd Feedback: {self.arm_high_spd_feedback_3}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgHighSpdFeed_4:
            return (
                f"Type: {self.type_}\n"
                f"High Spd Feedback: {self.arm_high_spd_feedback_4}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgHighSpdFeed_5:
            return (
                f"Type: {self.type_}\n"
                f"High Spd Feedback: {self.arm_high_spd_feedback_5}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgHighSpdFeed_6:
            return (
                f"Type: {self.type_}\n"
                f"High Spd Feedback: {self.arm_high_spd_feedback_6}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgLowSpdFeed_1:
            return (
                f"Type: {self.type_}\n"
                f"Low Spd Feedback: {self.arm_low_spd_feedback_1}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgLowSpdFeed_2:
            return (
                f"Type: {self.type_}\n"
                f"Low Spd Feedback: {self.arm_low_spd_feedback_2}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgLowSpdFeed_3:
            return (
                f"Type: {self.type_}\n"
                f"Low Spd Feedback: {self.arm_low_spd_feedback_3}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgLowSpdFeed_4:
            return (
                f"Type: {self.type_}\n"
                f"Low Spd Feedback: {self.arm_low_spd_feedback_4}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgLowSpdFeed_5:
            return (
                f"Type: {self.type_}\n"
                f"Low Spd Feedback: {self.arm_low_spd_feedback_5}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgLowSpdFeed_6:
            return (
                f"Type: {self.type_}\n"
                f"Low Spd Feedback: {self.arm_low_spd_feedback_6}\n"
            )
        # 发送
        elif self.type_ == ArmMsgType.PiperMsgMotionCtrl_1:
            return (
                f"Type: {self.type_}\n"
                f"PiperMsgMotionCtrl_1: {self.arm_motion_ctrl_1}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgMotionCtrl_2:
            return (
                f"Type: {self.type_}\n"
                f"PiperMsgMotionCtrl_2: {self.arm_motion_ctrl_2}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgMotionCtrlCartesian_1:
            return (
                f"Type: {self.type_}\n"
                f"ArmMsgMotionCtrlCartesian: {self.arm_motion_ctrl_cartesian}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgMotionCtrlCartesian_2:
            return (
                f"Type: {self.type_}\n"
                f"ArmMsgMotionCtrlCartesian: {self.arm_motion_ctrl_cartesian}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgMotionCtrlCartesian_3:
            return (
                f"Type: {self.type_}\n"
                f"ArmMsgMotionCtrlCartesian: {self.arm_motion_ctrl_cartesian}\n"
            )
        elif self.type_ == ArmMsgType.PiperMsgJointCtrl_12:
            return f"Type: {self.type_}\n" f"ArmMsgJointCtrl: {self.arm_joint_ctrl}\n"
        elif self.type_ == ArmMsgType.PiperMsgJointCtrl_34:
            return f"Type: {self.type_}\n" f"ArmMsgJointCtrl: {self.arm_joint_ctrl}\n"
        elif self.type_ == ArmMsgType.PiperMsgJointCtrl_56:
            return f"Type: {self.type_}\n" f"ArmMsgJointCtrl: {self.arm_joint_ctrl}\n"
        elif self.type_ == ArmMsgType.PiperMsgGripperCtrl:
            return (
                f"Type: {self.type_}\n"
                f"PiperMsgGripperCtrl: {self.arm_gripper_ctrl}\n"
            )
        else:
            return f"Type: {self.type_}\n"

    def __repr__(self):
        return self.__str__()
