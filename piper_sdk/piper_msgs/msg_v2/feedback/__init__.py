# 导入 feedback 子模块的类
from .arm_feedback_crash_protection_rating import ArmMsgFeedbackCrashProtectionRating
from .arm_feedback_end_pose import ArmMsgFeedBackEndPose
from .arm_feedback_current_motor_angle_limit_max_spd import ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd, ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd
from .arm_feedback_current_end_vel_acc_param import ArmMsgFeedbackCurrentEndVelAccParam
from .arm_feedback_current_motor_max_acc_limit import ArmMsgFeedbackCurrentMotorMaxAccLimit, ArmMsgFeedbackAllCurrentMotorMaxAccLimit
from .arm_feedback_joint_vel_acc import ArmMsgFeedbackJointVelAcc, ArmMsgFeedbackAllJointVelAcc
#----------------------------------基于V1.5-2版本后---------------------------------------------#
from .arm_feedback_gripper_teaching_param import ArmMsgFeedbackGripperTeachingPendantParam
#---------------------------------------------------------------------------------------------#
from .arm_feedback_high_spd import ArmMsgFeedbackHighSpd
from .arm_feedback_joint_states import ArmMsgFeedBackJointStates
from .arm_feedback_low_spd import ArmMsgFeedbackLowSpd
from .arm_feedback_status import ArmMsgFeedbackStatus, ArmMsgFeedbackStatusEnum
from .arm_feedback_gripper import ArmMsgFeedBackGripper
from .arm_feedback_set_instruction_response import ArmMsgFeedbackRespSetInstruction

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
