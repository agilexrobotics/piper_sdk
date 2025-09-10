#!/usr/bin/env python3
# -*-coding:utf8-*-
from enum import IntEnum, auto, unique

class _EnumBase(IntEnum):
    def __str__(self):
        # return f"{self.__class__.__name__}.{self.name}(0x{self.value:X})"
        return f"{self.name}(0x{self.value:X})"
    def __repr__(self):
        # return f"{self.__class__.__name__}.{self.name}(0x{self.value:X})"
        return f"{self.name}(0x{self.value:X})"
    @classmethod
    def match_value(cls, val):
        if not isinstance(val, int):
            raise ValueError(f"{cls.__name__}: input value must be an integer, got {type(val).__name__}")
        try:
            return cls(val)
        except ValueError:
            if hasattr(cls, "UNKNOWN"):
                return cls.UNKNOWN
            else:
                raise ValueError(f"{cls.__name__}: invalid enum value 0x{val:X}, and no UNKNOWN defined")

class ArmMsgFeedbackStatusEnum:
    @unique
    class CtrlMode(_EnumBase):
        STANDBY = 0x00
        CAN_CTRL = 0x01
        TEACHING_MODE = 0x02
        ETHERNET_CONTROL_MODE = 0x03
        WIFI_CONTROL_MODE = 0x04
        REMOTE_CONTROL_MODE = 0x05
        LINKAGE_TEACHING_INPUT_MODE = 0x06
        OFFLINE_TRAJECTORY_MODE = 0x07
        UNKNOWN = 0xFF
    @unique
    class ArmStatus(_EnumBase):
        NORMAL = 0x00
        EMERGENCY_STOP = 0x01
        NO_SOLUTION = 0x02
        SINGULARITY_POINT = 0x03
        TARGET_POS_EXCEEDS_LIMIT = 0x04
        JOINT_COMMUNICATION_ERR = 0x05
        JOINT_BRAKE_NOT_RELEASED = 0x06
        COLLISION_OCCURRED = 0x07
        OVERSPEED_DURING_TEACHING_DRAG = 0x08
        JOINT_STATUS_ERR = 0x09
        OTHER_ERR = 0x0A
        TEACHING_RECORD = 0x0B
        TEACHING_EXECUTION = 0x0C
        TEACHING_PAUSE = 0x0D
        MAIN_CONTROLLER_NTC_OVER_TEMPERATURE = 0x0E
        RELEASE_RESISTOR_NTC_OVER_TEMPERATURE = 0x0F
        UNKNOWN = 0xFF
    @unique
    class ModeFeed(_EnumBase):
        MOVE_P = 0x00
        MOVE_J = 0x01
        MOVE_L = 0x02
        MOVE_C = 0x03
        MOVE_M = 0x04
        MOVE_CPV = 0x05
        UNKNOWN = 0xFF
    @unique
    class TeachingState(_EnumBase):
        DISABLED = 0x00               # 关闭
        START_RECORDING = 0x01        # 开始示教记录（进入拖动示教模式）
        STOP_RECORDING = 0x02         # 结束示教记录（退出拖动示教模式）
        EXECUTE_TRAJECTORY = 0x03     # 执行示教轨迹（拖动示教轨迹复现）
        PAUSE_EXECUTION = 0x04        # 暂停执行
        RESUME_EXECUTION = 0x05       # 继续执行（轨迹复现继续）
        TERMINATE_EXECUTION = 0x06    # 终止执行
        MOVE_TO_START = 0x07          # 运动到轨迹起点
        UNKNOWN = 0xFF
    @unique
    class MotionStatus(_EnumBase):
        REACH_TARGET_POS_SUCCESSFULLY = 0x00
        REACH_TARGET_POS_FAILED = 0x01
        UNKNOWN = 0xFF

