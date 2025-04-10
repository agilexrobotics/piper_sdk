#!/usr/bin/env python3
# -*-coding:utf8-*-
import math
from typing_extensions import (
    Literal,
)
class ArmMsgFeedbackJointVelAcc:
    '''
    msg_v2_feedback
    
    反馈各个关节当前末端速度/加速度

    CAN ID:
        0x481 ~ 0x486
        代表 1~6 号关节

    Args:
        can_id: 当前canid,用来代表关节序号
        end_linear_vel: 末端线速度
        end_angular_vel: 末端角速度
        end_linear_acc: 末端线加速度
        end_angular_acc: 末端角加速度
    
    位描述:

        Byte 0: 末端线速度 H, uint16, 单位 0.001m/s
        Byte 1: 末端线速度 L,
        Byte 2: 末端角速度 H, uint16, 单位 0.001rad/s
        Byte 3: 末端角速度 L,
        Byte 4: 末端线加速度 H, uint16, 单位 0.001m/s^2
        Byte 5: 末端线加速度 L
        Byte 6: 末端角加速度 H, uint16, 单位 0.001rad/s^2
        Byte 7: 末端角加速度 L
    '''
    '''
    msg_v2_feedback
    
    Feedback on Current End-Effector Speed/Acceleration for Each Joint

    CAN ID:
        0x481 ~ 0x486
        Corresponds to Joints 1~6.

    Args:
        can_id: Current CAN ID, used to represent the joint number.
        end_linear_vel: End-effector linear velocity.
        end_angular_vel: End-effector angular velocity.
        end_linear_acc: End-effector linear acceleration.
        end_angular_acc: End-effector angular acceleration.
    
    Bit Description:

        Byte 0: End-Effector Linear Velocity (High Byte), uint16, unit: 0.001 m/s
        Byte 1: End-Effector Linear Velocity (Low Byte)
        Byte 2: End-Effector Angular Velocity (High Byte), uint16, unit: 0.001 rad/s
        Byte 3: End-Effector Angular Velocity (Low Byte)
        Byte 4: End-Effector Linear Acceleration (High Byte), uint16, unit: 0.001 m/s²
        Byte 5: End-Effector Linear Acceleration (Low Byte)
        Byte 6: End-Effector Angular Acceleration (High Byte), uint16, unit: 0.001 rad/s²
        Byte 7: End-Effector Angular Acceleration (Low Byte)
    '''
    def __init__(self, 
                 can_id: Literal[0, 0x481, 0x482, 0x483, 0x484, 0x485, 0x486] = 0,
                 end_linear_vel: int = 0, 
                 end_angular_vel: int = 0, 
                 end_linear_acc: int = 0,
                 end_angular_acc: int = 0
                 ):
        if can_id not in [0, 0x481, 0x482, 0x483, 0x484, 0x485, 0x486]:
            raise ValueError(f"'can_id' Value {can_id} out of range [0x481, 0x482, 0x483, 0x484, 0x485, 0x486]")
        self.can_id = can_id
        self.end_linear_vel = end_linear_vel
        self.end_angular_vel = end_angular_vel
        self.end_linear_acc = end_linear_acc
        self.end_angular_acc = end_angular_acc

    def __str__(self):
        return (f"ArmMsgFeedbackJointVelAcc(\n"
                f"  can_id: {self.can_id}\n"
                f"  end_linear_vel: {self.end_linear_vel}\n"
                f"  end_angular_vel: {self.end_angular_vel }\n"
                f"  end_linear_acc: {self.end_linear_acc }\n"
                f"  end_angular_acc: {self.end_angular_acc}\n"
                f")")

    def __repr__(self):
        return self.__str__()

class ArmMsgFeedbackAllJointVelAcc:
    '''
    反馈全部关节当前末端速度/加速度

    CAN ID:
        0x481 ~ 0x486
        代表 1~6 号关节

    Args:
        j1: 电机1的当前末端速度/加速度
        j2: 电机2的当前末端速度/加速度
        j3: 电机3的当前末端速度/加速度
        j4: 电机4的当前末端速度/加速度
        j5: 电机5的当前末端速度/加速度
        j6: 电机6的当前末端速度/加速度
    '''
    '''
    Feedback on Current End-Effector Speed/Acceleration for Each Joint

    CAN ID:
        0x481 ~ 0x486
        Corresponds to Joints 1~6.

    Args:
        j1: Current end-effector velocity/acceleration for motor 1.
        j2: Current end-effector velocity/acceleration for motor 2.
        j3: Current end-effector velocity/acceleration for motor 3.
        j4: Current end-effector velocity/acceleration for motor 4.
        j5: Current end-effector velocity/acceleration for motor 5.
        j6: Current end-effector velocity/acceleration for motor 6.
    '''
    def __init__(self, 
                 j1:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j2:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j3:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j4:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j5:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j6:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0)):
        self.j = [ArmMsgFeedbackJointVelAcc(0,0,0,0,0), j1, j2, j3, j4, j5, j6]
        self.joint = [ArmMsgFeedbackJointVelAcc() for _ in range(7)]
        self.joint[0] = ArmMsgFeedbackJointVelAcc(0,0,0,0,0)
    
    def assign(self):
        for i in range(1,7):
            if(self.j[i].can_id != 0):
                self.joint[i] = self.j[i]
    
    def __str__(self):
        return (f"{self.joint[1]}\n"
                f"{self.joint[2]}\n"
                f"{self.joint[3]}\n"
                f"{self.joint[4]}\n"
                f"{self.joint[5]}\n"
                f"{self.joint[6]}\n"
                f")")

    def __repr__(self):
        return self.__str__()