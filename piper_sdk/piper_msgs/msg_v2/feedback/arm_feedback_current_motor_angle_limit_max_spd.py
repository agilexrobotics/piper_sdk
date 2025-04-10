#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd:
    '''
    msg_v2_feedback
    
    反馈当前电机限制角度/最大速度
    
    CAN ID:
        0x473
    
    Args:
        motor_num: 关节电机序号
        max_angle_limit: 最大角度限制
        min_angle_limit: 最小角度限制
        max_joint_spd: 最大关节速度

    位描述:

        Byte 0: 关节电机序号, uint8
        Byte 1: 最大角度限制H,uint16, 单位 0.1度
        Byte 2: 最大角度限制L
        Byte 3: 最小角度限制H, uint16, 单位 0.1度
        Byte 4: 最小角度限制L
        Byte 5: 最大关节速度H, uint16, 单位 0.001rad/s
        Byte 6: 最大关节速度L
        Byte 7: 保留
    '''
    '''
    msg_v2_feedback
    
    Feedback on Current Motor Angle Limits/Maximum Speed

    CAN ID:
        0x473

    Args:
        motor_num: Joint motor number.
        max_angle_limit: Maximum angle limit.
        min_angle_limit: Minimum angle limit.
        max_joint_spd: Maximum joint speed.
    
    Bit Description:

        Byte 0: Joint Motor Index, uint8
        Byte 1: Maximum Angle Limit (High Byte), uint16, unit: 0.1°
        Byte 2: Maximum Angle Limit (Low Byte)
        Byte 3: Minimum Angle Limit (High Byte), uint16, unit: 0.1°
        Byte 4: Minimum Angle Limit (Low Byte)
        Byte 5: Maximum Joint Speed (High Byte), uint16, unit: 0.001 rad/s
        Byte 6: Maximum Joint Speed (Low Byte)
        Byte 7: Reserved
    '''
    def __init__(self, 
                 motor_num: Literal[0, 1, 2, 3, 4, 5, 6] = 0, 
                 max_angle_limit: int = 0, 
                 min_angle_limit: int = 0,
                 max_joint_spd: int = 0):
        if motor_num not in [0, 1, 2, 3, 4, 5, 6]:
            raise ValueError(f"'motor_num' Value {motor_num} out of range [1, 2, 3, 4, 5, 6]")
        self.motor_num = motor_num
        self.max_angle_limit = max_angle_limit
        self.min_angle_limit = min_angle_limit
        self.max_joint_spd = max_joint_spd

    def __str__(self):
        return (f"ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(\n"
                f"  motor_num: {self.motor_num}\n"
                f"  max_angle_limit: {self.max_angle_limit}\n"
                f"  min_angle_limit: {self.min_angle_limit}\n"
                f"  max_joint_spd: {self.max_joint_spd}\n"
                f")")

    def __repr__(self):
        return self.__str__()

class ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd:
    '''
    反馈所有电机限制角度/最大速度
    
    CAN ID:
        0x473
    
    :param m1: 电机1的限制角度/最大速度
    :param m2: 电机2的限制角度/最大速度
    :param m3: 电机3的限制角度/最大速度
    :param m4: 电机4的限制角度/最大速度
    :param m5: 电机5的限制角度/最大速度
    :param m6: 电机6的限制角度/最大速度
    '''
    '''
    Feedback on Current Motor Angle Limits/Maximum Speed

    CAN ID:
        0x473

    :param m1: Limit angle/maximum speed for motor 1.
    :param m2: Limit angle/maximum speed for motor 2.
    :param m3: Limit angle/maximum speed for motor 3.
    :param m4: Limit angle/maximum speed for motor 4.
    :param m5: Limit angle/maximum speed for motor 5.
    :param m6: Limit angle/maximum speed for motor 6.
    '''
    def __init__(self, 
                 m1:ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd = ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(0,0,0,0),
                 m2:ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd = ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(0,0,0,0),
                 m3:ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd = ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(0,0,0,0),
                 m4:ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd = ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(0,0,0,0),
                 m5:ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd = ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(0,0,0,0),
                 m6:ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd = ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(0,0,0,0)):
        self.__m = [ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(0,0,0,0), m1, m2, m3, m4, m5, m6]
        self.motor = [ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd() for _ in range(7)]
        self.motor[0] = ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd(0,0,0,0)
    
    def assign(self):
        for i in range(1,7):
            if(self.__m[i].motor_num != 0):
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