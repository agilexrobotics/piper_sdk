#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgFeedbackCurrentMotorMaxAccLimit:
    '''
    msg_v2_feedback
    
    反馈当前电机最大加速度限制

    CAN ID:
        0x47C

    Args:
        joint_motor_num: 关节电机序号
        max_joint_acc: 最大关节加速度
    
    位描述:

        Byte 0: 关节序号, uint8, 值域 1-6(1-6 代表关节驱动器序号)
        Byte 1: 最大关节加速度 H, uint16, 单位 0.001rad/^2
        Byte 2: 最大关节加速度 L
    '''
    '''
    msg_v2_feedback
    
    Feedback on Current Motor Maximum Acceleration Limit

    CAN ID: 
        0x47C

    Args:
        joint_motor_num: Joint motor number.
        max_joint_acc: Maximum joint acceleration.
    
    Bit Description:

        Byte 0: Joint Index, uint8, range 1-6(1-6 represent the joint motor index)
        Byte 1: Maximum Joint Acceleration (High Byte), uint16, unit: 0.001rad/^2
        Byte 2: Maximum Joint Acceleration (Low Byte)
    '''
    def __init__(self, 
                 joint_motor_num: Literal[0, 1, 2, 3, 4, 5, 6] = 0, 
                 max_joint_acc: int = 0
                 ):
        if joint_motor_num not in [0, 1, 2, 3, 4, 5, 6]:
            raise ValueError(f"'joint_motor_num' Value {joint_motor_num} out of range [1, 2, 3, 4, 5, 6]")
        self.joint_motor_num = joint_motor_num
        self.max_joint_acc = max_joint_acc

    def __str__(self):
        return (f"ArmMsgFeedbackCurrentMotorMaxAccLimit(\n"
                f"  joint_motor_num: {self.joint_motor_num}\n"
                f"  max_joint_acc: {self.max_joint_acc}\n"
                f")")

    def __repr__(self):
        return self.__str__()

class ArmMsgFeedbackAllCurrentMotorMaxAccLimit:
    '''
    反馈全部电机最大加速度限制

    CAN ID:
        0x47C

    :param m1: 电机1的最大加速度限制
    :param m2: 电机2的最大加速度限制
    :param m3: 电机3的最大加速度限制
    :param m4: 电机4的最大加速度限制
    :param m5: 电机5的最大加速度限制
    :param m6: 电机6的最大加速度限制
    '''
    '''
    Feedback on Current Motor Maximum Acceleration Limit

    CAN ID: 
        0x47C

    :param m1: Maximum acceleration limit for motor 1.
    :param m2: Maximum acceleration limit for motor 2.
    :param m3: Maximum acceleration limit for motor 3.
    :param m4: Maximum acceleration limit for motor 4.
    :param m5: Maximum acceleration limit for motor 5.
    :param m6: Maximum acceleration limit for motor 6.
    '''
    def __init__(self, 
                 m1:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), 
                 m2:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0),
                 m3:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), 
                 m4:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), 
                 m5:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), 
                 m6:ArmMsgFeedbackCurrentMotorMaxAccLimit=ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0)
                 ):
        self.__m = [ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0), m1, m2, m3, m4, m5, m6]
        self.motor = [ArmMsgFeedbackCurrentMotorMaxAccLimit(0,0) for _ in range(7)]

    def assign(self):
        for i in range(1,7):
            if(self.__m[i].joint_motor_num != 0):
                self.motor[i] = self.__m[i]
    
    def __str__(self):
        return (f"{self.motor[1]}\n"
                f"{self.motor[2]}\n"
                f"{self.motor[3]}\n"
                f"{self.motor[4]}\n"
                f"{self.motor[5]}\n"
                f"{self.motor[6]}\n"
                f")")

    def __repr__(self):
        return self.__str__()