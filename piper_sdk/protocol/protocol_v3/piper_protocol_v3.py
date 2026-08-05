#!/usr/bin/env python3
# -*-coding:utf8-*-
#机械臂协议V1版本，为方便后续修改协议升级，继承自base
import can
from typing import (
    Optional,
)

# import sys,os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from ..piper_protocol_base import C_PiperParserBase
# from ...protocol.piper_protocol_base import C_PiperParserBase
from ..protocol_v2 import C_PiperParserV2
from ...piper_msgs.msg_v3 import (
    ArmMsgType as ArmMsgType_V3, 
    PiperMessage as PiperMessage_V3, 
    CanIDPiper as CanIDPiper_V3,
    ArmMessageMapping as ArmMessageMapping_V3
)

class C_PiperParserV3(C_PiperParserV2):
    '''
    Piper机械臂解析数据类V3版本
    '''
    '''
    Piper Robotic Arm Data Parsing Class V3 Version
    '''
    ArmMsgType = ArmMsgType_V3
    PiperMessage = PiperMessage_V3
    CanIDPiper = CanIDPiper_V3
    ArmMessageMapping = ArmMessageMapping_V3
    
    def __init__(self) -> None:
        super().__init__()
        pass

    def GetParserProtocolVersion(self):
        '''
        获取当前协议版本,当前为V3
        '''
        '''
        Get the current protocol version, currently V3.
        '''
        return self.ProtocolVersion.ARM_PROROCOL_V3

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
        tx_can_frame.arbitration_id = self.ArmMessageMapping.get_mapping(msg_type=msg_type_)
        if(msg_type_ == self.ArmMsgType.PiperMsgMotionCtrl_1):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motion_ctrl_1.emergency_stop,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_1.track_ctrl,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_1.grag_teach_ctrl,False) + \
                                [0x00, 0x00, 0x00, 0x00, 0x00]
        elif(msg_type_ == self.ArmMsgType.PiperMsgMotionCtrl_2):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motion_ctrl_2.ctrl_mode,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.move_mode,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.move_spd_rate_ctrl,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.mit_mode,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.residence_time,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.installation_pos,False) + \
                                [0x00, 0x00]
        elif(msg_type_ == self.ArmMsgType.PiperMsgMotionCtrlCartesian_1):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.X_axis) + \
                                self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.Y_axis)
        elif(msg_type_ == self.ArmMsgType.PiperMsgMotionCtrlCartesian_2):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.Z_axis) + \
                                self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.RX_axis)
        elif(msg_type_ == self.ArmMsgType.PiperMsgMotionCtrlCartesian_3):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.RY_axis) + \
                                self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.RZ_axis)
        elif(msg_type_ == self.ArmMsgType.PiperMsgJointCtrl_12):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_1) + \
                                self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_2)
        elif(msg_type_ == self.ArmMsgType.PiperMsgJointCtrl_34):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_3) + \
                                self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_4)
        elif(msg_type_ == self.ArmMsgType.PiperMsgJointCtrl_56):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_5) + \
                                self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_6)
        elif(msg_type_ == self.ArmMsgType.PiperMsgCircularPatternCoordNumUpdateCtrl):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_circular_ctrl.instruction_num,False) + \
                                [0, 0, 0, 0, 0, 0, 0]
        elif(msg_type_ == self.ArmMsgType.PiperMsgGripperCtrl):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_gripper_ctrl.grippers_angle) + \
                                self.ConvertToList_16bit(msg.arm_gripper_ctrl.grippers_effort,False) + \
                                self.ConvertToList_8bit(msg.arm_gripper_ctrl.status_code,False) + \
                                self.ConvertToList_8bit(msg.arm_gripper_ctrl.set_zero,False)
        elif(msg_type_ == self.ArmMsgType.PiperMsgMasterSlaveModeConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_ms_config.linkage_config,False) + \
                                self.ConvertToList_8bit(msg.arm_ms_config.feedback_offset,False) + \
                                self.ConvertToList_8bit(msg.arm_ms_config.ctrl_offset,False) + \
                                self.ConvertToList_8bit(msg.arm_ms_config.linkage_offset,False) + \
                                [0, 0, 0, 0]
        elif(msg_type_ == self.ArmMsgType.PiperMsgMotorEnableDisableConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motor_enable.motor_num,False) + \
                                self.ConvertToList_8bit(msg.arm_motor_enable.enable_flag,False) + \
                                [0, 0, 0, 0, 0, 0]
        elif(msg_type_ == self.ArmMsgType.PiperMsgSearchMotorMaxAngleSpdAccLimit):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_search_motor_max_angle_spd_acc_limit.motor_num,False) + \
                                self.ConvertToList_8bit(msg.arm_search_motor_max_angle_spd_acc_limit.search_content,False) + \
                                [0, 0, 0, 0, 0, 0]
        elif(msg_type_ == self.ArmMsgType.PiperMsgMotorAngleLimitMaxSpdSet):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motor_angle_limit_max_spd_set.motor_num,False) + \
                                self.ConvertToList_16bit(msg.arm_motor_angle_limit_max_spd_set.max_angle_limit) + \
                                self.ConvertToList_16bit(msg.arm_motor_angle_limit_max_spd_set.min_angle_limit) + \
                                self.ConvertToList_16bit(msg.arm_motor_angle_limit_max_spd_set.max_joint_spd,False) + \
                                [0]
        elif(msg_type_ == self.ArmMsgType.PiperMsgJointConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_joint_config.joint_motor_num,False) + \
                                self.ConvertToList_8bit(msg.arm_joint_config.set_motor_current_pos_as_zero,False) + \
                                self.ConvertToList_8bit(msg.arm_joint_config.acc_param_config_is_effective_or_not,False) + \
                                self.ConvertToList_16bit(msg.arm_joint_config.max_joint_acc,False) + \
                                self.ConvertToList_8bit(msg.arm_joint_config.clear_joint_err,False) + \
                                [0, 0]
        elif(msg_type_ == self.ArmMsgType.PiperMsgInstructionResponseConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_set_instruction_response.instruction_index,False) + \
                                self.ConvertToList_8bit(msg.arm_set_instruction_response.zero_config_success_flag,False) + \
                                [0, 0, 0, 0, 0, 0]
        elif(msg_type_ == self.ArmMsgType.PiperMsgParamEnquiryAndConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.param_enquiry,False) + \
                                self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.param_setting,False) + \
                                self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.data_feedback_0x48x,False) + \
                                self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.end_load_param_setting_effective,False) + \
                                self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.set_end_load,False) + \
                                [0, 0, 0]
        elif(msg_type_ == self.ArmMsgType.PiperMsgEndVelAccParamConfig):
            tx_can_frame.data = self.ConvertToList_16bit(msg.arm_end_vel_acc_param_config.end_max_linear_vel,False) + \
                                self.ConvertToList_16bit(msg.arm_end_vel_acc_param_config.end_max_angular_vel,False) + \
                                self.ConvertToList_16bit(msg.arm_end_vel_acc_param_config.end_max_linear_acc,False) + \
                                self.ConvertToList_16bit(msg.arm_end_vel_acc_param_config.end_max_angular_acc,False)
        elif(msg_type_ == self.ArmMsgType.PiperMsgCrashProtectionRatingConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_1_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_2_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_3_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_4_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_5_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_6_protection_level,False) + \
                                [0, 0]
        elif(msg_type_ == self.ArmMsgType.PiperMsgGripperTeachingPendantParamConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_gripper_teaching_param_config.teaching_range_per,False) + \
                                self.ConvertToList_8bit(msg.arm_gripper_teaching_param_config.max_range_config,False) + \
                                self.ConvertToList_8bit(msg.arm_gripper_teaching_param_config.teaching_friction,False) + \
                                [0, 0, 0, 0, 0]
        # 机械臂MIT单独控制电机
        elif(msg_type_ == self.ArmMsgType.PiperMsgJointMitCtrl_1 or
             msg_type_ == self.ArmMsgType.PiperMsgJointMitCtrl_2 or
             msg_type_ == self.ArmMsgType.PiperMsgJointMitCtrl_3 or
             msg_type_ == self.ArmMsgType.PiperMsgJointMitCtrl_4 or
             msg_type_ == self.ArmMsgType.PiperMsgJointMitCtrl_5 or
             msg_type_ == self.ArmMsgType.PiperMsgJointMitCtrl_6 ):
            tx_can_frame.data = self.ConvertToList_16bit(msg.arm_joint_mit_ctrl.pos_ref,False) + \
                                self.ConvertToList_8bit(((msg.arm_joint_mit_ctrl.vel_ref >> 4)&0xFF),False) + \
                                self.ConvertToList_8bit(((((msg.arm_joint_mit_ctrl.vel_ref&0xF)<<4)&0xF0) | 
                                                         ((msg.arm_joint_mit_ctrl.kp>>8)&0x0F)),False) + \
                                self.ConvertToList_8bit(msg.arm_joint_mit_ctrl.kp&0xFF,False) + \
                                self.ConvertToList_8bit((msg.arm_joint_mit_ctrl.kd>>4)&0xFF,False) + \
                                self.ConvertToList_8bit(((((msg.arm_joint_mit_ctrl.kd&0xF)<<4)&0xF0)|
                                                         ((msg.arm_joint_mit_ctrl.t_ref>>8)&0x0F)),False) + \
                                self.ConvertToList_8bit(((msg.arm_joint_mit_ctrl.t_ref & 0xFF)),False)
            
            tx_can_frame.data = tx_can_frame.data
        else:
            ret = False
        return ret
            

