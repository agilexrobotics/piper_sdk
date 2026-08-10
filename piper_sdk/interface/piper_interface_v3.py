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
    """Piper V3 interface.

    Parameters
    -------
    `can_name`: str

        CAN port name. Default is `can0`.

    `judge_flag`: bool

        Whether to check if the CAN port is functioning correctly. Set to False
        when using a PCIe-to-CAN module.

    `can_auto_init`: bool

        Whether to initialize the CAN port automatically.

    `dh_is_offset`: int

        Whether joint 1 to joint 2 uses the 2 degree DH offset.

    - 0: no offset
    - 1: offset applied

    `start_sdk_joint_limit`: bool

        Whether to enable SDK-side joint limits.

    `start_sdk_gripper_limit`: bool

        Whether to enable SDK-side gripper limits.
    """
    ArmMsgType = ArmMsgType_V3
    CanIDPiper = CanIDPiper_V3
    PiperMessage = PiperMessage_V3

    class ArmStatus():
        """Arm status wrapper with timestamp and FPS."""
        def __init__(self):
            self.time_stamp: float = 0
            self.Hz: float = 0
            self.arm_status = ArmMsgFeedbackStatus()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.arm_status}\n")

    class ArmGripper():
        """Gripper feedback wrapper with timestamp and FPS."""
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.gripper_state=ArmMsgFeedBackGripper()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.gripper_state}\n")

    class ArmGripper_V3():
        """V3 gripper feedback wrapper with timestamp and FPS."""
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.gripper_state=ArmMsgFeedBackGripper_V3()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.gripper_state}\n")

    class ArmGripperCtrl():
        """Gripper control wrapper for leader-arm target messages."""
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.gripper_ctrl=ArmMsgGripperCtrl()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.gripper_ctrl}\n")

    class ArmGripperCtrl_V3():
        """V3 gripper control wrapper for leader-arm target messages."""
        def __init__(self):
            self.time_stamp: float=0
            self.Hz: float = 0
            self.gripper_ctrl=ArmMsgGripperCtrl_V3()
        def __str__(self):
            return (f"time stamp:{self.time_stamp}\n"
                    f"Hz:{self.Hz}\n"
                    f"{self.gripper_ctrl}\n")

    class ArmIKJointStates():
        """IK joint feedback wrapper with timestamp and FPS."""
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
        """Parse one received CAN frame and update cached feedback.

        Parameters
        -------
        `rx_message`: can.Message | None

            Raw CAN frame received from the bus.
        """
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
            # Update leader-arm command feedback.
            self._UpdateArmJointCtrl(msg)
            self._UpdateArmGripperCtrl(msg)
            self._UpdateArmCtrlCode151(msg)
            self._UpdateArmModeCtrl(msg)
            self._UpdatePiperFirmware(msg)
            self._UpdateRespSetInstruction(msg)
            # Feedback introduced in firmware V1.8-8.
            self._UpdateArmGripperState_V3(msg)
            self._UpdateArmGripperCtrl_V3(msg)
            self._UpdateArmIKJointState(msg)
            if self._start_sdk_fk_cal:
                self._UpdatePiperFeedbackFK()
                self._UpdatePiperCtrlFK()

    def GetCurrentInterfaceVersion(self):
        """
        Returns
        -------
        InterfaceVersion

            Current interface version.
        """
        return InterfaceVersion.INTERFACE_V3

    def GetArmStatus(self):
        """Get the arm status feedback.

        CAN ID
        -------
        0x2A1

        Returns
        -------
        `time_stamp`: float

            time stamp

        `Hz`: float

            msg fps

        `arm_status`: ArmMsgFeedbackStatus

            Arm status feedback.

        - ctrl_mode(int): Control mode
          - 0x00 Standby mode
          - 0x01 CAN instruction control mode
          - 0x02 Teaching mode
        - arm_status(int): Robotic arm status
          - 0x00 Normal
          - 0x01 Emergency stop
          - 0x02 No solution
          - 0x03 Singularity point
          - 0x04 Target angle exceeds limit
          - 0x05 Joint communication exception
          - 0x06 Joint brake not released
          - 0x07 Collision occurred
          - 0x08 Overspeed during teaching drag
          - 0x09 Joint status abnormal
          - 0x0A Other exception
          - 0x0B Teaching record
          - 0x0C Teaching execution
          - 0x0D Teaching pause
          - 0x0E Main controller NTC over temperature
          - 0x0F Release resistor NTC over temperature
        - mode_feed(int): Mode feedback
          - 0x00 MOVE P
          - 0x01 MOVE J
          - 0x02 MOVE L
          - 0x03 MOVE C
          - 0x06 MOVE M, supported since V1.8-8
          - 0x05 MOVE CPV, supported since V1.6.5
        - teach_status(int): Teaching status
        - motion_status(int): Motion status
          - 0x00 Reached the target position
          - 0x01 Not yet reached the target position
        - trajectory_num(int): Current trajectory point number
        - err_status(int): Error status
          - joint_1_angle_limit (bool): Joint 1 angle limit exceeded, True for exceeded
          - joint_2_angle_limit (bool): Joint 2 angle limit exceeded, True for exceeded
          - joint_3_angle_limit (bool): Joint 3 angle limit exceeded, True for exceeded
          - joint_4_angle_limit (bool): Joint 4 angle limit exceeded, True for exceeded
          - joint_5_angle_limit (bool): Joint 5 angle limit exceeded, True for exceeded
          - joint_6_angle_limit (bool): Joint 6 angle limit exceeded, True for exceeded
          - communication_status_joint_1 (bool): Joint 1 communication exception, True for exception
          - communication_status_joint_2 (bool): Joint 2 communication exception, True for exception
          - communication_status_joint_3 (bool): Joint 3 communication exception, True for exception
          - communication_status_joint_4 (bool): Joint 4 communication exception, True for exception
          - communication_status_joint_5 (bool): Joint 5 communication exception, True for exception
          - communication_status_joint_6 (bool): Joint 6 communication exception, True for exception
        """
        with self._arm_status_mtx:
            self._arm_status.Hz = self._fps_counter.get_fps("ArmStatus")
            return self._arm_status

    def GetArmGripperMsgs_V3(self):
        """Get the V3 gripper status feedback.

        CAN ID
        ------
        0x2A8

        Returns
        ------
        `time_stamp`: float

            time stamp

        `Hz`: float

            msg fps

        `gripper_state`: ArmMsgFeedBackGripper

            Gripper feedback state.

        - grippers_val(int): The gripper value, in 0.001 mm for width mode or 0.001 degree for angle mode.
        - grippers_effort(int): The torque of the gripper (in 0.001 N·m).
        - mode(int): The gripper control mode, 0x00 for width mode and 0x01 for angle mode.
        - foc_status(int): The status code of the gripper.
          - voltage_too_low(bool): Power voltage low (False: Normal, True: Low)
          - motor_overheating(bool): Motor over-temperature (False: Normal, True: Over-temperature)
          - driver_overcurrent(bool): Driver over-current (False: Normal, True: Over-current)
          - driver_overheating(bool): Driver over-temperature (False: Normal, True: Over-temperature)
          - sensor_status(bool): Sensor status (False: Normal, True: Abnormal)
          - driver_error_status(bool): Driver error status (False: Normal, True: Error)
          - driver_enable_status(bool): Driver enable status (False: Disabled, True: Enabled)
          - homing_status(bool): Zeroing status (False: Not zeroed, True: Zeroed or previously zeroed)
        """
        with self._arm_gripper_msgs_v3_mtx:
            self._arm_gripper_msgs_v3.Hz = self._fps_counter.get_fps('ArmGripper')
            return self._arm_gripper_msgs_v3

    def GetArmGripperCtrl_V3(self):
        """Get the V3 gripper control message sent by command 0x159.

        CAN ID
        ------
        0x159

        Returns
        ------
        `time_stamp`: float

            time stamp

        `Hz`: float

            msg fps

        `gripper_ctrl`: ArmMsgGripperCtrl

        - grippers_val(int): The gripper value, in 0.001 mm for width mode or 0.001 degree for angle mode.
        - grippers_effort(int): Gripper torque, represented as an integer, unit: 0.001N·m. Range 0-5000 (corresponds to 0-5 N·m)
        - status_code(int):
          - 0x00: Disabled;
          - 0x01: Enabled;
          - 0x03: Enable and clear errors in width mode;
          - 0x02: Disable and clear errors in width mode;
          - 0x04: Disable in angle mode;
          - 0x05: Enable in angle mode;
          - 0x06: Disable and clear errors in angle mode;
          - 0x07: Enable and clear errors in angle mode.
        - set_zero(int): Set the current position as the zero point.
          - 0x00: Invalid;
          - 0xAE: Set zero.
        """
        with self._arm_gripper_ctrl_msgs_v3_mtx:
            self._arm_gripper_ctrl_msgs_v3.Hz = self._fps_counter.get_fps("ArmGripperCtrl")
            return self._arm_gripper_ctrl_msgs_v3

    def GetArmIKJointMsgs(self):
        """Get the IK joint status feedback.

        Notes
        -------
        IK joint feedback is not published immediately after the arm is powered
        on. Set the arm to MOVE P mode and send a corresponding end-pose control
        command first; after that trigger, the arm will keep publishing IK joint
        feedback frames.

        Returns
        -------
        `time_stamp`: float

        `Hz`: float

        `ik_joint_states`: ArmMsgFeedBackIKJointStates

        - ik_joint_1(int): Feedback IK angle of joint 1, unit: 0.001 degree.
        - ik_joint_2(int): Feedback IK angle of joint 2, unit: 0.001 degree.
        - ik_joint_3(int): Feedback IK angle of joint 3, unit: 0.001 degree.
        - ik_joint_4(int): Feedback IK angle of joint 4, unit: 0.001 degree.
        - ik_joint_5(int): Feedback IK angle of joint 5, unit: 0.001 degree.
        - ik_joint_6(int): Feedback IK angle of joint 6, unit: 0.001 degree.
        """
        with self._arm_ik_joint_states_mtx:
            self._arm_ik_joint_states.Hz = self._fps_counter.cal_average(self._fps_counter.get_fps('ArmIKJoint_12'),
                                                                        self._fps_counter.get_fps('ArmIKJoint_34'),
                                                                        self._fps_counter.get_fps('ArmIKJoint_56'))
            return self._arm_ik_joint_states

    def _UpdateArmGripperState(self, msg:PiperMessage):
        """Update the legacy gripper status cache.

        Parameters
        -------
        `msg`: PiperMessage

            Aggregated robotic arm message.
        """
        with self._arm_gripper_msgs_mtx:
            if(msg.type_ == self.ArmMsgType.PiperMsgGripperFeedBack):
                gripper_angle = msg.gripper_feedback.grippers_angle
                _mode = msg.gripper_feedback_v3.mode
                if self.isFilterAbnormalData():
                    # Width mode limit: 150 mm * 1000.
                    if _mode == ArmMsgFeedbackGripperEnums_V3.CtrlMode.WIDTH and abs(gripper_angle) > 150000:
                        return
                    # Angle mode limit: 360 degree * 1000.
                    elif _mode == ArmMsgFeedbackGripperEnums_V3.CtrlMode.ANGLE and abs(gripper_angle) > 360000:
                        return
                # self._fps_counter.increment("ArmGripper")
                self._arm_gripper_msgs.time_stamp = msg.time_stamp
                self._arm_gripper_msgs.gripper_state.grippers_angle = self._CalGripperSDKLimit(gripper_angle, _mode)
                self._arm_gripper_msgs.gripper_state.grippers_effort = msg.gripper_feedback.grippers_effort
                self._arm_gripper_msgs.gripper_state.status_code = msg.gripper_feedback.status_code
            return self._arm_gripper_msgs

    def _UpdateArmGripperCtrl(self, msg:PiperMessage):
        """Update the legacy gripper control cache sent by the leader arm.

        Parameters
        -------
        `msg`: PiperMessage

            Aggregated robotic arm message.
        """
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
                   # Width mode limit: 150 mm * 1000.
                    if _mode == 0 and abs(gripper_angle) > 150000:
                        return
                    # Angle mode limit: 360 degree * 1000.
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
        """Update the V3 gripper status cache.

        Parameters
        -------
        `msg`: PiperMessage

            Aggregated robotic arm message.
        """
        with self._arm_gripper_msgs_v3_mtx:
            if(msg.type_ == self.ArmMsgType.PiperMsgGripperFeedBack):
                gripper_val = msg.gripper_feedback.grippers_angle
                _mode = msg.gripper_feedback_v3.mode
                if self.isFilterAbnormalData():
                    # Width mode limit: 150 mm * 1000.
                    if _mode == ArmMsgFeedbackGripperEnums_V3.CtrlMode.WIDTH and abs(gripper_val) > 150000:
                        return
                    # Angle mode limit: 360 degree * 1000.
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
        """Update the V3 gripper control cache sent by the leader arm.

        Parameters
        -------
        `msg`: PiperMessage

            Aggregated robotic arm message.
        """
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
                    # Width mode limit: 150 mm * 1000.
                    if _mode == 0 and abs(gripper_val) > 150000:
                        return
                    # Angle mode limit: 360 degree * 1000.
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
        """Update the IK joint status cache.

        Parameters
        -------
        `msg`: PiperMessage

            Aggregated robotic arm message.
        """
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
        """Send the robotic arm motion control command.

        CAN ID
        -------
        0x151

        Parameters
        -------
        `ctrl_mode`: int
        - 0x00: Standby mode
        - 0x01: CAN command control mode
        - 0x03: Ethernet control mode
        - 0x04: Wi-Fi control mode
        - 0x07: Offline trajectory mode

        `move_mode`: int
        - 0x00: MOVE P
        - 0x01: MOVE J
        - 0x02: MOVE L
        - 0x03: MOVE C
        - 0x06: MOVE M, supported since V1.8-8

        `move_spd_rate_ctrl`: int
        - Movement speed percentage. Range: 0~100.

        `is_mit_mode`: int
        - 0x00: Position-velocity mode
        - 0xAD: MIT mode
        - 0xFF: Invalid

        `residence_time`: int
        - Offline trajectory point residence time. Range: 0~254 seconds;
        - 255 terminates the trajectory.

        `installation_pos`: int

        Installation position. Pay attention to rear-facing wiring.
        - 0x00: Invalid value
        - 0x01: Horizontal upright
        - 0x02: Side mount left
        - 0x03: Side mount right
        - 0x04: Horizontal inverted --- v1.8-8
        """
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
        """Control the gripper in legacy width mode.

        CAN ID
        -------
        0x159

        Parameters
        -------
        `gripper_angle`: int
        - Gripper width, unit: 0.001 mm.

        `gripper_effort`: int
        - Gripper torque, unit: 0.001 N·m. Range: 0~5000.

        `gripper_code`: int
        - 0x00: Disable
        - 0x01: Enable
        - 0x02: Disable and clear error
        - 0x03: Enable and clear error

        `set_zero`: int
        - 0x00: Invalid value
        - 0xAE: Set current position as zero point
        """
        if gripper_code not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"'status_code' Value {gripper_code} out of range [0x00, 0x01, 0x02, 0x03]")
        self.GripperCtrl_V3(gripper_angle, gripper_effort, gripper_code, set_zero)

    def GripperCtrl_V3(self,
                    gripper_val: int = 0,
                    gripper_effort: int = 0,
                    gripper_code: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07] = 0,
                    set_zero: Literal[0x00, 0xAE] = 0):
        """Control the gripper in width mode or angle mode.

        CAN ID
        -------
        0x159

        Parameters
        -------
        `gripper_val`: int
        - Gripper value. Unit: 0.001 mm in width mode, or 0.001 degree in angle mode.

        `gripper_effort`: int
        - Gripper torque, unit: 0.001 N·m. Range: 0~5000.

        `gripper_code`: int
        - 0x00: Disable, width mode
        - 0x01: Enable, width mode
        - 0x02: Disable and clear error, width mode
        - 0x03: Enable and clear error, width mode
        - 0x04: Disable, angle mode
        - 0x05: Enable, angle mode
        - 0x06: Disable and clear error, angle mode
        - 0x07: Enable and clear error, angle mode

        `set_zero`: int
        - 0x00: Invalid value
        - 0xAE: Set current position as zero point
        """
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
        """Send a joint 1~6 MIT control command with protocol limits.

        CAN IDs
        -------
        0x15A, 0x15B, 0x15C, 0x15D, 0x15E, 0x15F

        Notes
        -------
        `p_min`, `p_max`, `v_min`, `v_max`, `kp_min`, `kp_max`, `kd_min`,
        `kd_max`, `t_min`, and `t_max` are protocol constants and should not be
        changed by callers.

        Parameters
        -------
        `motor_num`: int

            Motor index. Range: 1~6.

        `pos_ref`: float

            Desired target position.

        `vel_ref`: float

            Desired motor speed.

        `kp`: float

            Proportional gain.

        `kd`: float

            Derivative gain.

        `t_ref`: float

            Target torque reference.
        """
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
        """Send a joint 1~6 MIT control command.

        CAN IDs
        -------
        0x15A, 0x15B, 0x15C, 0x15D, 0x15E, 0x15F

        Parameters
        -------
        `motor_num`: int

            Motor index. Range: 1~6.

        `pos_ref`: float

            Desired target position, unit: rad. Range: -12.5~12.5.

        `vel_ref`: float

            Desired motor speed. Range: -45.0~45.0.

        `kp`: float

            Proportional gain. Reference value: 10. Range: 0.0~500.0.

        `kd`: float

            Derivative gain. Reference value: 0.8. Range: -5.0~5.0.

        `t_ref`: float

            Target torque reference. Range: -16.0~16.0.
        """
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
