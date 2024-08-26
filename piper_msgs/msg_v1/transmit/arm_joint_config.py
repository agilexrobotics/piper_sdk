#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgJointConfig:
    '''
    关节设置指令

    0x475

    :Byte 0 关节电机序号 uint8, 值域 1-7:   
                              1-6 代表关节驱动器序号；
                              7 代表全部关节电机
    :Byte 1 设置N号电机当前位置为零点: uint8, 有效值 : 0xAE
    :Byte 2 加速度参数设置是否生效: uint8, 有效值 : 0xAE
    :Byte 3 最大关节加速度 H: uint16, 单位 0.001rad/s
    :Byte 4 最大关节加速度 L
    :Byte 5 清除关节错误代码: uint8, 有效值 : 0xAE
    '''
    def __init__(self, 
                 joint_motor_num:Literal[1, 2, 3, 4, 5, 6, 7]=7, 
                 set_motor_current_pos_as_zero: Literal[0x00, 0xAE]=0, 
                 acc_param_config_is_effective_or_not: Literal[0x00, 0xAE]=0,
                 max_joint_acc: int=0,
                 clear_joint_err: Literal[0x00, 0xAE]=0):
        """
        初始化 ArmMsgMotorAngleSpdLimitConfig 实例。

        关节设置指令

        0x475

        :Byte 0 关节电机序号 uint8, 值域 1-7:   
                                1-6 代表关节驱动器序号；
                                7 代表全部关节电机
        :Byte 1 设置N号电机当前位置为零点: uint8, 有效值 : 0xAE
        :Byte 2 加速度参数设置是否生效: uint8, 有效值 : 0xAE
        :Byte 3 最大关节加速度 H: uint16, 单位 0.001rad/s
        :Byte 4 最大关节加速度 L
    :Byte 5 清除关节错误代码: uint8, 有效值 : 0xAE
        
        """
        if joint_motor_num not in [1, 2, 3, 4, 5, 6, 7]:
            raise ValueError(f"joint_motor_num 值 {joint_motor_num} 超出范围 [1, 2, 3, 4, 5, 6, 7]")
        if set_motor_current_pos_as_zero not in [0x00, 0xAE]:
            raise ValueError(f"set_motor_current_pos_as_zero 值 {set_motor_current_pos_as_zero} 超出范围 [0x00, 0xAE]")
        if acc_param_config_is_effective_or_not not in [0x00, 0xAE]:
            raise ValueError(f"acc_param_config_is_effective_or_not 值 {acc_param_config_is_effective_or_not} 超出范围 [0x00, 0xAE]")
        if not (0 <= max_joint_acc <= 65535):
            raise ValueError(f"max_joint_acc 值 {max_joint_acc} 超出范围 [0, 65535]")
        if clear_joint_err not in [0x00, 0xAE]:
            raise ValueError(f"clear_joint_err 值 {clear_joint_err} 超出范围 [0x00, 0xAE]")
        self.joint_motor_num = joint_motor_num
        self.set_motor_current_pos_as_zero = set_motor_current_pos_as_zero
        self.acc_param_config_is_effective_or_not = acc_param_config_is_effective_or_not
        self.max_joint_acc = max_joint_acc
        self.clear_joint_err = clear_joint_err

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmMsgJointConfig(\n"
                f"  joint_motor_num: {self.joint_motor_num},\n"
                f"  set_motor_current_pos_as_zero: {self.set_motor_current_pos_as_zero},\n"
                f"  acc_param_config_is_effective_or_not: {self.acc_param_config_is_effective_or_not},\n"
                f"  max_joint_acc: {self.max_joint_acc}, {self.max_joint_acc*0.001:.3f}\n"
                f"  clear_joint_err: {self.clear_joint_err}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
