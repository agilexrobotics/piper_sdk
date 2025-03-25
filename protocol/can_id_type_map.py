from ..piper_msgs.msg_v2 import (
    CanIDPiper,
    ArmMsgType,
)
from ..piper_msgs.msg_v1 import (
    ArmMsgType as ArmMsgTypeV1,
)
from .piper_protocol_base import C_PiperParserBase

class ProtocolMapping:
    # 初始化映射字典
    decodemsg_to_type_mapping_V1 = {
        # 反馈, feedback
        CanIDPiper.ARM_STATUS_FEEDBACK.value : C_PiperParserBase.ARM_STATUS_FEEDBACK,
        CanIDPiper.ARM_END_POSE_FEEDBACK_X_Y.value : C_PiperParserBase.ARM_END_POSE_FEEDBACK_X_Y,
        CanIDPiper.ARM_END_POSE_FEEDBACK_Z_RX.value : C_PiperParserBase.ARM_END_POSE_FEEDBACK_Z_RX,
        CanIDPiper.ARM_END_POSE_FEEDBACK_RY_RZ.value : C_PiperParserBase.ARM_END_POSE_FEEDBACK_RY_RZ,
        CanIDPiper.ARM_JOINT_FEEDBACK_12.value : C_PiperParserBase.ARM_JOINT_FEEDBACK_12,
        CanIDPiper.ARM_JOINT_FEEDBACK_34.value : C_PiperParserBase.ARM_JOINT_FEEDBACK_34,
        CanIDPiper.ARM_JOINT_FEEDBACK_56.value : C_PiperParserBase.ARM_JOINT_FEEDBACK_56,
        CanIDPiper.ARM_GRIPPER_FEEDBACK.value : C_PiperParserBase.ARM_GRIPPER_FEEDBACK,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR1.value : C_PiperParserBase.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR1,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR2.value : C_PiperParserBase.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR2,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR3.value : C_PiperParserBase.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR3,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR4.value : C_PiperParserBase.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR4,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR5.value : C_PiperParserBase.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR5,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR6.value : C_PiperParserBase.ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR6,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR1.value : C_PiperParserBase.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR1,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR2.value : C_PiperParserBase.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR2,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR3.value : C_PiperParserBase.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR3,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR4.value : C_PiperParserBase.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR4,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR5.value : C_PiperParserBase.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR5,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR6.value : C_PiperParserBase.ARM_INFO_LOW_SPD_FEEDBACK_MOTOR6,
        CanIDPiper.ARM_FEEDBACK_CURRENT_MOTOR_ANGLE_LIMIT_MAX_SPD.value : C_PiperParserBase.ARM_FEEDBACK_CURRENT_MOTOR_ANGLE_LIMIT_MAX_SPD,
        CanIDPiper.ARM_FEEDBACK_CURRENT_END_VEL_ACC_PARAM.value : C_PiperParserBase.ARM_FEEDBACK_CURRENT_END_VEL_ACC_PARAM,
        CanIDPiper.ARM_CRASH_PROTECTION_RATING_FEEDBACK.value : C_PiperParserBase.ARM_CRASH_PROTECTION_RATING_FEEDBACK,
        CanIDPiper.ARM_FEEDBACK_CURRENT_MOTOR_MAX_ACC_LIMIT.value : C_PiperParserBase.ARM_FEEDBACK_CURRENT_MOTOR_MAX_ACC_LIMIT,
        CanIDPiper.ARM_MOTION_CTRL_2.value : C_PiperParserBase.ARM_MOTION_CTRL_2,
        CanIDPiper.ARM_JOINT_CTRL_12.value : C_PiperParserBase.ARM_JOINT_CTRL_12,
        CanIDPiper.ARM_JOINT_CTRL_34.value : C_PiperParserBase.ARM_JOINT_CTRL_34,
        CanIDPiper.ARM_JOINT_CTRL_56.value : C_PiperParserBase.ARM_JOINT_CTRL_56,
        CanIDPiper.ARM_GRIPPER_CTRL.value : C_PiperParserBase.ARM_GRIPPER_CTRL,
        CanIDPiper.ARM_FIRMWARE_READ.value : C_PiperParserBase.ARM_FIRMWARE_READ,
    }
    
    decodemsg_to_type_mapping_V2 = decodemsg_to_type_mapping_V1.copy()
    decodemsg_to_type_mapping_V2.update({
    CanIDPiper.ARM_GRIPPER_TEACHING_PENDANT_PARAM_FEEDBACK.value: C_PiperParserBase.ARM_GRIPPER_TEACHING_PENDANT_PARAM_FEEDBACK,})
    @classmethod
    def decodemsg_get_handler(cls, can_id, version):
        """根据 can_id 获取对应的处理函数"""
        if version == "V1":
            handler = cls.decodemsg_to_type_mapping_V1.get(can_id)
        elif version == "V2":
            handler = cls.decodemsg_to_type_mapping_V2.get(can_id)
        if handler is None:
            # 返回错误提示或抛出异常
            # raise ValueError(f"Invalid CAN ID: {can_id:#x}")
            pass
        return handler
    encodemsg_to_type_mapping_V1 = {
        ArmMsgTypeV1.PiperMsgMotionCtrl_1 : C_PiperParserBase.PiperMsgMotionCtrl_1,
        ArmMsgTypeV1.PiperMsgMotionCtrl_2 : C_PiperParserBase.PiperMsgMotionCtrl_2_V1,
        ArmMsgTypeV1.PiperMsgMotionCtrlCartesian_1 : C_PiperParserBase.PiperMsgMotionCtrlCartesian_1,
        ArmMsgTypeV1.PiperMsgMotionCtrlCartesian_2 : C_PiperParserBase.PiperMsgMotionCtrlCartesian_2,
        ArmMsgTypeV1.PiperMsgMotionCtrlCartesian_3 : C_PiperParserBase.PiperMsgMotionCtrlCartesian_3,
        ArmMsgTypeV1.PiperMsgJointCtrl_12 : C_PiperParserBase.PiperMsgJointCtrl_12,
        ArmMsgTypeV1.PiperMsgJointCtrl_34 : C_PiperParserBase.PiperMsgJointCtrl_34,
        ArmMsgTypeV1.PiperMsgJointCtrl_56 : C_PiperParserBase.PiperMsgJointCtrl_56,
        ArmMsgTypeV1.PiperMsgCircularPatternCoordNumUpdateCtrl : C_PiperParserBase.PiperMsgCircularPatternCoordNumUpdateCtrl,
        ArmMsgTypeV1.PiperMsgGripperCtrl : C_PiperParserBase.PiperMsgGripperCtrl,
        ArmMsgTypeV1.PiperMsgMasterSlaveModeConfig : C_PiperParserBase.PiperMsgMasterSlaveModeConfig,
        ArmMsgTypeV1.PiperMsgMotorEnableDisableConfig : C_PiperParserBase.PiperMsgMotorEnableDisableConfig,
        ArmMsgTypeV1.PiperMsgSearchMotorMaxAngleSpdAccLimit : C_PiperParserBase.PiperMsgSearchMotorMaxAngleSpdAccLimit,
        ArmMsgTypeV1.PiperMsgMotorAngleLimitMaxSpdSet : C_PiperParserBase.PiperMsgMotorAngleLimitMaxSpdSet,
        ArmMsgTypeV1.PiperMsgJointConfig : C_PiperParserBase.PiperMsgJointConfig,
        ArmMsgTypeV1.PiperMsgInstructionResponseConfig : C_PiperParserBase.PiperMsgInstructionResponseConfig,
        ArmMsgTypeV1.PiperMsgParamEnquiryAndConfig : C_PiperParserBase.PiperMsgParamEnquiryAndConfig,
        ArmMsgTypeV1.PiperMsgEndVelAccParamConfig : C_PiperParserBase.PiperMsgEndVelAccParamConfig,
        ArmMsgTypeV1.PiperMsgCrashProtectionRatingConfig : C_PiperParserBase.PiperMsgCrashProtectionRatingConfig,
    }
    encodemsg_to_type_mapping_V2 = {
        ArmMsgType.PiperMsgMotionCtrl_1 : C_PiperParserBase.PiperMsgMotionCtrl_1,
        ArmMsgType.PiperMsgMotionCtrl_2 : C_PiperParserBase.PiperMsgMotionCtrl_2_V2,
        ArmMsgType.PiperMsgMotionCtrlCartesian_1 : C_PiperParserBase.PiperMsgMotionCtrlCartesian_1,
        ArmMsgType.PiperMsgMotionCtrlCartesian_2 : C_PiperParserBase.PiperMsgMotionCtrlCartesian_2,
        ArmMsgType.PiperMsgMotionCtrlCartesian_3 : C_PiperParserBase.PiperMsgMotionCtrlCartesian_3,
        ArmMsgType.PiperMsgJointCtrl_12 : C_PiperParserBase.PiperMsgJointCtrl_12,
        ArmMsgType.PiperMsgJointCtrl_34 : C_PiperParserBase.PiperMsgJointCtrl_34,
        ArmMsgType.PiperMsgJointCtrl_56 : C_PiperParserBase.PiperMsgJointCtrl_56,
        ArmMsgType.PiperMsgCircularPatternCoordNumUpdateCtrl : C_PiperParserBase.PiperMsgCircularPatternCoordNumUpdateCtrl,
        ArmMsgType.PiperMsgGripperCtrl : C_PiperParserBase.PiperMsgGripperCtrl,
        ArmMsgType.PiperMsgMasterSlaveModeConfig : C_PiperParserBase.PiperMsgMasterSlaveModeConfig,
        ArmMsgType.PiperMsgMotorEnableDisableConfig : C_PiperParserBase.PiperMsgMotorEnableDisableConfig,
        ArmMsgType.PiperMsgSearchMotorMaxAngleSpdAccLimit : C_PiperParserBase.PiperMsgSearchMotorMaxAngleSpdAccLimit,
        ArmMsgType.PiperMsgMotorAngleLimitMaxSpdSet : C_PiperParserBase.PiperMsgMotorAngleLimitMaxSpdSet,
        ArmMsgType.PiperMsgJointConfig : C_PiperParserBase.PiperMsgJointConfig,
        ArmMsgType.PiperMsgInstructionResponseConfig : C_PiperParserBase.PiperMsgInstructionResponseConfig,
        ArmMsgType.PiperMsgParamEnquiryAndConfig : C_PiperParserBase.PiperMsgParamEnquiryAndConfig,
        ArmMsgType.PiperMsgEndVelAccParamConfig : C_PiperParserBase.PiperMsgEndVelAccParamConfig,
        ArmMsgType.PiperMsgCrashProtectionRatingConfig : C_PiperParserBase.PiperMsgCrashProtectionRatingConfig,
    }
    encodemsg_to_type_mapping_V2 = encodemsg_to_type_mapping_V2.copy()
    encodemsg_to_type_mapping_V2[ArmMsgType.PiperMsgGripperTeachingPendantParamConfig] = C_PiperParserBase.PiperMsgGripperTeachingPendantParamConfig
    for i in range(1, 7):
        key = getattr(ArmMsgType, f"PiperMsgJointMitCtrl_{i}")
        encodemsg_to_type_mapping_V2[key] = C_PiperParserBase.PiperMsgJointMitCtrl
    @classmethod
    def encodemsg_get_handler(cls, msg_type, version):
        """根据 can_id 获取对应的处理函数"""
        if version == "V1":
            handler = cls.encodemsg_to_type_mapping_V1.get(msg_type)
        elif version == "V2":
            handler = cls.encodemsg_to_type_mapping_V2.get(msg_type)
        if handler is None:
            # 返回错误提示或抛出异常
            # raise ValueError(f"Invalid Msg Type: {msg_type}")
            pass
        return handler
