#!/usr/bin/env python3
# -*-coding:utf8-*-

from can.message import Message
from typing_extensions import (
    Literal,
)
from typing import (
    Optional,
    Type
)
import can
import threading
from ..hardware_port import *
from ..protocol.protocol_v3 import C_PiperParserV3 as PiperParser
from ..piper_msgs.msg_v3 import *
from ..piper_msgs.msg_v3 import ArmMsgType as ArmMsgType_V3
from ..piper_msgs.msg_v3 import CanIDPiper as CanIDPiper_V3
from ..piper_msgs.msg_v3 import PiperMessage as PiperMessage_V3
from ..kinematics import *
from ..utils import *
from ..utils import logger, global_area
from ..piper_param import *
from ..version import PiperSDKVersion
from .interface_version import InterfaceVersion

from .piper_interface_v2 import C_PiperInterface_V2

class C_PiperInterface_V3(C_PiperInterface_V2):
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
    ArmMsgType = ArmMsgType_V3
    CanIDPiper = CanIDPiper_V3
    PiperMessage = PiperMessage_V3

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

    class ArmGripper_V3():
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
            self.gripper_state=ArmMsgFeedBackGripper_V3()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.gripper_state}\n")

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

    class ArmGripperCtrl_V3():
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
            self.gripper_ctrl=ArmMsgGripperCtrl_V3()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.gripper_ctrl}\n")

    class ArmIKJointStates():
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
            self.ik_joint_states=ArmMsgFeedBackIKJointStates()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.ik_joint_states}\n")

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
        super().__init__(
                    can_name,
                    judge_flag,
                    can_auto_init,
                    # reconnect_after_disconnection:bool = False,
                    dh_is_offset,
                    start_sdk_joint_limit, 
                    start_sdk_gripper_limit,
                    logger_level,
                    log_to_file,
                    log_file_path)
        self._parser: Type[PiperParser] = PiperParser()
        self._arm_status_mtx = threading.Lock()
        self._arm_status = self.ArmStatus()

        self._arm_gripper_msgs_mtx = threading.Lock()
        self._arm_gripper_msgs = self.ArmGripper()
        self._arm_gripper_ctrl_msgs_mtx = threading.Lock()
        self._arm_gripper_ctrl_msgs = self.ArmGripperCtrl()

        self._arm_gripper_msgs_v3_mtx = threading.Lock()
        self._arm_gripper_msgs_v3 = self.ArmGripper_V3()
        self._arm_gripper_ctrl_msgs_v3_mtx = threading.Lock()
        self._arm_gripper_ctrl_msgs_v3 = self.ArmGripperCtrl_V3()
        self._arm_ik_joint_states_mtx = threading.Lock()
        self._arm_ik_joint_states = self.ArmIKJointStates()
        self._fps_counter.add_variable("ArmIKJoint_12")
        self._fps_counter.add_variable("ArmIKJoint_34")
        self._fps_counter.add_variable("ArmIKJoint_56")
        self.tx_msg = self.PiperMessage()
        self.rx_msg = self.PiperMessage()

    def ParseCANFrame(self, rx_message: Optional[can.Message]):
        '''can协议解析函数

        Args:
            rx_message (Optional[can.Message]): can接收的原始数据
        '''
        '''CAN protocol parsing function.

        Args:
            rx_message (Optional[can.Message]): The raw data received via CAN.
        '''
        msg = self.rx_msg
        receive_flag = self._parser.DecodeMessage(rx_message, msg)
        if(receive_flag):
            self._fps_counter.increment("CanMonitor")
            self._UpdateArmStatus(msg)
            self._UpdateArmEndPoseState(msg)
            self._UpdateArmJointState(msg)
            self._UpdateArmGripperState(msg)
            self._UpdateDriverInfoHighSpdFeedback(msg)
            self._UpdateDriverInfoLowSpdFeedback(msg)

            self._UpdateCurrentEndVelAndAccParam(msg)
            self._UpdateCrashProtectionLevelFeedback(msg)
            self._UpdateGripperTeachingPendantParamFeedback(msg)
            self._UpdateCurrentMotorAngleLimitMaxVel(msg)
            self._UpdateCurrentMotorMaxAccLimit(msg)
            self._UpdateAllCurrentMotorAngleLimitMaxVel(msg)
            self._UpdateAllCurrentMotorMaxAccLimit(msg)
            # 更新主臂发送消息
            self._UpdateArmJointCtrl(msg)
            self._UpdateArmGripperCtrl(msg)
            self._UpdateArmCtrlCode151(msg)
            self._UpdateArmModeCtrl(msg)
            self._UpdatePiperFirmware(msg)
            self._UpdateRespSetInstruction(msg)
            # 1.8-8
            self._UpdateArmGripperState_V3(msg)
            self._UpdateArmGripperCtrl_V3(msg)
            self._UpdateArmIKJointState(msg)
            if self._start_sdk_fk_cal:
                self._UpdatePiperFeedbackFK()
                self._UpdatePiperCtrlFK()
    
    def GetCurrentInterfaceVersion(self):
        '''
        Returns
        -------
            current interface version
        '''
        return InterfaceVersion.INTERFACE_V3

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
                    * 0x06 MOVE M ---基于V1.8-8版本后
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
            with self._arm_status_mtx:
                self._arm_status.Hz = self._fps_counter.get_fps("ArmStatus")
                return self._arm_status

    def GetArmGripperMsgs_V3(self):
        '''
        Retrieves the gripper status message of the robotic arm.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        gripper_state : ArmMsgFeedBackGripper

            - grippers_val (int): The gripper value, in 0.001 mm for width mode or 0.001 degree for angle mode.
            - grippers_effort (int): The torque of the gripper (in 0.001 N·m).
            - mode (int): The gripper control mode, 0x00 for width mode and 0x01 for angle mode.
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
        with self._arm_gripper_msgs_v3_mtx:
            self._arm_gripper_msgs_v3.Hz = self._fps_counter.get_fps('ArmGripper')
            return self._arm_gripper_msgs_v3

    def GetArmGripperCtrl_V3(self):
        '''
        Retrieves the gripper control message using the 0x159 command.

        Returns
        -------
        time_stamp : float
            time stamp
        Hz : float
            msg fps
        gripper_ctrl : ArmMsgGripperCtrl

            - grippers_val (int): The gripper value, in 0.001 mm for width mode or 0.001 degree for angle mode.
            - grippers_effort (int): Gripper torque, represented as an integer, unit: 0.001N·m. Range 0-5000 (corresponse 0-5N·m)
            - status_code (int): 
                0x00: Disabled;
                0x01: Enabled;
                0x03: Enable and clear errors in width mode;
                0x02: Disable and clear errors in width mode;
                0x04: Disable in angle mode;
                0x05: Enable in angle mode;
                0x06: Disable and clear errors in angle mode;
                0x07: Enable and clear errors in angle mode.
            - set_zero (int): Set the current position as the zero point.
                0x00: Invalid;
                0xAE: Set zero.
        '''
        with self._arm_gripper_ctrl_msgs_v3_mtx:
            self._arm_gripper_ctrl_msgs_v3.Hz = self._fps_counter.get_fps("ArmGripperCtrl")
            return self._arm_gripper_ctrl_msgs_v3

    def GetArmIKJointMsgs(self):
        '''
        Retrieves the IK joint status message of the robotic arm.(in 0.001 degrees)

        Returns
        -------
        time_stamp : float
        Hz : float
        ik_joint_states : ArmMsgFeedBackIKJointStates

            - ik_joint_1 (int): Feedback IK angle of joint 1, (in 0.001 degrees).
            - ik_joint_2 (int): Feedback IK angle of joint 2, (in 0.001 degrees).
            - ik_joint_3 (int): Feedback IK angle of joint 3, (in 0.001 degrees).
            - ik_joint_4 (int): Feedback IK angle of joint 4, (in 0.001 degrees).
            - ik_joint_5 (int): Feedback IK angle of joint 5, (in 0.001 degrees).
            - ik_joint_6 (int): Feedback IK angle of joint 6, (in 0.001 degrees).
        '''
        with self._arm_ik_joint_states_mtx:
            self._arm_ik_joint_states.Hz = self._fps_counter.cal_average(self._fps_counter.get_fps('ArmIKJoint_12'),
                                                                        self._fps_counter.get_fps('ArmIKJoint_34'),
                                                                        self._fps_counter.get_fps('ArmIKJoint_56'))
            return self._arm_ik_joint_states

    def _UpdateArmGripperState(self, msg:PiperMessage):
        '''更新夹爪状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the gripper status.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self._arm_gripper_msgs_mtx:
            if(msg.type_ == self.ArmMsgType.PiperMsgGripperFeedBack):
                gripper_angle = msg.gripper_feedback.grippers_angle
                _mode = msg.gripper_feedback_v3.mode
                if self.isFilterAbnormalData():
                    # 150 mm * 1000
                    if _mode == ArmMsgFeedbackGripperEnums_V3.CtrlMode.WIDTH and abs(gripper_angle) > 150000:
                        return
                    # 360 degree * 1000
                    elif _mode == ArmMsgFeedbackGripperEnums_V3.CtrlMode.ANGLE and abs(gripper_angle) > 360000:
                        return
                # self._fps_counter.increment("ArmGripper")
                self._arm_gripper_msgs.time_stamp = msg.time_stamp
                self._arm_gripper_msgs.gripper_state.grippers_angle = self._CalGripperSDKLimit(gripper_angle, _mode)
                self._arm_gripper_msgs.gripper_state.grippers_effort = msg.gripper_feedback.grippers_effort
                self._arm_gripper_msgs.gripper_state.status_code = msg.gripper_feedback.status_code
            return self._arm_gripper_msgs

    def _UpdateArmGripperCtrl(self, msg:PiperMessage):
        '''更新夹爪状态,为主臂发送的消息

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the gripper status, as sent by the main arm.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self._arm_gripper_ctrl_msgs_mtx:
            if(msg.type_ == self.ArmMsgType.PiperMsgGripperCtrl):
                gripper_angle = msg.arm_gripper_ctrl.grippers_angle
                status_code = msg.arm_gripper_ctrl.status_code
                _mode = 0
                if status_code in [0x00, 0x01, 0x02, 0x03]:
                    _mode = 0
                elif status_code in [0x04, 0x05, 0x06, 0x07]:
                    _mode = 1
                else: return
                if self.isFilterAbnormalData():
                   # 150 mm * 1000
                    if _mode == 0 and abs(gripper_angle) > 150000:
                        return
                    # 360 degree * 1000
                    elif _mode == 1 and abs(gripper_angle) > 360000:
                        return
                # self._fps_counter.increment("ArmGripperCtrl")
                self._arm_gripper_ctrl_msgs.time_stamp = msg.time_stamp
                self._arm_gripper_ctrl_msgs.gripper_ctrl.grippers_angle = self._CalGripperSDKLimit(gripper_angle, _mode)
                self._arm_gripper_ctrl_msgs.gripper_ctrl.grippers_effort = msg.arm_gripper_ctrl.grippers_effort
                self._arm_gripper_ctrl_msgs.gripper_ctrl.status_code = status_code
                self._arm_gripper_ctrl_msgs.gripper_ctrl.set_zero = msg.arm_gripper_ctrl.set_zero
            return self._arm_gripper_ctrl_msgs

    def _UpdateArmGripperState_V3(self, msg:PiperMessage):
        '''更新夹爪状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the gripper status.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self._arm_gripper_msgs_v3_mtx:
            if(msg.type_ == self.ArmMsgType.PiperMsgGripperFeedBack):
                gripper_val = msg.gripper_feedback.grippers_angle
                _mode = msg.gripper_feedback_v3.mode
                if self.isFilterAbnormalData():
                    # 150 mm * 1000
                    if _mode == ArmMsgFeedbackGripperEnums_V3.CtrlMode.WIDTH and abs(gripper_val) > 150000:
                        return
                    # 360 degree * 1000
                    elif _mode == ArmMsgFeedbackGripperEnums_V3.CtrlMode.ANGLE and abs(gripper_val) > 360000:
                        return
                self._fps_counter.increment("ArmGripper")
                self._arm_gripper_msgs_v3.time_stamp = msg.time_stamp
                self._arm_gripper_msgs_v3.gripper_state.grippers_val = self._CalGripperSDKLimit(gripper_val, _mode)
                self._arm_gripper_msgs_v3.gripper_state.grippers_effort = msg.gripper_feedback_v3.grippers_effort
                self._arm_gripper_msgs_v3.gripper_state.status_code = msg.gripper_feedback_v3.status_code
                self._arm_gripper_msgs_v3.gripper_state.mode = _mode
            return self._arm_gripper_msgs_v3

    def _UpdateArmGripperCtrl_V3(self, msg:PiperMessage):
        '''更新夹爪状态,为主臂发送的消息

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the gripper status, as sent by the main arm.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self._arm_gripper_ctrl_msgs_v3_mtx:
            if(msg.type_ == self.ArmMsgType.PiperMsgGripperCtrl):
                gripper_val = msg.arm_gripper_ctrl_v3.grippers_val
                status_code = msg.arm_gripper_ctrl.status_code
                _mode = 0
                if status_code in [0x00, 0x01, 0x02, 0x03]:
                    _mode = 0
                elif status_code in [0x04, 0x05, 0x06, 0x07]:
                    _mode = 1
                else: return
                if self.isFilterAbnormalData():
                    # 150 mm * 1000
                    if _mode == 0 and abs(gripper_val) > 150000:
                        return
                    # 360 degree * 1000
                    elif _mode == 1 and abs(gripper_val) > 360000:
                        return
                self._fps_counter.increment("ArmGripperCtrl")
                self._arm_gripper_ctrl_msgs_v3.time_stamp = msg.time_stamp
                self._arm_gripper_ctrl_msgs_v3.gripper_ctrl.grippers_val = self._CalGripperSDKLimit(gripper_val, _mode)
                self._arm_gripper_ctrl_msgs_v3.gripper_ctrl.grippers_effort = msg.arm_gripper_ctrl_v3.grippers_effort
                self._arm_gripper_ctrl_msgs_v3.gripper_ctrl.status_code = status_code
                self._arm_gripper_ctrl_msgs_v3.gripper_ctrl.set_zero = msg.arm_gripper_ctrl_v3.set_zero
            return self._arm_gripper_ctrl_msgs_v3

    def _UpdateArmIKJointState(self, msg:PiperMessage):
        '''更新 IK 关节状态

        Args:
            msg (PiperMessage): 输入为机械臂消息汇总
        '''
        '''Updates the IK joint status.

        Args:
            msg (PiperMessage): The input containing the summary of robotic arm messages.
        '''
        with self._arm_ik_joint_states_mtx:
            if(msg.type_ == self.ArmMsgType.PiperMsgIKJointFeedBack_12):
                _ik_joint1 = msg.arm_ik_joint_feedback.ik_joint_1
                _ik_joint2 = msg.arm_ik_joint_feedback.ik_joint_2
                if self.isFilterAbnormalData():
                    if abs(_ik_joint1) > 3000000 or abs(_ik_joint2) > 3000000:
                        return
                self._fps_counter.increment("ArmIKJoint_12")
                self._arm_ik_joint_states.time_stamp = msg.time_stamp
                self._arm_ik_joint_states.ik_joint_states.ik_joint_1 = _ik_joint1
                self._arm_ik_joint_states.ik_joint_states.ik_joint_2 = _ik_joint2
            elif(msg.type_ == self.ArmMsgType.PiperMsgIKJointFeedBack_34):
                _ik_joint3 = msg.arm_ik_joint_feedback.ik_joint_3
                _ik_joint4 = msg.arm_ik_joint_feedback.ik_joint_4
                if self.isFilterAbnormalData():
                    if abs(_ik_joint3) > 3000000 or abs(_ik_joint4) > 3000000:
                        return
                self._fps_counter.increment("ArmIKJoint_34")
                self._arm_ik_joint_states.time_stamp = msg.time_stamp
                self._arm_ik_joint_states.ik_joint_states.ik_joint_3 = _ik_joint3
                self._arm_ik_joint_states.ik_joint_states.ik_joint_4 = _ik_joint4
            elif(msg.type_ == self.ArmMsgType.PiperMsgIKJointFeedBack_56):
                _ik_joint5 = msg.arm_ik_joint_feedback.ik_joint_5
                _ik_joint6 = msg.arm_ik_joint_feedback.ik_joint_6
                if self.isFilterAbnormalData():
                    if abs(_ik_joint5) > 3000000 or abs(_ik_joint6) > 3000000:
                        return
                self._fps_counter.increment("ArmIKJoint_56")
                self._arm_ik_joint_states.time_stamp = msg.time_stamp
                self._arm_ik_joint_states.ik_joint_states.ik_joint_5 = _ik_joint5
                self._arm_ik_joint_states.ik_joint_states.ik_joint_6 = _ik_joint6
            return self._arm_ik_joint_states

    def MotionCtrl_2(self, 
                         ctrl_mode: Literal[0x00, 0x01, 0x03, 0x04, 0x07] = 0x01, 
                         move_mode: Literal[0x00, 0x01, 0x02, 0x03, 0x06, 0x05] = 0x01, 
                         move_spd_rate_ctrl: int = 50, 
                         is_mit_mode: Literal[0x00, 0xAD, 0xFF] = 0x00,
                         residence_time: int = 0,
                         installation_pos: Literal[0x00, 0x01, 0x02, 0x03, 0x04] = 0x00):
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
                    0x06 MOVE M ---基于V1.8-8版本后
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
                    0x04 水平倒装
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
                    0x06: MOVE M (MIT) ---- Based on version V1.8-8 and later
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
                    0x04 Horizontal Inversion
            '''
            tx_can = Message()
            motion_ctrl_2 = ArmMsgMotionCtrl_2(ctrl_mode, move_mode, move_spd_rate_ctrl, is_mit_mode, residence_time, installation_pos)
            msg = self.tx_msg
            msg.type_ = self.ArmMsgType.PiperMsgMotionCtrl_2
            msg.arm_motion_ctrl_2 = motion_ctrl_2
            self._parser.EncodeMessage(msg, tx_can)
            feedback = self._arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
            if feedback is not self._arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
                self.logger.error("0x151 send failed: SendCanMessage(%s)", feedback)

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
            gripper_effort (int): 夹爪力矩,单位 0.001N·m,范围0-5000,对应0-5N·m
            gripper_code (int): 
                - 0x00失能;
                - 0x01使能;
                - 0x02失能清除错误;
                - 0x03使能清除错误.
            set_zero:(int): 设定当前位置为0点,
                - 0x00无效值;
                - 0xAE设置零点
        '''
        '''
        Controls the gripper of the robotic arm.
        
        CAN ID:
            0x159
        
        Args:
            gripper_angle (int): Gripper range, expressed as an integer, unit 0.001mm.
            gripper_effort (int): The gripper torque, in 0.001 N·m. Range 0-5000, corresponse 0-5 N·m
            gripper_code (int): The gripper enable/disable/clear error command.
                - 0x00: Disable
                - 0x01: Enable
                - 0x03/0x02: Enable and clear error / Disable and clear error
            set_zero (int): Set the current position as the zero point.
                - 0x00: Invalid value
                - 0xAE: Set zero point
        '''
        if gripper_code not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"'status_code' Value {gripper_code} out of range [0x00, 0x01, 0x02, 0x03]")
        self.GripperCtrl_V3(gripper_angle, gripper_effort, gripper_code, set_zero)

    def GripperCtrl_V3(self, 
                    gripper_val: int = 0, 
                    gripper_effort: int = 0, 
                    gripper_code: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07] = 0, 
                    set_zero: Literal[0x00, 0xAE] = 0):
        '''
        Controls the gripper of the robotic arm.
        
        CAN ID:
            0x159
        
        Args:
            gripper_val (int): Gripper value, unit: 0.001 mm in width mode or 0.001 degree in angle mode.
            gripper_effort (int): The gripper torque, in 0.001 N·m. Range 0-5000, corresponse 0-5 N·m
            gripper_code (int): The gripper enable/disable/clear error command.
                - 0x00: disable/width
                - 0x01: enable/width
                - 0x02: disable/clear_err/width
                - 0x03: enable/clear_err/width
                - 0x04: disable/angle
                - 0x05: enable/angle
                - 0x06: disable/clear_err/angle
                - 0x07: enable/clear_err/angle
            set_zero (int): Set the current position as the zero point.
                - 0x00: Invalid value
                - 0xAE: Set zero point
        '''
        if gripper_code not in [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]:
            raise ValueError(f"'status_code' Value {gripper_code} out of range [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]")
        if not (0 <= gripper_effort <= 5000):
            raise ValueError(f"'grippers_effort' Value {gripper_effort} out of range 0-5000")
        if set_zero not in [0x00, 0xAE]:
            raise ValueError(f"'set_zero' Value {set_zero} out of range [0x00,0xAE]")
        tx_can = Message()
        _gripper_val = gripper_val
        if gripper_code in [0x00, 0x01, 0x02, 0x03]:
            _gripper_val = self._CalGripperSDKLimit(gripper_val, 0)
        else: _gripper_val = self._CalGripperSDKLimit(gripper_val, 1)
        gripper_ctrl = ArmMsgGripperCtrl_V3(_gripper_val, gripper_effort, gripper_code, set_zero)
        msg = self.tx_msg
        msg.type_ = self.ArmMsgType.PiperMsgGripperCtrl
        msg.arm_gripper_ctrl_v3 = gripper_ctrl
        self._parser.EncodeMessage(msg, tx_can)
        feedback = self._arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self._arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("GripperCtrl send failed: SendCanMessage(%s)", feedback)

    def _JointMitCtrl(self,motor_num:int,
                            pos_ref:float, vel_ref:float, kp:float, kd:float, t_ref:float,
                            p_min:float=-12.5,    p_max:float=12.5, 
                            v_min:float=-45.0,    v_max:float=45.0, 
                            kp_min:float=0.0,   kp_max:float=500.0, 
                            kd_min:float=-5.0,   kd_max:float=5.0,
                            t_min:float=-16.0,    t_max:float=16.0):
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
        pos_tmp = self._parser.FloatToUint(pos_ref, p_min, p_max, 16)
        vel_tmp = self._parser.FloatToUint(vel_ref, v_min, v_max, 12)
        kp_tmp = self._parser.FloatToUint(kp, kp_min, kp_max, 12)
        kd_tmp = self._parser.FloatToUint(kd, kd_min, kd_max, 12)
        t_tmp = self._parser.FloatToUint(t_ref, t_min, t_max, 12)
        tx_can = Message()
        mit_ctrl = ArmMsgJointMitCtrl(  pos_ref=pos_tmp, 
                                        vel_ref=vel_tmp,
                                        kp=kp_tmp, 
                                        kd=kd_tmp,
                                        t_ref=t_tmp)
        msg = self.tx_msg
        msg.arm_joint_mit_ctrl = mit_ctrl
        if(motor_num == 1):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_1
        elif(motor_num == 2):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_2
        elif(motor_num == 3):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_3
        elif(motor_num == 4):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_4
        elif(motor_num == 5):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_5
        elif(motor_num == 6):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_6
        else:
            raise ValueError(f"'motor_num' {motor_num} out of range 0-6.")
        self._parser.EncodeMessage(msg, tx_can)
        feedback = self._arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self._arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("JointMitCtrl send failed: SendCanMessage(%s)", feedback)
    
    def JointMitCtrl(self,motor_num:int,
                    pos_ref:float, vel_ref:float, kp:float, kd:float, t_ref:float):
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
            t_ref: Target torque reference, controls the torque applied by the motor, range [-16.0, 16.0]
        '''
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
            t_ref: 目标力矩参考值,用于控制电机施加的力矩或扭矩,[-16.0,16.0]
        '''
        self._JointMitCtrl(motor_num, pos_ref, vel_ref, kp, kd, t_ref)


    def _CalGripperSDKLimit(self, gripper_val:int, mode:int):
        if self._start_sdk_gripper_limit:
            if mode == 0:
                g_min, g_max = self.GetSDKGripperRangeParam()
                g_min = round(g_min *1000 * 1000)
                g_max = round(g_max *1000 * 1000)
                return max(g_min, min(gripper_val, g_max))
            elif mode == 1:
                g_min, g_max = self.GetSDKGripperAngleLimitParam()
                g_min = round(g_min * 1000)
                g_max = round(g_max * 1000)
                return max(g_min, min(gripper_val, g_max))
            else: return gripper_val
        else: return gripper_val

    def GetSDKGripperAngleLimitParam(self):
        return self._piper_param_mag.GetGripperAngleLimitParam()

    def SetSDKGripperAngleLimitParam(self,
                                min_val: float, 
                                max_val: float):
        self._piper_param_mag.SetGripperAngleLimitParam(min_val, max_val)
