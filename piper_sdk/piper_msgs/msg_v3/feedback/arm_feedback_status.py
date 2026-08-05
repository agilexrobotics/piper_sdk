#!/usr/bin/env python3
# -*-coding:utf8-*-
from enum import unique

from ...core import IntEnumBase

from ...msg_v2.feedback.arm_feedback_status import ArmMsgFeedbackStatusEnum, ArmMsgFeedbackStatus

class ArmMsgFeedbackStatusEnum_V3(ArmMsgFeedbackStatusEnum):
    @unique
    class ModeFeed(IntEnumBase):
        MOVE_P = 0x00
        MOVE_J = 0x01
        MOVE_L = 0x02
        MOVE_C = 0x03
        MOVE_M = 0x06
        MOVE_CPV = 0x05
        UNKNOWN = 0xFF

class ArmMsgFeedbackStatus_V3(ArmMsgFeedbackStatus):
    '''
    
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
            0x06 MOVE M ---基于V1.8-8版本后
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
            0x06: MOVE M
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
        self._ctrl_mode:ArmMsgFeedbackStatusEnum_V3.CtrlMode = ArmMsgFeedbackStatusEnum_V3.CtrlMode.match_value(ctrl_mode)
        self.ctrl_mode = self._ctrl_mode
        self._arm_status:ArmMsgFeedbackStatusEnum_V3.ArmStatus = ArmMsgFeedbackStatusEnum_V3.ArmStatus.match_value(arm_status)
        self.arm_status: int = self._arm_status      #机械臂状态
        self._mode_feed:ArmMsgFeedbackStatusEnum_V3.ModeFeed = ArmMsgFeedbackStatusEnum_V3.ModeFeed.match_value(mode_feed)
        self.mode_feed: int = self._mode_feed       #模式反馈
        self._teach_status:ArmMsgFeedbackStatusEnum_V3.TeachingState = ArmMsgFeedbackStatusEnum_V3.TeachingState.match_value(teach_status)
        self.teach_status: int = self._teach_status    #示教状态
        self._motion_status:ArmMsgFeedbackStatusEnum_V3.MotionStatus = ArmMsgFeedbackStatusEnum_V3.MotionStatus.match_value(motion_status)
        self.motion_status: int = self._motion_status   #运动状态
        self.trajectory_num: int = trajectory_num  #当前运行轨迹点序号
        self._err_code = err_code         #故障码
        self.err_status = self.ErrStatus()#故障码

    @property
    def ctrl_mode(self) -> ArmMsgFeedbackStatusEnum_V3.CtrlMode:
        return self._ctrl_mode
    @ctrl_mode.setter
    def ctrl_mode(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum_V3.CtrlMode):
            self._ctrl_mode = value
        else:
            self._ctrl_mode = ArmMsgFeedbackStatusEnum_V3.CtrlMode.match_value(value)
    
    @property
    def arm_status(self) -> ArmMsgFeedbackStatusEnum_V3.ArmStatus:
        return self._arm_status
    @arm_status.setter
    def arm_status(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum_V3.ArmStatus):
            self._arm_status = value
        else:
            self._arm_status = ArmMsgFeedbackStatusEnum_V3.ArmStatus.match_value(value)
    
    @property
    def mode_feed(self) -> ArmMsgFeedbackStatusEnum_V3.ModeFeed:
        return self._mode_feed
    @mode_feed.setter
    def mode_feed(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum_V3.ModeFeed):
            self._mode_feed = value
        else:
            self._mode_feed = ArmMsgFeedbackStatusEnum_V3.ModeFeed.match_value(value)
    
    @property
    def teach_status(self) -> ArmMsgFeedbackStatusEnum_V3.TeachingState:
        return self._teach_status
    @teach_status.setter
    def teach_status(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum_V3.TeachingState):
            self._teach_status = value
        else:
            self._teach_status = ArmMsgFeedbackStatusEnum_V3.TeachingState.match_value(value)

    @property
    def motion_status(self) -> ArmMsgFeedbackStatusEnum_V3.MotionStatus:
        return self._motion_status
    @motion_status.setter
    def motion_status(self, value:int):
        if isinstance(value, ArmMsgFeedbackStatusEnum_V3.MotionStatus):
            self._motion_status = value
        else:
            self._motion_status = ArmMsgFeedbackStatusEnum_V3.MotionStatus.match_value(value)
