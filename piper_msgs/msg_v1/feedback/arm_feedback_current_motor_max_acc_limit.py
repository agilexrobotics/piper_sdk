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
                 joint_motor_num:Literal[0, 1, 2, 3, 4, 5, 6]=0, 
                 max_joint_acc:int=0
                 ):
        """
        初始化 ArmMsgFeedbackCurrentMotorMaxAccLimit 实例。
        """
        if joint_motor_num not in [0, 1, 2, 3, 4, 5, 6]:
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

class ArmMsgFeedbackAllCurrentMotorMaxAccLimit:
    '''
    反馈当前电机最大加速度限制

    0x47C

    :Byte 0: 关节序号, uint8, 值域 1-6:
                             1-6 代表关节驱动器序号；
    :Byte 1: 最大关节加速度 H, uint16, 单位 RPM/s
    :Byte 2: 最大关节加速度 L
    '''
    def __init__(self, 
                 m1:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), 
                 m2:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0),
                 m3:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), 
                 m4:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), 
                 m5:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), 
                 m6:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0)
                 ):
        """
        初始化 ArmMsgFeedbackAllCurrentMotorMaxAccLimit 实例。
        """
        self.__m = [ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), m1, m2, m3, m4, m5, m6]
        self.motor = [ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0) for _ in range(7)]

    def assign(self):
        for i in range(1,7):
            if(self.__m[i].joint_motor_num != 0):
                self.motor[i] = self.__m[i]
    
    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"{self.motor[1]}\n"
                f"{self.motor[2]}\n"
                f"{self.motor[3]}\n"
                f"{self.motor[4]}\n"
                f"{self.motor[5]}\n"
                f"{self.motor[6]}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()