class ArmMsgFeedbackStatus:
    '''
    msg_v2_feedback
    
    机械臂状态

    CAN ID:
        0x2A1

    Args:
        ctrl_mode: 控制模式
        arm_status: 机械臂状态
        mode_feed: 模式反馈
        teach_status: 示教状态
        motion_status: 运动状态
        trajectory_num: 当前运行轨迹点序号
        err_code: 故障码
    
    位描述:

        Byte 0:控制模式,uint8 
            0x00 待机模式
            0x01 CAN指令控制模式
            0x02 示教模式
            0x03 以太网控制模式
            0x04 wifi控制模式
            0x05 遥控器控制模式
            0x06 联动示教输入模式
            0x07 离线轨迹模式
        Byte 1:机械臂状态,uint8 
            0x00 正常
            0x01 急停
            0x02 无解
            0x03 奇异点
            0x04 目标角度超过限
            0x05 关节通信异常
            0x06 关节抱闸未打开
            0x07 机械臂发生碰撞
            0x08 拖动示教时超速
            0x09 关节状态异常
            0x0A 其它异常
            0x0B 示教记录
            0x0C 示教执行
            0x0D 示教暂停
            0x0E 主控NTC过温
            0x0F 释放电阻NTC过温
        Byte 2:模式反馈,uint8 
            0x00 MOVE P
            0x01 MOVE J
            0x02 MOVE L
            0x03 MOVE C
            0x04 MOVE M ---基于V1.5-2版本后
            0x05 MOVE_CPV ---基于V1.6.5版本后
        Byte 3:示教状态,uint8 
            0x00 关闭
            0x01 开始示教记录（进入拖动示教模式）
            0x02 结束示教记录（退出拖动示教模式）
            0x03 执行示教轨迹（拖动示教轨迹复现）
            0x04 暂停执行
            0x05 继续执行（轨迹复现继续）
            0x06 终止执行
            0x07 运动到轨迹起点
        Byte 4:运动状态,uint8 
            0x00 到达指定点位
            0x01 未到达指定点位
        Byte 5:当前运行轨迹点序号,uint8_t
            0~255 (离线轨迹模式下反馈)
        Byte 6:故障码*,uint16
            bit[0]      1号关节角度超限位(0:正常 1:异常)
            bit[1]      2号关节角度超限位(0:正常 1:异常)
            bit[2]      3号关节角度超限位(0:正常 1:异常)
            bit[3]      4号关节角度超限位(0:正常 1:异常)
            bit[4]      5号关节角度超限位(0:正常 1:异常)
            bit[5]      6号关节角度超限位(0:正常 1:异常)
            bit[6]      保留(Reserved)
            bit[7]      保留(Reserved)
        Byte 7:故障码*,uint16
            bit[0]      1号关节通信异常(0:正常 1:异常)
            bit[1]      2号关节通信异常(0:正常 1:异常)
            bit[2]      3号关节通信异常(0:正常 1:异常)
            bit[3]      4号关节通信异常(0:正常 1:异常)
            bit[4]      5号关节通信异常(0:正常 1:异常)
            bit[5]      6号关节通信异常(0:正常 1:异常)
            bit[6]      保留
            bit[7]      保留
    '''
    '''
    msg_v2_feedback
    
    Robot Arm Status

    CAN ID: 
        0x2A1

    Arguments:
        ctrl_mode: Control mode
        arm_status: Robot arm status
        mode_feed: Mode feedback
        teach_status: Teaching status
        motion_status: Motion status
        trajectory_num: Current trajectory point number
        err_code: Error code
    
    Bit Description:

        Byte 0: Control mode, uint8
            0x00: Standby mode
            0x01: CAN instruction control mode
            0x02: Teaching mode
            0x03: Ethernet control mode
            0x04: Wi-Fi control mode
            0x05: Remote control mode
            0x06: Linkage teaching input mode
            0x07: Offline trajectory mode
        Byte 1: Robot arm status, uint8
            0x00: Normal
            0x01: Emergency stop
            0x02: No solution
            0x03: Singularity point
            0x04: Target angle exceeds limit
            0x05: Joint communication exception
            0x06: Joint brake not released
            0x07: Collision occurred
            0x08: Overspeed during teaching drag
            0x09: Joint status abnormal
            0x0A: Other exception
            0x0B: Teaching record
            0x0C: Teaching execution
            0x0D: Teaching pause
            0x0E: Main controller NTC over temperature
            0x0F: Release resistor NTC over temperature
        Byte 2: Mode feedback, uint8
            0x00: MOVE P
            0x01: MOVE J
            0x02: MOVE L
            0x03: MOVE C
            0x04: MOVE M
            0x05: MOVE_CPV
        Byte 3: Teaching status, uint8
            0x00: Off
            0x01: Start teaching record (enter drag teaching mode)
            0x02: End teaching record (exit drag teaching mode)
            0x03: Execute teaching trajectory (reproduce drag teaching trajectory)
            0x04: Pause execution
            0x05: Continue execution (continue trajectory reproduction)
            0x06: Terminate execution
            0x07: Move to trajectory starting point
        Byte 4: Motion status, uint8
            0x00: Reached the target position
            0x01: Not yet reached the target position
        Byte 5: Current trajectory point number, uint8_t
            0~255 (feedback in offline trajectory mode)
        Byte 6: Error code, uint16
            bit[0]: Joint 1 angle limit exceeded (0: normal, 1: abnormal)
            bit[1]: Joint 2 angle limit exceeded (0: normal, 1: abnormal)
            bit[2]: Joint 3 angle limit exceeded (0: normal, 1: abnormal)
            bit[3]: Joint 4 angle limit exceeded (0: normal, 1: abnormal)
            bit[4]: Joint 5 angle limit exceeded (0: normal, 1: abnormal)
            bit[5]: Joint 6 angle limit exceeded (0: normal, 1: abnormal)
            bit[6]: Reserved
            bit[7]: Reserved
        Byte 7: Error code, uint16
            bit[0]: Joint 1 communication exception (0: normal, 1: abnormal)
            bit[1]: Joint 2 communication exception (0: normal, 1: abnormal)
            bit[2]: Joint 3 communication exception (0: normal, 1: abnormal)
            bit[3]: Joint 4 communication exception (0: normal, 1: abnormal)
            bit[4]: Joint 5 communication exception (0: normal, 1: abnormal)
            bit[5]: Joint 6 communication exception (0: normal, 1: abnormal)
            bit[6]: Reserved
            bit[7]: Reserved
    '''
    
    def __init__(self,
                 ctrl_mode: int = 0,
                 arm_status: int = 0,
                 mode_feed: int = 0,
                 teach_status: int = 0,
                 motion_status: int = 0,
                 trajectory_num: int = 0,
                 err_code: int = 0):
        self._ctrl_mode:ArmMsgFeedbackStatusEnum.CtrlMode = ArmMsgFeedbackStatusEnum.CtrlMode.match_value(ctrl_mode)
        self.ctrl_mode = self._ctrl_mode
        self._arm_status:ArmMsgFeedbackStatusEnum.ArmStatus = ArmMsgFeedbackStatusEnum.ArmStatus.match_value(arm_status)
        self.arm_status: int = self._arm_status      #机械臂状态
        self._mode_feed:ArmMsgFeedbackStatusEnum.ModeFeed = ArmMsgFeedbackStatusEnum.ModeFeed.match_value(mode_feed)
        self.mode_feed: int = self._mode_feed       #模式反馈
        self._teach_status:ArmMsgFeedbackStatusEnum.TeachingState = ArmMsgFeedbackStatusEnum.TeachingState.match_value(teach_status)
        self.teach_status: int = self._teach_status    #示教状态
        self._motion_status:ArmMsgFeedbackStatusEnum.MotionStatus = ArmMsgFeedbackStatusEnum.MotionStatus.match_value(motion_status)
        self.motion_status: int = self._motion_status   #运动状态
        self.trajectory_num: int = trajectory_num  #当前运行轨迹点序号
        self._err_code = err_code         #故障码
        self.err_status = self.ErrStatus()#故障码

    @property
    def ctrl_mode(self) -> ArmMsgFeedbackStatusEnum.CtrlMode:
        return self._ctrl_mode
    @ctrl_mode.setter
    def ctrl_mode(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum.CtrlMode):
            self._ctrl_mode = value
        else:
            self._ctrl_mode = ArmMsgFeedbackStatusEnum.CtrlMode.match_value(value)
    
    @property
    def arm_status(self) -> ArmMsgFeedbackStatusEnum.ArmStatus:
        return self._arm_status
    @arm_status.setter
    def arm_status(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum.ArmStatus):
            self._arm_status = value
        else:
            self._arm_status = ArmMsgFeedbackStatusEnum.ArmStatus.match_value(value)
    
    @property
    def mode_feed(self) -> ArmMsgFeedbackStatusEnum.ModeFeed:
        return self._mode_feed
    @mode_feed.setter
    def mode_feed(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum.ModeFeed):
            self._mode_feed = value
        else:
            self._mode_feed = ArmMsgFeedbackStatusEnum.ModeFeed.match_value(value)
    
    @property
    def teach_status(self) -> ArmMsgFeedbackStatusEnum.TeachingState:
        return self._teach_status
    @teach_status.setter
    def teach_status(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum.TeachingState):
            self._teach_status = value
        else:
            self._teach_status = ArmMsgFeedbackStatusEnum.TeachingState.match_value(value)

    @property
    def motion_status(self) -> ArmMsgFeedbackStatusEnum.MotionStatus:
        return self._motion_status
    @motion_status.setter
    def motion_status(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum.MotionStatus):
            self._motion_status = value
        else:
            self._motion_status = ArmMsgFeedbackStatusEnum.MotionStatus.match_value(value)

    class ErrStatus:
        def __init__(self):
            self.joint_1_angle_limit = False
            self.joint_2_angle_limit = False
            self.joint_3_angle_limit = False
            self.joint_4_angle_limit = False
            self.joint_5_angle_limit = False
            self.joint_6_angle_limit = False
            self.communication_status_joint_1 = False
            self.communication_status_joint_2 = False
            self.communication_status_joint_3 = False
            self.communication_status_joint_4 = False
            self.communication_status_joint_5 = False
            self.communication_status_joint_6 = False
            
        def __str__(self):
            return (f" Joint 1 Angle Limit Status: {self.joint_1_angle_limit}\n"
                    f" Joint 2 Angle Limit Status: {self.joint_2_angle_limit}\n"
                    f" Joint 3 Angle Limit Status: {self.joint_3_angle_limit}\n"
                    f" Joint 4 Angle Limit Status: {self.joint_4_angle_limit}\n"
                    f" Joint 5 Angle Limit Status: {self.joint_5_angle_limit}\n"
                    f" Joint 6 Angle Limit Status: {self.joint_6_angle_limit}\n"
                    f" Joint 1 Communication Status: {self.communication_status_joint_1}\n"
                    f" Joint 2 Communication Status: {self.communication_status_joint_2}\n"
                    f" Joint 3 Communication Status: {self.communication_status_joint_3}\n"
                    f" Joint 4 Communication Status: {self.communication_status_joint_4}\n"
                    f" Joint 5 Communication Status: {self.communication_status_joint_5}\n"
                    f" Joint 6 Communication Status: {self.communication_status_joint_6}\n")

    @property
    def err_code(self):
        return self._err_code

    @err_code.setter
    def err_code(self, value: int):
        if not (0 <= value < 2**16):
            raise ValueError("err_code must be an 16-bit integer between 0 and 65535.")
        self._err_code = value
        # Update err_status based on the err_code bits
        # example: 42 0A -> 0100 0010 0000 1010
        # bit:              7654 3210 7654 3210
        # info:              |angle  | |communication
        self.err_status.communication_status_joint_1 = bool(value & (1 << 0))
        self.err_status.communication_status_joint_2 = bool(value & (1 << 1))
        self.err_status.communication_status_joint_3 = bool(value & (1 << 2))
        self.err_status.communication_status_joint_4 = bool(value & (1 << 3))
        self.err_status.communication_status_joint_5 = bool(value & (1 << 4))
        self.err_status.communication_status_joint_6 = bool(value & (1 << 5))
        self.err_status.joint_1_angle_limit = bool(value & (1 << 8))
        self.err_status.joint_2_angle_limit = bool(value & (1 << 9))
        self.err_status.joint_3_angle_limit = bool(value & (1 << 10))
        self.err_status.joint_4_angle_limit = bool(value & (1 << 11))
        self.err_status.joint_5_angle_limit = bool(value & (1 << 12))
        self.err_status.joint_6_angle_limit = bool(value & (1 << 13))

    def __str__(self):
        return (f"Control Mode: {self.ctrl_mode}\n"
                f"Arm Status: {self.arm_status}\n"
                f"Mode Feed: {self.mode_feed}\n"
                f"Teach Status: {self.teach_status}\n"
                f"Motion Status: {self.motion_status}\n"
                f"Trajectory Num: {self.trajectory_num}\n"
                f"Error Code: {self._err_code}\n"
                f"Error Status: \n{self.err_status}\n")

    def __repr__(self):
        return self.__str__()