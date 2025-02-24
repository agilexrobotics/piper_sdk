#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgStatus:
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
            bit[0]      1号关节通信异常(0:正常 1:异常)
            bit[1]      2号关节通信异常(0:正常 1:异常)
            bit[2]      3号关节通信异常(0:正常 1:异常)
            bit[3]      4号关节通信异常(0:正常 1:异常)
            bit[4]      5号关节通信异常(0:正常 1:异常)
            bit[5]      6号关节通信异常(0:正常 1:异常)
            bit[6]      保留(Reserved)
            bit[7]      保留(Reserved)
        Byte 7:故障码*,uint16
            bit[0]      1号关节角度超限位(0:正常 1:异常)
            bit[1]      2号关节角度超限位(0:正常 1:异常)
            bit[2]      3号关节角度超限位(0:正常 1:异常)
            bit[3]      4号关节角度超限位(0:正常 1:异常)
            bit[4]      5号关节角度超限位(0:正常 1:异常)
            bit[5]      6号关节角度超限位(0:正常 1:异常)
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
            bit[0]: Joint 1 communication exception (0: normal, 1: abnormal)
            bit[1]: Joint 2 communication exception (0: normal, 1: abnormal)
            bit[2]: Joint 3 communication exception (0: normal, 1: abnormal)
            bit[3]: Joint 4 communication exception (0: normal, 1: abnormal)
            bit[4]: Joint 5 communication exception (0: normal, 1: abnormal)
            bit[5]: Joint 6 communication exception (0: normal, 1: abnormal)
            bit[6]: Reserved
            bit[7]: Reserved
        Byte 7: Error code, uint16
            bit[0]: Joint 1 angle limit exceeded (0: normal, 1: abnormal)
            bit[1]: Joint 2 angle limit exceeded (0: normal, 1: abnormal)
            bit[2]: Joint 3 angle limit exceeded (0: normal, 1: abnormal)
            bit[3]: Joint 4 angle limit exceeded (0: normal, 1: abnormal)
            bit[4]: Joint 5 angle limit exceeded (0: normal, 1: abnormal)
            bit[5]: Joint 6 angle limit exceeded (0: normal, 1: abnormal)
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
        self.ctrl_mode: int = ctrl_mode       #控制模式
        self.arm_status: int = arm_status      #机械臂状态
        self.mode_feed: int = mode_feed       #模式反馈
        self.teach_status: int = teach_status    #示教状态
        self.motion_status: int = motion_status   #运动状态
        self.trajectory_num: int = trajectory_num  #当前运行轨迹点序号
        self._err_code = err_code         #故障码
        self.err_status = self.ErrStatus()#故障码

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
            raise ValueError("err_code must be an 8-bit integer between 0 and 255.")
        self._err_code = value
        # Update err_status based on the err_code bits
        self.err_status.communication_status_joint_1 = bool(value & (1 << 0))
        self.err_status.communication_status_joint_2 = bool(value & (1 << 1))
        self.err_status.communication_status_joint_3 = bool(value & (1 << 2))
        self.err_status.communication_status_joint_4 = bool(value & (1 << 3))
        self.err_status.communication_status_joint_5 = bool(value & (1 << 4))
        self.err_status.communication_status_joint_6 = bool(value & (1 << 5))
        self.err_status.communication_status_joint_1 = bool(value & (1 << 8))
        self.err_status.communication_status_joint_2 = bool(value & (1 << 9))
        self.err_status.communication_status_joint_3 = bool(value & (1 << 10))
        self.err_status.communication_status_joint_4 = bool(value & (1 << 11))
        self.err_status.communication_status_joint_5 = bool(value & (1 << 12))
        self.err_status.communication_status_joint_6 = bool(value & (1 << 13))

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