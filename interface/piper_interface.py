#!/usr/bin/env python3
# -*-coding:utf8-*-

#机械臂使用接口
import time
import can
from can.message import Message
from typing import (
    Optional,
)
from typing import Type
import threading
from typing_extensions import (
    Literal,
)
from ..hardware_port.can_encapsulation import C_STD_CAN
from ..protocol.protocol_v1 import C_PiperParserBase, C_PiperParserV1
from ..piper_msgs.msg_v1 import *

class C_PiperInterface():
    '''
    Piper机械臂接口
    '''
    class ArmStatus():
        '''
        机械臂状态二次封装类,增加时间戳
        '''
        time_stamp: float=0
        arm_status=ArmMsgStatus()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"{self.arm_status}\n")

    class ArmEndPose():
        '''
        机械臂末端姿态二次封装类,增加时间戳
        '''
        time_stamp: float=0
        end_pose=ArmMsgEndPoseFeedBack()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"{self.end_pose}\n")
    
    class ArmJointAndGripper():
        '''
        机械臂关节角度和夹爪二次封装类,将夹爪和关节角度信息放在一起,增加时间戳
        '''
        time_stamp: float=0
        joint_state=ArmMsgJointFeedBack()
        gripper_state=ArmMsgGripperFeedBack()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"{self.joint_state}\n"
                    f"{self.gripper_state}\n")
    
    class ArmMotorDriverInfoHighSpd():
        '''
        机械臂电机驱动高速反馈信息
        '''
        time_stamp: float=0
        motor_1=ArmHighSpdFeedback()
        motor_2=ArmHighSpdFeedback()
        motor_3=ArmHighSpdFeedback()
        motor_4=ArmHighSpdFeedback()
        motor_5=ArmHighSpdFeedback()
        motor_6=ArmHighSpdFeedback()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"motor_1:{self.motor_1}\n"
                    f"motor_2:{self.motor_2}\n"
                    f"motor_3:{self.motor_3}\n"
                    f"motor_4:{self.motor_4}\n"
                    f"motor_5:{self.motor_5}\n"
                    f"motor_6:{self.motor_6}\n")
    
    class ArmMotorDriverInfoLowSpd():
        '''
        机械臂电机驱动低速反馈信息
        '''
        time_stamp: float=0
        motor_1=ArmLowSpdFeedback()
        motor_2=ArmLowSpdFeedback()
        motor_3=ArmLowSpdFeedback()
        motor_4=ArmLowSpdFeedback()
        motor_5=ArmLowSpdFeedback()
        motor_6=ArmLowSpdFeedback()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"motor_1:{self.motor_1}\n"
                    f"motor_2:{self.motor_2}\n"
                    f"motor_3:{self.motor_3}\n"
                    f"motor_4:{self.motor_4}\n"
                    f"motor_5:{self.motor_5}\n"
                    f"motor_6:{self.motor_6}\n")
    
    class ArmMotorAngleLimitAndMaxVel():
        '''
        当前电机限制角度/最大速度
        '''
        time_stamp: float=0
        current_motor_angle_limit_max_vel=ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"current_motor_angle_limit_max_vel:{self.current_motor_angle_limit_max_vel}\n")

    class CurrentEndVelAndAccParam():
        '''
        当前末端速度/加速度参数
        '''
        time_stamp: float=0
        current_end_vel_acc_param=ArmMsgFeedbackCurrentEndVelAccParam()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"current_end_vel_acc_param:{self.current_end_vel_acc_param}\n")
    
    class CrashProtectionLevelFeedback():
        '''
        碰撞防护等级设置反馈指令
        '''
        time_stamp: float=0
        crash_protection_level_feedback=ArmMsgCrashProtectionRatingFeedback()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"crash_protection_level_feedback:{self.crash_protection_level_feedback}\n")
    
    class CurrentMotorMaxAccLimit():
        '''
        反馈当前电机最大加速度限制
        '''
        time_stamp: float=0
        current_motor_max_acc_limit=ArmMsgFeedbackCurrentMotorMaxAccLimit()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"current_motor_max_acc_limit:{self.current_motor_max_acc_limit}\n")

    class ArmJointAndGripperCtrl():
        '''
        机械臂关节角度和夹爪二次封装类,将夹爪和关节角度信息放在一起,增加时间戳
        这个是主臂发送的消息，用来读取发送给从臂的目标值
        '''
        time_stamp: float=0
        joint_ctrl=ArmMsgJointCtrl()
        gripper_ctrl=ArmMsgGripperCtrl()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"{self.joint_ctrl}\n"
                    f"{self.gripper_ctrl}\n")
    
    class ArmCtrlCode_151():
        '''
        机械臂发送控制指令0x151的消息接收,由主臂发送
        '''
        time_stamp: float=0
        ctrl_151=ArmMsgMotionCtrl_2()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"{self.ctrl_151}\n")

    class ArmTimeStamp():
        '''
        机械臂时间戳
        '''
        time_stamp_arm_status:float=0
        time_stamp_end_pose_1:float=0
        time_stamp_end_pose_2:float=0
        time_stamp_end_pose_3:float=0
        time_stamp_joint_12:float=0
        time_stamp_joint_34:float=0
        time_stamp_joint_56:float=0
        time_stamp_gripper:float=0
        time_stamp_motor_high_spd_1:float=0
        time_stamp_motor_high_spd_2:float=0
        time_stamp_motor_high_spd_3:float=0
        time_stamp_motor_high_spd_4:float=0
        time_stamp_motor_high_spd_5:float=0
        time_stamp_motor_high_spd_6:float=0
        time_stamp_motor_low_spd_1:float=0
        time_stamp_motor_low_spd_2:float=0
        time_stamp_motor_low_spd_3:float=0
        time_stamp_motor_low_spd_4:float=0
        time_stamp_motor_low_spd_5:float=0
        time_stamp_motor_low_spd_6:float=0
        time_stamp_joint_ctrl_12:float=0
        time_stamp_joint_ctrl_34:float=0
        time_stamp_joint_ctrl_56:float=0
        time_stamp_gripper_ctrl:float=0
    
    def __init__(self, can_name:str="can0") -> None:
        self.can_channel_name:str
        if isinstance(can_name, str):
            self.can_channel_name = can_name
        else:
            raise IndexError("C_PiperBase input can name is not str type")
        # print("----")
        self.arm_can=C_STD_CAN(can_name, "socketcan", 1000000, True, True, self.ParseCANFrame)
        # self.rx_original_msg:Optional[Message]
        # 协议解析
        self.parser: Type[C_PiperParserBase] = C_PiperParserV1()
        self.__arm_time_stamp = self.ArmTimeStamp()#时间戳
        # 二次封装数据类型
        self.__arm_status_mtx = threading.Lock()
        self.__arm_status = self.ArmStatus()

        self.__arm_end_pose_mtx = threading.Lock()
        self.__arm_end_pose = self.ArmEndPose()

        self.__arm_joint_gripper_msgs_mtx = threading.Lock()
        self.__arm_joint_gripper_msgs = self.ArmJointAndGripper()

        self.__arm_motor_info_high_spd_mtx = threading.Lock()
        self.__arm_motor_info_high_spd = self.ArmMotorDriverInfoHighSpd()

        self.__arm_motor_info_low_spd_mtx = threading.Lock()
        self.__arm_motor_info_low_spd = self.ArmMotorDriverInfoLowSpd()
        # 当前电机限制角度/最大速度
        self.__feedback_current_motor_angle_limit_max_vel_mtx = threading.Lock()
        self.__feedback_current_motor_angle_limit_max_vel = self.ArmMotorAngleLimitAndMaxVel()

        self.__feedback_current_end_vel_acc_param_mtx = threading.Lock()
        self.__feedback_current_end_vel_acc_param = self.CurrentEndVelAndAccParam()

        self.__feedback_crash_protection_level_mtx = threading.Lock()
        self.__feedback_crash_protection_level = self.CrashProtectionLevelFeedback()

        self.__feedback_current_motor_max_acc_limit_mtx = threading.Lock()
        self.__feedback_current_motor_max_acc_limit = self.CurrentMotorMaxAccLimit()

        self.__arm_joint_gripper_ctrl_msgs_mtx = threading.Lock()
        self.__arm_joint_gripper_ctrl_msgs = self.ArmJointAndGripperCtrl()

        self.__arm_ctrl_code_151_mtx = threading.Lock()
        self.__arm_ctrl_code_151 = self.ArmCtrlCode_151()
    
    def ConnectPort(self):
        # print("-----")
        # if(self.arm_can is None):
        # print("-==--")
        # self.arm_can = C_STD_CAN(can_name, "socketcan", 500000, True, True, self.ParseCANFrame)
        def ReadCan():
            while True:
                self.arm_can.ReadCanMessage()
                # print("=====")
        can_deal_th = threading.Thread(target=ReadCan)
        can_deal_th.daemon = True
        can_deal_th.start()
    
    def ParseCANFrame(self, rx_message: Optional[can.Message]):
        """can协议解析函数

        Args:
            rx_message (Optional[can.Message]): can接收的原始数据
        """
        msg = PiperMessage()
        receive_flag = self.parser.DecodeMessage(rx_message, msg)
        # print(receive_flag)
        if(receive_flag):
            self.UpdateArmStatus(msg)
            self.UpdateArmEndPoseState(msg)
            self.UpdateArmJointGripperState(msg)
            self.UpdateDriverInfoHighSpdFeedback(msg)
            self.UpdateDriverInfoLowSpdFeedback(msg)

            self.UpdateCurrentMotorAngleLimitMaxVel(msg)
            self.UpdateCurrentEndVelAndAccParam(msg)
            self.UpdateCrashProtectionLevelFeedback(msg)
            self.UpdateCurrentMotorMaxAccLimit(msg)
            # 更新主臂发送消息
            self.UpdateArmJointGripperStateCtrl(msg)
            self.UpdateArmCtrlCode151(msg)
    
    def JudgeExsitedArm(self, can_id:int):
        """判断当前can socket是否有指定的机械臂设备,通过can id筛选

        Args:
            can_id (int): 输入can 🆔
        """
        pass
    # 获取反馈值------------------------------------------------------------------------------------------------------
    def GetArmStatus(self):
        with self.__arm_status_mtx:
            return self.__arm_status

    def GetArmEndPoseMsgs(self):
        with self.__arm_end_pose_mtx:
            return self.__arm_end_pose

    def GetArmJointGripperMsgs(self):
        with self.__arm_joint_gripper_msgs_mtx:
            return self.__arm_joint_gripper_msgs
    
    def GetArmHighSpdInfoMsgs(self):
        with self.__arm_motor_info_high_spd_mtx:
            return self.__arm_motor_info_high_spd
    
    def GetArmLowSpdInfoMsgs(self):
        with self.__arm_motor_info_low_spd_mtx:
            return self.__arm_motor_info_low_spd
    
    def GetCurrentMotorAngleLimitMaxVel(self):
        with self.__feedback_current_motor_angle_limit_max_vel_mtx:
            return self.__feedback_current_motor_angle_limit_max_vel
    
    def GetCurrentEndVelAndAccParam(self):
        with self.__feedback_current_end_vel_acc_param_mtx:
            return self.__feedback_current_end_vel_acc_param
    
    def GetCrashProtectionLevelFeedback(self):
        with self.__feedback_crash_protection_level_mtx:
            return self.__feedback_crash_protection_level

    def GetCurrentMotorMaxAccLimit(self):
        with self.__feedback_current_motor_max_acc_limit_mtx:
            return self.__feedback_current_motor_max_acc_limit
    
    def GetArmJointGripperCtrlMsgs(self):
        with self.__arm_joint_gripper_ctrl_msgs_mtx:
            return self.__arm_joint_gripper_ctrl_msgs
    
    def GetArmCtrlCode151(self):
        with self.__arm_ctrl_code_151_mtx:
            return self.__arm_ctrl_code_151
    # 发送控制值-------------------------------------------------------------------------------------------------------

    # 接收反馈函数------------------------------------------------------------------------------------------------------
    def UpdateArmStatus(self, msg:PiperMessage):
        """更新机械臂状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        """
        with self.__arm_status_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgStatusFeedback):
                self.__arm_status.time_stamp = time.time_ns()/ 1_000_000_000
                self.__arm_status.arm_status.ctrl_mode = msg.arm_status_msgs.ctrl_mode
                self.__arm_status.arm_status.arm_status = msg.arm_status_msgs.arm_status
                self.__arm_status.arm_status.mode_feed = msg.arm_status_msgs.mode_feed
                self.__arm_status.arm_status.teach_status = msg.arm_status_msgs.teach_status
                self.__arm_status.arm_status.motion_status = msg.arm_status_msgs.motion_status
                self.__arm_status.arm_status.trajectory_num = msg.arm_status_msgs.trajectory_num
                self.__arm_status.arm_status.err_code = msg.arm_status_msgs.err_code
            # print(self.__arm_status)
            return self.__arm_status

    def UpdateArmEndPoseState(self, msg:PiperMessage):
        """更新末端位姿状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        """
        with self.__arm_end_pose_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgEndPoseFeedback_1):
                self.__arm_time_stamp.time_stamp_end_pose_1 = time.time_ns()
                self.__arm_end_pose.end_pose.X_axis = msg.arm_end_pose.X_axis
                self.__arm_end_pose.end_pose.Y_axis = msg.arm_end_pose.Y_axis
            elif(msg.type_ == ArmMsgType.PiperMsgEndPoseFeedback_2):
                self.__arm_time_stamp.time_stamp_end_pose_2 = time.time_ns()
                self.__arm_end_pose.end_pose.Z_axis = msg.arm_end_pose.Z_axis
                self.__arm_end_pose.end_pose.RX_axis = msg.arm_end_pose.RX_axis
            elif(msg.type_ == ArmMsgType.PiperMsgEndPoseFeedback_3):
                self.__arm_time_stamp.time_stamp_end_pose_3 = time.time_ns()
                self.__arm_end_pose.end_pose.RY_axis = msg.arm_end_pose.RY_axis
                self.__arm_end_pose.end_pose.RZ_axis = msg.arm_end_pose.RZ_axis
            self.__arm_end_pose.time_stamp = max(self.__arm_time_stamp.time_stamp_end_pose_1, 
                                                self.__arm_time_stamp.time_stamp_end_pose_2, 
                                                self.__arm_time_stamp.time_stamp_end_pose_3) / 1_000_000_000
            # print(self.__arm_end_pose)
            return self.__arm_end_pose

    def UpdateArmJointGripperState(self, msg:PiperMessage):
        """更新关节和夹爪状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        """
        with self.__arm_joint_gripper_msgs_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgJointFeedBack_12):
                self.__arm_time_stamp.time_stamp_joint_12 = time.time_ns()
                self.__arm_joint_gripper_msgs.joint_state.joint_1 = msg.arm_joint_feedback.joint_1
                self.__arm_joint_gripper_msgs.joint_state.joint_2 = msg.arm_joint_feedback.joint_2
            elif(msg.type_ == ArmMsgType.PiperMsgJointFeedBack_34):
                self.__arm_time_stamp.time_stamp_joint_34 = time.time_ns()
                self.__arm_joint_gripper_msgs.joint_state.joint_3 = msg.arm_joint_feedback.joint_3
                self.__arm_joint_gripper_msgs.joint_state.joint_4 = msg.arm_joint_feedback.joint_4
            elif(msg.type_ == ArmMsgType.PiperMsgJointFeedBack_56):
                self.__arm_time_stamp.time_stamp_joint_56 = time.time_ns()
                self.__arm_joint_gripper_msgs.joint_state.joint_5 = msg.arm_joint_feedback.joint_5
                self.__arm_joint_gripper_msgs.joint_state.joint_6 = msg.arm_joint_feedback.joint_6
            elif(msg.type_ == ArmMsgType.PiperMsgGripperFeedBack):
                self.__arm_time_stamp.time_stamp_gripper = time.time_ns()
                self.__arm_joint_gripper_msgs.gripper_state.grippers_angle = msg.gripper_feedback.grippers_angle
                self.__arm_joint_gripper_msgs.gripper_state.grippers_effort = msg.gripper_feedback.grippers_effort
                self.__arm_joint_gripper_msgs.gripper_state.status_code = msg.gripper_feedback.status_code
            else:
                pass
            # 更新时间戳，取筛选ID的最新一个
            self.__arm_joint_gripper_msgs.time_stamp = max(self.__arm_time_stamp.time_stamp_joint_12, 
                                                        self.__arm_time_stamp.time_stamp_joint_34, 
                                                        self.__arm_time_stamp.time_stamp_joint_56, 
                                                        self.__arm_time_stamp.time_stamp_gripper)/ 1_000_000_000
            # print(self.__arm_joint_gripper_msgs)
            return self.__arm_joint_gripper_msgs

    def UpdateDriverInfoHighSpdFeedback(self, msg:PiperMessage):
        """更新驱动器信息反馈, 高速

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        """
        with self.__arm_motor_info_high_spd_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_1):
                self.__arm_time_stamp.time_stamp_motor_low_spd_1 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_1.can_id = msg.arm_high_spd_feedback_1.can_id
                self.__arm_motor_info_high_spd.motor_1.motor_speed = msg.arm_high_spd_feedback_1.motor_speed
                self.__arm_motor_info_high_spd.motor_1.current = msg.arm_high_spd_feedback_1.current
                self.__arm_motor_info_high_spd.motor_1.pos = msg.arm_high_spd_feedback_1.pos
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_2):
                self.__arm_time_stamp.time_stamp_motor_low_spd_2 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_2.can_id = msg.arm_high_spd_feedback_2.can_id
                self.__arm_motor_info_high_spd.motor_2.motor_speed = msg.arm_high_spd_feedback_2.motor_speed
                self.__arm_motor_info_high_spd.motor_2.current = msg.arm_high_spd_feedback_2.current
                self.__arm_motor_info_high_spd.motor_2.pos = msg.arm_high_spd_feedback_2.pos
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_3):
                self.__arm_time_stamp.time_stamp_motor_low_spd_3 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_3.can_id = msg.arm_high_spd_feedback_3.can_id
                self.__arm_motor_info_high_spd.motor_3.motor_speed = msg.arm_high_spd_feedback_3.motor_speed
                self.__arm_motor_info_high_spd.motor_3.current = msg.arm_high_spd_feedback_3.current
                self.__arm_motor_info_high_spd.motor_3.pos = msg.arm_high_spd_feedback_3.pos
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_4):
                self.__arm_time_stamp.time_stamp_motor_low_spd_4 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_4.can_id = msg.arm_high_spd_feedback_4.can_id
                self.__arm_motor_info_high_spd.motor_4.motor_speed = msg.arm_high_spd_feedback_4.motor_speed
                self.__arm_motor_info_high_spd.motor_4.current = msg.arm_high_spd_feedback_4.current
                self.__arm_motor_info_high_spd.motor_4.pos = msg.arm_high_spd_feedback_4.pos
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_5):
                self.__arm_time_stamp.time_stamp_motor_low_spd_5 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_5.can_id = msg.arm_high_spd_feedback_5.can_id
                self.__arm_motor_info_high_spd.motor_5.motor_speed = msg.arm_high_spd_feedback_5.motor_speed
                self.__arm_motor_info_high_spd.motor_5.current = msg.arm_high_spd_feedback_5.current
                self.__arm_motor_info_high_spd.motor_5.pos = msg.arm_high_spd_feedback_5.pos
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_6):
                self.__arm_time_stamp.time_stamp_motor_low_spd_6 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_6.can_id = msg.arm_high_spd_feedback_6.can_id
                self.__arm_motor_info_high_spd.motor_6.motor_speed = msg.arm_high_spd_feedback_6.motor_speed
                self.__arm_motor_info_high_spd.motor_6.current = msg.arm_high_spd_feedback_6.current
                self.__arm_motor_info_high_spd.motor_6.pos = msg.arm_high_spd_feedback_6.pos
            else:
                pass
            # 更新时间戳，取筛选ID的最新一个
            self.__arm_motor_info_high_spd.time_stamp = max(self.__arm_time_stamp.time_stamp_motor_low_spd_1, 
                                                    self.__arm_time_stamp.time_stamp_motor_low_spd_2, 
                                                    self.__arm_time_stamp.time_stamp_motor_low_spd_3, 
                                                    self.__arm_time_stamp.time_stamp_motor_low_spd_4, 
                                                    self.__arm_time_stamp.time_stamp_motor_low_spd_5, 
                                                    self.__arm_time_stamp.time_stamp_motor_low_spd_6) / 1_000_000_000
            # print(self.__arm_motor_info_high_spd)
            return self.__arm_motor_info_high_spd
    
    def UpdateDriverInfoLowSpdFeedback(self, msg:PiperMessage):
        """更新驱动器信息反馈, 低速

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        """
        with self.__arm_motor_info_low_spd_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_1):
                self.__arm_time_stamp.time_stamp_motor_low_spd_1 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_1.can_id = msg.arm_low_spd_feedback_1.can_id
                self.__arm_motor_info_low_spd.motor_1.vol = msg.arm_low_spd_feedback_1.vol
                self.__arm_motor_info_low_spd.motor_1.foc_temp = msg.arm_low_spd_feedback_1.foc_temp
                self.__arm_motor_info_low_spd.motor_1.motor_temp = msg.arm_low_spd_feedback_1.motor_temp
                self.__arm_motor_info_low_spd.motor_1.foc_status_code = msg.arm_low_spd_feedback_1.foc_status_code
                self.__arm_motor_info_low_spd.motor_1.bus_current = msg.arm_low_spd_feedback_1.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_2):
                self.__arm_time_stamp.time_stamp_motor_low_spd_2 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_2.can_id = msg.arm_low_spd_feedback_2.can_id
                self.__arm_motor_info_low_spd.motor_2.vol= msg.arm_low_spd_feedback_2.vol
                self.__arm_motor_info_low_spd.motor_2.foc_temp = msg.arm_low_spd_feedback_2.foc_temp
                self.__arm_motor_info_low_spd.motor_2.motor_temp = msg.arm_low_spd_feedback_2.motor_temp
                self.__arm_motor_info_low_spd.motor_2.foc_status_code = msg.arm_low_spd_feedback_2.foc_status_code
                self.__arm_motor_info_low_spd.motor_2.bus_current = msg.arm_low_spd_feedback_2.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_3):
                self.__arm_time_stamp.time_stamp_motor_low_spd_3 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_3.can_id = msg.arm_low_spd_feedback_3.can_id
                self.__arm_motor_info_low_spd.motor_3.vol = msg.arm_low_spd_feedback_3.vol
                self.__arm_motor_info_low_spd.motor_3.foc_temp = msg.arm_low_spd_feedback_3.foc_temp
                self.__arm_motor_info_low_spd.motor_3.motor_temp = msg.arm_low_spd_feedback_3.motor_temp
                self.__arm_motor_info_low_spd.motor_3.foc_status_code = msg.arm_low_spd_feedback_3.foc_status_code
                self.__arm_motor_info_low_spd.motor_3.bus_current = msg.arm_low_spd_feedback_3.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_4):
                self.__arm_time_stamp.time_stamp_motor_low_spd_4 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_4.can_id = msg.arm_low_spd_feedback_4.can_id
                self.__arm_motor_info_low_spd.motor_4.vol = msg.arm_low_spd_feedback_4.vol
                self.__arm_motor_info_low_spd.motor_4.foc_temp = msg.arm_low_spd_feedback_4.foc_temp
                self.__arm_motor_info_low_spd.motor_4.motor_temp = msg.arm_low_spd_feedback_4.motor_temp
                self.__arm_motor_info_low_spd.motor_4.foc_status_code = msg.arm_low_spd_feedback_4.foc_status_code
                self.__arm_motor_info_low_spd.motor_4.bus_current = msg.arm_low_spd_feedback_4.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_5):
                self.__arm_time_stamp.time_stamp_motor_low_spd_5 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_5.can_id = msg.arm_low_spd_feedback_5.can_id
                self.__arm_motor_info_low_spd.motor_5.vol = msg.arm_low_spd_feedback_5.vol
                self.__arm_motor_info_low_spd.motor_5.foc_temp = msg.arm_low_spd_feedback_5.foc_temp
                self.__arm_motor_info_low_spd.motor_5.motor_temp = msg.arm_low_spd_feedback_5.motor_temp
                self.__arm_motor_info_low_spd.motor_5.foc_status_code = msg.arm_low_spd_feedback_5.foc_status_code
                self.__arm_motor_info_low_spd.motor_5.bus_current = msg.arm_low_spd_feedback_5.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_6):
                self.__arm_time_stamp.time_stamp_motor_low_spd_6 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_6.can_id = msg.arm_low_spd_feedback_6.can_id
                self.__arm_motor_info_low_spd.motor_6.vol = msg.arm_low_spd_feedback_6.vol
                self.__arm_motor_info_low_spd.motor_6.foc_temp = msg.arm_low_spd_feedback_6.foc_temp
                self.__arm_motor_info_low_spd.motor_6.motor_temp = msg.arm_low_spd_feedback_6.motor_temp
                self.__arm_motor_info_low_spd.motor_6.foc_status_code = msg.arm_low_spd_feedback_6.foc_status_code
                self.__arm_motor_info_low_spd.motor_6.bus_current = msg.arm_low_spd_feedback_6.bus_current
            else:
                pass
            # 更新时间戳，取筛选ID的最新一个
            self.__arm_motor_info_low_spd.time_stamp = max(self.__arm_time_stamp.time_stamp_motor_low_spd_1, 
                                                            self.__arm_time_stamp.time_stamp_motor_low_spd_2, 
                                                            self.__arm_time_stamp.time_stamp_motor_low_spd_3, 
                                                            self.__arm_time_stamp.time_stamp_motor_low_spd_4, 
                                                            self.__arm_time_stamp.time_stamp_motor_low_spd_5, 
                                                            self.__arm_time_stamp.time_stamp_motor_low_spd_6) / 1_000_000_000
            # print(self.__arm_motor_info_low_spd)
            return self.__arm_motor_info_low_spd
    
    def UpdateCurrentMotorAngleLimitMaxVel(self, msg:PiperMessage):
        '''
        更新
        反馈当前电机限制角度/最大速度
        为主动发送指令后反馈消息
        对应查询电机角度/最大速度/最大加速度限制指令 0x472 Byte 1 = 0x01
        
        0x473
        '''
        with self.__feedback_current_motor_angle_limit_max_vel_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgFeedbackCurrentMotorAngleLimitMaxSpd):
                self.__feedback_current_motor_angle_limit_max_vel.time_stamp = time.time_ns()/ 1_000_000_000
                self.__feedback_current_motor_angle_limit_max_vel.current_motor_angle_limit_max_vel.motor_num = \
                    msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num
                self.__feedback_current_motor_angle_limit_max_vel.current_motor_angle_limit_max_vel.max_angle_limit = \
                    msg.arm_feedback_current_motor_angle_limit_max_spd.max_angle_limit
                self.__feedback_current_motor_angle_limit_max_vel.current_motor_angle_limit_max_vel.min_angle_limit = \
                    msg.arm_feedback_current_motor_angle_limit_max_spd.min_angle_limit
                self.__feedback_current_motor_angle_limit_max_vel.current_motor_angle_limit_max_vel.max_jonit_spd = \
                    msg.arm_feedback_current_motor_angle_limit_max_spd.max_jonit_spd
            # print(self.__feedback_current_motor_angle_limit_max_vel)
            return self.__feedback_current_motor_angle_limit_max_vel
    
    def UpdateCurrentMotorMaxAccLimit(self, msg:PiperMessage):
        '''
        反馈当前电机最大加速度限制
        为主动发送指令后反馈消息
        对应查询电机角度/最大速度/最大加速度限制指令 0x472 Byte 1 = 0x02

        0x47C
        '''
        with self.__feedback_current_motor_max_acc_limit_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgFeedbackCurrentMotorMaxAccLimit):
                self.__feedback_current_motor_max_acc_limit.time_stamp = time.time_ns()/ 1_000_000_000
                self.__feedback_current_motor_max_acc_limit.current_motor_max_acc_limit.joint_motor_num = \
                    msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num
                self.__feedback_current_motor_max_acc_limit.current_motor_max_acc_limit.max_joint_acc = \
                    msg.arm_feedback_current_motor_max_acc_limit.max_joint_acc
            # print(self.__feedback_current_motor_max_acc_limit)
            return self.__feedback_current_motor_max_acc_limit
    
    def UpdateCurrentEndVelAndAccParam(self, msg:PiperMessage):
        '''
        反馈当前末端速度/加速度参数
        为主动发送指令后反馈消息

        对应机械臂参数查询与设置指令 0x477 Byte 0 = 0x01

        0x478
        '''
        with self.__feedback_current_end_vel_acc_param_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgFeedbackCurrentEndVelAccParam):
                self.__feedback_current_end_vel_acc_param.time_stamp = time.time_ns()/ 1_000_000_000
                self.__feedback_current_end_vel_acc_param.current_end_vel_acc_param.end_max_linear_vel = \
                    msg.arm_feedback_current_end_vel_acc_param.end_max_linear_vel
                self.__feedback_current_end_vel_acc_param.current_end_vel_acc_param.end_max_angular_vel = \
                    msg.arm_feedback_current_end_vel_acc_param.end_max_angular_vel
                self.__feedback_current_end_vel_acc_param.current_end_vel_acc_param.end_max_linear_acc = \
                    msg.arm_feedback_current_end_vel_acc_param.end_max_linear_acc
                self.__feedback_current_end_vel_acc_param.current_end_vel_acc_param.end_max_angular_acc = \
                    msg.arm_feedback_current_end_vel_acc_param.end_max_angular_acc
            # print(self.__feedback_current_end_vel_acc_param)
            return self.__feedback_current_end_vel_acc_param
    
    def UpdateCrashProtectionLevelFeedback(self, msg:PiperMessage):
        '''
        碰撞防护等级设置反馈指令
        为主动发送指令后反馈消息
        对应机械臂参数查询与设置指令 0x477 Byte 0 = 0x02

        0x47B
        '''
        with self.__feedback_crash_protection_level_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgCrashProtectionRatingFeedback):
                self.__feedback_crash_protection_level.time_stamp = time.time_ns()/ 1_000_000_000
                self.__feedback_crash_protection_level.crash_protection_level_feedback.jonit_1_protection_level=\
                    msg.arm_crash_protection_rating_feedback.jonit_1_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.jonit_2_protection_level=\
                    msg.arm_crash_protection_rating_feedback.jonit_2_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.jonit_3_protection_level=\
                    msg.arm_crash_protection_rating_feedback.jonit_3_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.jonit_4_protection_level=\
                    msg.arm_crash_protection_rating_feedback.jonit_4_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.jonit_5_protection_level=\
                    msg.arm_crash_protection_rating_feedback.jonit_5_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.jonit_6_protection_level=\
                    msg.arm_crash_protection_rating_feedback.jonit_6_protection_level
            # print(self.__feedback_crash_protection_level)
            return self.__feedback_crash_protection_level
    
    def UpdateArmJointGripperStateCtrl(self, msg:PiperMessage):
        """更新关节和夹爪状态,为主臂发送的消息

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        """
        with self.__arm_joint_gripper_ctrl_msgs_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgJointCtrl_12):
                self.__arm_time_stamp.time_stamp_joint_ctrl_12 = time.time_ns()
                # print(msg.arm_joint_ctrl)
                self.__arm_joint_gripper_ctrl_msgs.joint_ctrl.joint_1 = msg.arm_joint_ctrl.joint_1
                self.__arm_joint_gripper_ctrl_msgs.joint_ctrl.joint_2 = msg.arm_joint_ctrl.joint_2
            elif(msg.type_ == ArmMsgType.PiperMsgJointCtrl_34):
                self.__arm_time_stamp.time_stamp_joint_ctrl_34 = time.time_ns()
                self.__arm_joint_gripper_ctrl_msgs.joint_ctrl.joint_3 = msg.arm_joint_ctrl.joint_3
                self.__arm_joint_gripper_ctrl_msgs.joint_ctrl.joint_4 = msg.arm_joint_ctrl.joint_4
            elif(msg.type_ == ArmMsgType.PiperMsgJointCtrl_56):
                self.__arm_time_stamp.time_stamp_joint_ctrl_56 = time.time_ns()
                self.__arm_joint_gripper_ctrl_msgs.joint_ctrl.joint_5 = msg.arm_joint_ctrl.joint_5
                self.__arm_joint_gripper_ctrl_msgs.joint_ctrl.joint_6 = msg.arm_joint_ctrl.joint_6
            elif(msg.type_ == ArmMsgType.PiperMsgGripperCtrl):
                self.__arm_time_stamp.time_stamp_gripper_ctrl = time.time_ns()
                self.__arm_joint_gripper_ctrl_msgs.gripper_ctrl.grippers_angle = msg.arm_gripper_ctrl.grippers_angle
                self.__arm_joint_gripper_ctrl_msgs.gripper_ctrl.grippers_effort = msg.arm_gripper_ctrl.grippers_effort
                self.__arm_joint_gripper_ctrl_msgs.gripper_ctrl.status_code = msg.arm_gripper_ctrl.status_code
                self.__arm_joint_gripper_ctrl_msgs.gripper_ctrl.set_zero = msg.arm_gripper_ctrl.set_zero
            else:
                pass
            # 更新时间戳，取筛选ID的最新一个
            self.__arm_joint_gripper_ctrl_msgs.time_stamp = max(self.__arm_time_stamp.time_stamp_joint_ctrl_12, 
                                                        self.__arm_time_stamp.time_stamp_joint_ctrl_34, 
                                                        self.__arm_time_stamp.time_stamp_joint_ctrl_56, 
                                                        self.__arm_time_stamp.time_stamp_gripper_ctrl)/ 1_000_000_000
            # print(self.__arm_joint_gripper_ctrl_msgs)
            return self.__arm_joint_gripper_ctrl_msgs
    
    def UpdateArmCtrlCode151(self, msg:PiperMessage):
        '''
        更新主臂发送的151控制指令

        0x151
        '''
        with self.__arm_ctrl_code_151_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgMotionCtrl_2):
                self.__arm_ctrl_code_151.time_stamp = time.time_ns()/ 1_000_000_000
                self.__arm_ctrl_code_151.ctrl_151.ctrl_mode = \
                    msg.arm_motion_ctrl_2.ctrl_mode
                self.__arm_ctrl_code_151.ctrl_151.move_mode = \
                    msg.arm_motion_ctrl_2.move_mode
                self.__arm_ctrl_code_151.ctrl_151.move_spd_rate_ctrl = \
                    msg.arm_motion_ctrl_2.move_spd_rate_ctrl
                self.__arm_ctrl_code_151.ctrl_151.mit_mode = \
                    msg.arm_motion_ctrl_2.mit_mode
                self.__arm_ctrl_code_151.ctrl_151.residence_time = \
                    msg.arm_motion_ctrl_2.residence_time
            # print(self.__arm_ctrl_code_151)
            return self.__arm_ctrl_code_151
    # 控制发送函数------------------------------------------------------------------------------------------------------
    def MotionCtrl_1(self, emergency_stop, track_ctrl, grag_teach_ctrl):
        '''
        机械臂运动控制指令1 

        Byte 0 快速急停 uint8 0x00 无效
                            0x01 快速急停 0x02 恢复
        Byte 1 轨迹指令 uint8 0x00 关闭
                            0x01 暂停当前规划 
                            0x02 继续当前轨迹
                            0x03 清除当前轨迹 
                            0x04 清除所有轨迹 
                            0x05 获取当前规划轨迹 
                            0x06 终止执行 
                            0x07 轨迹传输 
                            0x08 轨迹传输结束
        Byte 2 拖动示教指令 uint8 0x00 关闭
                                0x01 开始示教记录（进入拖动示教模式） 
                                0x02 结束示教记录（退出拖动示教模式） 
                                0x03 执行示教轨迹（拖动示教轨迹复现） 
                                0x04 暂停执行 
                                0x05 继续执行（轨迹复现继续） 
                                0x06 终止执行 
                                0x07 运动到轨迹起点
        Byte 3 轨迹索引 uint8 标记刚才传输的轨迹点为第N个轨迹点
                                N=0~255 主控收到后会应答0x476 byte0 = 0x50 ;
                                byte 2=N(详见0x476 )未收到应答需要重传
        Byte 4 NameIndex_H uint16 当前轨迹包名称索引,由NameIndex和crc组成(应答0x477 byte0=03) Byte 5 crc16 uint16
        '''
        tx_can=Message()
        motion_ctrl_1 = ArmMsgMotionCtrl_1(emergency_stop, track_ctrl, grag_teach_ctrl)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrl_1, arm_motion_ctrl_1=motion_ctrl_1)
        self.parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def MotionCtrl_2(self, ctrl_mode, move_mode, move_spd_rate_ctrl):
        '''
        机械臂运动控制指令2

        0x151

        Byte 0 控制模式 uint8 0x00 待机模式
                                    0x01 CAN 指令控制模式 0x02 示教模式 0x03 以太网控制模式 0x04 wifi 控制模式 0x07 离线轨迹模式
        Byte 1 MOVE模式 uint8 0x00 MOVE P
                                    0x01 MOVE J 0x02 MOVE L 0x03 MOVE C
        Byte 2 运动速度百分比 uint8 0~100 
        
        Byte 3 mit模式 uint8 0x00 位置速度模式
                            0xAD MIT模式
        Byte 4 离线轨迹点停留时间 uint8 0~255 单位 s
        '''
        tx_can=Message()
        motion_ctrl_1 = ArmMsgMotionCtrl_2(ctrl_mode, move_mode, move_spd_rate_ctrl)
        # print(motion_ctrl_1)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrl_2, arm_motion_ctrl_2=motion_ctrl_1)
        self.parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def EndPoseCtrl(self,X,Y,Z,RX,RY,RZ):
        self.__CartesianCtrl_XY(X,Y)
        self.__CartesianCtrl_ZRX(Z,RX)
        self.__CartesianCtrl_RYRZ(RY,RZ)

    def __CartesianCtrl_XY(self, X, Y):
        tx_can=Message()
        cartesian_1 = ArmMsgMotionCtrlCartesian(X_axis=X, Y_axis=Y)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrlCartesian_1, arm_motion_ctrl_cartesian=cartesian_1)
        self.parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def __CartesianCtrl_ZRX(self, Z, RX):
        tx_can=Message()
        cartesian_2 = ArmMsgMotionCtrlCartesian(Z_axis=Z, RX_axis=RX)
        # print(cartesian_2)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrlCartesian_2, arm_motion_ctrl_cartesian=cartesian_2)
        self.parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def __CartesianCtrl_RYRZ(self, RY, RZ):
        tx_can=Message()
        cartesian_3 = ArmMsgMotionCtrlCartesian(RY_axis=RY, RZ_axis=RZ)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrlCartesian_3, arm_motion_ctrl_cartesian=cartesian_3)
        self.parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def JointCtrl(self, 
                  joint_1:int, 
                  joint_2:int,
                  joint_3:int,
                  joint_4:int,
                  joint_5:int,
                  joint_6:int):
        """机械臂关节控制

        Args:
            joint_1 (float): 关节1角度
            joint_2 (float): 关节2角度
            joint_3 (float): 关节3角度
            joint_4 (float): 关节4角度
            joint_5 (float): 关节5角度
            joint_6 (float): 关节6角度
        """
        self.__JointCtrl_12(joint_1, joint_2)
        self.__JointCtrl_34(joint_3, joint_4)
        self.__JointCtrl_56(joint_5, joint_6)
    
    def __JointCtrl_12(self, joint_1, joint_2):
        """机械臂1,2关节控制

        私有函数

        Args:
            joint_1 (_type_): 关节1角度
            joint_2 (_type_): 关节2角度
        """
        tx_can=Message()
        joint_ctrl = ArmMsgJointCtrl(joint_1=joint_1, joint_2=joint_2)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgJointCtrl_12, arm_joint_ctrl=joint_ctrl)
        self.parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def __JointCtrl_34(self, joint_3, joint_4):
        """机械臂3,4关节控制
        
        私有函数

        Args:
            joint_3 (_type_): 关节3角度
            joint_4 (_type_): 关节4角度
        """
        tx_can=Message()
        joint_ctrl = ArmMsgJointCtrl(joint_3=joint_3, joint_4=joint_4)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgJointCtrl_34, arm_joint_ctrl=joint_ctrl)
        self.parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def __JointCtrl_56(self, joint_5, joint_6):
        """机械臂5,6关节控制
        
        私有函数

        Args:
            joint_5 (_type_): 关节5角度
            joint_6 (_type_): 关节6角度
        """
        tx_can=Message()
        joint_ctrl = ArmMsgJointCtrl(joint_5=joint_5, joint_6=joint_6)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgJointCtrl_56, arm_joint_ctrl=joint_ctrl)
        self.parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def GripperCtrl(self, gripper_angle:int, gripper_effort:int, gripper_code:int, set_zero:int):
        """夹爪控制

        Args:
            gripper_angle (int): 夹爪角度
            gripper_effort (int): 夹爪力矩
            gripper_code (int): 夹爪使能/失能/清除错误
            set_zero:(int): 设定当前位置为0点
        """
        tx_can=Message()
        gripper_ctrl = ArmMsgGripperCtrl(gripper_angle, gripper_effort, gripper_code, set_zero)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgGripperCtrl, arm_gripper_ctrl=gripper_ctrl)
        self.parser.EncodeMessage(msg, tx_can)
        # print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def MasterSlaveConfig(self, linkage_config:int, feedback_offset:int, ctrl_offset:int, linkage_offset:int):
        """随动主从模式设置指令

        0x470
        
        Args:
            linkage_config ([0, 250, 252]): 联动设置指令
            feedback_offset ([0, 16, 32]): 反馈指令偏移值
            ctrl_offset ([0, 16, 32]): 控制指令偏移值
            linkage_offset ([0, 16, 32]): 联动模式控制目标地址偏移值
        """
        tx_can=Message()
        ms_config = ArmMsgMasterSlaveModeConfig(linkage_config, feedback_offset, ctrl_offset, linkage_offset)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMasterSlaveModeConfig, arm_ms_config=ms_config)
        self.parser.EncodeMessage(msg, tx_can)
        # print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def DisableArm(self, motor_num=0xFF, enable_flag=1):
        """失能电机
        0x471
        """
        tx_can=Message()
        enable = ArmMsgMotorEnableDisableConfig(motor_num, enable_flag)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotorEnableDisableConfig, arm_motor_enable=enable)
        self.parser.EncodeMessage(msg, tx_can)
        # print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def EnableArm(self, motor_num=0xFF, enable_flag=2):
        """使能电机
        0x471
        """
        tx_can=Message()
        disable = ArmMsgMotorEnableDisableConfig(motor_num, enable_flag)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotorEnableDisableConfig, arm_motor_enable=disable)
        self.parser.EncodeMessage(msg, tx_can)
        # print(hex(tx_can.arbitration_id), tx_can.data)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def SearchMotorMaxAngleSpdAccLimit(self, motor_num, search_content):
        '''
        查询电机角度/最大速度/最大加速度限制指令

        对应反馈当前电机限制角度/最大速度
        
        0x472
        '''
        tx_can=Message()
        search_motor = ArmMsgSearchMotorMaxAngleSpdAccLimit(motor_num, search_content)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgSearchMotorMaxAngleSpdAccLimit, arm_search_motor_max_angle_spd_acc_limit=search_motor)
        self.parser.EncodeMessage(msg, tx_can)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def MotorAngleLimitMaxSpdSet(self, motor_num, max_angle_limit, min_angle_limit, max_jonit_spd):
        '''
        电机角度限制/最大速度设置指令
        0x474
        '''
        tx_can=Message()
        motor_set = ArmMsgMotorAngleLimitMaxSpdSet(motor_num, max_angle_limit, min_angle_limit, max_jonit_spd)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotorAngleLimitMaxSpdSet, arm_motor_angle_limit_max_spd_set=motor_set)
        self.parser.EncodeMessage(msg, tx_can)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def JointConfig(self, 
                    joint_num:Literal[1, 2, 3, 4, 5, 6, 7]=7,
                    set_zero:Literal[0x00, 0xAE]=0,
                    acc_param_is_effective:Literal[0x00, 0xAE]=0,
                    set_acc:int=0,
                    clear_err:Literal[0x00, 0xAE]=0):
        '''
        关节设置
        '''
        tx_can=Message()
        joint_config = ArmMsgJointConfig(joint_num, set_zero,acc_param_is_effective,set_acc,clear_err)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgJointConfig,arm_joint_config=joint_config)
        self.parser.EncodeMessage(msg, tx_can)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def SetInstructionResponse(self, instruction_index, zero_config_success_flag):
        '''
        设置指令应答
        '''
        tx_can=Message()
        set_resp = ArmMsgInstructionResponseConfig(instruction_index, zero_config_success_flag)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgInstructionResponseConfig, arm_set_instruction_response=set_resp)
        self.parser.EncodeMessage(msg, tx_can)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def ArmParamEnquiryAndConfig(self, param_enquiry, param_setting, data_feedback_0x48x, end_load_param_setting_effective, set_end_load):
        '''
        机械臂参数查
        询与设置指令

        0x477

        param_enquiry Byte 0 = 0x01 ->0x478

        param_enquiry Byte 0 = 0x02 ->0x47B
        '''
        tx_can=Message()
        search_set_arm_param = ArmMsgParamEnquiryAndConfig(param_enquiry, 
                                                           param_setting, 
                                                           data_feedback_0x48x, 
                                                           end_load_param_setting_effective,
                                                           set_end_load)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgParamEnquiryAndConfig, arm_param_enquiry_and_config=search_set_arm_param)
        self.parser.EncodeMessage(msg, tx_can)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def EndSpdAndAccParamSet(self, end_max_linear_vel, end_max_angular_vel, end_max_linear_acc, end_max_angular_acc):
        '''
        末端速度/加
        速度参数设置
        指令
        '''
        tx_can=Message()
        end_set = ArmMsgEndVelAccParamConfig(end_max_linear_vel, 
                                            end_max_angular_vel, 
                                            end_max_linear_acc, 
                                            end_max_angular_acc,)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgEndVelAccParamConfig, arm_end_vel_acc_param_config=end_set)
        self.parser.EncodeMessage(msg, tx_can)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def CrashProtectionConfig(self, 
                              jonit_1_protection_level, 
                              jonit_2_protection_level, 
                              jonit_3_protection_level, 
                              jonit_4_protection_level,
                              jonit_5_protection_level,
                              jonit_6_protection_level):
        '''
        碰撞防护等级
        设置指令
        '''
        tx_can=Message()
        crash_config = ArmMsgCrashProtectionRatingConfig(jonit_1_protection_level, 
                                                        jonit_2_protection_level, 
                                                        jonit_3_protection_level, 
                                                        jonit_4_protection_level,
                                                        jonit_5_protection_level,
                                                        jonit_6_protection_level)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgCrashProtectionRatingConfig, arm_crash_protection_rating_config=crash_config)
        self.parser.EncodeMessage(msg, tx_can)
        self.arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

