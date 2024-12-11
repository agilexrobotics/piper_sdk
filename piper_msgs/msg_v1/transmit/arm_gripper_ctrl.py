#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgGripperCtrl:
    '''
    夹爪控制指令
    
    CAN ID:
        0x159
    
    Args:
        grippers_angle: 夹爪行程
        grippers_effort: 夹爪扭矩
        status_code: 夹爪使能/失能/清除错误
        set_zero: 夹爪零点设置
    
    位描述:
    
        Byte 0 grippers_angle: int32, 单位 0.001°, 夹爪角度,以整数表示。
        Byte 1
        Byte 2
        Byte 3
        Byte 4 grippers_effort: uint16, 单位 0.001N/m, 夹爪扭矩,以整数表示。
        Byte 5
        Byte 6 status_code: uint8, 夹爪状态码，使能/失能/清除错误
                - 0x00失能,0x01使能
                - 0x03/0x02,使能清除错误,失能清除错误
        Byte 7 set_zero: uint8, 设定当前位置为0点
                - 0x00无效值
                - 0xAE设置零点
    '''
    '''
    Gripper Control Command

    CAN ID:
        0x159

    Args:
        grippers_angle: Gripper stroke, represented as an integer, unit: 0.001°.
        grippers_effort: Gripper torque, represented as an integer, unit: 0.001N·m.
        status_code: Gripper state for enable/disable/clear error.
            0x00: Disable.
            0x01: Enable.
            0x03/0x02: Enable with clear error / Disable with clear error.
        set_zero: Set the current position as the zero point.

    Bit Description:

        Byte 0-3 grippers_angle: int32, unit: 0.001°, represents the gripper angle.
        Byte 4-5 grippers_effort: uint16, unit: 0.001N·m, represents the gripper torque.
        Byte 6 status_code: uint8, gripper status code for enable/disable/clear error.
        Byte 7 set_zero: uint8, flag to set the current position as the zero point.
    '''
    def __init__(self, 
                 grippers_angle: int=0, 
                 grippers_effort: int=0, 
                 status_code: Literal[0x00,0x01,0x02,0x03]=0,
                 set_zero: Literal[0x00,0xAE]=0):
        if status_code not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"status_code 值 {status_code} 超出范围 [0x00, 0x01, 0x02, 0x03]")
        self.grippers_angle = grippers_angle
        self.grippers_effort = grippers_effort
        self.status_code = status_code
        self.set_zero = set_zero

    def __str__(self):
        return (f"ArmMsgGripperCtrl(\n"
                f"  grippers_angle: {self.grippers_angle * 0.001:.3f},\n"
                f"  grippers_effort: {self.grippers_effort * 0.01:.2f},\n"
                f"  status_code: {self.status_code},\n"
                f"  set_zero: {self.set_zero}\n"
                f")")

    def __repr__(self):
        return self.__str__()
