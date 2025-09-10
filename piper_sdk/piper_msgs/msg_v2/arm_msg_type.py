#!/usr/bin/env python3
# -*-coding:utf8-*-

from enum import Enum, auto

class ArmMsgType(Enum):
    '''
    msg_v2
    
    机械臂消息类型,枚举类型
    '''
    '''
    msg_v2
    
    Robotic Arm Message Types (Enumeration)
    '''
    # feedback
    PiperMsgUnkonwn = 0x00             #未知类型
    PiperMsgStatusFeedback = auto()    #机械臂状态消息反馈
    PiperMsgEndPoseFeedback_1 = auto() #机械臂末端位姿反馈1
    PiperMsgEndPoseFeedback_2 = auto() #机械臂末端位姿反馈2
    PiperMsgEndPoseFeedback_3 = auto() #机械臂末端位姿反馈3
    PiperMsgJointFeedBack_12 = auto()  #机械臂臂部关节反馈12
    PiperMsgJointFeedBack_34 = auto()  #机械臂臂部关节反馈34
    PiperMsgJointFeedBack_56 = auto()  #机械臂臂部关节反馈56
    PiperMsgGripperFeedBack = auto()  #夹爪反馈指令
    PiperMsgHighSpdFeed_1 = auto()
    PiperMsgHighSpdFeed_2 = auto()
    PiperMsgHighSpdFeed_3 = auto()
    PiperMsgHighSpdFeed_4 = auto()
    PiperMsgHighSpdFeed_5 = auto()
    PiperMsgHighSpdFeed_6 = auto()
    PiperMsgLowSpdFeed_1 = auto()
    PiperMsgLowSpdFeed_2 = auto()
    PiperMsgLowSpdFeed_3 = auto()
    PiperMsgLowSpdFeed_4 = auto()
    PiperMsgLowSpdFeed_5 = auto()
    PiperMsgLowSpdFeed_6 = auto()
    # transmit
    PiperMsgMotionCtrl_1=auto()
    # PiperMsgStopCtrl = auto()
    # PiperMsgTrackCtrl = auto()
    # PiperMsgGragTeachCtrl = auto()
    PiperMsgMotionCtrl_2=auto()
    # PiperMsgModeCtrl = auto()
    # PiperMsgMoveModeCtrl = auto()
    # PiperMsgMoveSpdRateCtrl = auto()
    PiperMsgMotionCtrlCartesian_1 = auto()
    PiperMsgMotionCtrlCartesian_2 = auto()
    PiperMsgMotionCtrlCartesian_3 = auto()
    PiperMsgJointCtrl_12 = auto()
    PiperMsgJointCtrl_34 = auto()
    PiperMsgJointCtrl_56 = auto()
    PiperMsgCircularPatternCoordNumUpdateCtrl=auto()
    PiperMsgGripperCtrl = auto()
    #----------------------------------基于V1.5-2版本后---------------------------------------------#
    PiperMsgJointMitCtrl_1 = auto()
    PiperMsgJointMitCtrl_2 = auto()
    PiperMsgJointMitCtrl_3 = auto()
    PiperMsgJointMitCtrl_4 = auto()
    PiperMsgJointMitCtrl_5 = auto()
    PiperMsgJointMitCtrl_6 = auto()
    #---------------------------------------------------------------------------------------------#
    PiperMsgMasterSlaveModeConfig = auto()
    # PiperMsgMSLinkageConfig = auto()
    # PiperMsgMSFeedbackInstructionOffsetConfig=auto()
    # PiperMsgMSCtrlInstructionOffsetConfig=auto()
    # PiperMsgMSLinkageCtrlOffsetConfig=auto()
    PiperMsgMotorEnableDisableConfig=auto() # 电机使能/失能设置指令
    # PiperMsgMotorDisableConfig=auto()
    # PiperMsgSearchMotorAngleConfig=auto()
    PiperMsgSearchMotorMaxAngleSpdAccLimit=auto()
    # PiperMsgSearchMotorMaxAccConfig=auto()
    PiperMsgFeedbackCurrentMotorAngleLimitMaxSpd=auto()
    PiperMsgMotorAngleLimitMaxSpdSet=auto()#电机角度限制/最大速度设置指令
    PiperMsgJointConfig=auto()
    PiperMsgInstructionResponseConfig=auto()
    PiperMsgFeedbackRespSetInstruction=auto()
    PiperMsgParamEnquiryAndConfig=auto()
    PiperMsgFeedbackCurrentEndVelAccParam=auto()
    PiperMsgEndVelAccParamConfig=auto()
    PiperMsgCrashProtectionRatingConfig=auto()
    PiperMsgCrashProtectionRatingFeedback=auto()
    PiperMsgFeedbackCurrentMotorMaxAccLimit=auto()
    #----------------------------------基于V1.5-2版本后---------------------------------------------#
    PiperMsgGripperTeachingPendantParamConfig = auto()
    PiperMsgGripperTeachingPendantParamFeedback = auto()
    #---------------------------------------------------------------------------------------------#
    PiperMsgFeedbackJointVelAcc_1=auto()
    PiperMsgFeedbackJointVelAcc_2=auto()
    PiperMsgFeedbackJointVelAcc_3=auto()
    PiperMsgFeedbackJointVelAcc_4=auto()
    PiperMsgFeedbackJointVelAcc_5=auto()
    PiperMsgFeedbackJointVelAcc_6=auto()
    PiperMsgLightCtrl=auto()
    PiperMsgCanUpdateSilentModeConfig=auto()
    PiperMsgFirmwareRead=auto()
    def __str__(self):
        return f"{self.name} (0x{self.value:X})"
    def __repr__(self):
        return f"{self.name}: 0x{self.value:X}"