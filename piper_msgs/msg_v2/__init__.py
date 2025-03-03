# piper_msgs/msg_v2/__init__.py

# msg_v2/__init__.py

from .arm_messages import PiperMessage
from .can_id import CanIDPiper
from .arm_msg_type import ArmMsgType
from .arm_id_type_map import ArmMessageMapping
# 导入 feedback 子模块的类
from .feedback.arm_crash_protection_rating_feedback import ArmMsgCrashProtectionRatingFeedback
from .feedback.arm_end_pose import ArmMsgEndPoseFeedBack
from .feedback.arm_feedback_current_motor_angle_limit_max_spd import ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd, ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd
from .feedback.arm_feedback_current_end_vel_acc_param import ArmMsgFeedbackCurrentEndVelAccParam
from .feedback.arm_feedback_current_motor_max_acc_limit import ArmMsgFeedbackCurrentMotorMaxAccLimit, ArmMsgFeedbackAllCurrentMotorMaxAccLimit
from .feedback.arm_feedback_joint_vel_acc import ArmMsgFeedbackJointVelAcc, ArmMsgFeedbackAllJointVelAcc
#----------------------------------基于V1.5-2版本后---------------------------------------------#
from .feedback.arm_gripper_teaching_param_feedback import ArmMsgGripperTeachingPendantParamFeedback
#---------------------------------------------------------------------------------------------#
from .feedback.arm_high_spd_feedback import ArmHighSpdFeedback
from .feedback.arm_joint_feedback import ArmMsgJointFeedBack
from .feedback.arm_low_spd_feedback import ArmLowSpdFeedback
from .feedback.arm_status import ArmMsgStatus
from .feedback.gripper_feedback import ArmMsgGripperFeedBack

# 导入 transmit 子模块（假设 transmit 中也有需要导出的类）
from .transmit.arm_circular_pattern import ArmMsgCircularPatternCoordNumUpdateCtrl
from .transmit.arm_crash_protection_rating_config import ArmMsgCrashProtectionRatingConfig
from .transmit.arm_end_vel_acc_param_config import ArmMsgEndVelAccParamConfig
from .transmit.arm_gripper_ctrl import ArmMsgGripperCtrl
#----------------------------------基于V1.5-2版本后---------------------------------------------#
from .transmit.arm_gripper_teaching_param_config import ArmMsgGripperTeachingPendantParamConfig
#---------------------------------------------------------------------------------------------#
from .transmit.arm_joint_config import ArmMsgJointConfig
from .transmit.arm_joint_ctrl import ArmMsgJointCtrl
#----------------------------------基于V1.5-2版本后---------------------------------------------#
from .transmit.arm_joint_mit_ctrl import ArmMsgJointMitCtrl
from .transmit.arm_joint_mit_ctrl import ArmMsgAllJointMitCtrl
#---------------------------------------------------------------------------------------------#
from .transmit.arm_master_slave_config import ArmMsgMasterSlaveModeConfig
from .transmit.arm_motion_ctrl_1 import ArmMsgMotionCtrl_1
from .transmit.arm_motion_ctrl_2 import ArmMsgMotionCtrl_2
from .transmit.arm_motion_ctrl_cartesian import ArmMsgMotionCtrlCartesian
from .transmit.arm_motor_angle_limit_max_spd_config import ArmMsgMotorAngleLimitMaxSpdSet
from .transmit.arm_motor_enable_disable import ArmMsgMotorEnableDisableConfig
from .transmit.arm_param_enquiry_and_config import ArmMsgParamEnquiryAndConfig
from .transmit.arm_search_motor_max_angle_spd_acc_limit import ArmMsgSearchMotorMaxAngleSpdAccLimit
from .transmit.arm_set_instruction_response import ArmMsgInstructionResponseConfig

__all__ = [
    # 反馈
    'PiperMessage',
    'CanIDPiper',
    'ArmMsgEndPoseFeedBack',
    'ArmMsgJointFeedBack',
    'ArmMsgType',
    'ArmMsgStatus',
    'ArmMsgGripperFeedBack',
    'ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd',
    'ArmMsgFeedbackCurrentEndVelAccParam',
    'ArmMsgFeedbackCurrentMotorMaxAccLimit',
    'ArmMsgFeedbackJointVelAcc',
    'ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd',
    'ArmMsgFeedbackAllCurrentMotorMaxAccLimit',
    'ArmMsgFeedbackAllJointVelAcc',
    'ArmMsgCrashProtectionRatingFeedback',
    'ArmHighSpdFeedback',
    'ArmLowSpdFeedback',
    'ArmMsgGripperTeachingPendantParamFeedback',
    # 发送
    'ArmMsgMotionCtrl_1',
    'ArmMsgMotionCtrl_2',
    'ArmMsgMotionCtrlCartesian',
    'ArmMsgJointCtrl',
    'ArmMsgCircularPatternCoordNumUpdateCtrl',
    'ArmMsgGripperCtrl',
    'ArmMsgMasterSlaveModeConfig',
    'ArmMsgMotorEnableDisableConfig',
    'ArmMsgSearchMotorMaxAngleSpdAccLimit',
    'ArmMsgMotorAngleLimitMaxSpdSet',
    'ArmMsgJointConfig',
    'ArmMsgInstructionResponseConfig',
    'ArmMsgParamEnquiryAndConfig',
    'ArmMsgEndVelAccParamConfig',
    'ArmMsgCrashProtectionRatingConfig',
    'ArmMsgGripperTeachingPendantParamConfig',
    'ArmMsgJointMitCtrl',
    'ArmMsgAllJointMitCtrl'
]

