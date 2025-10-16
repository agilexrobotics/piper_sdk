#!/usr/bin/env python3
# -*-coding:utf8-*-

from typing import (
    Optional,
)
from .arm_msg_type import ArmMsgType
from .can_id import CanIDPiper

class ArmMessageMapping:
    '''
    msg_v2
    
    机械臂消息类型和CAN ID的映射
    '''
    '''
    msg_v2
    
    Mapping of Robotic Arm Message Types and CAN IDs
    '''
    # 初始化映射字典
    id_to_type_mapping = {
        # 反馈,feedback
        CanIDPiper.ARM_STATUS_FEEDBACK.value: ArmMsgType.PiperMsgStatusFeedback,
        CanIDPiper.ARM_END_POSE_FEEDBACK_1.value: ArmMsgType.PiperMsgEndPoseFeedback_1,
        CanIDPiper.ARM_END_POSE_FEEDBACK_2.value: ArmMsgType.PiperMsgEndPoseFeedback_2,
        CanIDPiper.ARM_END_POSE_FEEDBACK_3.value: ArmMsgType.PiperMsgEndPoseFeedback_3,
        CanIDPiper.ARM_JOINT_FEEDBACK_12.value: ArmMsgType.PiperMsgJointFeedBack_12,
        CanIDPiper.ARM_JOINT_FEEDBACK_34.value: ArmMsgType.PiperMsgJointFeedBack_34,
        CanIDPiper.ARM_JOINT_FEEDBACK_56.value: ArmMsgType.PiperMsgJointFeedBack_56,
        CanIDPiper.ARM_GRIPPER_FEEDBACK.value: ArmMsgType.PiperMsgGripperFeedBack,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_1.value: ArmMsgType.PiperMsgHighSpdFeed_1,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_2.value: ArmMsgType.PiperMsgHighSpdFeed_2,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_3.value: ArmMsgType.PiperMsgHighSpdFeed_3,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_4.value: ArmMsgType.PiperMsgHighSpdFeed_4,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_5.value: ArmMsgType.PiperMsgHighSpdFeed_5,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_6.value: ArmMsgType.PiperMsgHighSpdFeed_6,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_1.value: ArmMsgType.PiperMsgLowSpdFeed_1,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_2.value: ArmMsgType.PiperMsgLowSpdFeed_2,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_3.value: ArmMsgType.PiperMsgLowSpdFeed_3,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_4.value: ArmMsgType.PiperMsgLowSpdFeed_4,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_5.value: ArmMsgType.PiperMsgLowSpdFeed_5,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_6.value: ArmMsgType.PiperMsgLowSpdFeed_6,
        # 发送,transmit
        CanIDPiper.ARM_MOTION_CTRL_1.value: ArmMsgType.PiperMsgMotionCtrl_1,
        # CanIDPiper.ARM_STOP_CTRL.value: ArmMsgType.PiperMsgStopCtrl,
        # CanIDPiper.ARM_TRACK_CTRL.value: ArmMsgType.PiperMsgTrackCtrl,
        # CanIDPiper.ARM_GRAG_TEACH_CTRL.value: ArmMsgType.PiperMsgGragTeachCtrl,
        CanIDPiper.ARM_MOTION_CTRL_2.value: ArmMsgType.PiperMsgMotionCtrl_2,
        # CanIDPiper.ARM_MODE_CTRL.value: ArmMsgType.PiperMsgModeCtrl,
        # CanIDPiper.ARM_MOVE_MODE_CTRL.value: ArmMsgType.PiperMsgMoveModeCtrl,
        # CanIDPiper.ARM_MOVE_SPD_RATE_CTRL.value: ArmMsgType.PiperMsgMoveSpdRateCtrl,
        CanIDPiper.ARM_MOTION_CTRL_CARTESIAN_1.value: ArmMsgType.PiperMsgMotionCtrlCartesian_1,
        CanIDPiper.ARM_MOTION_CTRL_CARTESIAN_2.value: ArmMsgType.PiperMsgMotionCtrlCartesian_2,
        CanIDPiper.ARM_MOTION_CTRL_CARTESIAN_3.value: ArmMsgType.PiperMsgMotionCtrlCartesian_3,
        CanIDPiper.ARM_JOINT_CTRL_12.value: ArmMsgType.PiperMsgJointCtrl_12,
        CanIDPiper.ARM_JOINT_CTRL_34.value: ArmMsgType.PiperMsgJointCtrl_34,
        CanIDPiper.ARM_JOINT_CTRL_56.value: ArmMsgType.PiperMsgJointCtrl_56,
        CanIDPiper.ARM_CIRCULAR_PATTERN_COORD_NUM_UPDATE_CTRL.value: ArmMsgType.PiperMsgCircularPatternCoordNumUpdateCtrl,
        CanIDPiper.ARM_GRIPPER_CTRL.value: ArmMsgType.PiperMsgGripperCtrl,
        #----------------------------------基于V1.5-2版本后---------------------------------------------#
        CanIDPiper.ARM_JOINT_MIT_CTRL_1.value: ArmMsgType.PiperMsgJointMitCtrl_1,
        CanIDPiper.ARM_JOINT_MIT_CTRL_2.value: ArmMsgType.PiperMsgJointMitCtrl_2,
        CanIDPiper.ARM_JOINT_MIT_CTRL_3.value: ArmMsgType.PiperMsgJointMitCtrl_3,
        CanIDPiper.ARM_JOINT_MIT_CTRL_4.value: ArmMsgType.PiperMsgJointMitCtrl_4,
        CanIDPiper.ARM_JOINT_MIT_CTRL_5.value: ArmMsgType.PiperMsgJointMitCtrl_5,
        CanIDPiper.ARM_JOINT_MIT_CTRL_6.value: ArmMsgType.PiperMsgJointMitCtrl_6,
        #---------------------------------------------------------------------------------------------#
        CanIDPiper.ARM_MASTER_SLAVE_MODE_CONFIG.value: ArmMsgType.PiperMsgMasterSlaveModeConfig,
        # CanIDPiper.ARM_MS_LINKAGE_CONFIG.value: ArmMsgType.PiperMsgMSLinkageConfig,
        # CanIDPiper.ARM_MS_FEEDBACK_INSTRUCTION_OFFSET_CONFIG.value: ArmMsgType.PiperMsgMSFeedbackInstructionOffsetConfig,
        # CanIDPiper.ARM_MS_CTRL_INSTRUCTION_OFFSET_CONFIG.value: ArmMsgType.PiperMsgMSCtrlInstructionOffsetConfig,
        # CanIDPiper.ARM_MS_LINKAGE_CTRL_OFFSET_CONFIG.value: ArmMsgType.PiperMsgMSLinkageCtrlOffsetConfig,
        CanIDPiper.ARM_MOTOR_ENABLE_DISABLE_CONFIG.value: ArmMsgType.PiperMsgMotorEnableDisableConfig,
        # CanIDPiper.ARM_MOTOR_DISABLE_CONFIG.value: ArmMsgType.PiperMsgMotorDisableConfig,
        # CanIDPiper.ARM_SEARCH_MOTOR_ANGLE_CONFIG.value: ArmMsgType.PiperMsgSearchMotorAngleConfig,
        CanIDPiper.ARM_SEARCH_MOTOR_MAX_SPD_ACC_LIMIT.value: ArmMsgType.PiperMsgSearchMotorMaxAngleSpdAccLimit,
        # CanIDPiper.ARM_SEARCH_MOTOR_MAX_ACC_CONFIG.value: ArmMsgType.PiperMsgSearchMotorMaxAccConfig,
        CanIDPiper.ARM_FEEDBACK_CURRENT_MOTOR_ANGLE_LIMIT_MAX_SPD.value: ArmMsgType.PiperMsgFeedbackCurrentMotorAngleLimitMaxSpd,
        CanIDPiper.ARM_MOTOR_ANGLE_LIMIT_MAX_SPD_SET.value: ArmMsgType.PiperMsgMotorAngleLimitMaxSpdSet,
        CanIDPiper.ARM_JOINT_CONFIG.value: ArmMsgType.PiperMsgJointConfig,
        CanIDPiper.ARM_INSTRUCTION_RESPONSE_CONFIG.value: ArmMsgType.PiperMsgInstructionResponseConfig,
        CanIDPiper.ARM_FEEDBACK_RESP_SET_INSTRUCTION.value: ArmMsgType.PiperMsgFeedbackRespSetInstruction,
        CanIDPiper.ARM_PARAM_ENQUIRY_AND_CONFIG.value: ArmMsgType.PiperMsgParamEnquiryAndConfig,
        CanIDPiper.ARM_FEEDBACK_CURRENT_END_VEL_ACC_PARAM.value: ArmMsgType.PiperMsgFeedbackCurrentEndVelAccParam,
        CanIDPiper.ARM_END_VEL_ACC_PARAM_CONFIG.value: ArmMsgType.PiperMsgEndVelAccParamConfig,
        CanIDPiper.ARM_CRASH_PROTECTION_RATING_CONFIG.value: ArmMsgType.PiperMsgCrashProtectionRatingConfig,
        CanIDPiper.ARM_CRASH_PROTECTION_RATING_FEEDBACK.value: ArmMsgType.PiperMsgCrashProtectionRatingFeedback,
        CanIDPiper.ARM_FEEDBACK_CURRENT_MOTOR_MAX_ACC_LIMIT.value: ArmMsgType.PiperMsgFeedbackCurrentMotorMaxAccLimit,
        #----------------------------------基于V1.5-2版本后---------------------------------------------#
        CanIDPiper.ARM_GRIPPER_TEACHING_PENDANT_PARAM_CONFIG.value: ArmMsgType.PiperMsgGripperTeachingPendantParamConfig,
        CanIDPiper.ARM_GRIPPER_TEACHING_PENDANT_PARAM_FEEDBACK.value: ArmMsgType.PiperMsgGripperTeachingPendantParamFeedback,
        #---------------------------------------------------------------------------------------------#
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_1.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_1,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_2.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_2,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_3.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_3,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_4.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_4,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_5.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_5,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_6.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_6,
        CanIDPiper.ARM_LIGHT_CTRL.value: ArmMsgType.PiperMsgLightCtrl,
        CanIDPiper.ARM_CAN_UPDATE_SILENT_MODE_CONFIG.value: ArmMsgType.PiperMsgCanUpdateSilentModeConfig,
        CanIDPiper.ARM_FIRMWARE_READ.value: ArmMsgType.PiperMsgFirmwareRead,
    }

    type_to_id_mapping = {v: k for k, v in id_to_type_mapping.items()}

    @staticmethod
    def get_mapping(can_id: Optional[int] = None, msg_type: Optional[ArmMsgType] = None):
        '''
        根据输入的参数返回对应的映射值，输入 id 返回类型，输入类型返回 id
        
        :param can_id: CAN ID
        :param msg_type: 机械臂消息类型
        :return: 对应的类型或 id
        '''
        if can_id is not None and msg_type is not None:
            raise ValueError("只能输入 CAN ID 或消息类型中的一个")

        if can_id is not None:
            if can_id in ArmMessageMapping.id_to_type_mapping:
                return ArmMessageMapping.id_to_type_mapping[can_id]
            else:
                raise ValueError(f"CAN ID {can_id} 不在映射中")

        if msg_type is not None:
            if msg_type in ArmMessageMapping.type_to_id_mapping:
                return ArmMessageMapping.type_to_id_mapping[msg_type]
            else:
                raise ValueError(f"消息类型 {msg_type} 不在映射中")

        raise ValueError("必须输入 CAN ID 或消息类型中的一个")

# 测试代码
# if __name__ == "__main__":
#     # 根据 ID 查找类型
#     print(ArmMessageMapping.get_mapping(can_id=0x2A2))  # 输出: PiperMsgEndPoseFeedback_1 (0x2)

#     # 根据类型查找 ID
#     print(ArmMessageMapping.get_mapping(msg_type=ArmMsgType.PiperMsgJointFeedBack_56))  # 输出: 0x2A7
