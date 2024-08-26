#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgFeedbackCurrentMotorMaxAccLimit:
    '''
    反馈当前电机最大加速度限制

    0x47C

    :Byte 0: 关节序号, uint8, 值域 1-6:
                             1-6 代表关节驱动器序号；
    :Byte 1: 最大关节加速度 H, uint16, 单位 RPM/s
    :Byte 2: 最大关节加速度 L
    '''
    def __init__(self, 
                 joint_motor_num:Literal[1, 2, 3, 4, 5, 6]=1, 
                 max_joint_acc:int=0
                 ):
        """
        初始化 ArmMsgFeedbackCurrentMotorMaxAccLimit 实例。
        """
        if joint_motor_num not in [1, 2, 3, 4, 5, 6]:
            raise ValueError(f"joint_motor_num 值 {joint_motor_num} 超出范围 [1, 2, 3, 4, 5, 6]")
        self.joint_motor_num = joint_motor_num
        self.max_joint_acc = max_joint_acc

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmMsgFeedbackCurrentMotorMaxAccLimit(\n"
                f"  joint_motor_num: {self.joint_motor_num},\n"
                f"  max_joint_acc: {self.max_joint_acc}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
