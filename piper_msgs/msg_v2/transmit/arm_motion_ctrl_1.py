#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgMotionCtrl_1():
    '''
    msg_v2_transmit
    
    机械臂运动控制指令1
    
    CAN ID:
        0x150
    
    Args:
        emergency_stop: 快速急停
        track_ctrl: 轨迹指令
        grag_teach_ctrl: 拖动示教指令
    
    位描述:
    
        Byte 0: 快速急停     uint8    0x00 无效
                                    0x01 快速急停
                                    0x02 恢复
        Byte 1: 轨迹指令     uint8    0x00 关闭
                                    0x01 暂停当前规划
                                    0x02 继续当前轨迹
                                    0x03 清除当前轨迹
                                    0x04 清除所有轨迹
                                    0x05 获取当前规划轨迹
                                    0x06 终止执行
                                    0x07 轨迹传输
                                    0x08 轨迹传输结束
        Byte 2: 拖动示教指令 uint8     0x00 关闭
                                    0x01 开始示教记录（进入拖动示教模式）
                                    0x02 结束示教记录（退出拖动示教模式）
                                    0x03 执行示教轨迹（拖动示教轨迹复现）
                                    0x04 暂停执行
                                    0x05 继续执行（轨迹复现继续）
                                    0x06 终止执行
                                    0x07 运动到轨迹起点
        Byte 3: 轨迹索引    uint8     标记刚才传输的轨迹点为第N个轨迹点
                                    N=0~255
                                    主控收到后会应答0x476 byte0 = 0x50 ;byte 2=N(详见0x476 )未收到应答需要重传
        Byte 4: NameIndex_H uint16   当前轨迹包名称索引,由NameIndex和crc组成(应答0x477 byte0=03)
        Byte 5: NameIndex_L
        Byte 6: crc16_H     uint16  
        Byte 7: crc16_L
    '''
    '''
    msg_v2_transmit
    
    Robotic Arm Motion Control Command 1

    CAN ID:
        0x150

    Args:
        emergency_stop: Emergency stop command.
        track_ctrl: Trajectory control command.
        grag_teach_ctrl: Drag teach command.

    Bit Descriptions:

        Byte 0: emergency_stop: uint8, emergency stop control.
            0x00: Invalid.
            0x01: Activate emergency stop.
            0x02: Resume from emergency stop.

        Byte 1: track_ctrl: uint8, trajectory control instructions.
            0x00: Disable.
            0x01: Pause current planning.
            0x02: Resume current trajectory.
            0x03: Clear current trajectory.
            0x04: Clear all trajectories.
            0x05: Get the current planned trajectory.
            0x06: Terminate execution.
            0x07: Trajectory transfer.
            0x08: End trajectory transfer.

        Byte 2: grag_teach_ctrl: uint8, drag teach control.
            0x00: Disable.
            0x01: Start teaching record (enter drag teach mode).
            0x02: End teaching record (exit drag teach mode).
            0x03: Execute the teaching trajectory (reproduce drag teaching trajectory).
            0x04: Pause execution.
            0x05: Continue execution (resume trajectory reproduction).
            0x06: Terminate execution.
            0x07: Move to the starting point of the trajectory.

        Byte 3: trajectory_index: uint8, mark the transmitted trajectory point as the Nth trajectory point.
            N = 0~255:
            The controller responds with CAN ID: 0x476, Byte 0 = 0x50, Byte 2 = N. If no response is received, retransmission is required.

        Byte 4-5: NameIndex_H/L: uint16, current trajectory packet name index, composed of NameIndex and CRC.
            Response on CAN ID: 0x477, Byte 0 = 0x03.

        Byte 6-7: crc16_H/L: uint16, CRC checksum for validation.
    '''
    def __init__(self, 
                 emergency_stop: Literal[0x00, 0x01, 0x02] = 0, 
                 track_ctrl: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08] = 0, 
                 grag_teach_ctrl: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07] = 0):
        # 检查 emergency_stop 是否在有效范围内
        if emergency_stop not in [0x00, 0x01, 0x02]:
            raise ValueError(f"'emergency_stop' Value {emergency_stop} out of range [0x00, 0x01, 0x02]")
        
        # 检查 track_ctrl 是否在有效范围内
        if track_ctrl not in [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]:
            raise ValueError(f"'track_ctrl' Value {track_ctrl} out of range [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]")
        
        # 检查 grag_teach_ctrl 是否在有效范围内
        if grag_teach_ctrl not in [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]:
            raise ValueError(f"'grag_teach_ctrl' Value {grag_teach_ctrl} out of range [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]")
        self.emergency_stop = emergency_stop
        self.track_ctrl = track_ctrl
        self.grag_teach_ctrl = grag_teach_ctrl

    def __str__(self):
        dict_ = [
            (" emergency_stop ", self.emergency_stop),
            (" track_ctrl ", self.track_ctrl),
            (" grag_teach_ctrl ", self.grag_teach_ctrl)
        ]

        # 生成格式化字符串，保留三位小数
        formatted_ = "\n".join([f"{name}: {value}" for name, value in dict_])
        
        return f"ArmMsgMotionCtrl_1:\n{formatted_}"
    
    def __repr__(self):
        return self.__str__()