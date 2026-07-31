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
from ..hardware_port import *
from ..protocol.protocol_v2 import C_PiperParserV2
from ..piper_msgs.msg_v2 import *
from ..kinematics import *
from ..utils import *
from ..utils import logger, global_area
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
        dh_is_offset([0,1] -> default 0x01): Does the j1-j2 offset by 2° in the DH parameters? 
                    0 -> No offset
                    1 -> Offset applied
        start_sdk_joint_limit(bool -> False):Whether to enable the software joint limit of SDK
        start_sdk_gripper_limit(bool -> False):Whether to enable the software gripper limit of SDK
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
            self.arm_status = ArmMsgFeedbackStatus()
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
            self.end_pose=ArmMsgFeedBackEndPose()
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
            self.joint_state=ArmMsgFeedBackJointStates()
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
            self.gripper_state=ArmMsgFeedBackGripper()
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
            self.motor_1=ArmMsgFeedbackHighSpd()
            self.motor_2=ArmMsgFeedbackHighSpd()
            self.motor_3=ArmMsgFeedbackHighSpd()
            self.motor_4=ArmMsgFeedbackHighSpd()
            self.motor_5=ArmMsgFeedbackHighSpd()
            self.motor_6=ArmMsgFeedbackHighSpd()
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
            self.motor_1=ArmMsgFeedbackLowSpd()
            self.motor_2=ArmMsgFeedbackLowSpd()
            self.motor_3=ArmMsgFeedbackLowSpd()
            self.motor_4=ArmMsgFeedbackLowSpd()
            self.motor_5=ArmMsgFeedbackLowSpd()
            self.motor_6=ArmMsgFeedbackLowSpd()
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
            self.crash_protection_level_feedback=ArmMsgFeedbackCrashProtectionRating()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"crash_protection_level_feedback:{self.crash_protection_level_feedback}\n")
    
    class GripperTeachingPendantParamFeedback():
        '''
        夹爪/示教器参数反馈指令
        0x477 Byte 0 = 0x04 -> 0x47E
        '''
        '''
        Gripper/Teaching Pendant Parameter Feedback Command
        0x477 Byte 0 = 0x04 -> 0x47E
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.arm_gripper_teaching_param_feedback=ArmMsgFeedbackGripperTeachingPendantParam()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"arm_gripper_teaching_param_feedback:{self.arm_gripper_teaching_param_feedback}\n")
    
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
    
    class ArmModeCtrl():
        '''
        机械臂发送控制指令0x151的消息接收,由主臂发送
        '''
        '''
        The control command message 0x151 is sent by the main arm for reception
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.mode_ctrl=ArmMsgMotionCtrl_2()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.mode_ctrl}\n")
    
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
    
    class ArmRespSetInstruction():
        '''
        设置指令应答
        '''
        '''
        Sets the response for the instruction.
        '''
        def __init__(self):
            self.time_stamp: float=0
            self.instruction_response=ArmMsgFeedbackRespSetInstruction()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"{self.instruction_response}\n")

    _instances = {}  # 存储不同参数的实例
    _lock = threading.Lock()

    def __new__(cls, 
                can_name:str="can0", 
                judge_flag=True,
                can_auto_init=True,
                # reconnect_after_disconnection:bool = False,
                dh_is_offset: int = 0x01,
                start_sdk_joint_limit: bool = False,
                start_sdk_gripper_limit: bool = False,
                logger_level:LogLevel = LogLevel.WARNING,
                log_to_file:bool = False,
                log_file_path = None):
        """
        实现单例模式：
        - 相同 can_name参数，只会创建一个实例
        - 不同参数，允许创建新的实例
        """
        key = (can_name)  # 生成唯一 Key
        with cls._lock:
            if key not in cls._instances:
                instance = super().__new__(cls)  # 创建新实例
                instance._initialized = False  # 确保 init 只执行一次
                cls._instances[key] = instance  # 存入缓存
        return cls._instances[key]

    def __init__(self,
                can_name:str="can0",
                judge_flag=True,
                can_auto_init=True,
                # reconnect_after_disconnection:bool = False,
                dh_is_offset: int = 0x01,
                start_sdk_joint_limit: bool = False, 
                start_sdk_gripper_limit: bool = False,
                logger_level:LogLevel = LogLevel.WARNING,
                log_to_file:bool = False,
                log_file_path = None) -> None:
        if getattr(self, "_initialized", False): 
            return  # 避免重复初始化
        # log
        LogManager.update_logger(global_area=global_area,
                                 local_area="InterfaceV2", 
                                 level=logger_level, 
                                 log_to_file=log_to_file, 
                                 log_file_path=log_file_path,
                                 file_mode='a',
                                 force_update=True)
        self.__local_area = self._instances
        self.logger = LogManager.get_logger(global_area, self.__local_area)
        logging.getLogger("can").setLevel(logger_level)
        self.logger.info("CAN interface created")
        self.logger.info("%s = %s", "can_name", can_name)
        self.logger.info("%s = %s", "judge_flag", judge_flag)
        self.logger.info("%s = %s", "can_auto_init", can_auto_init)
        # self.logger.info("%s = %s", "reconnect_after_disconnection", reconnect_after_disconnection)
        self.logger.info("%s = %s", "dh_is_offset", dh_is_offset)
        self.logger.info("%s = %s", "start_sdk_joint_limit", start_sdk_joint_limit)
        self.logger.info("%s = %s", "start_sdk_gripper_limit", start_sdk_gripper_limit)
        self.logger.info("%s = %s", "logger_level", logger_level)
        self.logger.info("%s = %s", "log_to_file", log_to_file)
        self.logger.info("%s = %s", "log_file_path", LogManager.get_log_file_path(global_area))
        self.__can_channel_name:str
        if isinstance(can_name, str):
            self.__can_channel_name = can_name
        else:
            raise IndexError("C_PiperInterface_V2 input can name is not str type")
        self.__can_judge_flag = judge_flag
        self.__can_auto_init = can_auto_init
        # self.__reconnect_after_disconnection = reconnect_after_disconnection
        try:
            if(can_auto_init):
                self.__arm_can=C_STD_CAN(can_name, "socketcan", 1000000, judge_flag, True, self.ParseCANFrame)
            else:
                self.__arm_can=None
        except Exception as e:
            self.logger.error(e)
            raise ConnectionError("['%s' Interface __init__ ERROR]" % can_name)
            # self.logger.error("exit...")
            # exit()
        self.__dh_is_offset = dh_is_offset
        self.__piper_fk = C_PiperForwardKinematics(self.__dh_is_offset)
        self.__start_sdk_joint_limit = start_sdk_joint_limit
        self.__start_sdk_gripper_limit = start_sdk_gripper_limit
        self.__start_sdk_fk_cal = False
        self.__abnormal_data_filter = True
        self.__piper_param_mag = C_PiperParamManager()
        # protocol
        self.__parser: Type[C_PiperParserV2] = C_PiperParserV2()
        # thread
        self.__read_can_stop_event = threading.Event()  # 控制 ReadCan 线程
        self.__can_monitor_stop_event = threading.Event()  # 控制 CanMonitor 线程
        self.__lock = threading.Lock()  # 保护线程安全
        self.__can_deal_th = None
        self.__can_monitor_th = None
        self.__connected = False  # 连接状态
        # FPS cal
        self.__fps_counter = C_FPSCounter()
        self.__fps_counter.set_cal_fps_time_interval(0.1)
        self.__fps_counter.add_variable("CanMonitor")
        self.__q_can_fps = Queue(maxsize=5)
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
        self.__fps_counter.add_variable("ArmModeCtrl")
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
        
        self.__feedback_gripper_teaching_pendant_param_mtx = threading.Lock()
        self.__feedback_gripper_teaching_pendant_param = self.GripperTeachingPendantParamFeedback()

        self.__feedback_current_motor_max_acc_limit_mtx = threading.Lock()
        self.__feedback_current_motor_max_acc_limit = self.CurrentMotorMaxAccLimit()

        self.__arm_joint_ctrl_msgs_mtx = threading.Lock()
        self.__arm_joint_ctrl_msgs = self.ArmJointCtrl()
        
        self.__arm_gripper_ctrl_msgs_mtx = threading.Lock()
        self.__arm_gripper_ctrl_msgs = self.ArmGripperCtrl()

        self.__arm_ctrl_code_151_mtx = threading.Lock()
        self.__arm_ctrl_code_151 = self.ArmCtrlCode_151()
        self.__arm_mode_ctrl_mtx = threading.Lock()
        self.__arm_mode_ctrl = self.ArmModeCtrl()
        
        self.__arm_all_motor_max_acc_limit_mtx = threading.Lock()
        self.__arm_all_motor_max_acc_limit = self.AllCurrentMotorMaxAccLimit()
        
        self.__arm_all_motor_angle_limit_max_spd_mtx = threading.Lock()
        self.__arm_all_motor_angle_limit_max_spd = self.AllCurrentMotorAngleLimitMaxSpd()

        self.__feedback_instruction_response_mtx = threading.Lock()
        self.__feedback_instruction_response = self.ArmRespSetInstruction()

        self._initialized = True  # 标记已初始化
    
    @classmethod
    def get_instance(cls, can_name="can0", judge_flag=True, can_auto_init=True):
        '''Get a class instance object

        Returns:
            cls: The instance object of the current class
        '''
        return cls(can_name, judge_flag, can_auto_init)
    
    def get_connect_status(self):
        '''Get connect status

        Returns:
            bool: The return value. True for success, False otherwise.
        '''
        return self.__connected

    def CreateCanBus(self, 
                    can_name:str, 
                    bustype="socketcan", 
                    expected_bitrate:int=1000000,
                    judge_flag:bool=False):
        '''
        创建can有关的接口
        
        Args:
            can_name: can的端口名称
            bustype: can总线类型,默认为'socketcan',如果是串口can模块需要改为'slcan'
            expected_bitrate: 预期can总线的波特率
            judge_flag: 是否在实例化该类时进行can端口判断,有些情况需要False 
        '''
        '''
        Create can related interfaces

        Args:
            can_name: The name of the CAN port.
            bustype: CAN bus type, the default is 'socketcan', if it is a serial port CAN module, it needs to be changed to 'slcan'.
            expected_bitrate: The expected bitrate for the CAN bus.
            judge_flag: Whether to check the CAN port during the instantiation of the class. In some cases, it should be set to False.
        '''
        try:
            self.__arm_can=C_STD_CAN(can_name, bustype, expected_bitrate, judge_flag, False, self.ParseCANFrame)
            self.__arm_can.Init()
        except Exception as e:
            self.logger.error(e)
            raise ConnectionError("['%s' CreateCanBus ERROR]" % can_name)

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
        if(self.__arm_can is None):
            raise ValueError("Interface 'can_auto_init' is False and '__arm_can' is None!! \n" \
            "['%s' ConnectPort ERROR] When 'can_auto_init' is False, execute 'CreateCanBus' to initialize " \
            "'__arm_can' first and then execute 'ConnectPort'" % self.__can_channel_name)
        if(can_init or not self.__connected):
            self.logger.info("[ConnectPort] Start Can Init")
            init_status = None
            try:
                # self.__arm_can=C_STD_CAN(self.__can_channel_name, "socketcan", 1000000, False, False, self.ParseCANFrame)
                init_status = self.__arm_can.Init()
            except Exception as e:
                # self.__arm_can = None
                self.logger.error("[ConnectPort] can bus create: %s", e)
            self.logger.info("[ConnectPort] init_status: %s", init_status)
        # 检查线程是否开启
        with self.__lock:
            if self.__connected:
                return
            self.__connected = True
            self.__read_can_stop_event.clear()
            self.__can_monitor_stop_event.clear()  # 允许线程运行
        # 读取can数据线程----------------------------------------------------------
        def ReadCan():
            self.logger.info("[ReadCan] ReadCan Thread started")
            while not self.__read_can_stop_event.is_set():
                # self.__fps_counter.increment("CanMonitor")
                # if(self.__arm_can is None):
                #     try:
                #         self.logger.debug("[ReadCan] __arm_can create")
                #         self.__arm_can=C_STD_CAN(self.__can_channel_name, "socketcan", 1000000, self.__can_judge_flag, False, self.ParseCANFrame)
                #     except Exception as e:
                #         pass
                #     continue
                try:
                    read_status = self.__arm_can.ReadCanMessage()
                    # if(read_status != self.__arm_can.CAN_STATUS.READ_CAN_MSG_OK):
                    #     time.sleep(0.00002)
                    # if self.__reconnect_after_disconnection:
                    #     if(read_status != self.__arm_can.CAN_STATUS.READ_CAN_MSG_OK):
                    #         try:
                    #             self.logger.debug("[ReadCan] can_reconnect -> close")
                    #             self.__arm_can.Close()
                    #             self.logger.debug("[ReadCan] can_reconnect -> init")
                    #             self.__arm_can.Init()
                    #         except Exception as e:
                    #             pass
                    # self.logger.debug("[ReadCan] read_status: %s", read_status)
                except can.CanOperationError:
                    self.logger.error("[ReadCan] CAN is closed, stop ReadCan thread")
                    break
                except Exception as e:
                    self.logger.error("[ReadCan] 'error: %s'", e)
                    break
        #--------------------------------------------------------------------------
        def CanMonitor():
            self.logger.info("[ReadCan] CanMonitor Thread started")
            while not self.__can_monitor_stop_event.is_set():
                try:
                    self.__CanMonitor()
                except Exception as e:
                    self.logger.error("CanMonitor() exception: %s", e)
                    break
                # try:
                #     self.__CanMonitor()
                #     is_exist = self.__arm_can.is_can_socket_available(self.__can_channel_name)
                #     is_up = self.__arm_can.is_can_port_up(self.__can_channel_name)
                #     if(is_exist != self.__arm_can.CAN_STATUS.CHECK_CAN_EXIST or 
                #        is_up != self.__arm_can.CAN_STATUS.CHECK_CAN_UP):
                #         print("[ERROR] CanMonitor ", is_exist, is_up)
                # except Exception as e:
                #     print(f"[ERROR] CanMonitor() 发生异常: {e}")
                #     # break
                self.__can_monitor_stop_event.wait(0.05)
        #--------------------------------------------------------------------------

        try:
            if start_thread:
                if not self.__can_deal_th or not self.__can_deal_th.is_alive():
                    self.__can_deal_th = threading.Thread(target=ReadCan, daemon=True)
                    self.__can_deal_th.start()
                if not self.__can_monitor_th or not self.__can_monitor_th.is_alive():
                    self.__can_monitor_th = threading.Thread(target=CanMonitor, daemon=True)
                    self.__can_monitor_th.start()
                self.__fps_counter.start()
            if piper_init and self.__arm_can is not None:
                self.PiperInit()
        except Exception as e:
            self.logger.error("[ConnectPort] 'Thread start failed: %s'", e)
            self.__connected = False  # 回滚状态
            self.__read_can_stop_event.set()
            self.__can_monitor_stop_event.set()  # 确保线程不会意外运行
    
    def DisconnectPort(self, thread_timeout=0.1):
        '''
        Disconnect the port without blocking the main thread
        
        Args:
            thread_timeout(float): Same as threading.Thread.join(timeout=thread_timeout)
        '''
        with self.__lock:
            if not self.__connected:
                return
            self.__connected = False
            self.__read_can_stop_event.set()

        if hasattr(self, 'can_deal_th') and self.__can_deal_th.is_alive():
            self.__can_deal_th.join(timeout=thread_timeout)  # 加入超时，避免无限阻塞
            if self.__can_deal_th.is_alive():
                self.logger.warning("[DisconnectPort] The [ReadCan] thread failed to exit within the timeout period")

        # if hasattr(self, 'can_monitor_th') and self.__can_monitor_th.is_alive():
        #     self.__can_monitor_th.join(timeout=thread_timeout)
        #     if self.__can_monitor_th.is_alive():
        #         self.logger.warning("The CanMonitor thread failed to exit within the timeout period")

        try:
            self.__arm_can.Close()  # 关闭 CAN 端口
            self.logger.info("[DisconnectPort] CAN port is closed")
        except Exception as e:
            self.logger.error("[DisconnectPort] 'An exception occurred while closing the CAN port: %s'", e)
    
    def PiperInit(self):
        '''
        发送查询关节电机最大角度速度指令
        发送查询关节电机最大加速度限制指令
        发送查询机械臂固件指令
        '''
        self.SearchAllMotorMaxAngleSpd()
        self.SearchAllMotorMaxAccLimit()
        self.SearchPiperFirmwareVersion()

    def EnableFkCal(self):
        '''
        Enable fk calculation

        Returns
        -------
            bool: The state of the fk cal flag
        '''
        self.__start_sdk_fk_cal = True
        return self.__start_sdk_fk_cal

    def DisableFkCal(self):
        '''
        Disable fk calculation

        Returns
        -------
            bool: The state of the fk cal flag
        '''
        self.__start_sdk_fk_cal = False
        return self.__start_sdk_fk_cal
    
    def isCalFk(self):
        '''
        Returns
        -------
            bool: The state of the fk cal flag
        '''
        return self.__start_sdk_fk_cal

    def EnableFilterAbnormalData(self):
        '''
        Enable filter abnormal data,joint data or end pose data

        Returns
        -------
            bool: Enable abnormal data filtering
        '''
        self.__abnormal_data_filter = True
        return self.__abnormal_data_filter

    def DisableFilterAbnormalData(self):
        '''
        Disable filter abnormal data,joint data or end pose data

        Returns
        -------
            bool: Disable abnormal data filtering
        '''
        self.__abnormal_data_filter = False
        return self.__abnormal_data_filter

    def isFilterAbnormalData(self):
        '''
        Returns
        -------
            bool: Whether to filter abnormal data, True to enable filtering
        '''
        return self.__abnormal_data_filter

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
            self.__UpdateGripperTeachingPendantParamFeedback(msg)
            self.__UpdateCurrentMotorAngleLimitMaxVel(msg)
            self.__UpdateCurrentMotorMaxAccLimit(msg)
            self.__UpdateAllCurrentMotorAngleLimitMaxVel(msg)
            self.__UpdateAllCurrentMotorMaxAccLimit(msg)
            # 更新主臂发送消息
            self.__UpdateArmJointCtrl(msg)
            self.__UpdateArmGripperCtrl(msg)
            self.__UpdateArmCtrlCode151(msg)
            self.__UpdateArmModeCtrl(msg)
            self.__UpdatePiperFirmware(msg)
            self.__UpdateRespSetInstruction(msg)
            if self.__start_sdk_fk_cal:
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
    def __GetCurrentTime(self):
        return time.time_ns() / 1e9
    
    def GetCanBus(self):
        '''
        Returns
        -------
        self.__arm_can : C_STD_CAN
            can encapsulation class, which contains some socketcan related functions
        '''
        return self.__arm_can

    def GetCanName(self):
        '''
        Returns
        -------
        can_name : str
            The CAN port name read in the current class
        '''
        return self.__can_channel_name

    def GetCurrentInterfaceVersion(self):
        '''
        Returns
        -------
            current interface version
        '''
        return InterfaceVersion.INTERFACE_V2
    
    def GetCurrentSDKVersion(self):
        '''
        Returns
        -------
            piper_sdk current version
        '''
        return PiperSDKVersion.PIPER_SDK_CURRENT_VERSION
    
    def GetCurrentProtocolVersion(self):
        '''
        Returns
        -------
            return piper_sdk current prptocol version
        '''
        return self.__parser.GetParserProtocolVersion()
    
    def GetCanFps(self):
        '''
        Get the frame rate of the robotic arm CAN module

        Returns
        -------
            float
        '''
        return self.__fps_counter.get_fps("CanMonitor")
    
    def GetArmStatus(self):
        '''
        Retrieves the current status of the robotic arm.

        CAN ID:
            0x2A1

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        arm_status : ArmMsgFeedbackStatus
            机械臂状态

            - ctrl_mode (int): 控制模式
                * 0x00 待机模式
                * 0x01 CAN指令控制模式
                * 0x02 示教模式
            - arm_status (int): 机械臂状态
                * 0x00 正常
                * 0x01 急停
                * 0x02 无解
                * 0x03 奇异点
                * 0x04 目标角度超过限
                * 0x05 关节通信异常
                * 0x06 关节抱闸未打开
                * 0x07 机械臂发生碰撞
                * 0x08 拖动示教时超速
                * 0x09 关节状态异常
                * 0x0A 其它异常
                * 0x0B 示教记录
                * 0x0C 示教执行
                * 0x0D 示教暂停
                * 0x0E 主控NTC过温
                * 0x0F 释放电阻NTC过温
            - mode_feed (int): 模式反馈
                * 0x00 MOVE P
                * 0x01 MOVE J
                * 0x02 MOVE L
                * 0x03 MOVE C
                * 0x04 MOVE M ---基于V1.5-2版本后
                * 0x05 MOVE_CPV ---基于V1.6.5版本后
            - teach_status (int): 示教状态
            - motion_status (int): 运动状态
                * 0x00 到达指定点位
                * 0x01 未到达指定点位
            - trajectory_num (int): 当前运行轨迹点序号
            - err_status (int): 故障状态
            {
                * joint_1_angle_limit (bool): 1号关节角度是否超限位, True为超限
                * joint_2_angle_limit (bool): 2号关节角度是否超限位, True为超限
                * joint_3_angle_limit (bool): 3号关节角度是否超限位, True为超限
                * joint_4_angle_limit (bool): 4号关节角度是否超限位, True为超限
                * joint_5_angle_limit (bool): 5号关节角度是否超限位, True为超限
                * joint_6_angle_limit (bool): 6号关节角度是否超限位, True为超限
                * communication_status_joint_1 (bool): 1号关节通信是否异常, True为通信异常
                * communication_status_joint_2 (bool): 2号关节通信是否异常, True为通信异常
                * communication_status_joint_3 (bool): 3号关节通信是否异常, True为通信异常
                * communication_status_joint_4 (bool): 4号关节通信是否异常, True为通信异常
                * communication_status_joint_5 (bool): 5号关节通信是否异常, True为通信异常
                * communication_status_joint_6 (bool): 6号关节通信是否异常, True为通信异常
            }
        '''
        with self.__arm_status_mtx:
            self.__arm_status.Hz = self.__fps_counter.get_fps("ArmStatus")
            return self.__arm_status

    def GetArmEndPoseMsgs(self):
        '''
        Retrieves the end effector pose message of the robotic arm. Euler angle representation.

        Returns
        -------
        time_stamp : float
        Hz : float
        end_pose : ArmMsgFeedBackEndPose

            - X_axis (int): X position, (in 0.001 mm)
            - Y_axis (int): Y position, (in 0.001 mm)
            - Z_axis (int): Z position, (in 0.001 mm)
            - RX_axis (int): RX orientation, (in 0.001 degrees)
            - RY_axis (int): RY orientation, (in 0.001 degrees)
            - RZ_axis (int): RZ orientation, (in 0.001 degrees)
        '''
        with self.__arm_end_pose_mtx:
            self.__arm_end_pose.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_fps('ArmEndPose_XY'),
                                                                  self.__fps_counter.get_fps('ArmEndPose_ZRX'),
                                                                  self.__fps_counter.get_fps('ArmEndPose_RYRZ'))
            return self.__arm_end_pose

    def GetArmJointMsgs(self):
        '''
        Retrieves the joint status message of the robotic arm.(in 0.001 degrees)

        Returns
        -------
        time_stamp : float
        Hz : float
        joint_state : ArmMsgFeedBackJointStates

            - joint_1 (int): Feedback angle of joint 1, (in 0.001 degrees).
            - joint_2 (int): Feedback angle of joint 2, (in 0.001 degrees).
            - joint_3 (int): Feedback angle of joint 3, (in 0.001 degrees).
            - joint_4 (int): Feedback angle of joint 4, (in 0.001 degrees).
            - joint_5 (int): Feedback angle of joint 5, (in 0.001 degrees).
            - joint_6 (int): Feedback angle of joint 6, (in 0.001 degrees).
        '''
        with self.__arm_joint_msgs_mtx:
            self.__arm_joint_msgs.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_fps('ArmJoint_12'),
                                                                    self.__fps_counter.get_fps('ArmJoint_34'),
                                                                    self.__fps_counter.get_fps('ArmJoint_56'))
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
        '''
        Retrieves the gripper status message of the robotic arm.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        gripper_state : ArmMsgFeedBackGripper

            - grippers_angle (int): The stroke of the gripper (in 0.001 mm).
            - grippers_effort (int): The torque of the gripper (in 0.001 N·m).
            - foc_status (int):  The status code of the gripper.
            {
                * voltage_too_low (bool): Power voltage low (False: Normal, True: Low)
                * motor_overheating (bool): Motor over-temperature (False: Normal, True: Over-temperature)
                * driver_overcurrent (bool): Driver over-current (False: Normal, True: Over-current)
                * driver_overheating (bool): Driver over-temperature (False: Normal, True: Over-temperature)
                * sensor_status (bool): Sensor status (False: Normal, True: Abnormal)
                * driver_error_status (bool): Driver error status (False: Normal, True: Error)
                * driver_enable_status (bool): Driver enable status (False: Disabled, True: Enabled)
                * homing_status (bool): Zeroing status (False: Not zeroed, True: Zeroed or previously zeroed)
            }
        '''
        with self.__arm_gripper_msgs_mtx:
            self.__arm_gripper_msgs.Hz = self.__fps_counter.get_fps('ArmGripper')
            return self.__arm_gripper_msgs
    
    def GetArmHighSpdInfoMsgs(self):
        '''
        Retrieves the high-speed feedback message of the robotic arm.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        motor_x : ArmMsgFeedbackHighSpd

            - can_id (int): Current CAN ID, used to represent the joint number.
            - motor_speed (int): Motor Speed (in 0.001rad/s).
            - current (int): Motor  (in 0.001A).
            - pos (int): Motor Position (rad).
            - effort (int): Torque converted using a fixed coefficient, (in 0.001 N/m).
        '''
        with self.__arm_motor_info_high_spd_mtx:
            self.__arm_motor_info_high_spd.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_fps('ArmMotorDriverInfoHighSpd_1'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoHighSpd_2'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoHighSpd_3'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoHighSpd_4'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoHighSpd_5'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoHighSpd_6'))
            return self.__arm_motor_info_high_spd
    
    def GetMotorStates(self):
        '''
        Retrieves the robot arm motor status message of the robotic arm.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        motor_x : ArmMsgFeedbackHighSpd

            - can_id (int): Current CAN ID, used to represent the joint number.
            - motor_speed (int): Motor Speed (in 0.001rad/s).
            - current (int): Motor  (in 0.001A).
            - pos (int): Motor Position (rad).
            - effort (int): Torque converted using a fixed coefficient, (in 0.001 N/m).
        '''
        return self.GetArmHighSpdInfoMsgs()

    def GetArmLowSpdInfoMsgs(self):
        '''
        Retrieves the low-speed feedback message of the robotic arm.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        motor_x : ArmMsgFeedbackLowSpd

            - can_id (int): CAN ID, representing the current motor number.
            - vol (int): Current driver voltage (in 0.1V).
            - foc_temp (int): Driver temperature (in 1℃).
            - motor_temp (int): Motor temperature (in 1℃).
            - foc_status (int): Driver status.
            {
                * voltage_too_low (bool): Power voltage low (False: Normal, True: Low)
                * motor_overheating (bool): Motor over-temperature (False: Normal, True: Over-temperature)
                * driver_overcurrent (bool): Driver over-current (False: Normal, True: Over-current)
                * driver_overheating (bool): Driver over-temperature (False: Normal, True: Over-temperature)
                * collision_status (bool): Collision protection status (False: Normal, True: Trigger protection)
                * driver_error_status (bool): Driver error status (False: Normal, True: Error)
                * driver_enable_status (bool): Driver enable status (False: Disabled, True: Enabled)
                * stall_status (bool): Stalling protection status (False: Normal, True: Trigger protection)
            }
            - bus_current (int): Current driver current (in 0.001A).
        '''
        with self.__arm_motor_info_low_spd_mtx:
            self.__arm_motor_info_low_spd.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_fps('ArmMotorDriverInfoLowSpd_1'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoLowSpd_2'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoLowSpd_3'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoLowSpd_4'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoLowSpd_5'),
                                                                            self.__fps_counter.get_fps('ArmMotorDriverInfoLowSpd_6'))
            return self.__arm_motor_info_low_spd
    
    def GetDriverStates(self):
        '''
        Retrieves the robot drive status message of the robotic arm.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        motor_x : ArmMsgFeedbackLowSpd

            - can_id (int): CAN ID, representing the current motor number.
            - vol (int): Current driver voltage (in 0.1V).
            - foc_temp (int): Driver temperature (in 1℃).
            - motor_temp (int): Motor temperature (in 1℃).
            - foc_status (int): Driver status.
            {
                * voltage_too_low (bool): Power voltage low (False: Normal, True: Low)
                * motor_overheating (bool): Motor over-temperature (False: Normal, True: Over-temperature)
                * driver_overcurrent (bool): Driver over-current (False: Normal, True: Over-current)
                * driver_overheating (bool): Driver over-temperature (False: Normal, True: Over-temperature)
                * collision_status (bool): Collision protection status (False: Normal, True: Trigger protection)
                * driver_error_status (bool): Driver error status (False: Normal, True: Error)
                * driver_enable_status (bool): Driver enable status (False: Disabled, True: Enabled)
                * stall_status (bool): Stalling protection status (False: Normal, True: Trigger protection)
            }
            - bus_current (int): Current driver current (in 0.001A).
        '''
        return self.GetArmLowSpdInfoMsgs()

    def GetArmEnableStatus(self)->list:
        '''
        Get the robot arm enable status

        Returns
        -------
            list : bool
        '''
        enable_list = []
        enable_list.append(self.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_enable_status)
        enable_list.append(self.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_enable_status)
        enable_list.append(self.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_enable_status)
        enable_list.append(self.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_enable_status)
        enable_list.append(self.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_enable_status)
        enable_list.append(self.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_enable_status)
        return enable_list
    
    def GetCurrentMotorAngleLimitMaxVel(self):
        '''获取电机角度限制/最大速度指令
        
        包括最大角度限制,最小角度限制,最大关节速度
        
        为主动发送指令后反馈消息
        
        对应查询电机角度/最大速度/最大加速度限制指令 0x472 Byte 1 = 0x01
        
        ArmParamEnquiryAndConfig(param_enquiry=0x01)
        
        CAN ID:
            0x473

        Returns
        -------
        time_stamp : float
            time stamp
        current_motor_angle_limit_max_vel : ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd

            - motor_num (int): 关节电机序号
            - max_angle_limit (int): 最大角度限制, 单位 0.1度
            - min_angle_limit (int): 最小角度限制, 单位 0.1度
            - max_joint_spd (int): 最大关节速度, 单位 0.001rad/s
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
        
        Returns
        -------
        time_stamp : float
            time stamp
        current_end_vel_acc_param : ArmMsgFeedbackCurrentEndVelAccParam

            - end_max_linear_vel (int): 末端最大线速度, 单位 0.001m/s
            - end_max_angular_vel (int): 末端最大角速度, 单位 0.001rad/s
            - end_max_linear_acc (int): 末端最大线加速度, 单位 0.001m/s^2
            - end_max_angular_acc (int): 末端最大角加速度, 单位 0.001rad/s^2
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
        
        Returns
        -------
        time_stamp : float
        crash_protection_level_feedback : ArmMsgFeedbackCrashProtectionRating

            - joint_1_protection_level (int): 1号关节碰撞防护等级
            - joint_2_protection_level (int): 2号关节碰撞防护等级
            - joint_3_protection_level (int): 3号关节碰撞防护等级
            - joint_4_protection_level (int): 4号关节碰撞防护等级
            - joint_5_protection_level (int): 5号关节碰撞防护等级
            - joint_6_protection_level (int): 6号关节碰撞防护等级
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
    
    def GetGripperTeachingPendantParamFeedback(self):
        '''夹爪/示教器参数反馈指令
        
        包括示教器行程系数反馈、夹爪/示教器最大控制行程限制值反馈,
        
        为主动发送指令后反馈消息,
        
        对应机械臂参数查询与设置指令 0x477 Byte 0 = 0x04
        
        ArmParamEnquiryAndConfig(param_enquiry=0x04)
        
        CAN ID:
            0x47E
        
        Returns
        -------
        time_stamp : float
            time stamp
        arm_gripper_teaching_param_feedback : ArmMsgFeedbackGripperTeachingPendantParam

            - teaching_range_per (int): 示教器行程系数反馈,仅适用于设置主从臂的主臂，用于放大控制行程给从臂,范围[100~200]
            - max_range_config (int): 夹爪/示教器最大控制行程限制值反馈,(0,70,100)
                无效值---0
                小夹爪为---70mm
                大夹爪为---100mm
            - teaching_friction (int): 示教器摩擦系数设置,范围[1, 10]
        '''
        '''Gripper/Teaching Pendant Parameter Feedback Command
        This includes the following information:
            Teaching pendant travel coefficient
            Maximum control travel limit values for gripper/teaching pendant
        This is the feedback message after actively sending a command.
        Corresponds to robotic arm parameter query and setting command 0x477, Byte 0 = 0x04
        ArmParamEnquiryAndConfig(param_enquiry=0x04)
        
        CAN ID:
            0x47E
        '''
        with self.__feedback_gripper_teaching_pendant_param_mtx:
            return self.__feedback_gripper_teaching_pendant_param

    def GetCurrentMotorMaxAccLimit(self):
        '''获取当前电机最大加速度限制
        
        当前电机序号,当前电机的最大关节加速度

        Returns
        -------
        time_stamp : float
            time stamp
        current_motor_max_acc_limit : ArmMsgFeedbackCurrentMotorMaxAccLimit

            - joint_motor_num (int): 关节电机序号
            - max_joint_acc (int): 最大关节加速度, 单位 0.001rad/^2
        '''
        '''Retrieves the current motor's maximum acceleration limit.

        This includes the following information:
            Current motor number
            The maximum joint acceleration of the current motor
        '''
        with self.__feedback_current_motor_max_acc_limit_mtx:
            return self.__feedback_current_motor_max_acc_limit
    
    def GetArmJointCtrl(self):
        '''
        Retrieves the 0x155, 0x156, and 0x157 control commands, which are joint control commands.(in 0.001 degrees)

        Returns
        -------
        time_stamp : float
        Hz : float
        joint_ctrl : ArmMsgFeedBackJointStates

            - joint_1 (int): Feedback angle of joint 1, in 0.001 degrees.
            - joint_2 (int): Feedback angle of joint 2, in 0.001 degrees.
            - joint_3 (int): Feedback angle of joint 3, in 0.001 degrees.
            - joint_4 (int): Feedback angle of joint 4, in 0.001 degrees.
            - joint_5 (int): Feedback angle of joint 5, in 0.001 degrees.
            - joint_6 (int): Feedback angle of joint 6, in 0.001 degrees.
        '''
        with self.__arm_joint_ctrl_msgs_mtx:
            self.__arm_joint_ctrl_msgs.Hz = self.__fps_counter.cal_average(self.__fps_counter.get_fps('ArmJointCtrl_12'),
                                                                        self.__fps_counter.get_fps('ArmJointCtrl_34'),
                                                                        self.__fps_counter.get_fps('ArmJointCtrl_56'))
            return self.__arm_joint_ctrl_msgs
    
    def GetArmGripperCtrl(self):
        '''
        Retrieves the gripper control message using the 0x159 command.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        gripper_ctrl : ArmMsgGripperCtrl

            - grippers_angle (int): The stroke of the gripper (in 0.001 mm).
            - grippers_effort (int): Gripper torque, represented as an integer, unit: 0.001N·m.Range 0-5000 (corresponse 0-5N/m)
            - status_code (int): 
                0x00: Disabled;
                0x01: Enabled;
                0x03: Enable and clear errors;
                0x02: Disable and clear errors.
            - set_zero (int): Set the current position as the zero point.
                0x00: Invalid;
                0xAE: Set zero.
        '''
        with self.__arm_gripper_ctrl_msgs_mtx:
            self.__arm_gripper_ctrl_msgs.Hz = self.__fps_counter.get_fps("ArmGripperCtrl")
            return self.__arm_gripper_ctrl_msgs
    
    def GetArmCtrlCode151(self):
        '''
        Retrieves the 0x151 control command, which is the robotic arm mode control command.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        ctrl_151 : ArmMsgMotionCtrl_2

            - ctrl_mode (int): Control mode.
                * 0x00: Standby mode.
                * 0x01: CAN command control mode.
                * 0x03: Ethernet control mode.
                * 0x04: Wi-Fi control mode.
                * 0x07: Offline trajectory mode.
            - move_mode (int): MOVE mode.
                * 0x00: MOVE P (Position).
                * 0x01: MOVE J (Joint).
                * 0x02: MOVE L (Linear).
                * 0x03: MOVE C (Circular).
                * 0x04: MOVE M (MIT)
            - move_spd_rate_ctrl (int): Movement speed as a percentage.Range: 0~100.
            - mit_mode (int): MIT mode.
                * 0x00: Position-speed mode.
                * 0xAD: MIT mode.
                * 0xFF: Invalid.
            - residence_time (int): Hold time at offline trajectory points.
                Range: 0~255, unit: seconds.
            - installation_pos (int): Installation Position - Note: Wiring should face 
            {
                * 0x00: Invalid value
                * 0x01: Horizontal upright
                * 0x02: Left-side mount
                * 0x03: Right-side mount
            }
        '''
        with self.__arm_ctrl_code_151_mtx:
            self.__arm_ctrl_code_151.Hz = self.__fps_counter.get_fps("ArmCtrlCode_151")
            return self.__arm_ctrl_code_151
    
    def GetArmModeCtrl(self):
        '''
        Retrieves the 0x151 control command, which is the robotic arm mode control command.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        ctrl_151 : ArmMsgMotionCtrl_2

            - ctrl_mode (int): Control mode.
                * 0x00: Standby mode.
                * 0x01: CAN command control mode.
                * 0x03: Ethernet control mode.
                * 0x04: Wi-Fi control mode.
                * 0x07: Offline trajectory mode.
            - move_mode (int): MOVE mode.
                * 0x00: MOVE P (Position).
                * 0x01: MOVE J (Joint).
                * 0x02: MOVE L (Linear).
                * 0x03: MOVE C (Circular).
                * 0x04: MOVE M (MIT)
            - move_spd_rate_ctrl (int): Movement speed as a percentage.Range: 0~100.
            - mit_mode (int): MIT mode.
                * 0x00: Position-speed mode.
                * 0xAD: MIT mode.
                * 0xFF: Invalid.
            - residence_time (int): Hold time at offline trajectory points.
                Range: 0~255, unit: seconds.
            - installation_pos (int): Installation Position - Note: Wiring should face 
            {
                * 0x00: Invalid value
                * 0x01: Horizontal upright
                * 0x02: Left-side mount
                * 0x03: Right-side mount
            }
        '''
        with self.__arm_mode_ctrl_mtx:
            self.__arm_mode_ctrl.Hz = self.__fps_counter.get_fps("ArmModeCtrl")
            return self.__arm_mode_ctrl

    
    def GetAllMotorMaxAccLimit(self):
        '''获取所有电机的最大加速度限制,(m1-m6)
        
        此为应答式消息,意为需要发送请求指令该数据才会有数值
        
        Returns
        -------
        time_stamp : float
            time stamp
        
        all_motor_max_acc_limit : ArmMsgFeedbackAllCurrentMotorMaxAccLimit

            - motor (ArmMsgFeedbackCurrentMotorMaxAccLimit): 当前电机最大加速度限制
            {
                * joint_motor_num (int): 关节电机序号
                * max_joint_acc (int): 最大关节加速度, 单位 0.001rad/^2
            }
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

        Returns
        -------
        time_stamp : float
            time stamp
        
        all_motor_angle_limit_max_spd : ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd

            - motor (ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd): 当前电机限制角度/最大速度
            {
                * motor_num (int): 关节电机序号
                * max_angle_limit (int): 最大角度限制, 单位 0.1度
                * min_angle_limit (int): 最小角度限制, 单位 0.1度
                * max_joint_spd (int): 最大关节速度, 单位 0.001rad/s
            }
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
    
    def GetRespInstruction(self):
        '''
        Sets the response for the instruction.
        
        CAN ID: 0x476
        
        Returns
        -------
        time_stamp : float
            time stamp
        
        instruction_index (int): The response instruction index.
            This is derived from the last byte of the set instruction ID.
            For example, when responding to the 0x471 set instruction, this would be 0x71.
        
        zero_config_success_flag (int): Flag indicating whether the zero point was successfully set.
            - 0x01: Zero point successfully set.
            - 0x00: Zero point set failed/not set.
            - This is only applicable when responding to a joint setting instruction that successfully sets motor N's current position as the zero point.
        '''
        with self.__feedback_instruction_response_mtx:
            return self.__feedback_instruction_response

    def isOk(self):
        '''
        Feedback on whether the CAN data reading thread is functioning normally

        Returns
        -------
        bool: 
            True is normal
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
                self.__arm_status.time_stamp = msg.time_stamp
                self.__arm_status.arm_status.ctrl_mode = msg.arm_status_msgs.ctrl_mode
                self.__arm_status.arm_status.arm_status = msg.arm_status_msgs.arm_status
                self.__arm_status.arm_status.mode_feed = msg.arm_status_msgs.mode_feed
                self.__arm_status.arm_status.teach_status = msg.arm_status_msgs.teach_status
                self.__arm_status.arm_status.motion_status = msg.arm_status_msgs.motion_status
                self.__arm_status.arm_status.trajectory_num = msg.arm_status_msgs.trajectory_num
                self.__arm_status.arm_status.err_code = msg.arm_status_msgs.err_code
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
            if(msg.type_ == ArmMsgType.PiperMsgEndPoseFeedback_1):
                if self.isFilterAbnormalData():
                    # 1m * 1000 * 1000
                    if abs(msg.arm_end_pose.X_axis) > 1e6 or abs(msg.arm_end_pose.Y_axis) > 1e6:
                        return
                self.__fps_counter.increment("ArmEndPose_XY")
                self.__arm_end_pose.time_stamp = msg.time_stamp
                self.__arm_end_pose.end_pose.X_axis = msg.arm_end_pose.X_axis
                self.__arm_end_pose.end_pose.Y_axis = msg.arm_end_pose.Y_axis
            elif(msg.type_ == ArmMsgType.PiperMsgEndPoseFeedback_2):
                if self.isFilterAbnormalData():
                    # 1m * 1000 * 1000
                    if abs(msg.arm_end_pose.Z_axis) > 1e6:
                        return
                    # 361 degree * 1000
                    if abs(msg.arm_end_pose.RX_axis) > 361000:
                        return
                self.__fps_counter.increment("ArmEndPose_ZRX")
                self.__arm_end_pose.time_stamp = msg.time_stamp
                self.__arm_end_pose.end_pose.Z_axis = msg.arm_end_pose.Z_axis
                self.__arm_end_pose.end_pose.RX_axis = msg.arm_end_pose.RX_axis
            elif(msg.type_ == ArmMsgType.PiperMsgEndPoseFeedback_3):
                if self.isFilterAbnormalData():
                    # 361 degree * 1000
                    if abs(msg.arm_end_pose.RY_axis) > 361000 or abs(msg.arm_end_pose.RZ_axis) > 361000:
                        return
                self.__fps_counter.increment("ArmEndPose_RYRZ")
                self.__arm_end_pose.time_stamp = msg.time_stamp
                self.__arm_end_pose.end_pose.RY_axis = msg.arm_end_pose.RY_axis
                self.__arm_end_pose.end_pose.RZ_axis = msg.arm_end_pose.RZ_axis
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
                _joint1 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_1, "j1")
                _joint2 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_2, "j2")
                if self.isFilterAbnormalData():
                # 300 degree * 1000
                    if abs(_joint1) > 3000000 or abs(_joint2) > 3000000:
                        return
                self.__fps_counter.increment("ArmJoint_12")
                self.__arm_joint_msgs.time_stamp = msg.time_stamp
                self.__arm_joint_msgs.joint_state.joint_1 = _joint1
                self.__arm_joint_msgs.joint_state.joint_2 = _joint2
            elif(msg.type_ == ArmMsgType.PiperMsgJointFeedBack_34):
                _joint3 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_3, "j3")
                _joint4 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_4, "j4")
                if self.isFilterAbnormalData():
                    if abs(_joint3) > 3000000 or abs(_joint4) > 3000000:
                        return
                self.__fps_counter.increment("ArmJoint_34")
                self.__arm_joint_msgs.time_stamp = msg.time_stamp
                self.__arm_joint_msgs.joint_state.joint_3 = _joint3
                self.__arm_joint_msgs.joint_state.joint_4 = _joint4
            elif(msg.type_ == ArmMsgType.PiperMsgJointFeedBack_56):
                _joint5 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_5, "j5")
                _joint6 = self.__CalJointSDKLimit(msg.arm_joint_feedback.joint_6, "j6")
                if self.isFilterAbnormalData():
                    if abs(_joint5) > 3000000 or abs(_joint6) > 3000000:
                        return
                self.__fps_counter.increment("ArmJoint_56")
                self.__arm_joint_msgs.time_stamp = msg.time_stamp
                self.__arm_joint_msgs.joint_state.joint_5 = _joint5
                self.__arm_joint_msgs.joint_state.joint_6 = _joint6
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
                gripper_val = self.__CalGripperSDKLimit(msg.gripper_feedback.grippers_angle)
                if self.isFilterAbnormalData():
                    # 150mm * 1000
                    if abs(gripper_val) > 150000:
                        return
                self.__fps_counter.increment("ArmGripper")
                self.__arm_gripper_msgs.time_stamp = msg.time_stamp
                self.__arm_gripper_msgs.gripper_state.grippers_angle = self.__CalGripperSDKLimit(msg.gripper_feedback.grippers_angle)
                self.__arm_gripper_msgs.gripper_state.grippers_effort = msg.gripper_feedback.grippers_effort
                self.__arm_gripper_msgs.gripper_state.status_code = msg.gripper_feedback.status_code
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
            if(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_1):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_1")
                self.__arm_motor_info_high_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_high_spd.motor_1.can_id = msg.arm_high_spd_feedback_1.can_id
                self.__arm_motor_info_high_spd.motor_1.motor_speed = msg.arm_high_spd_feedback_1.motor_speed
                self.__arm_motor_info_high_spd.motor_1.current = msg.arm_high_spd_feedback_1.current
                self.__arm_motor_info_high_spd.motor_1.pos = msg.arm_high_spd_feedback_1.pos
                self.__arm_motor_info_high_spd.motor_1.effort = msg.arm_high_spd_feedback_1.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_2):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_2")
                self.__arm_motor_info_high_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_high_spd.motor_2.can_id = msg.arm_high_spd_feedback_2.can_id
                self.__arm_motor_info_high_spd.motor_2.motor_speed = msg.arm_high_spd_feedback_2.motor_speed
                self.__arm_motor_info_high_spd.motor_2.current = msg.arm_high_spd_feedback_2.current
                self.__arm_motor_info_high_spd.motor_2.pos = msg.arm_high_spd_feedback_2.pos
                self.__arm_motor_info_high_spd.motor_2.effort = msg.arm_high_spd_feedback_2.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_3):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_3")
                self.__arm_motor_info_high_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_high_spd.motor_3.can_id = msg.arm_high_spd_feedback_3.can_id
                self.__arm_motor_info_high_spd.motor_3.motor_speed = msg.arm_high_spd_feedback_3.motor_speed
                self.__arm_motor_info_high_spd.motor_3.current = msg.arm_high_spd_feedback_3.current
                self.__arm_motor_info_high_spd.motor_3.pos = msg.arm_high_spd_feedback_3.pos
                self.__arm_motor_info_high_spd.motor_3.effort = msg.arm_high_spd_feedback_3.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_4):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_4")
                self.__arm_motor_info_high_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_high_spd.motor_4.can_id = msg.arm_high_spd_feedback_4.can_id
                self.__arm_motor_info_high_spd.motor_4.motor_speed = msg.arm_high_spd_feedback_4.motor_speed
                self.__arm_motor_info_high_spd.motor_4.current = msg.arm_high_spd_feedback_4.current
                self.__arm_motor_info_high_spd.motor_4.pos = msg.arm_high_spd_feedback_4.pos
                self.__arm_motor_info_high_spd.motor_4.effort = msg.arm_high_spd_feedback_4.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_5):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_5")
                self.__arm_motor_info_high_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_high_spd.motor_5.can_id = msg.arm_high_spd_feedback_5.can_id
                self.__arm_motor_info_high_spd.motor_5.motor_speed = msg.arm_high_spd_feedback_5.motor_speed
                self.__arm_motor_info_high_spd.motor_5.current = msg.arm_high_spd_feedback_5.current
                self.__arm_motor_info_high_spd.motor_5.pos = msg.arm_high_spd_feedback_5.pos
                self.__arm_motor_info_high_spd.motor_5.effort = msg.arm_high_spd_feedback_5.cal_effort()
            elif(msg.type_ == ArmMsgType.PiperMsgHighSpdFeed_6):
                self.__fps_counter.increment("ArmMotorDriverInfoHighSpd_6")
                self.__arm_motor_info_high_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_high_spd.motor_6.can_id = msg.arm_high_spd_feedback_6.can_id
                self.__arm_motor_info_high_spd.motor_6.motor_speed = msg.arm_high_spd_feedback_6.motor_speed
                self.__arm_motor_info_high_spd.motor_6.current = msg.arm_high_spd_feedback_6.current
                self.__arm_motor_info_high_spd.motor_6.pos = msg.arm_high_spd_feedback_6.pos
                self.__arm_motor_info_high_spd.motor_6.effort = msg.arm_high_spd_feedback_6.cal_effort()
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
            if(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_1):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_1")
                self.__arm_motor_info_low_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_low_spd.motor_1.can_id = msg.arm_low_spd_feedback_1.can_id
                self.__arm_motor_info_low_spd.motor_1.vol = msg.arm_low_spd_feedback_1.vol
                self.__arm_motor_info_low_spd.motor_1.foc_temp = msg.arm_low_spd_feedback_1.foc_temp
                self.__arm_motor_info_low_spd.motor_1.motor_temp = msg.arm_low_spd_feedback_1.motor_temp
                self.__arm_motor_info_low_spd.motor_1.foc_status_code = msg.arm_low_spd_feedback_1.foc_status_code
                self.__arm_motor_info_low_spd.motor_1.bus_current = msg.arm_low_spd_feedback_1.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_2):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_2")
                self.__arm_motor_info_low_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_low_spd.motor_2.can_id = msg.arm_low_spd_feedback_2.can_id
                self.__arm_motor_info_low_spd.motor_2.vol= msg.arm_low_spd_feedback_2.vol
                self.__arm_motor_info_low_spd.motor_2.foc_temp = msg.arm_low_spd_feedback_2.foc_temp
                self.__arm_motor_info_low_spd.motor_2.motor_temp = msg.arm_low_spd_feedback_2.motor_temp
                self.__arm_motor_info_low_spd.motor_2.foc_status_code = msg.arm_low_spd_feedback_2.foc_status_code
                self.__arm_motor_info_low_spd.motor_2.bus_current = msg.arm_low_spd_feedback_2.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_3):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_3")
                self.__arm_motor_info_low_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_low_spd.motor_3.can_id = msg.arm_low_spd_feedback_3.can_id
                self.__arm_motor_info_low_spd.motor_3.vol = msg.arm_low_spd_feedback_3.vol
                self.__arm_motor_info_low_spd.motor_3.foc_temp = msg.arm_low_spd_feedback_3.foc_temp
                self.__arm_motor_info_low_spd.motor_3.motor_temp = msg.arm_low_spd_feedback_3.motor_temp
                self.__arm_motor_info_low_spd.motor_3.foc_status_code = msg.arm_low_spd_feedback_3.foc_status_code
                self.__arm_motor_info_low_spd.motor_3.bus_current = msg.arm_low_spd_feedback_3.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_4):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_4")
                self.__arm_motor_info_low_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_low_spd.motor_4.can_id = msg.arm_low_spd_feedback_4.can_id
                self.__arm_motor_info_low_spd.motor_4.vol = msg.arm_low_spd_feedback_4.vol
                self.__arm_motor_info_low_spd.motor_4.foc_temp = msg.arm_low_spd_feedback_4.foc_temp
                self.__arm_motor_info_low_spd.motor_4.motor_temp = msg.arm_low_spd_feedback_4.motor_temp
                self.__arm_motor_info_low_spd.motor_4.foc_status_code = msg.arm_low_spd_feedback_4.foc_status_code
                self.__arm_motor_info_low_spd.motor_4.bus_current = msg.arm_low_spd_feedback_4.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_5):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_5")
                self.__arm_motor_info_low_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_low_spd.motor_5.can_id = msg.arm_low_spd_feedback_5.can_id
                self.__arm_motor_info_low_spd.motor_5.vol = msg.arm_low_spd_feedback_5.vol
                self.__arm_motor_info_low_spd.motor_5.foc_temp = msg.arm_low_spd_feedback_5.foc_temp
                self.__arm_motor_info_low_spd.motor_5.motor_temp = msg.arm_low_spd_feedback_5.motor_temp
                self.__arm_motor_info_low_spd.motor_5.foc_status_code = msg.arm_low_spd_feedback_5.foc_status_code
                self.__arm_motor_info_low_spd.motor_5.bus_current = msg.arm_low_spd_feedback_5.bus_current
            elif(msg.type_ == ArmMsgType.PiperMsgLowSpdFeed_6):
                self.__fps_counter.increment("ArmMotorDriverInfoLowSpd_6")
                self.__arm_motor_info_low_spd.time_stamp = msg.time_stamp
                self.__arm_motor_info_low_spd.motor_6.can_id = msg.arm_low_spd_feedback_6.can_id
                self.__arm_motor_info_low_spd.motor_6.vol = msg.arm_low_spd_feedback_6.vol
                self.__arm_motor_info_low_spd.motor_6.foc_temp = msg.arm_low_spd_feedback_6.foc_temp
                self.__arm_motor_info_low_spd.motor_6.motor_temp = msg.arm_low_spd_feedback_6.motor_temp
                self.__arm_motor_info_low_spd.motor_6.foc_status_code = msg.arm_low_spd_feedback_6.foc_status_code
                self.__arm_motor_info_low_spd.motor_6.bus_current = msg.arm_low_spd_feedback_6.bus_current
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
                self.__feedback_current_motor_angle_limit_max_vel.time_stamp = msg.time_stamp
                self.__feedback_current_motor_angle_limit_max_vel.current_motor_angle_limit_max_vel.motor_num = \
                    msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num
                self.__feedback_current_motor_angle_limit_max_vel.current_motor_angle_limit_max_vel.max_angle_limit = \
                    msg.arm_feedback_current_motor_angle_limit_max_spd.max_angle_limit
                self.__feedback_current_motor_angle_limit_max_vel.current_motor_angle_limit_max_vel.min_angle_limit = \
                    msg.arm_feedback_current_motor_angle_limit_max_spd.min_angle_limit
                self.__feedback_current_motor_angle_limit_max_vel.current_motor_angle_limit_max_vel.max_joint_spd = \
                    msg.arm_feedback_current_motor_angle_limit_max_spd.max_joint_spd
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
                self.__feedback_current_motor_max_acc_limit.time_stamp = msg.time_stamp
                self.__feedback_current_motor_max_acc_limit.current_motor_max_acc_limit.joint_motor_num = \
                    msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num
                self.__feedback_current_motor_max_acc_limit.current_motor_max_acc_limit.max_joint_acc = \
                    msg.arm_feedback_current_motor_max_acc_limit.max_joint_acc
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
                    self.__arm_all_motor_angle_limit_max_spd.time_stamp = msg.time_stamp
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[1]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 2):
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[2]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 3):
                    self.__arm_all_motor_angle_limit_max_spd.time_stamp = msg.time_stamp
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[3]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 4):
                    self.__arm_all_motor_angle_limit_max_spd.time_stamp = msg.time_stamp
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[4]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 5):
                    self.__arm_all_motor_angle_limit_max_spd.time_stamp = msg.time_stamp
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[5]=msg.arm_feedback_current_motor_angle_limit_max_spd
                elif(msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num == 6):
                    self.__arm_all_motor_angle_limit_max_spd.time_stamp = msg.time_stamp
                    self.__arm_all_motor_angle_limit_max_spd.all_motor_angle_limit_max_spd.motor[6]=msg.arm_feedback_current_motor_angle_limit_max_spd
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
                    self.__arm_all_motor_max_acc_limit.time_stamp = msg.time_stamp
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[1]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 2):
                    self.__arm_all_motor_max_acc_limit.time_stamp = msg.time_stamp
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[2]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 3):
                    self.__arm_all_motor_max_acc_limit.time_stamp = msg.time_stamp
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[3]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 4):
                    self.__arm_all_motor_max_acc_limit.time_stamp = msg.time_stamp
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[4]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 5):
                    self.__arm_all_motor_max_acc_limit.time_stamp = msg.time_stamp
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[5]=msg.arm_feedback_current_motor_max_acc_limit
                elif(msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num == 6):
                    self.__arm_all_motor_max_acc_limit.time_stamp = msg.time_stamp
                    self.__arm_all_motor_max_acc_limit.all_motor_max_acc_limit.motor[6]=msg.arm_feedback_current_motor_max_acc_limit
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
                self.__feedback_current_end_vel_acc_param.time_stamp = msg.time_stamp
                self.__feedback_current_end_vel_acc_param.current_end_vel_acc_param.end_max_linear_vel = \
                    msg.arm_feedback_current_end_vel_acc_param.end_max_linear_vel
                self.__feedback_current_end_vel_acc_param.current_end_vel_acc_param.end_max_angular_vel = \
                    msg.arm_feedback_current_end_vel_acc_param.end_max_angular_vel
                self.__feedback_current_end_vel_acc_param.current_end_vel_acc_param.end_max_linear_acc = \
                    msg.arm_feedback_current_end_vel_acc_param.end_max_linear_acc
                self.__feedback_current_end_vel_acc_param.current_end_vel_acc_param.end_max_angular_acc = \
                    msg.arm_feedback_current_end_vel_acc_param.end_max_angular_acc
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
                self.__feedback_crash_protection_level.time_stamp = msg.time_stamp
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
            return self.__feedback_crash_protection_level
    
    def __UpdateGripperTeachingPendantParamFeedback(self, msg:PiperMessage):
        '''
        夹爪/示教器参数反馈指令
        为主动发送指令后反馈消息
        对应机械臂参数查询与设置指令 0x477 Byte 0 = 0x04
        
        ArmParamEnquiryAndConfig(param_enquiry=0x04)
        
        CAN_ID:
            0x47E
        '''
        '''
        Gripper/Teaching Pendant Parameter Feedback Command
        This is the feedback message after actively sending a command.
        Corresponds to robotic arm parameter query and setting command 0x477, Byte 0 = 0x04
        
        ArmParamEnquiryAndConfig(param_enquiry=0x04)
        
        CAN ID:
            0x47E
        '''
        with self.__feedback_gripper_teaching_pendant_param_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgGripperTeachingPendantParamFeedback):
                self.__feedback_gripper_teaching_pendant_param.time_stamp = msg.time_stamp
                self.__feedback_gripper_teaching_pendant_param.arm_gripper_teaching_param_feedback.max_range_config = \
                    msg.arm_gripper_teaching_param_feedback.max_range_config
                self.__feedback_gripper_teaching_pendant_param.arm_gripper_teaching_param_feedback.teaching_range_per = \
                    msg.arm_gripper_teaching_param_feedback.teaching_range_per
                self.__feedback_gripper_teaching_pendant_param.arm_gripper_teaching_param_feedback.teaching_friction = \
                    msg.arm_gripper_teaching_param_feedback.teaching_friction
            return self.__feedback_gripper_teaching_pendant_param
    
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
                self.__arm_joint_ctrl_msgs.time_stamp = msg.time_stamp
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_1 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_1, "j1")
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_2 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_2, "j2")
            elif(msg.type_ == ArmMsgType.PiperMsgJointCtrl_34):
                self.__fps_counter.increment("ArmJointCtrl_34")
                self.__arm_joint_ctrl_msgs.time_stamp = msg.time_stamp
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_3 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_3, "j3")
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_4 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_4, "j4")
            elif(msg.type_ == ArmMsgType.PiperMsgJointCtrl_56):
                self.__fps_counter.increment("ArmJointCtrl_56")
                self.__arm_joint_ctrl_msgs.time_stamp = msg.time_stamp
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_5 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_5, "j5")
                self.__arm_joint_ctrl_msgs.joint_ctrl.joint_6 = self.__CalJointSDKLimit(msg.arm_joint_ctrl.joint_6, "j6")
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
                self.__arm_gripper_ctrl_msgs.time_stamp = msg.time_stamp
                self.__arm_gripper_ctrl_msgs.gripper_ctrl.grippers_angle = self.__CalGripperSDKLimit(msg.arm_gripper_ctrl.grippers_angle)
                self.__arm_gripper_ctrl_msgs.gripper_ctrl.grippers_effort = msg.arm_gripper_ctrl.grippers_effort
                self.__arm_gripper_ctrl_msgs.gripper_ctrl.status_code = msg.arm_gripper_ctrl.status_code
                self.__arm_gripper_ctrl_msgs.gripper_ctrl.set_zero = msg.arm_gripper_ctrl.set_zero
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
                self.__arm_ctrl_code_151.time_stamp = msg.time_stamp
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
            return self.__arm_ctrl_code_151
    
    def __UpdateArmModeCtrl(self, msg:PiperMessage):
        '''
        更新主臂发送的模式控制指令

        0x151
        '''
        '''Updates the mode control command 0x151 sent by the main arm.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self.__arm_mode_ctrl_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgMotionCtrl_2):
                self.__fps_counter.increment("ArmModeCtrl")
                self.__arm_mode_ctrl.time_stamp = msg.time_stamp
                self.__arm_mode_ctrl.mode_ctrl.ctrl_mode = \
                    msg.arm_motion_ctrl_2.ctrl_mode
                self.__arm_mode_ctrl.mode_ctrl.move_mode = \
                    msg.arm_motion_ctrl_2.move_mode
                self.__arm_mode_ctrl.mode_ctrl.move_spd_rate_ctrl = \
                    msg.arm_motion_ctrl_2.move_spd_rate_ctrl
                self.__arm_mode_ctrl.mode_ctrl.mit_mode = \
                    msg.arm_motion_ctrl_2.mit_mode
                self.__arm_mode_ctrl.mode_ctrl.residence_time = \
                    msg.arm_motion_ctrl_2.residence_time
            return self.__arm_mode_ctrl
    
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
    
    def __UpdateRespSetInstruction(self, msg:PiperMessage):
        '''
        更新设置应答反馈指令
        '''
        with self.__feedback_instruction_response_mtx:
            if(msg.type_ == ArmMsgType.PiperMsgFeedbackRespSetInstruction):
                self.__feedback_instruction_response.time_stamp = msg.time_stamp
                self.__feedback_instruction_response.instruction_response.instruction_index = \
                    msg.arm_feedback_resp_set_instruction.instruction_index
                self.__feedback_instruction_response.instruction_response.is_set_zero_successfully = \
                    msg.arm_feedback_resp_set_instruction.is_set_zero_successfully
            return self.__feedback_instruction_response
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("0x150 send failed: SendCanMessage(%s)", feedback)

    def EmergencyStop(self, 
                        emergency_stop: Literal[0x00, 0x01, 0x02] = 0):
        '''
        机械臂紧急停止以及重置
        
        CAN ID:
            0x150
        
        Args:
            emergency_stop: 快速急停 uint8 
                0x00 无效
                0x01 快速急停
                0x02 恢复
        '''
        '''
        Sends the robotic arm motion control command (0x150).
        
        Args:
            emergency_stop (int): The emergency stop command.
                0x00: Invalid
                0x01: Emergency stop
                0x02: Resume
        '''
        self.MotionCtrl_1(emergency_stop, 0x00, 0x00)

    def ResetPiper(self):
        '''
        机械臂重置

        机械臂会立刻失电落下，清除所有错误和内部标志位
        
        CAN ID:
            0x150
        '''
        '''
        Robotic Arm Reset.
        
        The robot will immediately lose power and fall down, clearing all errors and internal flags.

        CAN ID:
            0x150
        '''
        self.MotionCtrl_1(0x02, 0x00, 0x00)

    def MotionCtrl_2(self, 
                     ctrl_mode: Literal[0x00, 0x01, 0x03, 0x04, 0x07] = 0x01, 
                     move_mode: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05] = 0x01, 
                     move_spd_rate_ctrl: int = 50, 
                     is_mit_mode: Literal[0x00, 0xAD, 0xFF] = 0x00,
                     residence_time: int = 0,
                     installation_pos: Literal[0x00, 0x01, 0x02, 0x03] = 0x00):
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
                0x04 MOVE M ---基于V1.5-2版本后
                0x05 MOVE CPV ---基于V1.8-1版本后
            move_spd_rate_ctrl 运动速度百分比 uint8
                数值范围0~100 
            is_mit_mode: mit模式 uint8 
                0x00 位置速度模式
                0xAD MIT模式
                0xFF 无效
            residence_time: 离线轨迹点停留时间 
                uint8 0~254 ,单位: s;255:轨迹终止
            installation_pos: 安装位置 uint8 注意接线朝后 ---基于V1.5-2版本后
                    0x00 无效值
                    0x01 水平正装
                    0x02 侧装左
                    0x03 侧装右
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
                0x04: MOVE M (MIT) ---- Based on version V1.5-2 and later
                0x05: MOVE CPV ---- Based on version V1.8-1 and later
            move_spd_rate_ctrl (int): The movement speed percentage (0-100).
            is_mit_mode (int): The MIT mode.
                0x00: Position-velocity mode
                0xAD: MIT mode
                0xFF: Invalid
            residence_time: Offline trajectory point residence time
                uint8 0~254, unit: seconds; 255: trajectory termination
            installation_pos: Installation position uint8 (Pay attention to rear-facing wiring) --- Based on version V1.5-2 and later
                            0x00 Invalid value
                            0x01 Horizontal upright
                            0x02 Side mount left
                            0x03 Side mount right
        '''
        tx_can = Message()
        motion_ctrl_2 = ArmMsgMotionCtrl_2(ctrl_mode, move_mode, move_spd_rate_ctrl, is_mit_mode, residence_time, installation_pos)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrl_2, arm_motion_ctrl_2=motion_ctrl_2)
        self.__parser.EncodeMessage(msg, tx_can)
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("0x151 send failed: SendCanMessage(%s)", feedback)
    
    def ModeCtrl(self, 
                ctrl_mode: Literal[0x00, 0x01] = 0x01, 
                move_mode: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05] = 0x01, 
                move_spd_rate_ctrl: int = 50, 
                is_mit_mode: Literal[0x00, 0xAD, 0xFF] = 0x00):
        '''
        机械臂模式控制
        
        CAN ID:
            0x151
        
        Args:
            ctrl_mode: 控制模式 uint8 
                0x00 待机模式
                0x01 CAN 指令控制模式
            move_mode: MOVE模式 uint8 
                0x00 MOVE P
                0x01 MOVE J
                0x02 MOVE L
                0x03 MOVE C
                0x04 MOVE M ---基于V1.5-2版本后
                0x05 MOVE CPV ---基于V1.8-1版本后
            move_spd_rate_ctrl 运动速度百分比 uint8
                数值范围0~100 
            is_mit_mode: mit模式 uint8 
                0x00 位置速度模式
                0xAD MIT模式
                0xFF 无效
        '''
        '''
        Sends the robotic arm motion control command (0x151).
        
        Args:
            ctrl_mode (int): The control mode.
                0x00: Standby mode
                0x01: CAN command control mode
            move_mode (int): The MOVE mode.
                0x00: MOVE P (Position)
                0x01: MOVE J (Joint)
                0x02: MOVE L (Linear)
                0x03: MOVE C (Circular)
                0x04: MOVE M (MIT) ---- Based on version V1.5-2 and later
                0x05: MOVE CPV ---- Based on version V1.8-1 and later
            move_spd_rate_ctrl (int): The movement speed percentage (0-100).
            is_mit_mode (int): The MIT mode.
                0x00: Position-velocity mode
                0xAD: MIT mode
                0xFF: Invalid
        '''
        self.MotionCtrl_2(ctrl_mode, move_mode, move_spd_rate_ctrl, is_mit_mode)

    def __ValidateEndPoseValue(self, endpose_num:str, endpose_value):
        # 类型判断
        if not isinstance(endpose_value, int):
            self.logger.error(f"Error: EndPose_{endpose_num} value {endpose_value} is not an integer.")
            return False
        return True
    
    def EndPoseCtrl(self, X: int, Y: int, Z: int, RX: int, RY: int, RZ: int):
        '''
        机械臂末端数值发送,发送前需要切换机械臂模式为末端控制模式
        
        末端表示为欧拉角

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
        
        The ends are expressed as Euler angles

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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("EndPoseXY send failed: SendCanMessage(%s)", feedback)
    
    def __CartesianCtrl_ZRX(self, Z:int, RX:int):
        tx_can = Message()
        cartesian_2 = ArmMsgMotionCtrlCartesian(Z_axis=Z, RX_axis=RX)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrlCartesian_2, arm_motion_ctrl_cartesian=cartesian_2)
        self.__parser.EncodeMessage(msg, tx_can)
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("EndPoseZRX send failed: SendCanMessage(%s)", feedback)
    
    def __CartesianCtrl_RYRZ(self, RY:int, RZ:int):
        tx_can = Message()
        cartesian_3 = ArmMsgMotionCtrlCartesian(RY_axis=RY, RZ_axis=RZ)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotionCtrlCartesian_3, arm_motion_ctrl_cartesian=cartesian_3)
        self.__parser.EncodeMessage(msg, tx_can)
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("EndPoseRYRZ send failed: SendCanMessage(%s)", feedback)
    
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
        
        |joint_name|     limit(rad)       |    limit(angle)    |
        |----------|     ----------       |     ----------     |
        |joint1    |   [-2.6179, 2.6179]  |    [-150.0, 150.0] |
        |joint2    |   [0, 3.14]          |    [0, 180.0]      |
        |joint3    |   [-2.967, 0]        |    [-170, 0]       |
        |joint4    |   [-1.745, 1.745]    |    [-100.0, 100.0] |
        |joint5    |   [-1.22, 1.22]      |    [-70.0, 70.0]   |
        |joint6    |   [-2.09439, 2.09439]|    [-120.0, 120.0] |
        
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
        
        |joint_name|     limit(rad)       |    limit(angle)    |
        |----------|     ----------       |     ----------     |
        |joint1    |   [-2.6179, 2.6179]  |    [-150.0, 150.0] |
        |joint2    |   [0, 3.14]          |    [0, 180.0]      |
        |joint3    |   [-2.967, 0]        |    [-170, 0]       |
        |joint4    |   [-1.745, 1.745]    |    [-100.0, 100.0] |
        |joint5    |   [-1.22, 1.22]      |    [-70.0, 70.0]   |
        |joint6    |   [-2.09439, 2.09439]|    [-120.0, 120.0] |
        
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("JointCtrl_J12 send failed: SendCanMessage(%s)", feedback)
    
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("JointCtrl_J34 send failed: SendCanMessage(%s)", feedback)
    
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("JointCtrl_J56 send failed: SendCanMessage(%s)", feedback)

    def MoveJS(self,
               joint_1: int,
               joint_2: int,
               joint_3: int,
               joint_4: int,
               joint_5: int,
               joint_6: int,
               move_spd_rate_ctrl: int = 50):
        '''
        机械臂JS模式关节控制(快速响应模式)

        JS模式 = MOVE J(0x01) + MIT模式标志(0xAD), 即在关节控制的基础上开启MIT模式,
        等效于 MotionCtrl_2(0x01, 0x01, move_spd_rate_ctrl, 0xAD) + JointCtrl(...)

        该模式用于"即时"响应场景(如高频流式下发连续目标点的遥操作):

        - 无平滑处理
        - 无轨迹规划
        - 控制器会以尽可能快的速度(并非无限快)响应目标位置

        警告:
            若目标点与当前位置距离较大, 可能造成剧烈的机械冲击、震荡或不稳定!
            风险等级: 极高, 请保证相邻目标点足够接近

        CAN ID:
            0x151, 0x155, 0x156, 0x157

        |joint_name|     limit(rad)       |    limit(angle)    |
        |----------|     ----------       |     ----------     |
        |joint1    |   [-2.6179, 2.6179]  |    [-150.0, 150.0] |
        |joint2    |   [0, 3.14]          |    [0, 180.0]      |
        |joint3    |   [-2.967, 0]        |    [-170, 0]       |
        |joint4    |   [-1.745, 1.745]    |    [-100.0, 100.0] |
        |joint5    |   [-1.22, 1.22]      |    [-70.0, 70.0]   |
        |joint6    |   [-2.09439, 2.09439]|    [-120.0, 120.0] |

        Args:
            joint_1 (int): 关节1角度,单位0.001度
            joint_2 (int): 关节2角度,单位0.001度
            joint_3 (int): 关节3角度,单位0.001度
            joint_4 (int): 关节4角度,单位0.001度
            joint_5 (int): 关节5角度,单位0.001度
            joint_6 (int): 关节6角度,单位0.001度
            move_spd_rate_ctrl (int): 运动速度百分比, 数值范围0~100
        '''
        '''
        JS-mode joint control (fast response mode).

        JS mode = MOVE J (0x01) + MIT mode flag (0xAD), i.e. joint position
        control with the MIT mode flag enabled. Equivalent to
        MotionCtrl_2(0x01, 0x01, move_spd_rate_ctrl, 0xAD) + JointCtrl(...)

        This API is intended for "instantaneous" response scenarios
        (e.g. teleoperation streaming continuous targets at high frequency):

        - No smoothing.
        - No trajectory planning.
        - The controller/driver will try to respond as fast as possible
          (not infinitely fast) to reach the target.

        WARNING:
            If the target is far from the current position, this may cause
            severe mechanical shock, oscillation, or instability!
            Risk level: EXTREMELY HIGH. Keep adjacent targets close enough.

        CAN ID:
            0x151, 0x155, 0x156, 0x157

        |joint_name|     limit(rad)       |    limit(angle)    |
        |----------|     ----------       |     ----------     |
        |joint1    |   [-2.6179, 2.6179]  |    [-150.0, 150.0] |
        |joint2    |   [0, 3.14]          |    [0, 180.0]      |
        |joint3    |   [-2.967, 0]        |    [-170, 0]       |
        |joint4    |   [-1.745, 1.745]    |    [-100.0, 100.0] |
        |joint5    |   [-1.22, 1.22]      |    [-70.0, 70.0]   |
        |joint6    |   [-2.09439, 2.09439]|    [-120.0, 120.0] |

        Args:
            joint_1 (int): The angle of joint 1.in 0.001°
            joint_2 (int): The angle of joint 2.in 0.001°
            joint_3 (int): The angle of joint 3.in 0.001°
            joint_4 (int): The angle of joint 4.in 0.001°
            joint_5 (int): The angle of joint 5.in 0.001°
            joint_6 (int): The angle of joint 6.in 0.001°
            move_spd_rate_ctrl (int): The movement speed percentage (0-100).
        '''
        self.MotionCtrl_2(0x01, 0x01, move_spd_rate_ctrl, 0xAD)
        self.JointCtrl(joint_1, joint_2, joint_3, joint_4, joint_5, joint_6)

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
        最后使用 EndPoseCtrl 确定终点,piper.MoveCAxisUpdateCtrl(0x03)
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("MoveCAxisUpdateCtrl send failed: SendCanMessage(%s)", feedback)
    
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
            gripper_angle (int):  夹爪范围, 以整数表示, 单位0.001mm
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
            gripper_angle (int): Gripper range, expressed as an integer, unit 0.001mm.
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("GripperCtrl send failed: SendCanMessage(%s)", feedback)
    
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("MasterSlaveConfig send failed: SendCanMessage(%s)", feedback)

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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("DisableArm send failed: SendCanMessage(%s)", feedback)
    
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("EnableArm send failed: SendCanMessage(%s)", feedback)
    
    def EnablePiper(self)->bool:
        '''
        使能机械臂
        '''
        enable_list = self.GetArmEnableStatus()
        self.EnableArm(7)
        return all(enable_list)
    
    def DisablePiper(self)->bool:
        '''
        失能机械臂
        '''
        enable_list = self.GetArmEnableStatus()
        self.DisableArm(7)
        return any(enable_list)
    
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("SearchMotorMaxAngleSpdAccLimit send failed: SendCanMessage(%s)", feedback)

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
                                 motor_num: Literal[1, 2, 3, 4, 5, 6] = 1, 
                                 max_angle_limit: int = 0x7FFF, 
                                 min_angle_limit: int = 0x7FFF, 
                                 max_joint_spd: int = 0x7FFF):
        '''
        电机角度限制/最大速度设置指令
        
        CAN ID:
            0x474
        
        Args:
            motor_num: 关节电机序号
            max_angle_limit: 最大角度限制,单位 0.1°,0x7FFF为设定无效数值
            min_angle_limit: 最小角度限制,单位 0.1°,0x7FFF为设定无效数值
            max_joint_spd: 最大关节速度,单位 0.001rad/s,范围[0,3000],0x7FFF为设定无效数值
        
        |joint_name|     limit(rad/s)   |
        |----------|     ----------     |
        |joint1    |      [0, 3.0]      |
        |joint2    |      [0, 3.0]      |
        |joint3    |      [0, 3.0]      |
        |joint4    |      [0, 3.0]      |
        |joint5    |      [0, 3.0]      |
        |joint6    |      [0, 3.0]      |
        '''
        '''
        Sets the motor angle limit/maximum speed limit command 
        
        CAN ID:
            0x474
        
        Args:
            motor_num: Joint motor index.
            max_angle_limit: Maximum angle limit, unit 0.1°.(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
            min_angle_limit: Minimum angle limit, unit 0.1°.(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
            max_joint_spd: Maximum joint speed, unit 0.001 rad/s.Range [0,3000],(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
        
        |joint_name|     limit(rad/s)   |
        |----------|     ----------     |
        |joint1    |      [0, 3.0]      |
        |joint2    |      [0, 3.0]      |
        |joint3    |      [0, 3.0]      |
        |joint4    |      [0, 3.0]      |
        |joint5    |      [0, 3.0]      |
        |joint6    |      [0, 3.0]      |
        '''
        tx_can = Message()
        motor_set = ArmMsgMotorAngleLimitMaxSpdSet(motor_num, max_angle_limit, min_angle_limit, max_joint_spd)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgMotorAngleLimitMaxSpdSet, arm_motor_angle_limit_max_spd_set=motor_set)
        self.__parser.EncodeMessage(msg, tx_can)
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("MotorAngleLimitMaxSpdSet send failed: SendCanMessage(%s)", feedback)
    
    def MotorMaxSpdSet(self, motor_num:Literal[1, 2, 3, 4, 5, 6] = 6, max_joint_spd:int = 3000):
        '''
        电机最大速度设置指令(基于V1.5-2版本后)
        
        CAN ID:
            0x474
        
        范围: 0-3000 
        
        对应: 0-3 rad/s
        
        Args:
            motor_num: 电机序号
            max_joint_spd: 关节电机最大速度设定,单位 0.001rad/s,0x7FFF为设定无效数值
        '''
        '''
        Motor Maximum Speed Setting Command (Based on version V1.5-2 and later)
        
        CAN ID:
            0x474
        
        Range: 0-3000 
        
        Correspond: 0-3 rad/s
        
        Args:
            max_joint_spd: Maximum speed setting for joint motor, unit: 0.001 rad/s. 0x7FFF indicates an invalid value.
        '''
        self.MotorAngleLimitMaxSpdSet(motor_num, 0x7FFF, 0x7FFF, max_joint_spd)

    def JointConfig(self, 
                    joint_num: Literal[1, 2, 3, 4, 5, 6, 7] = 7,
                    set_zero: Literal[0x00, 0xAE] = 0,
                    acc_param_is_effective: Literal[0x00, 0xAE] = 0,
                    max_joint_acc: int = 500,
                    clear_err: Literal[0x00, 0xAE] = 0):
        r'''
        关节设置
        
        CAN ID:
            0x475
        
        Args:
            joint_motor_num: 关节电机序号值域 1-7
                1-6 代表关节驱动器序号;
                7 代表全部关节电机;
            set_motor_current_pos_as_zero: 设置当前位置为零点,有效值,0xAE
            acc_param_config_is_effective_or_not: 加速度参数设置是否生效,有效值,0xAE
            max_joint_acc: 最大关节加速度,单位0.01rad/s^2(0x7FFF为设定无效数值)
                           输入范围\[0, 500\]-->[0 rad/s^2, 5.0 rad/s^2]
            clear_joint_err: 清除关节错误代码,有效值,0xAE
        '''
        r'''
        Joint Configuration Command
        
        CAN ID:
            0x475
        
        Args:
            joint_motor_num: Joint motor number.
                Value range: 1-6 represents individual joint motor numbers.
                Value 7 applies to all joint motors.
            set_motor_current_pos_as_zero: Command to set the current position of the specified joint motor as zero, with a valid value of 0xAE.
            acc_param_config_is_effective_or_not: Indicates whether the acceleration parameter configuration is effective, with a valid value of 0xAE.
            max_joint_acc: Maximum joint acceleration, unit: 0.01rad/s^2.(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
                           Range is \[0, 500\]-->[0 rad/s^2, 5.0 rad/s^2]
            clear_joint_err: Command to clear joint error codes, with a valid value of 0xAE.
        '''
        tx_can = Message()
        joint_config = ArmMsgJointConfig(joint_num, set_zero, acc_param_is_effective, max_joint_acc, clear_err)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgJointConfig,arm_joint_config=joint_config)
        self.__parser.EncodeMessage(msg, tx_can)
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("JointConfig send failed: SendCanMessage(%s)", feedback)
    
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
    
    def SetInstructionResponse(self, instruction_index: int=0, zero_config_success_flag: Literal[0, 1] = 0):
        '''
        This function has been deprecated (since version 0.5.0)
        '''
        self.logger.warning("The SetInstructionResponse function has been deprecated (since version 0.5.0)")
    
    def ArmParamEnquiryAndConfig(self, 
                                 param_enquiry: Literal[0x00, 0x01, 0x02, 0x03, 0x04] = 0x00, 
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
                
                0x04 ->0x47E,查询夹爪/示教器参数索引 ---- 基于V1.5-2版本后
            param_setting: 参数设置
                设置末端 V/acc 参数为初始值--0x01
                设置全部关节限位、关节最大速度、关节加速度为默认值--0x02
            data_feedback_0x48x: 0x48X报文反馈设置
                无效--0x00;
                开启周期反馈--0x01;
                关闭周期反馈--0x02;
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
                0x04 -> 0x47E: Query gripper/teaching pendant parameter index(Based on version V1.5-2 and later)
            
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("ArmParamEnquiryAndConfig send failed: SendCanMessage(%s)", feedback)
    
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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("EndSpdAndAccParamSet send failed: SendCanMessage(%s)", feedback)

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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("CrashProtectionConfig send failed: SendCanMessage(%s)", feedback)

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
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("SearchPiperFirmwareVersion send failed: SendCanMessage(%s)", feedback)
        self.__firmware_data = bytearray()
    
    def __JointMitCtrl(self,motor_num:int,
                            pos_ref:float, vel_ref:float, kp:float, kd:float, t_ref:float,
                            p_min:float=-12.5,    p_max:float=12.5, 
                            v_min:float=-45.0,    v_max:float=45.0, 
                            kp_min:float=0.0,   kp_max:float=500.0, 
                            kd_min:float=-5.0,   kd_max:float=5.0,
                            t_min:float=-8.0,    t_max:float=8.0):
        '''
        机械臂关节1~6MIT控制指令
        
        CAN ID:
            0x15A,0x15B,0x15C,0x15D,0x15E,0x15F
        
        注意:p_min,p_max,v_min,v_max,kp_min,kp_max,kd_min,kd_max,t_min,t_max参数为固定,不要更改
        
        Args:
            motor_num:电机序号[1,6]
            pos_ref: 设定期望的目标位置
            vel_ref: 设定电机运动的速度
            kp: 比例增益,控制位置误差对输出力矩的影响
            kd: 微分增益,控制速度误差对输出力矩的影响
            t_ref: 目标力矩参考值,用于控制电机施加的力矩或扭矩
            p_min:位置最小值
            p_max:位置最大值
            v_min:速度最小值
            v_max:速度最大值
            kp_min:p参数最小值
            kp_max:p参数最大值
            kd_min:d参数最小值
            kd_max:d参数最大值
            t_min:扭矩参数最小值
            t_max:扭矩参数最大值
        '''
        pos_tmp = self.__parser.FloatToUint(pos_ref, p_min, p_max, 16)
        vel_tmp = self.__parser.FloatToUint(vel_ref, v_min, v_max, 12)
        kp_tmp = self.__parser.FloatToUint(kp, kp_min, kp_max, 12)
        kd_tmp = self.__parser.FloatToUint(kd, kd_min, kd_max, 12)
        t_tmp = self.__parser.FloatToUint(t_ref, t_min, t_max, 8)
        tx_can = Message()
        mit_ctrl = ArmMsgJointMitCtrl(  pos_ref=pos_tmp, 
                                        vel_ref=vel_tmp,
                                        kp=kp_tmp, 
                                        kd=kd_tmp,
                                        t_ref=t_tmp)
        if(motor_num == 1):
            msg = PiperMessage(type_=ArmMsgType.PiperMsgJointMitCtrl_1, arm_joint_mit_ctrl=mit_ctrl)
        elif(motor_num == 2):
            msg = PiperMessage(type_=ArmMsgType.PiperMsgJointMitCtrl_2, arm_joint_mit_ctrl=mit_ctrl)
        elif(motor_num == 3):
            msg = PiperMessage(type_=ArmMsgType.PiperMsgJointMitCtrl_3, arm_joint_mit_ctrl=mit_ctrl)
        elif(motor_num == 4):
            msg = PiperMessage(type_=ArmMsgType.PiperMsgJointMitCtrl_4, arm_joint_mit_ctrl=mit_ctrl)
        elif(motor_num == 5):
            msg = PiperMessage(type_=ArmMsgType.PiperMsgJointMitCtrl_5, arm_joint_mit_ctrl=mit_ctrl)
        elif(motor_num == 6):
            msg = PiperMessage(type_=ArmMsgType.PiperMsgJointMitCtrl_6, arm_joint_mit_ctrl=mit_ctrl)
        else:
            raise ValueError(f"'motor_num' {motor_num} out of range 0-6.")
        self.__parser.EncodeMessage(msg, tx_can)
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("JointMitCtrl send failed: SendCanMessage(%s)", feedback)
    
    def JointMitCtrl(self,motor_num:int,
                    pos_ref:float, vel_ref:float, kp:float, kd:float, t_ref:float):
        '''
        机械臂关节1~6MIT控制指令
        
        CAN ID:
            0x15A,0x15B,0x15C,0x15D,0x15E,0x15F
        
        Args:
            motor_num:电机序号,[1,6]
            pos_ref: 设定期望的目标位置,单位rad,[-12.5,12.5]
            vel_ref: 设定电机运动的速度,[-45.0,45.0]
            kp: 比例增益,控制位置误差对输出力矩的影响,参考值---10,[0.0,500.0]
            kd: 微分增益,控制速度误差对输出力矩的影响,参考值---0.8,[-5.0,5.0]
            t_ref: 目标力矩参考值,用于控制电机施加的力矩或扭矩,[-18.0,18.0]
        '''
        '''
        Robotic Arm Joint 1~6 MIT Control Command
        
        CAN IDs:
            0x15A, 0x15B, 0x15C, 0x15D, 0x15E, 0x15F
        
        Args:
            motor_num: Motor index, range [1, 6]
            pos_ref: Desired target position, unit: rad, range [-12.5, 12.5]
            vel_ref: Desired motor speed, range [-45.0, 45.0]
            kp: Proportional gain, controls the influence of position error on output torque, reference value: 10, range [0.0, 500.0]
            kd: Derivative gain, controls the influence of speed error on output torque, reference value: 0.8, range [-5.0, 5.0]
            t_ref: Target torque reference, controls the torque applied by the motor, range [-18.0, 18.0]
        '''
        self.__JointMitCtrl(motor_num, pos_ref, vel_ref, kp, kd, t_ref)
    
    def GripperTeachingPendantParamConfig(self, 
                                          teaching_range_per:int=100, 
                                          max_range_config:int=70,
                                          teaching_friction:int=1):
        '''
        夹爪/示教器参数设置指令(基于V1.5-2版本后)
        
        CAN ID:
            0x47D
        
        Args:
            teaching_range_per: 示教器行程系数设置,[100~200]
            max_range_config: 夹爪/示教器最大控制行程限制值设置,[0,70,100]
        '''
        '''
        Gripper/Teach Pendant Parameter Setting Command (Based on version V1.5-2 and later)
        
        CAN ID:
            0x47D
        
        Args:
            teaching_range_per: Teach pendant travel range coefficient setting, [100~200]
            max_range_config: Gripper/Teach pendant maximum control travel limit setting, [0,70,100]
        '''
        tx_can = Message()
        gripper_teaching_pendant_param_config = ArmMsgGripperTeachingPendantParamConfig(teaching_range_per, max_range_config,teaching_friction)
        msg = PiperMessage(type_=ArmMsgType.PiperMsgGripperTeachingPendantParamConfig, arm_gripper_teaching_param_config=gripper_teaching_pendant_param_config)
        self.__parser.EncodeMessage(msg, tx_can)
        feedback = self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self.__arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("GripperTeachingPendantParamConfig send failed: SendCanMessage(%s)", feedback)
    
    def ReqMasterArmMoveToHome(self, mode:Literal[0, 1, 2]):
        '''
        请求主臂回零指令(基于V1.7-4版本后)
        
        CAN ID:
            0x191
        
        Args:
            mode: 请求回零模式

                0: 恢复主从臂模式

                1: 主臂回零

                2: 主从臂一起回零
        '''
        '''
        Request Master Arm Move to Home Command (Based on version V1.7-4 and later)

        CAN ID:
            0x191
        
        Args:
            mode (int): Request return-to-zero mode.

                0: Restore master-slave arm mode.

                1: Master arm return-to-zero.

                2: Master and slave arms return-to-zero together.
        '''
        tx_can = Message()
        tx_can.arbitration_id = 0x191
        if mode == 0:
            # 恢复主从臂模式
            tx_can.data = [0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        elif mode == 1:
            # 主臂回零
            tx_can.data = [0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]
        elif mode == 2:
            # 主从臂一起回零
            tx_can.data = [0x01, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00]
        self.__arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
    
    def ClearRespSetInstruction(self):
        '''
        清除SDK保存的设置指令应答信息

        将指令应答反馈中的
        time_stamp = 0;
        instruction_response.instruction_index = -1;
        instruction_response.is_set_zero_successfully = -1
        '''
        '''
        Clear saved SDK command responses.

        Set the command response related parameters to -1.
        '''
        self.__feedback_instruction_response.time_stamp = 0
        self.__feedback_instruction_response.instruction_response.instruction_index = -1
        self.__feedback_instruction_response.instruction_response.is_set_zero_successfully = -1
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
