#!/usr/bin/env python3
# -*-coding:utf8-*-

import time
import can
from can.message import Message
from typing import (
    Optional,
    Type
)
from typing_extensions import (
    Literal,
)
from queue import Queue
import threading
import math
from ..hardware_port.can_encapsulation import C_STD_CAN
from ..protocol.protocol_v1 import C_PiperParserBase, C_PiperParserV1
from ..piper_msgs.msg_v1 import *
from ..kinematics import *
from ..monitor import *
from ..piper_param import *
from ..version import PiperSDKVersion
from .interface_version import InterfaceVersion

class C_PiperInterface():
    '''
    Piper interface class
    
    Args:
        can_name(str): can port name
        judge_flag(bool): Determines if the CAN port is functioning correctly.
                        When using a PCIe-to-CAN module, set to false.
        can_auto_init(bool): Determines if the CAN port is automatically initialized.
        dh_is_offset([0,1] -> default 0): Does the j1-j2 offset by 2° in the DH parameters? 
                    0 -> No offset
                    1 -> Offset applied
    '''
    class ArmStatus():
        '''
        机械臂状态二次封装类,增加时间戳
        '''
        '''
        Piper Status Secondary Encapsulation Class, Add Timestamp
        '''
        def __init__(self):
            self.time_stamp: float = 0
            self.Hz: float = 0
            self.arm_status = ArmMsgStatus()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.arm_status}\n")

    class ArmEndPose():
        '''
        机械臂末端姿态二次封装类,增加时间戳
        '''
        '''
        Secondary Encapsulation Class for Robotic Arm End-Effector Pose, Add Timestamp
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.end_pose=ArmMsgEndPoseFeedBack()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.end_pose}\n")
    
    class ArmJoint():
        '''
        机械臂关节角度和夹爪二次封装类,将夹爪和关节角度信息放在一起,增加时间戳
        '''
        '''
        Secondary Encapsulation Class for Robotic Arm Joint Angles and Gripper, 
        Combine Gripper and Joint Angle Information Together, Add Timestamp
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.joint_state=ArmMsgJointFeedBack()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.joint_state}\n")
    
    class ArmGripper():
        '''
        机械臂关节角度和夹爪二次封装类,将夹爪和关节角度信息放在一起,增加时间戳
        '''
        '''
        Secondary Encapsulation Class for Robotic Arm Joint Angles and Gripper, 
        Combining Gripper and Joint Angle Information Together, with Timestamp
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.gripper_state=ArmMsgGripperFeedBack()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.gripper_state}\n")
    
    class ArmMotorDriverInfoHighSpd():
        '''
        机械臂电机驱动高速反馈信息
        '''
        '''
        Robotic Arm Motor Driver High-Speed Feedback Information
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.motor_1=ArmHighSpdFeedback()
            self.motor_2=ArmHighSpdFeedback()
            self.motor_3=ArmHighSpdFeedback()
            self.motor_4=ArmHighSpdFeedback()
            self.motor_5=ArmHighSpdFeedback()
            self.motor_6=ArmHighSpdFeedback()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
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
        '''
        Robotic Arm Motor Driver Low-Speed Feedback Information
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.motor_1=ArmLowSpdFeedback()
            self.motor_2=ArmLowSpdFeedback()
            self.motor_3=ArmLowSpdFeedback()
            self.motor_4=ArmLowSpdFeedback()
            self.motor_5=ArmLowSpdFeedback()
            self.motor_6=ArmLowSpdFeedback()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
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
        '''
        Current Motor Limit Angle/Maximum Speed
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.current_motor_angle_limit_max_vel=ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"current_motor_angle_limit_max_vel:{self.current_motor_angle_limit_max_vel}\n")

    class CurrentEndVelAndAccParam():
        '''
        当前末端速度/加速度参数
        0x477 Byte 0 = 0x01 -> 0x478
        '''
        '''
        Current End-Effector Velocity/Acceleration Parameters
        0x477 Byte 0 = 0x01 -> 0x478
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.current_end_vel_acc_param=ArmMsgFeedbackCurrentEndVelAccParam()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"current_end_vel_acc_param:{self.current_end_vel_acc_param}\n")
    
    class CrashProtectionLevelFeedback():
        '''
        碰撞防护等级设置反馈指令
        0x477 Byte 0 = 0x02 -> 0x47B
        '''
        '''
        Collision Protection Level Setting Feedback Command
        0x477 Byte 0 = 0x02 -> 0x47B
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.crash_protection_level_feedback=ArmMsgCrashProtectionRatingFeedback()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"crash_protection_level_feedback:{self.crash_protection_level_feedback}\n")
    
    class CurrentMotorMaxAccLimit():
        '''
        反馈当前电机最大加速度限制
        '''
        '''
        Feedback Current Motor Maximum Acceleration Limit
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.current_motor_max_acc_limit=ArmMsgFeedbackCurrentMotorMaxAccLimit()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"current_motor_max_acc_limit:{self.current_motor_max_acc_limit}\n")

    class ArmJointCtrl():
        '''
        机械臂关节角度和夹爪二次封装类,将夹爪和关节角度信息放在一起,增加时间戳
        这个是主臂发送的消息，用来读取发送给从臂的目标值
        '''
        '''
        Secondary Encapsulation Class for Robotic Arm Joint Angles and Gripper, Combining Gripper and Joint Angle Information, Adding Timestamp
        This is the message sent by the main arm to read the target values sent to the slave arm.
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.joint_ctrl=ArmMsgJointCtrl()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.joint_ctrl}\n")
    
    class ArmGripperCtrl():
        '''
        机械臂关节角度和夹爪二次封装类,将夹爪和关节角度信息放在一起,增加时间戳
        这个是主臂发送的消息，用来读取发送给从臂的目标值
        '''
        '''
        Secondary Encapsulation Class for Robotic Arm Joint Angles and Gripper, Combining Gripper and Joint Angle Information, Adding Timestamp
        This is a message sent by the main arm to read the target values sent to the slave arm.
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.gripper_ctrl=ArmMsgGripperCtrl()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.gripper_ctrl}\n")
    
    class ArmCtrlCode_151():
        '''
        机械臂发送控制指令0x151的消息接收,由主臂发送
        '''
        '''
        The control command message 0x151 is sent by the main arm for reception
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.ctrl_151=ArmMsgMotionCtrl_2()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.ctrl_151}\n")
    
    class AllCurrentMotorMaxAccLimit():
        '''
        全部电机最大加速度限制,带时间戳
        '''
        '''
        The maximum acceleration limit for all motors, with a timestamp.
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.all_motor_max_acc_limit=ArmMsgFeedbackAllCurrentMotorMaxAccLimit()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"{self.all_motor_max_acc_limit}\n")
    
    class AllCurrentMotorAngleLimitMaxSpd():
        '''
        所有电机限制角度/最大速度,带时间戳
        '''
        '''
        The angular/maximum speed limits for all motors, with a timestamp.
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.all_motor_angle_limit_max_spd=ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"{self.all_motor_angle_limit_max_spd}\n")
    
    class ArmTimeStamp():
        '''
        机械臂时间戳
        '''
        '''
        piper msgs timestamp
        '''
        def __init__(self):
            self.time_stamp_arm_status:float=0
            self.time_stamp_end_pose_1:float=0
            self.time_stamp_end_pose_2:float=0
            self.time_stamp_end_pose_3:float=0
            self.time_stamp_joint_12:float=0
            self.time_stamp_joint_34:float=0
            self.time_stamp_joint_56:float=0
            self.time_stamp_motor_high_spd_1:float=0
            self.time_stamp_motor_high_spd_2:float=0
            self.time_stamp_motor_high_spd_3:float=0
            self.time_stamp_motor_high_spd_4:float=0
            self.time_stamp_motor_high_spd_5:float=0
            self.time_stamp_motor_high_spd_6:float=0
            self.time_stamp_motor_low_spd_1:float=0
            self.time_stamp_motor_low_spd_2:float=0
            self.time_stamp_motor_low_spd_3:float=0
            self.time_stamp_motor_low_spd_4:float=0
            self.time_stamp_motor_low_spd_5:float=0
            self.time_stamp_motor_low_spd_6:float=0
            self.time_stamp_joint_ctrl_12:float=0
            self.time_stamp_joint_ctrl_34:float=0
            self.time_stamp_joint_ctrl_56:float=0
            self.time_stamp_motor_max_acc_limit_1=0
            self.time_stamp_motor_max_acc_limit_2=0
            self.time_stamp_motor_max_acc_limit_3=0
            self.time_stamp_motor_max_acc_limit_4=0
            self.time_stamp_motor_max_acc_limit_5=0
            self.time_stamp_motor_max_acc_limit_6=0
            self.time_stamp_motor_angle_limit_max_spd_1=0
            self.time_stamp_motor_angle_limit_max_spd_2=0
            self.time_stamp_motor_angle_limit_max_spd_3=0
            self.time_stamp_motor_angle_limit_max_spd_4=0
            self.time_stamp_motor_angle_limit_max_spd_5=0
            self.time_stamp_motor_angle_limit_max_spd_6=0
    
    _instances = {}  # 存储不同参数的实例

    def __new__(cls, 
                can_name:str="can0", 
                judge_flag=True,
                can_auto_init=True,
                dh_is_offset: int = 0,
                start_sdk_joint_limit: bool = True,
                start_sdk_gripper_limit: bool = True):
        """
        实现单例模式：
        - 相同 can_name & can_auto_init 参数，只会创建一个实例
        - 不同参数，允许创建新的实例
        """
        key = (can_name)  # 生成唯一 Key
        if key not in cls._instances:
            instance = super().__new__(cls)  # 创建新实例
            instance._initialized = False  # 确保 init 只执行一次
            cls._instances[key] = instance  # 存入缓存
        return cls._instances[key]

    def __init__(self,
                 can_name:str="can0",
                 judge_flag=True,
                 can_auto_init=True,
                 dh_is_offset: int = 0,
                 start_sdk_joint_limit: bool = True, 
                 start_sdk_gripper_limit: bool = True) -> None:
        if getattr(self, "_initialized", False):  
            return  # 避免重复初始化
        self.__can_channel_name:str
        if isinstance(can_name, str):
            self.__can_channel_name = can_name
        else:
            raise IndexError("C_PiperBase input can name is not str type")
        self.__can_judge_flag = judge_flag
        self.__can_auto_init = can_auto_init
        self.__arm_can=C_STD_CAN(can_name, "socketcan", 1000000, judge_flag, can_auto_init, self.ParseCANFrame)
        self.__dh_is_offset = dh_is_offset
        self.__piper_fk = C_PiperForwardKinematics(self.__dh_is_offset)
        self.__start_sdk_joint_limit = start_sdk_joint_limit
        self.__start_sdk_gripper_limit = start_sdk_gripper_limit
        self.__piper_param_mag = C_PiperParamManager()
        # protocol
        self.__parser: Type[C_PiperParserBase] = C_PiperParserV1()
        # thread
        self.__read_can_stop_event = threading.Event()  # 控制 ReadCan 线程
        self.__can_monitor_stop_event = threading.Event()  # 控制 CanMonitor 线程
        self.__lock = threading.Lock()  # 保护线程安全
        self.__can_deal_th = None
        self.__can_monitor_th = None
        self.__connected = False  # 连接状态
        # FPS cal
        self.__fps_counter = C_FPSCounter()
        self.__fps_counter.add_variable("CanMonitor")
        self.__q_can_fps = Queue(maxsize=20)
        self.__is_ok_mtx = threading.Lock()
        self.__is_ok = True
        self.__fps_counter.add_variable("ArmStatus")
        self.__fps_counter.add_variable("ArmEndPose_XY")
        self.__fps_counter.add_variable("ArmEndPose_ZRX")
        self.__fps_counter.add_variable("ArmEndPose_RYRZ")
        self.__fps_counter.add_variable("ArmJoint_12")
        self.__fps_counter.add_variable("ArmJoint_34")
        self.__fps_counter.add_variable("ArmJoint_56")
        self.__fps_counter.add_variable("ArmGripper")
        self.__fps_counter.add_variable("ArmMotorDriverInfoHighSpd_1")
        self.__fps_counter.add_variable("ArmMotorDriverInfoHighSpd_2")
        self.__fps_counter.add_variable("ArmMotorDriverInfoHighSpd_3")
        self.__fps_counter.add_variable("ArmMotorDriverInfoHighSpd_4")
        self.__fps_counter.add_variable("ArmMotorDriverInfoHighSpd_5")
        self.__fps_counter.add_variable("ArmMotorDriverInfoHighSpd_6")
        self.__fps_counter.add_variable("ArmMotorDriverInfoLowSpd_1")
        self.__fps_counter.add_variable("ArmMotorDriverInfoLowSpd_2")
        self.__fps_counter.add_variable("ArmMotorDriverInfoLowSpd_3")
        self.__fps_counter.add_variable("ArmMotorDriverInfoLowSpd_4")
        self.__fps_counter.add_variable("ArmMotorDriverInfoLowSpd_5")
        self.__fps_counter.add_variable("ArmMotorDriverInfoLowSpd_6")
        self.__fps_counter.add_variable("ArmJointCtrl_12")
        self.__fps_counter.add_variable("ArmJointCtrl_34")
        self.__fps_counter.add_variable("ArmJointCtrl_56")
        self.__fps_counter.add_variable("ArmGripperCtrl")
        self.__fps_counter.add_variable("ArmCtrlCode_151")
        # 时间戳
        self.__arm_time_stamp = self.ArmTimeStamp()#时间戳
        # 机械臂反馈消息正解，包含每个关节的正解
        self.__piper_feedback_fk_mtx = threading.Lock()
        self.__link_feedback_fk = [[0.0] * 6 for _ in range(6)]
        # 机械臂控制消息正解，包含每个关节的正解
        self.__piper_ctrl_fk_mtx = threading.Lock()
        self.__link_ctrl_fk = [[0.0] * 6 for _ in range(6)]
        # 固件版本
        self.__firmware_data_mtx = threading.Lock()
        self.__firmware_data = bytearray()
        # 二次封装数据类型
        self.__arm_status_mtx = threading.Lock()
        self.__arm_status = self.ArmStatus()

        self.__arm_end_pose_mtx = threading.Lock()
        self.__arm_end_pose = self.ArmEndPose()

        self.__arm_joint_msgs_mtx = threading.Lock()
        self.__arm_joint_msgs = self.ArmJoint()

        self.__arm_gripper_msgs_mtx = threading.Lock()
        self.__arm_gripper_msgs = self.ArmGripper()

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

        self.__arm_joint_ctrl_msgs_mtx = threading.Lock()
        self.__arm_joint_ctrl_msgs = self.ArmJointCtrl()
        
        self.__arm_gripper_ctrl_msgs_mtx = threading.Lock()
        self.__arm_gripper_ctrl_msgs = self.ArmGripperCtrl()

        self.__arm_ctrl_code_151_mtx = threading.Lock()
        self.__arm_ctrl_code_151 = self.ArmCtrlCode_151()
        
        self.__arm_all_motor_max_acc_limit_mtx = threading.Lock()
        self.__arm_all_motor_max_acc_limit = self.AllCurrentMotorMaxAccLimit()
        
        self.__arm_all_motor_angle_limit_max_spd_mtx = threading.Lock()
        self.__arm_all_motor_angle_limit_max_spd = self.AllCurrentMotorAngleLimitMaxSpd()
        self._initialized = True  # 标记已初始化
    
    @classmethod
    def get_instance(cls, can_name="can0", judge_flag=True, can_auto_init=True):
        """获取实例，简化调用"""
        return cls(can_name, judge_flag, can_auto_init)
    
    def ConnectPort(self, 
                    can_init :bool = False, 
                    piper_init :bool = True, 
                    start_thread :bool = True):
        '''
        Starts a thread to process data from the connected CAN port.
        
        Args:
            can_init(bool): can port init flag, Behind you using DisconnectPort(), you should set it True.
            piper_init(bool): Execute the robot arm initialization function
            start_thread(bool): Start the reading thread
        '''
        if(can_init or not self.__connected):
            self.__arm_can.Init()
        # 检查线程是否开启
        with self.__lock:
            if self.__connected:
                return
            self.__connected = True
            self.__read_can_stop_event.clear()
            self.__can_monitor_stop_event.clear()  # 允许线程运行
        # 读取can数据线程
        def ReadCan():
            while not self.__read_can_stop_event.is_set():
                try:
                    self.__arm_can.ReadCanMessage()
                except can.CanOperationError:
                    print("[ERROR] CAN 端口关闭，停止 ReadCan 线程")
                    break
                except Exception as e:
                    print(f"[ERROR] ReadCan() 发生异常: {e}")
                    break
        def CanMonitor():
            while not self.__can_monitor_stop_event.is_set():
                try:
                    self.__CanMonitor()
                except Exception as e:
                    print(f"[ERROR] CanMonitor() 发生异常: {e}")
                    break
                self.__can_monitor_stop_event.wait(0.01)
        try:
            if start_thread:
                if not self.__can_deal_th or not self.__can_deal_th.is_alive():
                    self.__can_deal_th = threading.Thread(target=ReadCan, daemon=True)
                    self.__can_deal_th.start()
                if not self.__can_monitor_th or not self.__can_monitor_th.is_alive():
                    self.__can_monitor_th = threading.Thread(target=CanMonitor, daemon=True)
                    self.__can_monitor_th.start()
                self.__fps_counter.start()
            if piper_init:
                self.PiperInit()
        except Exception as e:
            print(f"[ERROR] 线程启动失败: {e}")
            self.__connected = False  # 回滚状态
            self.__read_can_stop_event.set()
            self.__can_monitor_stop_event.set()  # 确保线程不会意外运行
    
    def DisconnectPort(self, thread_timeout=0.1):
        '''
        断开端口但不阻塞主线程
        '''
        with self.__lock:
            if not self.__connected:
                return
            self.__connected = False
            self.__read_can_stop_event.set()

        if hasattr(self, 'can_deal_th') and self.__can_deal_th.is_alive():
            self.__can_deal_th.join(timeout=thread_timeout)  # 加入超时，避免无限阻塞
            if self.__can_deal_th.is_alive():
                print("[WARN] ReadCan 线程未能在超时时间内退出！")

        # if hasattr(self, 'can_monitor_th') and self.__can_monitor_th.is_alive():
        #     self.__can_monitor_th.join(timeout=thread_timeout)
        #     if self.__can_monitor_th.is_alive():
        #         print("[WARN] CanMonitor 线程未能在超时时间内退出！")

        try:
            self.__arm_can.Close()  # 关闭 CAN 端口
            print("[INFO] CAN 端口已断开")
        except Exception as e:
            print(f"[ERROR] 关闭 CAN 端口时发生异常: {e}")
    
    def PiperInit(self):
        '''
        发送查询关节电机最大角度速度指令
        发送查询关节电机最大加速度限制指令
        发送查询机械臂固件指令
        '''
        self.SearchAllMotorMaxAngleSpd()
        self.SearchAllMotorMaxAccLimit()
        self.SearchPiperFirmwareVersion()

    def ParseCANFrame(self, rx_message: Optional[can.Message]):
        '''can协议解析函数

        Args:
            rx_message (Optional[can.Message]): can接收的原始数据
        '''
        '''CAN protocol parsing function.

        Args:
            rx_message (Optional[can.Message]): The raw data received via CAN.
        '''
        msg = PiperMessage()
        receive_flag = self.__parser.DecodeMessage(rx_message, msg)
        if(receive_flag):
            self.__fps_counter.increment("CanMonitor")
            self.__UpdateArmStatus(msg)
            self.__UpdateArmEndPoseState(msg)
            self.__UpdateArmJointState(msg)
            self.__UpdateArmGripperState(msg)
            self.__UpdateDriverInfoHighSpdFeedback(msg)
            self.__UpdateDriverInfoLowSpdFeedback(msg)

            self.__UpdateCurrentEndVelAndAccParam(msg)
            self.__UpdateCrashProtectionLevelFeedback(msg)
            self.__UpdateCurrentMotorAngleLimitMaxVel(msg)
            self.__UpdateCurrentMotorMaxAccLimit(msg)
            self.__UpdateAllCurrentMotorAngleLimitMaxVel(msg)
            self.__UpdateAllCurrentMotorMaxAccLimit(msg)
            # 更新主臂发送消息
            self.__UpdateArmJointCtrl(msg)
            self.__UpdateArmGripperCtrl(msg)
            self.__UpdateArmCtrlCode151(msg)
            self.__UpdatePiperFirmware(msg)
            self.__UpdatePiperFeedbackFK()
            self.__UpdatePiperCtrlFK()
    
    # def JudgeExsitedArm(self, can_id:int):
    #     '''判断当前can socket是否有指定的机械臂设备,通过can id筛选
    #     Args:
    #         can_id (int): 输入can 🆔
    #     '''
    #     '''Checks if the current CAN socket contains the specified robotic arm device by filtering through the CAN ID.
    #     Args:
    #         can_id (int): The input CAN ID
    #     '''
    #     pass
    # 获取反馈值------------------------------------------------------------------------------------------------------
    def GetCurrentInterfaceVersion(self):
        return InterfaceVersion.INTERFACE_V1
    
    def GetCurrentSDKVersion(self):
        '''
        return piper_sdk current version
        '''
        return PiperSDKVersion.PIPER_SDK_CURRENT_VERSION
    
    def GetCurrentProtocolVersion(self):
        '''
        return piper_sdk current prptocol version
        '''
        return self.__parser.GetParserProtocolVersion()
    
    def GetCanFps(self):
        '''
        获取机械臂can模块帧率
        '''
        '''
        Get the frame rate of the robotic arm CAN module
        '''
        return self.__fps_counter.get_real_time_fps("CanMonitor")
    
    def GetArmStatus(self):
        '''获取机械臂状态,0x2A1,详见 ArmMsgStatus
        '''
        '''Retrieves the current status of the robotic arm.
        For detailed information, refer to the `ArmMsgStatus` class.
        '''
        with self.__arm_status_mtx:
            self.__arm_status.Hz = self.__fps_counter.get_real_time_fps("ArmStatus")
            return self.__arm_status

    def GetArmEndPoseMsgs(self):
        '''获取机械臂末端位姿消息
        
        X,Y,Z单位0.001mm
        RX,RY,RZ单位0.001度
        '''
        '''Retrieves the end effector pose message of the robotic arm.

        This includes the following information:
            X, Y, Z position (in 0.001 mm)
            RX, RY, RZ orientation (in 0.001 degrees)
        '''
        with self.__arm_end_pose_mtx:
            self.__arm_end_pose.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_real_time_fps('ArmEndPose_XY'),
                                                                  self.__fps_counter.get_real_time_fps('ArmEndPose_ZRX'),
                                                                  self.__fps_counter.get_real_time_fps('ArmEndPose_RYRZ'))
            return self.__arm_end_pose

    def GetArmJointMsgs(self):
        '''获取机械臂关节消息,单位0.001度
        '''
        '''Retrieves the joint status message of the robotic arm.(in 0.001 degrees)
        '''
        with self.__arm_joint_msgs_mtx:
            self.__arm_joint_msgs.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_real_time_fps('ArmJoint_12'),
                                                                    self.__fps_counter.get_real_time_fps('ArmJoint_34'),
                                                                    self.__fps_counter.get_real_time_fps('ArmJoint_56'))
            return self.__arm_joint_msgs
    
    def GetFK(self, mode:Literal["feedback", "control"]="feedback"):
        '''获取机械臂每个关节的正向运动学解。XYZ 的单位为毫米 (mm),RX、RY、RZ 的单位为度 
        返回一个包含 6 个浮点数的列表，表示 1-6 号关节相对于 base_link 的位姿

        Args:
            mode (str): "feedback" 获取反馈数据，"control" 获取控制数据  

        Returns:
            list: 一个包含 6 个浮点数的列表，表示 1-6 号关节的位姿
        '''
        '''Obtain the forward kinematics solution for each joint of the robotic arm. The units for XYZ are in millimeters (mm), and for RX, RY, RZ are in degrees.
        Returns a list containing 6 floating-point numbers, representing the pose of joints 1-6 relative to the base_link.

        Args:
            mode (str): "feedback" to retrieve feedback data, "control" to retrieve control data  

        Returns:
            list: A list containing 6 floating-point numbers, representing the pose of joints 1-6
        '''

        if mode == "feedback":
            with self.__piper_feedback_fk_mtx:
                return self.__link_feedback_fk
        elif mode == "control":
            with self.__piper_ctrl_fk_mtx:
                return self.__link_ctrl_fk
        else:
            raise ValueError("Invalid mode! Use 'feedback' or 'control'.")
    
    def GetArmGripperMsgs(self):
        '''获取机械臂夹爪消息
        '''
        '''Retrieves the gripper status message of the robotic arm.
        '''
        with self.__arm_gripper_msgs_mtx:
            self.__arm_gripper_msgs.Hz = self.__fps_counter.get_real_time_fps('ArmGripper')
            return self.__arm_gripper_msgs
    
    def GetArmHighSpdInfoMsgs(self):
        '''获取机械臂高速反馈消息
        
        包括转速,电流,位置消息
        '''
        '''Retrieves the high-speed feedback message of the robotic arm.

        This includes the following information:
            Speed (rotation speed)
            Current
            Position
        '''
        with self.__arm_motor_info_high_spd_mtx:
            self.__arm_motor_info_high_spd.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoHighSpd_1'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoHighSpd_2'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoHighSpd_3'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoHighSpd_4'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoHighSpd_5'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoHighSpd_6'))
            return self.__arm_motor_info_high_spd
    
    def GetArmLowSpdInfoMsgs(self):
        '''获取机械臂低速反馈消息
        
        包括电压,驱动器温度,电机温度,驱动器状态,母线电流消息
        '''
        '''Retrieves the low-speed feedback message of the robotic arm.

        This includes the following information:
            Voltage
            Driver temperature
            Motor temperature
            Driver status
            Bus current
        '''
        with self.__arm_motor_info_low_spd_mtx:
            self.__arm_motor_info_low_spd.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoLowSpd_1'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoLowSpd_2'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoLowSpd_3'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoLowSpd_4'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoLowSpd_5'),
                                                                            self.__fps_counter.get_real_time_fps('ArmMotorDriverInfoLowSpd_6'))
            return self.__arm_motor_info_low_spd
    
    def GetCurrentMotorAngleLimitMaxVel(self):
        '''获取电机角度限制/最大速度指令
        
        包括最大角度限制,最小角度限制,最大关节速度
        
        为主动发送指令后反馈消息
        
        对应查询电机角度/最大速度/最大加速度限制指令 0x472 Byte 1 = 0x01
        
        ArmParamEnquiryAndConfig(param_enquiry=0x01)
        
        CAN ID:
            0x473
        '''
        '''Retrieves the motor angle limit/maximum speed command.

        This includes the following information:
            Maximum angle limit
            Minimum angle limit
            Maximum joint speed
        This is the feedback message after actively sending a command.
        Corresponds to the query for motor angle/maximum speed/maximum acceleration limit command 0x472,
        with Byte 1 = 0x01

        ArmParamEnquiryAndConfig(param_enquiry=0x01)
        
        CAN ID:
            0x473
        '''
        with self.__feedback_current_motor_angle_limit_max_vel_mtx:
            return self.__feedback_current_motor_angle_limit_max_vel
    
    def GetCurrentEndVelAndAccParam(self):
        '''获取末端速度/加速度参数
        
        包括末端线速度,末端角速度,末端线加速度,末端角加速度
        
        为主动发送指令后反馈消息

        对应机械臂参数查询与设置指令 0x477 Byte 0 = 0x01
        
        ArmParamEnquiryAndConfig(param_enquiry=0x01)

        CAN ID:
            0x478
        '''
        '''Retrieves the end effector velocity and acceleration parameters.

        This includes the following information:
            End effector linear velocity
            End effector angular velocity
            End effector linear acceleration
            End effector angular acceleration
        This is the feedback message after actively sending a command.
        Corresponds to the robotic arm parameter query and setting command 0x477,
        with Byte 0 = 0x01
        
        ArmParamEnquiryAndConfig(param_enquiry=0x01)

        CAN ID:
            0x478
        '''
        with self.__feedback_current_end_vel_acc_param_mtx:
            return self.__feedback_current_end_vel_acc_param
    
    def GetCrashProtectionLevelFeedback(self):
        '''获取碰撞防护等级反馈
        
        获取1-6关节碰撞等级,数值0-8,0代表不检测碰撞,1-8检测等级逐级递增(代表检测阈值逐级增加),
        
        为主动发送指令后反馈消息,
        
        对应机械臂参数查询与设置指令 0x477 Byte 0 = 0x02

        ArmParamEnquiryAndConfig(param_enquiry=0x02)
        
        CAN ID:
            0x47B
        '''
        '''Retrieves the collision protection level feedback.

        This includes the following information:
            Collision level for joints 1-6 (values range from 0 to 8).
                0: No collision detection.
                1-8: Detection levels, where the threshold for collision detection increases progressively.
        This is the feedback message after actively sending a command.
        Corresponds to the robotic arm parameter query and setting command 0x477,
        with Byte 0 = 0x02
        
        ArmParamEnquiryAndConfig(param_enquiry=0x02)
        
        CAN ID:
            0x47B
        '''
        with self.__feedback_crash_protection_level_mtx:
            return self.__feedback_crash_protection_level

    def GetCurrentMotorMaxAccLimit(self):
        '''获取当前电机最大加速度限制
        
        当前电机序号,当前电机的最大关节加速度
        '''
        '''Retrieves the current motor's maximum acceleration limit.

        This includes the following information:
            Current motor number
            The maximum joint acceleration of the current motor
        '''
        with self.__feedback_current_motor_max_acc_limit_mtx:
            return self.__feedback_current_motor_max_acc_limit
    
    def GetArmJointCtrl(self):
        '''获取0x155,0x156,0x157控制指令,是关节控制指令,单位0.001度
        '''
        '''Retrieves the 0x155, 0x156, and 0x157 control commands, which are joint control commands.

        The units for these commands are 0.001 degrees.
        '''
        with self.__arm_joint_ctrl_msgs_mtx:
            self.__arm_joint_ctrl_msgs.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_real_time_fps('ArmJointCtrl_12'),
                                                                        self.__fps_counter.get_real_time_fps('ArmJointCtrl_34'),
                                                                        self.__fps_counter.get_real_time_fps('ArmJointCtrl_56'))
            return self.__arm_joint_ctrl_msgs
    
    def GetArmGripperCtrl(self):
        '''获取夹爪控制消息,0x159指令
        
        self.gripper_ctrl
        
        Args:
            grippers_angle: int32, 单位 0.001°, 夹爪角度,以整数表示。
            grippers_effort: uint16, 单位 0.001N/m, 夹爪扭矩,以整数表示。
            status_code: uint8
                0x00失能;
                0x01使能;
                0x02失能清除错误;
                0x03使能清除错误.
            set_zero: uint8, 设定当前位置为0点.
                0x00无效值;
                0xAE设置零点
        '''
        ''' Retrieves the gripper control message using the 0x159 command.

        Args:
            grippers_angle (int): The gripper angle, in 0.001° (integer representation).
            grippers_effort (int): The gripper torque, in 0.001 N/m (integer representation).
            status_code (int): The gripper status code for enabling/disabling/clearing errors.
                0x00: Disabled;
                0x01: Enabled;
                0x03: Enable and clear errors;
                0x02: Disable and clear errors.
            set_zero (int): Set the current position as the zero point.
                0x00: Invalid;
                0xAE: Set zero.
        '''
        with self.__arm_gripper_ctrl_msgs_mtx:
            self.__arm_gripper_ctrl_msgs.Hz = self.__fps_counter.get_real_time_fps("ArmGripperCtrl")
            return self.__arm_gripper_ctrl_msgs
    
    def GetArmCtrlCode151(self):
        '''获取0x151控制指令,机械臂模式控制指令,详看 ArmMsgMotionCtrl_1 类
        '''
        '''Retrieves the 0x151 control command, which is the robotic arm mode control command.

        For detailed information, refer to the `ArmMsgMotionCtrl_1` class.
        '''
        with self.__arm_ctrl_code_151_mtx:
            self.__arm_ctrl_code_151.Hz = self.__fps_counter.get_real_time_fps("ArmCtrlCode_151")
            return self.__arm_ctrl_code_151
    
    def GetAllMotorMaxAccLimit(self):
        '''获取所有电机的最大加速度限制,(m1-m6)
        
        此为应答式消息,意为需要发送请求指令该数据才会有数值
        
        已经在 ConnectPort 中调用了请求指令 self.SearchAllMotorMaxAccLimit()
        '''
        '''Retrieves the maximum acceleration limits for all motors (m1-m6).

        This is a response message, meaning the data will only be available after sending a request command.
        The request command `self.SearchAllMotorMaxAccLimit()` has already been called in the `ConnectPort`.
        '''
        with self.__arm_all_motor_max_acc_limit_mtx:
            return self.__arm_all_motor_max_acc_limit
    
    def GetAllMotorAngleLimitMaxSpd(self):
        '''获取所有电机的最大限制角度/最小限制角度/最大速度,(m1-m6)
        
        此为应答式消息,意为需要发送请求指令该数据才会有数值
        
        已经在 ConnectPort 中调用了请求指令 self.SearchAllMotorMaxAngleSpd()
        '''
        '''Retrieves the maximum limit angle, minimum limit angle, and maximum speed for all motors (m1-m6).

        This is a response message, meaning the data will only be available after sending a request command.
        The request command `self.SearchAllMotorMaxAngleSpd()` has already been called in the `ConnectPort`.
        '''
        with self.__arm_all_motor_angle_limit_max_spd_mtx:
            return self.__arm_all_motor_angle_limit_max_spd
    
    def GetPiperFirmwareVersion(self):
        '''
        获取piper软件固件版本
        
        获取成功 return 对应字符串
        失败 return -0x4AF
        '''
        '''
        Retrieve Piper Software Firmware Version

        Success: Returns the corresponding string.
        Failure: Returns -0x4AF.
        '''
        with self.__firmware_data_mtx:
            # 查找固件版本信息
            version_start = self.__firmware_data.find(b'S-V')
            if version_start == -1:
                return -0x4AF  # 没有找到以 S-V 开头的字符串
            # 固定长度为 8
            version_length = 8
            # 确保不会超出 bytearray 的长度
            version_end = min(version_start + version_length, len(self.__firmware_data))
            # 提取版本信息，截取固定长度的字节数据
            firmware_version = self.__firmware_data[version_start:version_end].decode('utf-8', errors='ignore')
            return firmware_version  # 返回找到的固件版本字符串
    
    def isOk(self):
        '''
        反馈can数据读取线程是否正常
        '''
        '''
        Feedback on whether the CAN data reading thread is functioning normally
        '''
        with self.__is_ok_mtx:
            return self.__is_ok
    # 发送控制值-------------------------------------------------------------------------------------------------------

    # 接收反馈函数------------------------------------------------------------------------------------------------------
    def __CanMonitor(self):
        '''
        can数据帧率检测
        '''
        '''
        CAN data frame rate detection
        '''
        if self.__q_can_fps.full():
            self.__q_can_fps.get()
        self.__q_can_fps.put(self.GetCanFps())
        with self.__is_ok_mtx:
            if self.__q_can_fps.full() and all(x == 0 for x in self.__q_can_fps.queue):
                    self.__is_ok = False
            else:
                self.__is_ok = True
    
    def __CalJointSDKLimit(self, joint_value, joint_num:str):
        if(self.__start_sdk_joint_limit):
            j_min, j_max = self.GetSDKJointLimitParam(joint_num)
            j_min = round(math.degrees(j_min) * 1000)
            j_max = round(math.degrees(j_max) * 1000)
            return max(j_min, min(joint_value, j_max))
        else: return joint_value

    def __CalGripperSDKLimit(self, gripper_val:int):
        if self.__start_sdk_gripper_limit:
            g_min, g_max = self.GetSDKGripperRangeParam()
            g_min = round(g_min *1000 * 1000)
            g_max = round(g_max *1000 * 1000)
            return max(g_min, min(gripper_val, g_max))
        else: return gripper_val

    def __UpdateArmStatus(self, msg:PiperMessage):
        '''更新机械臂状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the robotic arm status.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_status_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgStatusFeedback):
                self.__fps_counter.increment("ArmStatus")
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

    def __UpdateArmEndPoseState(self, msg:PiperMessage):
        '''更新末端位姿状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the end effector pose status.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_end_pose_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgEndPoseFeedback_X_Y):
                self.__fps_counter.increment("ArmEndPose_XY")
                self.__arm_time_stamp.time_stamp_end_pose_1 = time.time_ns()
                self.__arm_end_pose.end_pose.X_axis = msg.arm_end_pose.X_axis
                self.__arm_end_pose.end_pose.Y_axis = msg.arm_end_pose.Y_axis
            elif(msg.type_ == ArmMsgType.PiperMsgEndPoseFeedback_Z_RX):
                self.__fps_counter.increment("ArmEndPose_ZRX")
                self.__arm_time_stamp.time_stamp_end_pose_2 = time.time_ns()
                self.__arm_end_pose.end_pose.Z_axis = msg.arm_end_pose.Z_axis
                self.__arm_end_pose.end_pose.RX_axis = msg.arm_end_pose.RX_axis
            elif(msg.type_ == ArmMsgType.PiperMsgEndPoseFeedback_RY_RZ):
                self.__fps_counter.increment("ArmEndPose_RYRZ")
                self.__arm_time_stamp.time_stamp_end_pose_3 = time.time_ns()
                self.__arm_end_pose.end_pose.RY_axis = msg.arm_end_pose.RY_axis
                self.__arm_end_pose.end_pose.RZ_axis = msg.arm_end_pose.RZ_axis
            self.__arm_end_pose.time_stamp = max(self.__arm_time_stamp.time_stamp_end_pose_1, 
                                                self.__arm_time_stamp.time_stamp_end_pose_2, 
                                                self.__arm_time_stamp.time_stamp_end_pose_3) / 1_000_000_000
            # print(self.__arm_end_pose)
            return self.__arm_end_pose

    def __UpdateArmJointState(self, msg:PiperMessage):
        '''更新关节状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the joint status.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_joint_msgs_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgJointFeedBack_12):
                self.__fps_counter.increment("ArmJoint_12")
                self.__arm_time_stamp.time_stamp_joint_12 = time.time_ns()
                self.__arm_joint_msgs.joint_state.joint_1 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_1, "j1")
                self.__arm_joint_msgs.joint_state.joint_2 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_2, "j2")
            elif(msg.type_ == ArmMsgType.PiperMsgJointFeedBack_34):
                self.__fps_counter.increment("ArmJoint_34")
                self.__arm_time_stamp.time_stamp_joint_34 = time.time_ns()
                self.__arm_joint_msgs.joint_state.joint_3 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_3, "j3")
                self.__arm_joint_msgs.joint_state.joint_4 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_4, "j4")
            elif(msg.type_ == ArmMsgType.PiperMsgJointFeedBack_56):
                self.__fps_counter.increment("ArmJoint_56")
                self.__arm_time_stamp.time_stamp_joint_56 = time.time_ns()
                self.__arm_joint_msgs.joint_state.joint_5 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_5, "j5")
                self.__arm_joint_msgs.joint_state.joint_6 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_6, "j6")
            else:
                pass
            # 更新时间戳，取筛选ID的最新一个
            self.__arm_joint_msgs.time_stamp = max(self.__arm_time_stamp.time_stamp_joint_12, 
                                                        self.__arm_time_stamp.time_stamp_joint_34, 
                                                        self.__arm_time_stamp.time_stamp_joint_56)/ 1_000_000_000
            # print(self.__arm_joint_msgs)
            return self.__arm_joint_msgs

    def __UpdateArmGripperState(self, msg:PiperMessage):
        '''更新夹爪状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the gripper status.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_gripper_msgs_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgGripperFeedBack):
                self.__fps_counter.increment("ArmGripper")
                self.__arm_gripper_msgs.time_stamp = time.time_ns()
                self.__arm_gripper_msgs.gripper_state.grippers_angle = self.__CalGripperSDKLimit(msg.gripper_feedback.grippers_angle)
                self.__arm_gripper_msgs.gripper_state.grippers_effort = msg.gripper_feedback.grippers_effort
                self.__arm_gripper_msgs.gripper_state.status_code = msg.gripper_feedback.status_code
            # print(self.__arm_gripper_msgs)
            return self.__arm_gripper_msgs
    
    def __UpdateDriverInfoHighSpdFeedback(self, msg:PiperMessage):
        '''更新驱动器信息反馈, 高速

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the driver information feedback at high speed.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_motor_info_high_spd_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_MOTOR1):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_1")
                self.__arm_time_stamp.time_stamp_motor_high_spd_1 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_1.can_id = msg.arm_high_spd_feedback_1.can_id
                self.__arm_motor_info_high_spd.motor_1.motor_speed = msg.arm_high_spd_feedback_1.motor_speed
                self.__arm_motor_info_high_spd.motor_1.current = msg.arm_high_spd_feedback_1.current
                self.__arm_motor_info_high_spd.motor_1.pos = msg.arm_high_spd_feedback_1.pos
                self.__arm_motor_info_high_spd.motor_1.effort = msg.arm_high_spd_feedback_1.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_MOTOR2):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_2")
                self.__arm_time_stamp.time_stamp_motor_high_spd_2 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_2.can_id = msg.arm_high_spd_feedback_2.can_id
                self.__arm_motor_info_high_spd.motor_2.motor_speed = msg.arm_high_spd_feedback_2.motor_speed
                self.__arm_motor_info_high_spd.motor_2.current = msg.arm_high_spd_feedback_2.current
                self.__arm_motor_info_high_spd.motor_2.pos = msg.arm_high_spd_feedback_2.pos
                self.__arm_motor_info_high_spd.motor_2.effort = msg.arm_high_spd_feedback_2.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_MOTOR3):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_3")
                self.__arm_time_stamp.time_stamp_motor_high_spd_3 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_3.can_id = msg.arm_high_spd_feedback_3.can_id
                self.__arm_motor_info_high_spd.motor_3.motor_speed = msg.arm_high_spd_feedback_3.motor_speed
                self.__arm_motor_info_high_spd.motor_3.current = msg.arm_high_spd_feedback_3.current
                self.__arm_motor_info_high_spd.motor_3.pos = msg.arm_high_spd_feedback_3.pos
                self.__arm_motor_info_high_spd.motor_3.effort = msg.arm_high_spd_feedback_3.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_MOTOR4):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_4")
                self.__arm_time_stamp.time_stamp_motor_high_spd_4 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_4.can_id = msg.arm_high_spd_feedback_4.can_id
                self.__arm_motor_info_high_spd.motor_4.motor_speed = msg.arm_high_spd_feedback_4.motor_speed
                self.__arm_motor_info_high_spd.motor_4.current = msg.arm_high_spd_feedback_4.current
                self.__arm_motor_info_high_spd.motor_4.pos = msg.arm_high_spd_feedback_4.pos
                self.__arm_motor_info_high_spd.motor_4.effort = msg.arm_high_spd_feedback_4.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_MOTOR5):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_5")
                self.__arm_time_stamp.time_stamp_motor_high_spd_5 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_5.can_id = msg.arm_high_spd_feedback_5.can_id
                self.__arm_motor_info_high_spd.motor_5.motor_speed = msg.arm_high_spd_feedback_5.motor_speed
                self.__arm_motor_info_high_spd.motor_5.current = msg.arm_high_spd_feedback_5.current
                self.__arm_motor_info_high_spd.motor_5.pos = msg.arm_high_spd_feedback_5.pos
                self.__arm_motor_info_high_spd.motor_5.effort = msg.arm_high_spd_feedback_5.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_MOTOR6):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_6")
                self.__arm_time_stamp.time_stamp_motor_high_spd_6 = time.time_ns()
                self.__arm_motor_info_high_spd.motor_6.can_id = msg.arm_high_spd_feedback_6.can_id
                self.__arm_motor_info_high_spd.motor_6.motor_speed = msg.arm_high_spd_feedback_6.motor_speed
                self.__arm_motor_info_high_spd.motor_6.current = msg.arm_high_spd_feedback_6.current
                self.__arm_motor_info_high_spd.motor_6.pos = msg.arm_high_spd_feedback_6.pos
                self.__arm_motor_info_high_spd.motor_6.effort = msg.arm_high_spd_feedback_6.cal_effort()
            else:
                pass
            # 更新时间戳，取筛选ID的最新一个
            self.__arm_motor_info_high_spd.time_stamp = max(self.__arm_time_stamp.time_stamp_motor_high_spd_1, 
                                                    self.__arm_time_stamp.time_stamp_motor_high_spd_2, 
                                                    self.__arm_time_stamp.time_stamp_motor_high_spd_3, 
                                                    self.__arm_time_stamp.time_stamp_motor_high_spd_4, 
                                                    self.__arm_time_stamp.time_stamp_motor_high_spd_5, 
                                                    self.__arm_time_stamp.time_stamp_motor_high_spd_6) / 1_000_000_000
            # print(self.__arm_motor_info_high_spd)
            return self.__arm_motor_info_high_spd
    
    def __UpdateDriverInfoLowSpdFeedback(self, msg:PiperMessage):
        '''更新驱动器信息反馈, 低速

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the driver information feedback at low speed.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_motor_info_low_spd_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_MOTOR1):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_1")
                self.__arm_time_stamp.time_stamp_motor_low_spd_1 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_1.can_id = msg.arm_low_spd_feedback_1.can_id
                self.__arm_motor_info_low_spd.motor_1.vol = msg.arm_low_spd_feedback_1.vol
                self.__arm_motor_info_low_spd.motor_1.foc_temp = msg.arm_low_spd_feedback_1.foc_temp
                self.__arm_motor_info_low_spd.motor_1.motor_temp = msg.arm_low_spd_feedback_1.motor_temp
                self.__arm_motor_info_low_spd.motor_1.foc_status_code = msg.arm_low_spd_feedback_1.foc_status_code
                self.__arm_motor_info_low_spd.motor_1.bus_current = msg.arm_low_spd_feedback_1.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_MOTOR2):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_2")
                self.__arm_time_stamp.time_stamp_motor_low_spd_2 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_2.can_id = msg.arm_low_spd_feedback_2.can_id
                self.__arm_motor_info_low_spd.motor_2.vol= msg.arm_low_spd_feedback_2.vol
                self.__arm_motor_info_low_spd.motor_2.foc_temp = msg.arm_low_spd_feedback_2.foc_temp
                self.__arm_motor_info_low_spd.motor_2.motor_temp = msg.arm_low_spd_feedback_2.motor_temp
                self.__arm_motor_info_low_spd.motor_2.foc_status_code = msg.arm_low_spd_feedback_2.foc_status_code
                self.__arm_motor_info_low_spd.motor_2.bus_current = msg.arm_low_spd_feedback_2.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_MOTOR3):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_3")
                self.__arm_time_stamp.time_stamp_motor_low_spd_3 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_3.can_id = msg.arm_low_spd_feedback_3.can_id
                self.__arm_motor_info_low_spd.motor_3.vol = msg.arm_low_spd_feedback_3.vol
                self.__arm_motor_info_low_spd.motor_3.foc_temp = msg.arm_low_spd_feedback_3.foc_temp
                self.__arm_motor_info_low_spd.motor_3.motor_temp = msg.arm_low_spd_feedback_3.motor_temp
                self.__arm_motor_info_low_spd.motor_3.foc_status_code = msg.arm_low_spd_feedback_3.foc_status_code
                self.__arm_motor_info_low_spd.motor_3.bus_current = msg.arm_low_spd_feedback_3.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_MOTOR4):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_4")
                self.__arm_time_stamp.time_stamp_motor_low_spd_4 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_4.can_id = msg.arm_low_spd_feedback_4.can_id
                self.__arm_motor_info_low_spd.motor_4.vol = msg.arm_low_spd_feedback_4.vol
                self.__arm_motor_info_low_spd.motor_4.foc_temp = msg.arm_low_spd_feedback_4.foc_temp
                self.__arm_motor_info_low_spd.motor_4.motor_temp = msg.arm_low_spd_feedback_4.motor_temp
                self.__arm_motor_info_low_spd.motor_4.foc_status_code = msg.arm_low_spd_feedback_4.foc_status_code
                self.__arm_motor_info_low_spd.motor_4.bus_current = msg.arm_low_spd_feedback_4.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_MOTOR5):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_5")
                self.__arm_time_stamp.time_stamp_motor_low_spd_5 = time.time_ns()
                self.__arm_motor_info_low_spd.motor_5.can_id = msg.arm_low_spd_feedback_5.can_id
                self.__arm_motor_info_low_spd.motor_5.vol = msg.arm_low_spd_feedback_5.vol
                self.__arm_motor_info_low_spd.motor_5.foc_temp = msg.arm_low_spd_feedback_5.foc_temp
                self.__arm_motor_info_low_spd.motor_5.motor_temp = msg.arm_low_spd_feedback_5.motor_temp
                self.__arm_motor_info_low_spd.motor_5.foc_status_code = msg.arm_low_spd_feedback_5.foc_status_code
                self.__arm_motor_info_low_spd.motor_5.bus_current = msg.arm_low_spd_feedback_5.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_MOTOR6):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_6")
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
    
    def __UpdateCurrentMotorAngleLimitMaxVel(self, msg:PiperMessage):
        '''
        更新
        反馈当前电机限制角度/最大速度
        为主动发送指令后反馈消息
        对应查询电机角度/最大速度/最大加速度限制指令 0x472 Byte 1 = 0x01
        
        SearchMotorMaxAngleSpdAccLimit(search_content=0x01)
        
        CAN_ID:
            0x473
        '''
        '''
        Updates feedback for the current motor limit angles/maximum speeds.
        This is the feedback message after actively sending a command.
        Corresponds to the query for motor angle/maximum speed/maximum acceleration limit command 0x472,
        with Byte 1 = 0x01
        
        SearchMotorMaxAngleSpdAccLimit(search_content=0x01)
        
        CAN_ID:
            0x473

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
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
                self.__feedback_current_motor_angle_limit_max_vel.current_motor_angle_limit_max_vel.max_joint_spd = \
                    msg.arm_feedback_current_motor_angle_limit_max_spd.max_joint_spd
            # print(self.__feedback_current_motor_angle_limit_max_vel)
            return self.__feedback_current_motor_angle_limit_max_vel
    
    def __UpdateCurrentMotorMaxAccLimit(self, msg:PiperMessage):
        '''
        反馈当前电机最大加速度限制
        为主动发送指令后反馈消息
        对应查询电机角度/最大速度/最大加速度限制指令 0x472 Byte 1 = 0x02
        
        SearchMotorMaxAngleSpdAccLimit(search_content=0x02)

        CAN_ID:
            0x47C
        '''
        '''
        Updates feedback for the current motor maximum acceleration limit.
        This is the feedback message after actively sending a command.
        Corresponds to the query for motor angle/maximum speed/maximum acceleration limit command 0x472,
        with Byte 1 = 0x02
        
        SearchMotorMaxAngleSpdAccLimit(search_content=0x02)

        CNA_ID:
            0x47C
        
        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
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
    
    def __UpdateAllCurrentMotorAngleLimitMaxVel(self, msg:PiperMessage):
        '''
        更新
        反馈全部电机限制角度/最大速度(注意是全部)
        为主动发送指令后反馈消息
        对应查询电机角度/最大速度/最大加速度限制指令 0x472 Byte 1 = 0x01
        
        SearchMotorMaxAngleSpdAccLimit(search_content=0x01)
        
        CAN_ID:
            0x473
        '''
        '''
        Updates feedback for the angle/maximum speed limits of all motors.
        This is the feedback message after actively sending a command.
        Corresponds to the query for motor angle/maximum speed/maximum acceleration limit command 0x472,
        with Byte 1 = 0x01
        
        SearchMotorMaxAngleSpdAccLimit(search_content=0x01)
        
        CAN_ID:
            0x473

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_all_motor_angle_limit_max_spd_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgFeedbackCurrentMotorAngleLimitMaxSpd):
                if(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 1):
                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_1 = time.time_ns()
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[1]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 2):
                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_2 = time.time_ns()
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[2]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 3):
                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_3 = time.time_ns()
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[3]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 4):
                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_4 = time.time_ns()
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[4]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 5):
                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_5 = time.time_ns()
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[5]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 6):
                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_6 = time.time_ns()
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[6]=msg.arm_feedback_current_motor_angle_limit_max_spd
                # 更新时间戳，取筛选ID的最新一个
                self.__arm_all_motor_angle_limit_max_spd.time_stamp = max(self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_1, 
                                                                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_2, 
                                                                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_3, 
                                                                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_4, 
                                                                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_5, 
                                                                    self.__arm_time_stamp.time_stamp_motor_angle_limit_max_spd_6) / 1_000_000_000
            # print(self.__arm_all_motor_angle_limit_max_spd)
            return self.__arm_all_motor_angle_limit_max_spd
    
    def __UpdateAllCurrentMotorMaxAccLimit(self, msg:PiperMessage):
        '''
        反馈全部电机最大加速度限制(注意是全部)
        为主动发送指令后反馈消息
        对应查询电机角度/最大速度/最大加速度限制指令 0x472 Byte 1 = 0x02
        
        SearchMotorMaxAngleSpdAccLimit(search_content=0x02)

        CAN_ID:
            0x47C
        '''
        '''
        Updates feedback for the maximum acceleration limits of all motors.
        This is the feedback message after actively sending a command.
        Corresponds to the query for motor angle/maximum speed/maximum acceleration limit command 0x472,
        with Byte 1 = 0x02
        
        CAN_ID:
            0x47C

        SearchMotorMaxAngleSpdAccLimit(search_content=0x02)
        
        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_all_motor_max_acc_limit_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgFeedbackCurrentMotorMaxAccLimit):
                if(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 1):
                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_1 = time.time_ns()
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[1]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 2):
                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_2 = time.time_ns()
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[2]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 3):
                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_3 = time.time_ns()
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[3]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 4):
                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_4 = time.time_ns()
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[4]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 5):
                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_5 = time.time_ns()
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[5]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 6):
                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_6 = time.time_ns()
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[6]=msg.arm_feedback_current_motor_max_acc_limit
                # 更新时间戳，取筛选ID的最新一个
                self.__arm_all_motor_max_acc_limit.time_stamp = max(self.__arm_time_stamp.time_stamp_motor_max_acc_limit_1, 
                                                                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_2, 
                                                                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_3, 
                                                                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_4, 
                                                                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_5, 
                                                                    self.__arm_time_stamp.time_stamp_motor_max_acc_limit_6) / 1_000_000_000
            # print(self.__arm_all_motor_max_acc_limit)
            return self.__arm_all_motor_max_acc_limit
    
    def __UpdateCurrentEndVelAndAccParam(self, msg:PiperMessage):
        '''
        反馈当前末端速度/加速度参数
        为主动发送指令后反馈消息

        对应机械臂参数查询与设置指令 0x477 Byte 0 = 0x01
        ArmParamEnquiryAndConfig(param_enquiry=0x01)
        
        CAN_ID:
            0x478
        '''
        '''
        Updates feedback for the current end effector velocity/acceleration parameters.
        This is the feedback message after actively sending a command.
        Corresponds to the robotic arm parameter query and setting command 0x477,
        ArmParamEnquiryAndConfig(param_enquiry=0x01)
        with Byte 0 = 0x01
        
        CAN_ID:
            0x478

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
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
    
    def __UpdateCrashProtectionLevelFeedback(self, msg:PiperMessage):
        '''
        碰撞防护等级设置反馈指令
        为主动发送指令后反馈消息
        对应机械臂参数查询与设置指令 0x477 Byte 0 = 0x02
        
        ArmParamEnquiryAndConfig(param_enquiry=0x02)
        
        CAN_ID:
            0x47B
        '''
        '''
        Updates feedback for the collision protection level setting.
        This is the feedback message after actively sending a command.
        Corresponds to the robotic arm parameter query and setting command 0x477,
        with Byte 0 = 0x02
        
        ArmParamEnquiryAndConfig(param_enquiry=0x02)
        
        CAN_ID:
            0x47B

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__feedback_crash_protection_level_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgCrashProtectionRatingFeedback):
                self.__feedback_crash_protection_level.time_stamp = time.time_ns()/ 1_000_000_000
                self.__feedback_crash_protection_level.crash_protection_level_feedback.joint_1_protection_level=\
                    msg.arm_crash_protection_rating_feedback.joint_1_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.joint_2_protection_level=\
                    msg.arm_crash_protection_rating_feedback.joint_2_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.joint_3_protection_level=\
                    msg.arm_crash_protection_rating_feedback.joint_3_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.joint_4_protection_level=\
                    msg.arm_crash_protection_rating_feedback.joint_4_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.joint_5_protection_level=\
                    msg.arm_crash_protection_rating_feedback.joint_5_protection_level
                self.__feedback_crash_protection_level.crash_protection_level_feedback.joint_6_protection_level=\
                    msg.arm_crash_protection_rating_feedback.joint_6_protection_level
            # print(self.__feedback_crash_protection_level)
            return self.__feedback_crash_protection_level
    
    def __UpdateArmJointCtrl(self, msg:PiperMessage):
        '''更新关节和夹爪状态,为主臂发送的消息

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the joint and gripper status, as sent by the main arm.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_joint_ctrl_msgs_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgJointCtrl_12):
                self.__fps_counter.increment("ArmJointCtrl_12")
                self.__arm_time_stamp.time_stamp_joint_ctrl_12 = time.time_ns()
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_1 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_1, "j1")
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_2 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_2, "j2")
            elif(msg.type_ == ArmMsgType.PiperMsgJointCtrl_34):
                self.__fps_counter.increment("ArmJointCtrl_34")
                self.__arm_time_stamp.time_stamp_joint_ctrl_34 = time.time_ns()
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_3 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_3, "j3")
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_4 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_4, "j4")
            elif(msg.type_ == ArmMsgType.PiperMsgJointCtrl_56):
                self.__fps_counter.increment("ArmJointCtrl_56")
                self.__arm_time_stamp.time_stamp_joint_ctrl_56 = time.time_ns()
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_5 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_5, "j5")
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_6 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_6, "j6")
            else:
                pass
            # 更新时间戳，取筛选ID的最新一个
            self.__arm_joint_ctrl_msgs.time_stamp = max(self.__arm_time_stamp.time_stamp_joint_ctrl_12, 
                                                        self.__arm_time_stamp.time_stamp_joint_ctrl_34, 
                                                        self.__arm_time_stamp.time_stamp_joint_ctrl_56)/ 1_000_000_000
            # print(self.__arm_joint_ctrl_msgs)
            return self.__arm_joint_ctrl_msgs
    
    def __UpdateArmGripperCtrl(self, msg:PiperMessage):
        '''更新夹爪状态,为主臂发送的消息

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the gripper status, as sent by the main arm.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_gripper_ctrl_msgs_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgGripperCtrl):
                self.__fps_counter.increment("ArmGripperCtrl")
                self.__arm_gripper_ctrl_msgs.time_stamp = time.time_ns()
                self.__arm_gripper_ctrl_msgs.gripper_ctrl.grippers_angle = self.__CalGripperSDKLimit(msg.arm_gripper_ctrl.grippers_angle)
                self.__arm_gripper_ctrl_msgs.gripper_ctrl.grippers_effort = msg.arm_gripper_ctrl.grippers_effort
                self.__arm_gripper_ctrl_msgs.gripper_ctrl.status_code = msg.arm_gripper_ctrl.status_code
                self.__arm_gripper_ctrl_msgs.gripper_ctrl.set_zero = msg.arm_gripper_ctrl.set_zero
            # print(self.__arm_gripper_ctrl_msgs)
            return self.__arm_gripper_ctrl_msgs
    
    def __UpdateArmCtrlCode151(self, msg:PiperMessage):
        '''
        更新主臂发送的151控制指令

        0x151
        '''
        '''Updates the control command 0x151 sent by the main arm.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_ctrl_code_151_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgMotionCtrl_2):
                self.__fps_counter.increment("ArmCtrlCode_151")
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
    
    def __UpdatePiperFirmware(self, msg:PiperMessage):
        '''
        更新piper固件字符信息
        '''
        '''
        Update Piper firmware character information.
        '''
        with self.__firmware_data_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgFirmwareRead):
                self.__firmware_data = self.__firmware_data + msg.firmware_data
            return self.__firmware_data
    
    def __UpdatePiperFeedbackFK(self):
        '''
        更新piper反馈消息正解数据
        '''
        '''
        Update Piper FK Data
        '''
        with self.__arm_joint_msgs_mtx:
            joint_states = [self.__arm_joint_msgs.joint_state.joint_1 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_msgs.joint_state.joint_2 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_msgs.joint_state.joint_3 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_msgs.joint_state.joint_4 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_msgs.joint_state.joint_5 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_msgs.joint_state.joint_6 / (1000*self.__piper_fk.RADIAN)]
        with self.__piper_feedback_fk_mtx:
            self.__link_feedback_fk = self.__piper_fk.CalFK(joint_states)
    
    def __UpdatePiperCtrlFK(self):
        '''
        更新piper控制消息正解数据
        '''
        '''
        Update Piper FK Data
        '''
        with self.__arm_joint_ctrl_msgs_mtx:
            joint_states = [self.__arm_joint_ctrl_msgs.joint_ctrl.joint_1 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_ctrl_msgs.joint_ctrl.joint_2 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_ctrl_msgs.joint_ctrl.joint_3 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_ctrl_msgs.joint_ctrl.joint_4 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_ctrl_msgs.joint_ctrl.joint_5 / (1000*self.__piper_fk.RADIAN),
                            self.__arm_joint_ctrl_msgs.joint_ctrl.joint_6 / (1000*self.__piper_fk.RADIAN)]
        with self.__piper_ctrl_fk_mtx:
            self.__link_ctrl_fk = self.__piper_fk.CalFK(joint_states)
    
    # 控制发送函数------------------------------------------------------------------------------------------------------
    def MotionCtrl_1(self, 
                    emergency_stop: Literal[0x00, 0x01, 0x02] = 0, 
                    track_ctrl: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08] = 0, 
                    grag_teach_ctrl: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07] = 0):
        '''
        机械臂运动控制指令1 
        
        CAN ID:
            0x150
        
        Args:
            emergency_stop: 快速急停 uint8 
                0x00 无效
                0x01 快速急停
                0x02 恢复
            track_ctrl: 轨迹指令 uint8 
                0x00 关闭
                0x01 暂停当前规划 
                0x02 继续当前轨迹
                0x03 清除当前轨迹 
                0x04 清除所有轨迹 
                0x05 获取当前规划轨迹 
                0x06 终止执行 
                0x07 轨迹传输 
                0x08 轨迹传输结束
            grag_teach_ctrl: 拖动示教指令 uint8 
                0x00 关闭
                0x01 开始示教记录（进入拖动示教模式）
                0x02 结束示教记录（退出拖动示教模式） 
                0x03 执行示教轨迹（拖动示教轨迹复现） 
                0x04 暂停执行 
                0x05 继续执行（轨迹复现继续） 
                0x06 终止执行 
                0x07 运动到轨迹起点
        '''
        '''
        Sends the robotic arm motion control command (0x150).
        
        Args:
            emergency_stop (int): The emergency stop command.
                0x00: Invalid
                0x01: Emergency stop
                0x02: Resume
            track_ctrl (int): The trajectory control command.
                0x00: Disable
                0x01: Pause current plan
                0x02: Continue current trajectory
                0x03: Clear current trajectory
                0x04: Clear all trajectories
                0x05: Get current planned trajectory
                0x06: Terminate execution
                0x07: Trajectory transmission
                0x08: End of trajectory transmission
            grag_teach_ctrl (int): The teach mode control command.
                0x00: Disable
                0x01: Start teaching record (enter teach mode)
                0x02: End teaching record (exit teach mode)
                0x03: Execute taught trajectory (reproduce teach mode trajectory)
                0x04: Pause execution
                0x05: Continue execution (resume trajectory reproduction)
                0x06: Terminate execution
                0x07: Move to trajectory start point
        '''
        tx_can = Message()
        motion_ctrl_1 = ArmMsgMotionCtrl_1(emergency_stop, track_ctrl, grag_teach_ctrl)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrl_1, arm_motion_ctrl_1=motion_ctrl_1)
        self.__parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def MotionCtrl_2(self, 
                     ctrl_mode: Literal[0x00, 0x01, 0x03, 0x04, 0x07] = 0x01, 
                     move_mode: Literal[0x00, 0x01, 0x02, 0x03] = 0x01, 
                     move_spd_rate_ctrl: int = 50, 
                     is_mit_mode: Literal[0x00, 0xAD, 0xFF] = 0x00):
        '''
        机械臂运动控制指令2
        
        CAN ID:
            0x151
        
        Args:
            ctrl_mode: 控制模式 uint8 
                0x00 待机模式
                0x01 CAN 指令控制模式
                0x03 以太网控制模式
                0x04 wifi 控制模式
                0x07 离线轨迹模式
            move_mode: MOVE模式 uint8 
                0x00 MOVE P
                0x01 MOVE J
                0x02 MOVE L
                0x03 MOVE C
            move_spd_rate_ctrl 运动速度百分比 uint8
                数值范围0~100 
            is_mit_mode: mit模式 uint8 
                0x00 位置速度模式
                0xAD MIT模式
                0xFF 无效
            residence_time: 离线轨迹点停留时间 
                uint8 0~254 ,单位: s;255:轨迹终止
        '''
        '''
        Sends the robotic arm motion control command (0x151).
        
        Args:
            ctrl_mode (int): The control mode.
                0x00: Standby mode
                0x01: CAN command control mode
                0x03: Ethernet control mode
                0x04: Wi-Fi control mode
                0x07: Offline trajectory mode
            move_mode (int): The MOVE mode.
                0x00: MOVE P (Position)
                0x01: MOVE J (Joint)
                0x02: MOVE L (Linear)
                0x03: MOVE C (Circular)
            move_spd_rate_ctrl (int): The movement speed percentage (0-100).
            is_mit_mode (int): The MIT mode.
                0x00: Position-velocity mode
                0xAD: MIT mode
                0xFF: Invalid
            residence_time: Offline trajectory point residence time
                uint8 0~254, unit: seconds; 255: trajectory termination
        '''
        tx_can = Message()
        motion_ctrl_2 = ArmMsgMotionCtrl_2(ctrl_mode, move_mode, move_spd_rate_ctrl, is_mit_mode)
        # print(motion_ctrl_1)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrl_2, arm_motion_ctrl_2=motion_ctrl_2)
        self.__parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def __ValidateEndPoseValue(self, endpose_num:str, endpose_value):
        # 类型判断
        if not isinstance(endpose_value, int):
            print(f"Error: EndPose_{endpose_num} value {endpose_value} is not an integer.")
            return False
        return True
    
    def EndPoseCtrl(self, X: int, Y: int, Z: int, RX: int, RY: int, RZ: int):
        '''
        机械臂末端数值发送,发送前需要切换机械臂模式为末端控制模式
        
        CAN ID:
            0x152,0x153,0x154
        
        Args:
            X_axis: X坐标,单位0.001mm
            Y_axis: Y坐标,单位0.001mm
            Z_axis: Z坐标,单位0.001mm
            RX_axis: RX角度,单位0.001度
            RY_axis: RY角度,单位0.001度
            RZ_axis: RZ角度,单位0.001度
        '''
        '''
        Updates the joint control for the robotic arm.
        
        CAN ID:
            0x152,0x153,0x154
        
        Args:
            X_axis: X-axis coordinate, in 0.001 mm.
            Y_axis: Y-axis coordinate, in 0.001 mm.
            Z_axis: Z-axis coordinate, in 0.001 mm.
            RX_axis: Rotation about X-axis, in 0.001 degrees.
            RY_axis: Rotation about Y-axis, in 0.001 degrees.
            RZ_axis: Rotation about Z-axis, in 0.001 degrees.
        '''
        if not self.__ValidateEndPoseValue("X", X) or \
        not self.__ValidateEndPoseValue("Y", Y) or \
        not self.__ValidateEndPoseValue("Z", Z) or \
        not self.__ValidateEndPoseValue("RX", RX) or \
        not self.__ValidateEndPoseValue("RY", RY) or \
        not self.__ValidateEndPoseValue("RZ", RZ):
            return
        self.__CartesianCtrl_XY(X,Y)
        self.__CartesianCtrl_ZRX(Z,RX)
        self.__CartesianCtrl_RYRZ(RY,RZ)
    
    def __CartesianCtrl_XY(self, X:int, Y:int):
        tx_can = Message()
        cartesian_1 = ArmMsgMotionCtrlCartesian(X_axis=X, Y_axis=Y)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrlCartesian_1, arm_motion_ctrl_cartesian=cartesian_1)
        self.__parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def __CartesianCtrl_ZRX(self, Z:int, RX:int):
        tx_can = Message()
        cartesian_2 = ArmMsgMotionCtrlCartesian(Z_axis=Z, RX_axis=RX)
        # print(cartesian_2)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrlCartesian_2, arm_motion_ctrl_cartesian=cartesian_2)
        self.__parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def __CartesianCtrl_RYRZ(self, RY:int, RZ:int):
        tx_can = Message()
        cartesian_3 = ArmMsgMotionCtrlCartesian(RY_axis=RY, RZ_axis=RZ)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrlCartesian_3, arm_motion_ctrl_cartesian=cartesian_3)
        self.__parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def JointCtrl(self, 
                  joint_1: int, 
                  joint_2: int,
                  joint_3: int,
                  joint_4: int,
                  joint_5: int,
                  joint_6: int):
        '''
        机械臂关节控制, 发送前需要切换机械臂模式为关节控制模式
        
        CAN ID:
            0x155,0x156,0x157
        
        |joint_name|     limit(rad)     |    limit(angle)    |
        |----------|     ----------     |     ----------     |
        |joint1    |   [-2.618, 2.618]  |    [-150.0, 150.0] |
        |joint2    |   [0, 3.14]        |    [0, 180.0]      |
        |joint3    |   [-2.967, 0]      |    [-170, 0]       |
        |joint4    |   [-1.745, 1.745]  |    [-100.0, 100.0] |
        |joint5    |   [-1.22, 1.22]    |    [-70.0, 70.0]   |
        |joint6    |   [-2.0944, 2.0944]|    [-120.0, 120.0] |
        
        Args:
            joint_1 (int): 关节1角度,单位0.001度
            joint_2 (int): 关节2角度,单位0.001度
            joint_3 (int): 关节3角度,单位0.001度
            joint_4 (int): 关节4角度,单位0.001度
            joint_5 (int): 关节5角度,单位0.001度
            joint_6 (int): 关节6角度,单位0.001度
        '''
        '''
        Updates the joint control for the robotic arm.Before sending, switch the robotic arm mode to joint control mode
        
        CAN ID:
            0x155,0x156,0x157
        
        |joint_name|     limit(rad)     |    limit(angle)    |
        |----------|     ----------     |     ----------     |
        |joint1    |   [-2.618, 2.618]  |    [-150.0, 150.0] |
        |joint2    |   [0, 3.14]        |    [0, 180.0]      |
        |joint3    |   [-2.967, 0]      |    [-170, 0]       |
        |joint4    |   [-1.745, 1.745]  |    [-100.0, 100.0] |
        |joint5    |   [-1.22, 1.22]    |    [-70.0, 70.0]   |
        |joint6    |   [-2.0944, 2.0944]|    [-120.0, 120.0] |
        
        Args:
            joint_1 (int): The angle of joint 1.in 0.001°
            joint_2 (int): The angle of joint 2.in 0.001°
            joint_3 (int): The angle of joint 3.in 0.001°
            joint_4 (int): The angle of joint 4.in 0.001°
            joint_5 (int): The angle of joint 5.in 0.001°
            joint_6 (int): The angle of joint 6.in 0.001°
        '''
        joint_1 = self.__CalJointSDKLimit(joint_1, "j1")
        joint_2 = self.__CalJointSDKLimit(joint_2, "j2")
        joint_3 = self.__CalJointSDKLimit(joint_3, "j3")
        joint_4 = self.__CalJointSDKLimit(joint_4, "j4")
        joint_5 = self.__CalJointSDKLimit(joint_5, "j5")
        joint_6 = self.__CalJointSDKLimit(joint_6, "j6")
        self.__JointCtrl_12(joint_1, joint_2)
        self.__JointCtrl_34(joint_3, joint_4)
        self.__JointCtrl_56(joint_5, joint_6)
    
    def __JointCtrl_12(self, joint_1: int, joint_2: int):
        '''
        机械臂1,2关节控制
        
        私有函数
        
        Args:
            joint_1 (int): 关节1角度,单位0.001度
            joint_2 (int): 关节2角度,单位0.001度
        '''
        '''
        Controls the joints 1 and 2 of the robotic arm.
        
        This is a private function.
        
        Args:
            joint_1 (int): The angle of joint 1.in 0.001°
            joint_2 (int): The angle of joint 2.in 0.001°
        '''
        tx_can = Message()
        joint_ctrl = ArmMsgJointCtrl(joint_1=joint_1, joint_2=joint_2)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgJointCtrl_12, arm_joint_ctrl=joint_ctrl)
        self.__parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def __JointCtrl_34(self, joint_3: int, joint_4: int):
        '''
        机械臂3,4关节控制
        
        私有函数
        
        Args:
            joint_3 (int): 关节3角度,单位0.001度
            joint_4 (int): 关节4角度,单位0.001度
        '''
        '''
        Controls the joints 3 and 4 of the robotic arm.
        
        This is a private function.
        
        Args:
            joint_3 (int): The angle of joint 3.in 0.001°
            joint_4 (int): The angle of joint 4.in 0.001°
        '''
        tx_can = Message()
        joint_ctrl = ArmMsgJointCtrl(joint_3=joint_3, joint_4=joint_4)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgJointCtrl_34, arm_joint_ctrl=joint_ctrl)
        self.__parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def __JointCtrl_56(self, joint_5: int, joint_6: int):
        '''
        机械臂5,6关节控制
        
        私有函数
        
        Args:
            joint_5 (int): 关节5角度,单位0.001度
            joint_6 (int): 关节6角度,单位0.001度
        '''
        '''
        Controls the joints 5 and 6 of the robotic arm.
        
        This is a private function.
        
        Args:
            joint_5 (int): The angle of joint 5.in 0.001°
            joint_6 (int): The angle of joint 6.in 0.001°
        '''
        tx_can = Message()
        joint_ctrl = ArmMsgJointCtrl(joint_5=joint_5, joint_6=joint_6)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgJointCtrl_56, arm_joint_ctrl=joint_ctrl)
        self.__parser.EncodeMessage(msg, tx_can)
        #print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def MoveCAxisUpdateCtrl(self, instruction_num: Literal[0x00, 0x01, 0x02, 0x03] = 0x00):
        '''
        MoveC模式坐标点更新指令, 发送前需要切换机械臂模式为MoveC控制模式
        
        Args:
            instruction_num (int): 指令点序号
                0x00 无效 
                0x01 起点 
                0x02 中点 
                0x03 终点
        首先使用 EndPoseCtrl 确定起点,piper.MoveCAxisUpdateCtrl(0x01)
        然后使用 EndPoseCtrl 确定中点,piper.MoveCAxisUpdateCtrl(0x02)
        最后使用 EndPoseCtrl 确定中点,piper.MoveCAxisUpdateCtrl(0x03)
        '''
        '''
        MoveC Mode Coordinate Point Update Command.Before sending, switch the robotic arm mode to MoveC control mode
        
        Args:
            instruction_num (int): Instruction point sequence number
                0x00 Invalid
                0x01 Start point
                0x02 Midpoint
                0x03 Endpoint
        First, use EndPoseCtrl to determine the start point:piper.MoveCAxisUpdateCtrl(0x01)
        Then, use EndPoseCtrl to determine the midpoint:piper.MoveCAxisUpdateCtrl(0x02)
        Finally, use EndPoseCtrl again to determine the endpoint:piper.MoveCAxisUpdateCtrl(0x03)
        '''
        tx_can = Message()
        move_c = ArmMsgCircularPatternCoordNumUpdateCtrl(instruction_num)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgCircularPatternCoordNumUpdateCtrl, arm_circular_ctrl=move_c)
        self.__parser.EncodeMessage(msg, tx_can)
        # print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def GripperCtrl(self, 
                    gripper_angle: int = 0, 
                    gripper_effort: int = 0, 
                    gripper_code: Literal[0x00, 0x01, 0x02, 0x03] = 0, 
                    set_zero: Literal[0x00, 0xAE] = 0):
        '''
        夹爪控制
        
        CAN ID:
            0x159
        
        Args:
            gripper_angle (int): 夹爪角度,单位 0.001°
            gripper_effort (int): 夹爪力矩,单位 0.001N/m,范围0-5000,对应0-5N/m
            gripper_code (int): 
                0x00失能;
                0x01使能;
                0x02失能清除错误;
                0x03使能清除错误.
            set_zero:(int): 设定当前位置为0点,
                0x00无效值;
                0xAE设置零点
        '''
        '''
        Controls the gripper of the robotic arm.
        
        CAN ID:
            0x159
        
        Args:
            gripper_angle (int): The gripper angle, in 0.001°.
            gripper_effort (int): The gripper torque, in 0.001 N/m.Range 0-5000,corresponse 0-5N/m
            gripper_code (int): The gripper enable/disable/clear error command.
                0x00: Disable
                0x01: Enable
                0x03/0x02: Enable and clear error / Disable and clear error
            set_zero (int): Set the current position as the zero point.
                0x00: Invalid value
                0xAE: Set zero point
        '''
        tx_can = Message()
        gripper_angle = self.__CalGripperSDKLimit(gripper_angle)
        gripper_ctrl = ArmMsgGripperCtrl(gripper_angle, gripper_effort, gripper_code, set_zero)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgGripperCtrl, arm_gripper_ctrl=gripper_ctrl)
        self.__parser.EncodeMessage(msg, tx_can)
        # print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def MasterSlaveConfig(self, linkage_config: int, feedback_offset: int, ctrl_offset: int, linkage_offset: int):
        '''
        随动主从模式设置指令
        
        CAN ID:
            0x470
        
        Args:
            linkage_config: uint8, 联动设置指令。
                0x00 无效
                0xFA 设置为示教输入臂
                0xFC 设置为运动输出臂
            feedback_offset: uint8, 反馈指令偏移值。
                0x00 : 不偏移/恢复默认
                0x10 ：反馈指令基 ID 由 2Ax偏移为 2Bx
                0x20 ：反馈指令基 ID 由 2Ax偏移为 2Cx
            ctrl_offset: uint8, 控制指令偏移值。
                0x00 : 不偏移/恢复默认
                0x10 ：控制指令基 ID 由 15x偏移为 16x
                0x20 ：控制指令基 ID 由 15x偏移为 17x
            linkage_offset: uint8, 联动模式控制目标地址偏移值。
                0x00 : 不偏移/恢复默认
                0x10 : 控制目标地址基 ID由 15x 偏移为 16x
                0x20 : 控制目标地址基 ID由 15x 偏移为 17x
        '''
        '''
        Sets the linkage mode configuration.
        
        CAN ID:
            0x470
        
        Args:
            linkage_config (int): The linkage setting command.
                0x00: Invalid
                0xFA: Set as teaching input arm
                0xFC: Set as motion output arm
            feedback_offset (int): The feedback command offset value.
                0x00: No offset / restore default
                0x10: Feedback command base ID shifts from 2Ax to 2Bx
                0x20: Feedback command base ID shifts from 2Ax to 2Cx
            ctrl_offset (int): The control command offset value.
                0x00: No offset / restore default
                0x10: Control command base ID shifts from 15x to 16x
                0x20: Control command base ID shifts from 15x to 17x
            linkage_offset (int): The linkage mode control target address offset value.
                0x00: No offset / restore default
                0x10: Control target address base ID shifts from 15x to 16x
                0x20: Control target address base ID shifts from 15x to 17x
        '''
        tx_can = Message()
        ms_config = ArmMsgMasterSlaveModeConfig(linkage_config, feedback_offset, ctrl_offset, linkage_offset)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMasterSlaveModeConfig, arm_ms_config=ms_config)
        self.__parser.EncodeMessage(msg, tx_can)
        # print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def DisableArm(self, 
                   motor_num: Literal[1, 2, 3, 4, 5, 6, 7, 0xFF] = 7, 
                   enable_flag: Literal[0x01, 0x02] = 0x01):
        '''
        失能电机
        
        CAN ID:
            0x471
        
        Args:
            motor_num: 电机序号[1,7],7代表所有电机

            enable_flag: 0x01-失能
        '''
        '''
        Enable the motor(s).
        
        CAN ID:
            0x471
        
        Args:
            motor_num (int): The motor number, ranging from 1 to 7. 
                            7 represents all motors.
            enable_flag (int): The enable flag.
                0x01: Disable
        '''
        tx_can = Message()
        enable = ArmMsgMotorEnableDisableConfig(motor_num, enable_flag)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotorEnableDisableConfig, arm_motor_enable=enable)
        self.__parser.EncodeMessage(msg, tx_can)
        # print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def EnableArm(self, 
                  motor_num: Literal[1, 2, 3, 4, 5, 6, 7, 0xFF] = 7, 
                  enable_flag: Literal[0x01, 0x02] = 0x02):
        '''
        使能电机
        
        CAN ID:
            0x471
        
        Args:
            motor_num: 电机序号[1,7],7代表所有电机

            enable_flag: 0x02-使能
        '''
        '''
        Disable the motor(s).
        
        CAN ID:
            0x471
        
        Args:
            motor_num (int): The motor number, ranging from 1 to 7. 
                            7 represents all motors.
            enable_flag (int): The enable flag.
                0x02: Enable
        '''
        tx_can = Message()
        disable = ArmMsgMotorEnableDisableConfig(motor_num, enable_flag)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotorEnableDisableConfig, arm_motor_enable=disable)
        self.__parser.EncodeMessage(msg, tx_can)
        # print(hex(tx_can.arbitration_id), tx_can.data)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def SearchMotorMaxAngleSpdAccLimit(self, 
                                       motor_num: Literal[1, 2, 3, 4, 5, 6] = 1, 
                                       search_content: Literal[0x01, 0x02] = 0x01):
        '''
        查询电机角度/最大速度/最大加速度限制指令
        
        对应反馈当前电机限制角度/最大速度
        
        CAN ID:
            0x472
        
        Args:
            motor_num: uint8, 关节电机序号。
                值域 1-6,1-6 代表关节驱动器序号
            search_content: uint8, 查询内容。
                0x01 : 查询电机角度/最大速度
                0x02 : 查询电机最大加速度限制
        '''
        '''Queries the motor angle/maximum speed/maximum acceleration limit command (0x472).
        
        This corresponds to feedback on the current motor angle/maximum speed limits.

        CAN ID:
            0x472
        
        Args:
            command (list): The command list containing the following elements:
            
            motor_num (uint8)
                The joint motor number (1-6), representing the joint driver number.
            
            search_content (uint8)
                0x01: Query motor angle/maximum speed.
                0x02: Query motor maximum acceleration limit.
        '''
        tx_can = Message()
        search_motor = ArmMsgSearchMotorMaxAngleSpdAccLimit(motor_num, search_content)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgSearchMotorMaxAngleSpdAccLimit, arm_search_motor_max_angle_spd_acc_limit=search_motor)
        self.__parser.EncodeMessage(msg, tx_can)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def SearchAllMotorMaxAngleSpd(self):
        '''查询全部电机的电机最大角度/最小角度/最大速度指令

        CAN ID:
            0x472
        '''
        '''Queries the maximum angle, minimum angle, and maximum speed for all motors.

        CAN ID:
            0x472
        '''
        self.SearchMotorMaxAngleSpdAccLimit(1, 0x01)
        self.SearchMotorMaxAngleSpdAccLimit(2, 0x01)
        self.SearchMotorMaxAngleSpdAccLimit(3, 0x01)
        self.SearchMotorMaxAngleSpdAccLimit(4, 0x01)
        self.SearchMotorMaxAngleSpdAccLimit(5, 0x01)
        self.SearchMotorMaxAngleSpdAccLimit(6, 0x01)
    
    def SearchAllMotorMaxAccLimit(self):
        '''查询全部电机的最大加速度限制指令

        CAN ID:
            0x472
        '''
        '''Queries the maximum acceleration limits for all motors.

        CAN ID:
            0x472
        '''
        self.SearchMotorMaxAngleSpdAccLimit(1, 0x02)
        self.SearchMotorMaxAngleSpdAccLimit(2, 0x02)
        self.SearchMotorMaxAngleSpdAccLimit(3, 0x02)
        self.SearchMotorMaxAngleSpdAccLimit(4, 0x02)
        self.SearchMotorMaxAngleSpdAccLimit(5, 0x02)
        self.SearchMotorMaxAngleSpdAccLimit(6, 0x02)
    
    def MotorAngleLimitMaxSpdSet(self, 
                                 motor_num: Literal[1, 2, 3, 4, 5, 6], 
                                 max_angle_limit: int, 
                                 min_angle_limit: int, 
                                 max_joint_spd: int = 3000):
        '''
        电机角度限制/最大速度设置指令
        
        CAN ID:
            0x474
        
        Args:
            motor_num: 关节电机序号
            max_angle_limit: 最大角度限制,单位 0.1°
            min_angle_limit: 最小角度限制,单位 0.1°
            max_joint_spd: 最大关节速度,单位 0.001rad/s,范围[0,3000]
        
        |joint_name|     limit(rad)     |    limit(angle)    |     limit(rad/s)   |
        |----------|     ----------     |     ----------     |     ----------     |
        |joint1    |   [-2.618, 2.618]  |    [-150.0, 150.0] |      [0, 3.0]      |
        |joint2    |   [0, 3.14]        |    [0, 180.0]      |      [0, 3.0]      |
        |joint3    |   [-2.967, 0]      |    [-170, 0]       |      [0, 3.0]      |
        |joint4    |   [-1.745, 1.745]  |    [-100.0, 100.0] |      [0, 3.0]      |
        |joint5    |   [-1.22, 1.22]    |    [-70.0, 70.0]   |      [0, 3.0]      |
        |joint6    |   [-2.0944, 2.0944]|    [-120.0, 120.0] |      [0, 3.0]      |
        '''
        '''
        Sets the motor angle limit/maximum speed limit command 
        
        CAN ID:
            0x474
        
        Args:
            motor_num: Joint motor index.
            max_angle_limit: Maximum angle limit, unit 0.1°.
            min_angle_limit: Minimum angle limit, unit 0.1°.
            max_joint_spd: Maximum joint speed, unit 0.001 rad/s.Range [0,3000].
        
        |joint_name|     limit(rad)     |    limit(angle)    |     limit(rad/s)   |
        |----------|     ----------     |     ----------     |     ----------     |
        |joint1    |   [-2.618, 2.618]  |    [-150.0, 150.0] |      [0, 3.0]      |
        |joint2    |   [0, 3.14]        |    [0, 180.0]      |      [0, 3.0]      |
        |joint3    |   [-2.967, 0]      |    [-170, 0]       |      [0, 3.0]      |
        |joint4    |   [-1.745, 1.745]  |    [-100.0, 100.0] |      [0, 3.0]      |
        |joint5    |   [-1.22, 1.22]    |    [-70.0, 70.0]   |      [0, 3.0]      |
        |joint6    |   [-2.0944, 2.0944]|    [-120.0, 120.0] |      [0, 3.0]      |
        '''
        tx_can = Message()
        motor_set = ArmMsgMotorAngleLimitMaxSpdSet(motor_num, max_angle_limit, min_angle_limit, max_joint_spd)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotorAngleLimitMaxSpdSet, arm_motor_angle_limit_max_spd_set=motor_set)
        self.__parser.EncodeMessage(msg, tx_can)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def JointConfig(self, 
                    joint_num: Literal[1, 2, 3, 4, 5, 6, 7] = 7,
                    set_zero: Literal[0x00, 0xAE] = 0,
                    acc_param_is_effective: Literal[0x00, 0xAE] = 0,
                    max_joint_acc: int = 500,
                    clear_err: Literal[0x00, 0xAE] = 0):
        '''
        关节设置
        
        CAN ID:
            0x475
        
        Args:
            joint_motor_num: 关节电机序号值域 1-7
                1-6 代表关节驱动器序号;
                7 代表全部关节电机;
            set_motor_current_pos_as_zero: 设置当前位置为零点,有效值,0xAE
            acc_param_config_is_effective_or_not: 加速度参数设置是否生效,有效值,0xAE
            max_joint_acc: 最大关节加速度,单位0.01rad/s^2
                           输入范围\[0, 500\]-->[0 rad/s^2, 5.0 rad/s^2]
            clear_joint_err: 清除关节错误代码,有效值,0xAE
        '''
        '''
        Joint Configuration Command
        
        CAN ID:
            0x475
        
        Args:
            joint_motor_num: Joint motor number.
                Value range: 1-6 represents individual joint motor numbers.
                Value 7 applies to all joint motors.
            set_motor_current_pos_as_zero: Command to set the current position of the specified joint motor as zero, with a valid value of 0xAE.
            acc_param_config_is_effective_or_not: Indicates whether the acceleration parameter configuration is effective, with a valid value of 0xAE.
            max_joint_acc: Maximum joint acceleration, unit: 0.01rad/s^2.
                           Range is \[0, 500\]-->[0 rad/s^2, 5.0 rad/s^2]
            clear_joint_err: Command to clear joint error codes, with a valid value of 0xAE.
        '''
        tx_can = Message()
        joint_config = ArmMsgJointConfig(joint_num, set_zero, acc_param_is_effective, max_joint_acc, clear_err)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgJointConfig,arm_joint_config=joint_config)
        self.__parser.EncodeMessage(msg, tx_can)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def JointMaxAccConfig(self, motor_num: Literal[1, 2, 3, 4, 5, 6] = 6, max_joint_acc: int = 500):
        '''
        关节最大加速度设置指令
        
        CAN ID:
            0x475
        
        范围: 0-500 
        
        对应: 0-5 rad/s^2
        
        Args:
            motor_num: 电机序号[1,6]
            max_joint_acc: 关节电机最大速度设定,单位 0.01rad/s^2
        '''
        '''
        Joint Maximum Acceleration Command
        
        CAN ID:
            0x475
        
        Range: 0-500
        
        Correspond: 0-5 rad/s^2
        
        Args:
            motor_num:[1,6]
            max_joint_acc: Maximum speed setting for joint motor, unit: 0.01 rad/s^2
        '''
        self.JointConfig(motor_num, 0, 0xAE, max_joint_acc, 0)
    
    def SetInstructionResponse(self, instruction_index: int, zero_config_success_flag: Literal[0, 1] = 0):
        '''
        设置指令应答
        
        CAN ID:
            0x476
        
        Args:
            instruction_index: 应答指令索引
                取设置指令 id 最后一个字节
                例如,应答 0x471 设置指令时此位填充0x71
            zero_config_success_flag: 零点是否设置成功
                零点成功设置-0x01
                设置失败/未设置-0x00
                仅在关节设置指令--成功设置 N 号电机当前位置为零点时应答-0x01
        '''
        '''
        Sets the response for the instruction.
        
        CAN ID: 0x476
        
        Args:
            instruction_index (int): The response instruction index.
                This is derived from the last byte of the set instruction ID.
                For example, when responding to the 0x471 set instruction, this would be 0x71.
            
            zero_config_success_flag (int): Flag indicating whether the zero point was successfully set.
                0x01: Zero point successfully set.
                0x00: Zero point set failed/not set.
                This is only applicable when responding to a joint setting instruction that successfully sets motor N's current position as the zero point.
        '''
        tx_can = Message()
        set_resp = ArmMsgInstructionResponseConfig(instruction_index, zero_config_success_flag)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgInstructionResponseConfig, arm_set_instruction_response=set_resp)
        self.__parser.EncodeMessage(msg, tx_can)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def ArmParamEnquiryAndConfig(self, 
                                 param_enquiry: Literal[0x00, 0x01, 0x02, 0x03] = 0x00, 
                                 param_setting: Literal[0x00, 0x01, 0x02] = 0x00, 
                                 data_feedback_0x48x: Literal[0x00, 0x01, 0x02] = 0x00, 
                                 end_load_param_setting_effective: Literal[0x00, 0xAE] = 0x00, 
                                 set_end_load: Literal[0x00, 0x01, 0x02, 0x03] = 0x03):
        '''
        机械臂参数查询与设置指令
        
        CAN ID:
            0x477
        
        Args:
            param_enquiry: 参数查询
                0x01 ->0x478,查询末端 V/acc
                
                0x02 ->0x47B,查询碰撞防护等级
                
                0x03 查询当前轨迹索引
                
            param_setting: 参数设置
                设置末端 V/acc 参数为初始值--0x01
                设置全部关节限位、关节最大速度、关节加速度为默认值--0x02
            data_feedback_0x48x: 0x48X报文反馈设置
                无效--0x00
                关闭周期反馈--0x01
                开启周期反馈--0x02
                开启后周期上报 1~6 号关节当前末端速度/加速度
            end_load_param_setting_effective: 末端负载参数设置是否生效,有效值-0xAE
            set_end_load: 设置末端负载
                0x00--空载
                0x01--半载
                0x02--满载
                0x03--无效
        '''
        '''
        Robotic arm parameter query and setting instruction.
        
        CAN ID:
            0x477
        
        Args:
            param_enquiry (int): Parameter enquiry.
                0x01 -> 0x478: Query end-effector velocity/acceleration
                0x02 -> 0x47B: Query collision protection level
                0x03: Query current trajectory index            
            param_setting (int): Parameter setting.
                0x01: Set end effector velocity/acceleration parameters to initial values.
                0x02: Set all joint limits, joint maximum speed, and joint acceleration to default values.
            
            data_feedback_0x48x (int): 0x48X message feedback settings.
                0x00: Invalid.
                0x01: Disable periodic feedback.
                0x02: Enable periodic feedback.
                When enabled, periodic reporting includes the current end effector speed/acceleration for joints 1-6.
            
            end_load_param_setting_effective (int): Whether the end load parameter setting is effective.
                Valid value: 0xAE.
            
            set_end_load (int): Set end load.
                0x00: No load.
                0x01: Half load.
                0x02: Full load.
                0x03: Invalid.
        '''
        tx_can = Message()
        search_set_arm_param = ArmMsgParamEnquiryAndConfig(param_enquiry, 
                                                           param_setting, 
                                                           data_feedback_0x48x, 
                                                           end_load_param_setting_effective,
                                                           set_end_load)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgParamEnquiryAndConfig, arm_param_enquiry_and_config=search_set_arm_param)
        self.__parser.EncodeMessage(msg, tx_can)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def EndSpdAndAccParamSet(self, 
                             end_max_linear_vel: int, 
                             end_max_angular_vel: int, 
                             end_max_linear_acc: int, 
                             end_max_angular_acc: int):
        '''
        末端速度/加
        速度参数设置
        指令
        
        CAN ID:
            0x479
        
        Args:
            end_max_linear_vel: 末端最大线速度,单位 0.001m/s
            end_max_angular_vel: 末端最大角速度,单位 0.001rad/s
            end_max_linear_acc: 末端最大线加速度,单位 0.001m/s^2
            end_max_angular_acc: 末端最大角加速度,单位 0.001rad/s^2
        '''
        '''
        Sets the end effector velocity/acceleration parameters.
        
        CAN ID: 0x479
        
        Args:
            end_max_linear_vel (int): The maximum linear velocity of the end effector, in 0.001 m/s.
            end_max_angular_vel (int): The maximum angular velocity of the end effector, in 0.001 rad/s.
            end_max_linear_acc (int): The maximum linear acceleration of the end effector, in 0.001 m/s^2.
            end_max_angular_acc (int): The maximum angular acceleration of the end effector, in 0.001 rad/s^2.
        '''
        tx_can = Message()
        end_set = ArmMsgEndVelAccParamConfig(end_max_linear_vel, 
                                            end_max_angular_vel, 
                                            end_max_linear_acc, 
                                            end_max_angular_acc,)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgEndVelAccParamConfig, arm_end_vel_acc_param_config=end_set)
        self.__parser.EncodeMessage(msg, tx_can)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def CrashProtectionConfig(self, 
                              joint_1_protection_level:int, 
                              joint_2_protection_level:int, 
                              joint_3_protection_level:int, 
                              joint_4_protection_level:int,
                              joint_5_protection_level:int,
                              joint_6_protection_level:int):
        '''
        碰撞防护等级
        设置指令
        
        CAN ID:
            0x47A
        
        有效值 : 0~8
        
        等级 0 代表不检测碰撞； 6个关节可以独立设置
        
        Args:
            joint_1_protection_level: 关节1的碰撞等级设定
            joint_2_protection_level: 关节2的碰撞等级设定
            joint_3_protection_level: 关节3的碰撞等级设定
            joint_4_protection_level: 关节4的碰撞等级设定
            joint_5_protection_level: 关节5的碰撞等级设定
            joint_6_protection_level: 关节6的碰撞等级设定
        '''
        '''
        End Effector Speed/Acceleration Parameter Setting Command
        
        CAN ID:
            0x47A
        
        Valid Values: 0~8
            Level 0 indicates no collision detection.
            Collision protection levels can be set independently for the six joints.
        
        Args:
            joint_1_protection_level: Collision protection level for Joint 1.
            joint_2_protection_level: Collision protection level for Joint 2.
            joint_3_protection_level: Collision protection level for Joint 3.
            joint_4_protection_level: Collision protection level for Joint 4.
            joint_5_protection_level: Collision protection level for Joint 5.
            joint_6_protection_level: Collision protection level for Joint 6.
        '''
        tx_can = Message()
        crash_config = ArmMsgCrashProtectionRatingConfig(joint_1_protection_level, 
                                                        joint_2_protection_level, 
                                                        joint_3_protection_level, 
                                                        joint_4_protection_level,
                                                        joint_5_protection_level,
                                                        joint_6_protection_level)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgCrashProtectionRatingConfig, arm_crash_protection_rating_config=crash_config)
        self.__parser.EncodeMessage(msg, tx_can)
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)

    def SearchPiperFirmwareVersion(self):
        '''
        发送piper机械臂固件版本查询指令
        
        CAN ID:
            0x4AF
        '''
        '''
        Send a firmware version query command for the Piper robotic arm.
        
        CAN ID:
            0x4AF
        '''
        tx_can = Message()
        tx_can.arbitration_id = 0x4AF
        tx_can.data = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        self.__firmware_data = bytearray()

#----------------------------------------------------------------------------------
    def GetSDKJointLimitParam(self,
                           joint_name: Literal["j1", "j2", "j3", "j4", "j5", "j6"]):
        return self.__piper_param_mag.GetJointLimitParam(joint_name)
    
    def GetSDKGripperRangeParam(self):
        return self.__piper_param_mag.GetGripperRangeParam()

    def SetSDKJointLimitParam(self, 
                            joint_name: Literal["j1", "j2", "j3", "j4", "j5", "j6"],
                            min_val: float, 
                            max_val: float):
        self.__piper_param_mag.SetJointLimitParam(joint_name, min_val, max_val)
    
    def SetSDKGripperRangeParam(self,
                             min_val: float, 
                             max_val: float):
        self.__piper_param_mag.SetGripperRangeParam(min_val, max_val)
