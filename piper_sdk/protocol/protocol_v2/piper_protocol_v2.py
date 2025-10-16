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
from ...piper_msgs.msg_v2 import (
    ArmMsgType, 
    PiperMessage, 
    CanIDPiper,
    ArmMessageMapping
)

class C_PiperParserV2(C_PiperParserBase):
    '''
    Piper机械臂解析数据类V2版本
    '''
    '''
    Piper Robotic Arm Data Parsing Class V2 Version
    '''
    def __init__(self) -> None:
        super().__init__()
        pass

    def GetParserProtocolVersion(self):
        '''
        获取当前协议版本,当前为V2
        '''
        '''
        Get the current protocol version, currently V2.
        '''
        return self.ProtocolVersion.ARM_PROROCOL_V2

    def DecodeMessage(self, rx_can_frame: Optional[can.Message], msg:PiperMessage):
        '''解码消息,将can数据帧转为设定的类型

        Args:
            rx_can_frame (Optional[can.Message]): can 数据帧, 为输入
            msg (PiperMessage): 自定义中间层数据, 为输出

        Returns:
            bool:
                can消息的id如果存在, 反馈True

                can消息的id若不存在, 反馈False
        '''
        '''Decode the message, convert the CAN data frame to the specified type.

        Args:

            rx_can_frame (Optional[can.Message]): CAN data frame, input.
            msg (PiperMessage): Custom intermediate data, output.

        Returns:

            bool:
                If the CAN message ID exists, return True.
                If the CAN message ID does not exist, return False.
        '''
        ret:bool = True
        can_id:int = rx_can_frame.arbitration_id
        can_data:bytearray = rx_can_frame.data
        can_time_now = rx_can_frame.timestamp
        # 机械臂状态反馈,piper Status Feedback
        if(can_id == CanIDPiper.ARM_STATUS_FEEDBACK.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_status_msgs.ctrl_mode = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
            msg.arm_status_msgs.arm_status = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,1,2),False)
            msg.arm_status_msgs.mode_feed = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,2,3),False)
            msg.arm_status_msgs.teach_status = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,3,4),False)
            msg.arm_status_msgs.motion_status = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5),False)
            msg.arm_status_msgs.trajectory_num = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
            msg.arm_status_msgs.err_code = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
        # 机械臂末端位姿,piper End-Effector Pose
        elif(can_id == CanIDPiper.ARM_END_POSE_FEEDBACK_1.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_end_pose.X_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_end_pose.Y_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_END_POSE_FEEDBACK_2.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_end_pose.Z_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_end_pose.RX_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_END_POSE_FEEDBACK_3.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_end_pose.RY_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_end_pose.RZ_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        # 关节角度反馈,Joint Angle Feedback
        elif(can_id == CanIDPiper.ARM_JOINT_FEEDBACK_12.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_joint_feedback.joint_1 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_joint_feedback.joint_2 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_JOINT_FEEDBACK_34.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_joint_feedback.joint_3 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_joint_feedback.joint_4 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_JOINT_FEEDBACK_56.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_joint_feedback.joint_5 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_joint_feedback.joint_6 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        # 夹爪反馈,Gripper Feedback
        elif(can_id == CanIDPiper.ARM_GRIPPER_FEEDBACK.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.gripper_feedback.grippers_angle = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.gripper_feedback.grippers_effort = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,4,6))
            msg.gripper_feedback.status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,6,7),False)
        # 驱动器信息高速反馈,High-Speed Driver Information Feedback
        elif(can_id == CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_1.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_high_spd_feedback_1.can_id = can_id
            msg.arm_high_spd_feedback_1.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
            msg.arm_high_spd_feedback_1.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_high_spd_feedback_1.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_2.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_high_spd_feedback_2.can_id = can_id
            msg.arm_high_spd_feedback_2.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
            msg.arm_high_spd_feedback_2.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_high_spd_feedback_2.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_3.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_high_spd_feedback_3.can_id = can_id
            msg.arm_high_spd_feedback_3.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
            msg.arm_high_spd_feedback_3.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_high_spd_feedback_3.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_4.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_high_spd_feedback_4.can_id = can_id
            msg.arm_high_spd_feedback_4.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
            msg.arm_high_spd_feedback_4.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_high_spd_feedback_4.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_5.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_high_spd_feedback_5.can_id = can_id
            msg.arm_high_spd_feedback_5.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
            msg.arm_high_spd_feedback_5.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_high_spd_feedback_5.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_6.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_high_spd_feedback_6.can_id = can_id
            msg.arm_high_spd_feedback_6.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
            msg.arm_high_spd_feedback_6.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_high_spd_feedback_6.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        # 驱动器信息低速反馈,Low-Speed Driver Information Feedback
        elif(can_id == CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_1.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_low_spd_feedback_1.can_id = can_id
            msg.arm_low_spd_feedback_1.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
            msg.arm_low_spd_feedback_1.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_low_spd_feedback_1.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
            msg.arm_low_spd_feedback_1.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
            msg.arm_low_spd_feedback_1.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
        elif(can_id == CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_2.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_low_spd_feedback_2.can_id = can_id
            msg.arm_low_spd_feedback_2.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
            msg.arm_low_spd_feedback_2.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_low_spd_feedback_2.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
            msg.arm_low_spd_feedback_2.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
            msg.arm_low_spd_feedback_2.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
        elif(can_id == CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_3.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_low_spd_feedback_3.can_id = can_id
            msg.arm_low_spd_feedback_3.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
            msg.arm_low_spd_feedback_3.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_low_spd_feedback_3.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
            msg.arm_low_spd_feedback_3.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
            msg.arm_low_spd_feedback_3.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
        elif(can_id == CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_4.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_low_spd_feedback_4.can_id = can_id
            msg.arm_low_spd_feedback_4.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
            msg.arm_low_spd_feedback_4.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_low_spd_feedback_4.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
            msg.arm_low_spd_feedback_4.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
            msg.arm_low_spd_feedback_4.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
        elif(can_id == CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_5.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_low_spd_feedback_5.can_id = can_id
            msg.arm_low_spd_feedback_5.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
            msg.arm_low_spd_feedback_5.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_low_spd_feedback_5.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
            msg.arm_low_spd_feedback_5.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
            msg.arm_low_spd_feedback_5.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
        elif(can_id == CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_6.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_low_spd_feedback_6.can_id = can_id
            msg.arm_low_spd_feedback_6.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
            msg.arm_low_spd_feedback_6.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
            msg.arm_low_spd_feedback_6.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
            msg.arm_low_spd_feedback_6.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
            msg.arm_low_spd_feedback_6.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
        # 设置指令应答，0x476
        elif(can_id == CanIDPiper.ARM_FEEDBACK_RESP_SET_INSTRUCTION.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_feedback_resp_set_instruction.instruction_index = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
            msg.arm_feedback_resp_set_instruction.is_set_zero_successfully = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,1,2),False)
        elif(can_id == CanIDPiper.ARM_FEEDBACK_CURRENT_MOTOR_ANGLE_LIMIT_MAX_SPD.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
            msg.arm_feedback_current_motor_angle_limit_max_spd.max_angle_limit = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,1,3))
            msg.arm_feedback_current_motor_angle_limit_max_spd.min_angle_limit = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,3,5))
            msg.arm_feedback_current_motor_angle_limit_max_spd.max_joint_spd = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,5,7),False)
        elif(can_id == CanIDPiper.ARM_FEEDBACK_CURRENT_END_VEL_ACC_PARAM.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_feedback_current_end_vel_acc_param.end_max_linear_vel = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
            msg.arm_feedback_current_end_vel_acc_param.end_max_angular_vel = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4),False)
            msg.arm_feedback_current_end_vel_acc_param.end_max_linear_acc = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,4,6),False)
            msg.arm_feedback_current_end_vel_acc_param.end_max_angular_acc = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
        elif(can_id == CanIDPiper.ARM_CRASH_PROTECTION_RATING_FEEDBACK.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_crash_protection_rating_feedback.joint_1_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
            msg.arm_crash_protection_rating_feedback.joint_2_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,1,2),False)
            msg.arm_crash_protection_rating_feedback.joint_3_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,2,3),False)
            msg.arm_crash_protection_rating_feedback.joint_4_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,3,4),False)
            msg.arm_crash_protection_rating_feedback.joint_5_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5),False)
            msg.arm_crash_protection_rating_feedback.joint_6_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
        elif(can_id == CanIDPiper.ARM_FEEDBACK_CURRENT_MOTOR_MAX_ACC_LIMIT.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
            msg.arm_feedback_current_motor_max_acc_limit.max_joint_acc = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,1,3),False)
        # 机械臂控制指令2,0x151
        elif(can_id == CanIDPiper.ARM_MOTION_CTRL_2.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_motion_ctrl_2.ctrl_mode = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
            msg.arm_motion_ctrl_2.move_mode = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,1,2),False)
            msg.arm_motion_ctrl_2.move_spd_rate_ctrl = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,2,3),False)
            msg.arm_motion_ctrl_2.mit_mode = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,3,4),False)
            msg.arm_motion_ctrl_2.residence_time = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5),False)
        # 读取主臂发送的目标joint数值
        elif(can_id == CanIDPiper.ARM_JOINT_CTRL_12.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_joint_ctrl.joint_1 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_joint_ctrl.joint_2 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_JOINT_CTRL_34.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_joint_ctrl.joint_3 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_joint_ctrl.joint_4 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        elif(can_id == CanIDPiper.ARM_JOINT_CTRL_56.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_joint_ctrl.joint_5 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_joint_ctrl.joint_6 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
        # 夹爪
        elif(can_id == CanIDPiper.ARM_GRIPPER_CTRL.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_gripper_ctrl.grippers_angle = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
            msg.arm_gripper_ctrl.grippers_effort = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,4,6))
            msg.arm_gripper_ctrl.status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,6,7),False)
            msg.arm_gripper_ctrl.set_zero = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,7,8),False)
        # 固件版本
        elif(can_id == CanIDPiper.ARM_FIRMWARE_READ.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.firmware_data = can_data
        # 夹爪/示教器参数反馈指令(基于V1.5-2版本后)
        elif(can_id == CanIDPiper.ARM_GRIPPER_TEACHING_PENDANT_PARAM_FEEDBACK.value):
            msg.type_ = ArmMessageMapping.get_mapping(can_id=can_id)
            msg.time_stamp = can_time_now
            msg.arm_gripper_teaching_param_feedback.teaching_range_per = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
            msg.arm_gripper_teaching_param_feedback.max_range_config = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,1,2),False)
            # (基于V1.5-8版本后)
            msg.arm_gripper_teaching_param_feedback.teaching_friction = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,2,3),False)
        else:
            ret = False
        return ret

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
        tx_can_frame.arbitration_id = ArmMessageMapping.get_mapping(msg_type=msg_type_)
        if(msg_type_ == ArmMsgType.PiperMsgMotionCtrl_1):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motion_ctrl_1.emergency_stop,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_1.track_ctrl,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_1.grag_teach_ctrl,False) + \
                                [0x00, 0x00, 0x00, 0x00, 0x00]
        elif(msg_type_ == ArmMsgType.PiperMsgMotionCtrl_2):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motion_ctrl_2.ctrl_mode,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.move_mode,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.move_spd_rate_ctrl,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.mit_mode,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.residence_time,False) + \
                                self.ConvertToList_8bit(msg.arm_motion_ctrl_2.installation_pos,False) + \
                                [0x00, 0x00]
        elif(msg_type_ == ArmMsgType.PiperMsgMotionCtrlCartesian_1):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.X_axis) + \
                                self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.Y_axis)
        elif(msg_type_ == ArmMsgType.PiperMsgMotionCtrlCartesian_2):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.Z_axis) + \
                                self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.RX_axis)
        elif(msg_type_ == ArmMsgType.PiperMsgMotionCtrlCartesian_3):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.RY_axis) + \
                                self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.RZ_axis)
        elif(msg_type_ == ArmMsgType.PiperMsgJointCtrl_12):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_1) + \
                                self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_2)
        elif(msg_type_ == ArmMsgType.PiperMsgJointCtrl_34):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_3) + \
                                self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_4)
        elif(msg_type_ == ArmMsgType.PiperMsgJointCtrl_56):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_5) + \
                                self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_6)
        elif(msg_type_ == ArmMsgType.PiperMsgCircularPatternCoordNumUpdateCtrl):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_circular_ctrl.instruction_num,False) + \
                                [0, 0, 0, 0, 0, 0, 0]
        elif(msg_type_ == ArmMsgType.PiperMsgGripperCtrl):
            tx_can_frame.data = self.ConvertToList_32bit(msg.arm_gripper_ctrl.grippers_angle) + \
                                self.ConvertToList_16bit(msg.arm_gripper_ctrl.grippers_effort,False) + \
                                self.ConvertToList_8bit(msg.arm_gripper_ctrl.status_code,False) + \
                                self.ConvertToList_8bit(msg.arm_gripper_ctrl.set_zero,False)
        elif(msg_type_ == ArmMsgType.PiperMsgMasterSlaveModeConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_ms_config.linkage_config,False) + \
                                self.ConvertToList_8bit(msg.arm_ms_config.feedback_offset,False) + \
                                self.ConvertToList_8bit(msg.arm_ms_config.ctrl_offset,False) + \
                                self.ConvertToList_8bit(msg.arm_ms_config.linkage_offset,False) + \
                                [0, 0, 0, 0]
        elif(msg_type_ == ArmMsgType.PiperMsgMotorEnableDisableConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motor_enable.motor_num,False) + \
                                self.ConvertToList_8bit(msg.arm_motor_enable.enable_flag,False) + \
                                [0, 0, 0, 0, 0, 0]
        elif(msg_type_ == ArmMsgType.PiperMsgSearchMotorMaxAngleSpdAccLimit):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_search_motor_max_angle_spd_acc_limit.motor_num,False) + \
                                self.ConvertToList_8bit(msg.arm_search_motor_max_angle_spd_acc_limit.search_content,False) + \
                                [0, 0, 0, 0, 0, 0]
        elif(msg_type_ == ArmMsgType.PiperMsgMotorAngleLimitMaxSpdSet):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motor_angle_limit_max_spd_set.motor_num,False) + \
                                self.ConvertToList_16bit(msg.arm_motor_angle_limit_max_spd_set.max_angle_limit) + \
                                self.ConvertToList_16bit(msg.arm_motor_angle_limit_max_spd_set.min_angle_limit) + \
                                self.ConvertToList_16bit(msg.arm_motor_angle_limit_max_spd_set.max_joint_spd,False) + \
                                [0]
        elif(msg_type_ == ArmMsgType.PiperMsgJointConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_joint_config.joint_motor_num,False) + \
                                self.ConvertToList_8bit(msg.arm_joint_config.set_motor_current_pos_as_zero,False) + \
                                self.ConvertToList_8bit(msg.arm_joint_config.acc_param_config_is_effective_or_not,False) + \
                                self.ConvertToList_16bit(msg.arm_joint_config.max_joint_acc,False) + \
                                self.ConvertToList_8bit(msg.arm_joint_config.clear_joint_err,False) + \
                                [0, 0]
        elif(msg_type_ == ArmMsgType.PiperMsgInstructionResponseConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_set_instruction_response.instruction_index,False) + \
                                self.ConvertToList_8bit(msg.arm_set_instruction_response.zero_config_success_flag,False) + \
                                [0, 0, 0, 0, 0, 0]
        elif(msg_type_ == ArmMsgType.PiperMsgParamEnquiryAndConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.param_enquiry,False) + \
                                self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.param_setting,False) + \
                                self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.data_feedback_0x48x,False) + \
                                self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.end_load_param_setting_effective,False) + \
                                self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.set_end_load,False) + \
                                [0, 0, 0]
        elif(msg_type_ == ArmMsgType.PiperMsgEndVelAccParamConfig):
            tx_can_frame.data = self.ConvertToList_16bit(msg.arm_end_vel_acc_param_config.end_max_linear_vel,False) + \
                                self.ConvertToList_16bit(msg.arm_end_vel_acc_param_config.end_max_angular_vel,False) + \
                                self.ConvertToList_16bit(msg.arm_end_vel_acc_param_config.end_max_linear_acc,False) + \
                                self.ConvertToList_16bit(msg.arm_end_vel_acc_param_config.end_max_angular_acc,False)
        elif(msg_type_ == ArmMsgType.PiperMsgCrashProtectionRatingConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_1_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_2_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_3_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_4_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_5_protection_level,False) + \
                                self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_6_protection_level,False) + \
                                [0, 0]
        elif(msg_type_ == ArmMsgType.PiperMsgGripperTeachingPendantParamConfig):
            tx_can_frame.data = self.ConvertToList_8bit(msg.arm_gripper_teaching_param_config.teaching_range_per,False) + \
                                self.ConvertToList_8bit(msg.arm_gripper_teaching_param_config.max_range_config,False) + \
                                self.ConvertToList_8bit(msg.arm_gripper_teaching_param_config.teaching_friction,False) + \
                                [0, 0, 0, 0, 0]
        # 机械臂MIT单独控制电机
        elif(msg_type_ == ArmMsgType.PiperMsgJointMitCtrl_1 or
             msg_type_ == ArmMsgType.PiperMsgJointMitCtrl_2 or
             msg_type_ == ArmMsgType.PiperMsgJointMitCtrl_3 or
             msg_type_ == ArmMsgType.PiperMsgJointMitCtrl_4 or
             msg_type_ == ArmMsgType.PiperMsgJointMitCtrl_5 or
             msg_type_ == ArmMsgType.PiperMsgJointMitCtrl_6 ):
            tx_can_frame.data = self.ConvertToList_16bit(msg.arm_joint_mit_ctrl.pos_ref,False) + \
                                self.ConvertToList_8bit(((msg.arm_joint_mit_ctrl.vel_ref >> 4)&0xFF),False) + \
                                self.ConvertToList_8bit(((((msg.arm_joint_mit_ctrl.vel_ref&0xF)<<4)&0xF0) | 
                                                         ((msg.arm_joint_mit_ctrl.kp>>8)&0x0F)),False) + \
                                self.ConvertToList_8bit(msg.arm_joint_mit_ctrl.kp&0xFF,False) + \
                                self.ConvertToList_8bit((msg.arm_joint_mit_ctrl.kd>>4)&0xFF,False) + \
                                self.ConvertToList_8bit(((((msg.arm_joint_mit_ctrl.kd&0xF)<<4)&0xF0)|
                                                         ((msg.arm_joint_mit_ctrl.t_ref>>4)&0x0F)),False)
            crc = (tx_can_frame.data[0]^tx_can_frame.data[1]^tx_can_frame.data[2]^tx_can_frame.data[3]^tx_can_frame.data[4]^tx_can_frame.data[5]^ \
                tx_can_frame.data[6])&0x0F
            msg.arm_joint_mit_ctrl.crc = crc
            tx_can_frame.data = tx_can_frame.data + self.ConvertToList_8bit((((msg.arm_joint_mit_ctrl.t_ref<<4)&0xF0) | crc),False)
        else:
            ret = False
        return ret
            

