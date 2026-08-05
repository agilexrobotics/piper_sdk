# 导入 feedback 子模块的类
from ...msg_v2.feedback.arm_feedback_crash_protection_rating import ArmMsgFeedbackCrashProtectionRating
from ...msg_v2.feedback.arm_feedback_end_pose import ArmMsgFeedBackEndPose
from ...msg_v2.feedback.arm_feedback_current_motor_angle_limit_max_spd import ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd, ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd
from ...msg_v2.feedback.arm_feedback_current_end_vel_acc_param import ArmMsgFeedbackCurrentEndVelAccParam
from ...msg_v2.feedback.arm_feedback_current_motor_max_acc_limit import ArmMsgFeedbackCurrentMotorMaxAccLimit, ArmMsgFeedbackAllCurrentMotorMaxAccLimit
from ...msg_v2.feedback.arm_feedback_joint_vel_acc import ArmMsgFeedbackJointVelAcc, ArmMsgFeedbackAllJointVelAcc
#----------------------------------基于V1.5-2版本后---------------------------------------------#
from ...msg_v2.feedback.arm_feedback_gripper_teaching_param import ArmMsgFeedbackGripperTeachingPendantParam
#---------------------------------------------------------------------------------------------#
from ...msg_v2.feedback.arm_feedback_high_spd import ArmMsgFeedbackHighSpd
from ...msg_v2.feedback.arm_feedback_joint_states import ArmMsgFeedBackJointStates
from ...msg_v2.feedback.arm_feedback_low_spd import ArmMsgFeedbackLowSpd
from .arm_feedback_status import ArmMsgFeedbackStatus_V3 as ArmMsgFeedbackStatus
from .arm_feedback_status import ArmMsgFeedbackStatusEnum_V3 as ArmMsgFeedbackStatusEnum
from ...msg_v2.feedback.arm_feedback_gripper import ArmMsgFeedBackGripper
from ...msg_v2.feedback.arm_feedback_set_instruction_response import ArmMsgFeedbackRespSetInstruction

__all__ = [
    # 反馈
    'ArmMsgFeedBackEndPose',
    'ArmMsgFeedBackJointStates',
    'ArmMsgFeedbackStatus',
    'ArmMsgFeedbackStatusEnum',
    'ArmMsgFeedBackGripper',
    'ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd',
    'ArmMsgFeedbackCurrentEndVelAccParam',
    'ArmMsgFeedbackCurrentMotorMaxAccLimit',
    'ArmMsgFeedbackJointVelAcc',
    'ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd',
    'ArmMsgFeedbackAllCurrentMotorMaxAccLimit',
    'ArmMsgFeedbackAllJointVelAcc',
    'ArmMsgFeedbackCrashProtectionRating',
    'ArmMsgFeedbackHighSpd',
    'ArmMsgFeedbackLowSpd',
    'ArmMsgFeedbackGripperTeachingPendantParam',
    'ArmMsgFeedbackRespSetInstruction',
]
