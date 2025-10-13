#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgGripperCtrl:
    '''
    msg_v2_transmit
    
    夹爪控制指令
    
    CAN ID:
        0x159
    
    Args:
        grippers_angle: 夹爪行程
        grippers_effort: 夹爪扭矩,范围0-5000,对应0-5N/m
        status_code: 
                0x00失能;
                0x01使能;
                0x02失能清除错误;
                0x03使能清除错误.
        set_zero: 夹爪零点设置
                0x00无效值
                0xAE设置零点
    
    位描述:
    
        Byte 0 grippers_angle: int32, 单位 0.001mm, 夹爪行程,以整数表示。
        Byte 1
        Byte 2
        Byte 3
        Byte 4 grippers_effort: uint16, 单位 0.001N/m, 夹爪扭矩,以整数表示。
        Byte 5
        Byte 6 status_code: uint8, 夹爪状态码, 使能/失能/清除错误;
                0x00失能;
                0x01使能;
                0x02失能清除错误;
                0x03使能清除错误.
        Byte 7 set_zero: uint8, 设定当前位置为0点
                0x00无效值
                0xAE设置零点
    '''
    '''
    msg_v2_transmit
    
    Gripper Control Command

    CAN ID:
        0x159

    Args:
        grippers_angle: Gripper stroke, represented as an integer, unit: 0.001mm.
        grippers_effort: Gripper torque, represented as an integer, unit: 0.001N·m.Range 0-5000,corresponse 0-5N/m
        status_code: 
            0x00: Disable;
            0x01: Enable;
            0x03: Enable with clear error;
            0x02: Disable with clear error.
        set_zero: Set the current position as the zero point.
            0x00: Invalid;
            0xAE: Set zero.

    Bit Description:

        Byte 0-3 grippers_angle: int32, unit: 0.001°, represents the gripper stroke.
        Byte 4-5 grippers_effort: uint16, unit: 0.001N·m, represents the gripper torque.
        Byte 6 status_code: uint8, gripper status code for enable/disable/clear error.
            0x00: Disable;
            0x01: Enable;
            0x03: Enable with clear error;
            0x02: Disable with clear error.
        Byte 7 set_zero: uint8, flag to set the current position as the zero point.
            0x00: Invalid;
            0xAE: Set zero.
    '''
    def __init__(self, 
                 grippers_angle: int = 0, 
                 grippers_effort: int = 0, 
                 status_code: Literal[0x00, 0x01, 0x02, 0x03] = 0,
                 set_zero: Literal[0x00, 0xAE] = 0):
        if status_code not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"'status_code' Value {status_code} out of range [0x00, 0x01, 0x02, 0x03]")
        if not (0 <= grippers_effort <= 5000):
            raise ValueError(f"'grippers_effort' Value {grippers_effort} out of range 0-5000")
        if set_zero not in [0x00, 0xAE]:
            raise ValueError(f"'set_zero' Value {set_zero} out of range [0x00,0xAE]")
        self.grippers_angle = grippers_angle
        self.grippers_effort = grippers_effort
        self.status_code = status_code
        self.set_zero = set_zero

    def __str__(self):
        return (f"ArmMsgGripperCtrl(\n"
                f"  grippers_angle: {self.grippers_angle}, {self.grippers_angle * 0.001:.3f},\n"
                f"  grippers_effort: {self.grippers_effort} \t {self.grippers_effort * 0.001:.3f},\n"
                f"  status_code: {self.status_code},\n"
                f"  set_zero: {self.set_zero}\n"
                f")")

    def __repr__(self):
        return self.__str__()
