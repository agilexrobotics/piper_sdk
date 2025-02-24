#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgJointConfig:
    '''
    msg_v2_transmit
    
    关节设置指令

    CAN ID:
        0x475

    Args:
        joint_motor_num: 关节电机序号,[1, 7]
        set_motor_current_pos_as_zero: 设置当前位置为零点, 有效值-0xAE
        acc_param_config_is_effective_or_not: 加速度参数设置是否生效, 有效值-0xAE
        max_joint_acc: 最大关节加速度,单位0.01rad/s^2(0x7FFF为设定无效数值),输入范围\[0, 500\]-->[0 rad/s^2, 5.0 rad/s^2]
        clear_joint_err: 清除关节错误代码, 有效值-0xAE
    
    位描述:
    
        Byte 0: 关节电机序号 uint8, 值域 1-7
                1-6 代表关节驱动器序号；
                7 代表全部关节电机
        Byte 1: 设置N号电机当前位置为零点: uint8, 有效值-0xAE
        Byte 2: 加速度参数设置是否生效: uint8, 有效值-0xAE
        Byte 3: 最大关节加速度 H: uint16, 单位 0.01rad/s^2.(基于V1.5-2版本后增加无效数值0x7FFF)
        Byte 4: 最大关节加速度 L
        Byte 5: 清除关节错误代码: uint8, 有效值-0xAE
        Byte 6: 保留
        Byte 7: 保留
    '''
    '''
    msg_v2_transmit
    
    Joint Configuration Command

    CAN ID:
    0x475
    
    Args:
        joint_motor_num: Joint motor number.
            Value range: 1-6 represents individual joint motor numbers.
            Value 7 applies to all joint motors.
        set_motor_current_pos_as_zero: Command to set the current position of the specified joint motor as zero, with a valid value of 0xAE.
        acc_param_config_is_effective_or_not: Indicates whether the acceleration parameter configuration is effective, with a valid value of 0xAE.
        max_joint_acc: Maximum joint acceleration, unit: 0.01rad/s^2, 0x7FFF is defined as the invalid value.Range is \[0, 500\]-->[0 rad/s^2, 5.0 rad/s^2]
        clear_joint_err: Command to clear joint error codes, with a valid value of 0xAE.

    Bit Description:

        Byte 0: Joint motor number (uint8).
                - 1-6: Corresponds to individual joint motor numbers.
                - 7: Represents all joint motors.
        Byte 1: Set the current position of the specified joint motor as zero (uint8).
                - Valid value: 0xAE.
        Byte 2: Determines if the acceleration parameter configuration is effective (uint8).
                - Valid value: 0xAE.
        Byte 3-4: Maximum joint acceleration (uint16).(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
                - Unit: 0.01rad/s^2.
                - Byte 3: High byte, Byte 4: Low byte.
        Byte 5: Clear joint error code (uint8).
                - Valid value: 0xAE.
        Byte 6: Reserved
        Byte 7: Reserved
    '''
    def __init__(self, 
                 joint_motor_num: Literal[1, 2, 3, 4, 5, 6, 7] = 7, 
                 set_motor_current_pos_as_zero: Literal[0x00, 0xAE] = 0, 
                 acc_param_config_is_effective_or_not: Literal[0x00, 0xAE] = 0,
                 max_joint_acc: int = 500,
                 clear_joint_err: Literal[0x00, 0xAE] = 0):
        if joint_motor_num not in [1, 2, 3, 4, 5, 6, 7]:
            raise ValueError(f"'joint_motor_num Value' {joint_motor_num} out of range [1, 2, 3, 4, 5, 6, 7]")
        if set_motor_current_pos_as_zero not in [0x00, 0xAE]:
            raise ValueError(f"'set_motor_current_pos_as_zero' Value {set_motor_current_pos_as_zero} out of range [0x00, 0xAE]")
        if acc_param_config_is_effective_or_not not in [0x00, 0xAE]:
            raise ValueError(f"'acc_param_config_is_effective_or_not' Value {acc_param_config_is_effective_or_not} out of range [0x00, 0xAE]")
        if not (0 <= max_joint_acc <= 500 or max_joint_acc == 0x7FFF):
            raise ValueError(f"'max_joint_acc' Value {max_joint_acc} out of range 0-500 or not equal to 0x7FFF")
        if clear_joint_err not in [0x00, 0xAE]:
            raise ValueError(f"clear_joint_err' Value {clear_joint_err} out of range [0x00, 0xAE]")
        self.joint_motor_num = joint_motor_num
        self.set_motor_current_pos_as_zero = set_motor_current_pos_as_zero
        self.acc_param_config_is_effective_or_not = acc_param_config_is_effective_or_not
        self.max_joint_acc = max_joint_acc
        self.clear_joint_err = clear_joint_err

    def __str__(self):
        return (f"ArmMsgJointConfig(\n"
                f"  joint_motor_num: {self.joint_motor_num},\n"
                f"  set_motor_current_pos_as_zero: {self.set_motor_current_pos_as_zero},\n"
                f"  acc_param_config_is_effective_or_not: {self.acc_param_config_is_effective_or_not},\n"
                f"  max_joint_acc: {self.max_joint_acc}, {self.max_joint_acc*0.01:.2f}\n"
                f"  clear_joint_err: {self.clear_joint_err}\n"
                f")")

    def __repr__(self):
        return self.__str__()
