#!/usr/bin/env python3
# -*-coding:utf8-*-
import math
class ArmMsgFeedbackCurrentEndVelAccParam:
    '''
    msg_v2_feedback
    
    反馈当前末端速度/加速度参数
    
    0x477 Byte 0 = 0x01 feedback

    CAN ID:
        0x478

    Args:
        end_max_linear_vel: 末端最大线速度
        end_max_angular_vel: 末端最大角速度
        end_max_linear_acc: 末端最大线加速度
        end_max_angular_acc: 末端最大角加速度
    
    位描述:

        Byte 0: 末端最大线速度 H, uint16, 单位 0.001m/s
        Byte 1: 末端最大线速度 L,
        Byte 2: 末端最大角速度 H, uint16, 单位 0.001rad/s
        Byte 3: 末端最大角速度 L,
        Byte 4: 末端最大线加速度 H, uint16, 单位 0.001m/s^2
        Byte 5: 末端最大线加速度 L
        Byte 6: 末端最大角加速度 H, uint16, 单位 0.001rad/s^2
        Byte 7: 末端最大角加速度 L
    '''
    '''
    msg_v2_feedback
    
    Feedback of Current End-Effector Speed/Acceleration Parameters

    0x477 Byte 0 = 0x01 feedback
    
    CAN ID: 
        0x478

    Args:
        end_max_linear_vel: Maximum linear velocity of the end-effector.
        end_max_angular_vel: Maximum angular velocity of the end-effector.
        end_max_linear_acc: Maximum linear acceleration of the end-effector.
        end_max_angular_acc: Maximum angular acceleration of the end-effector.
    
    Bit Description:

        Byte 0: Maximum Linear Velocity (High Byte), uint16, unit: 0.001 m/s
        Byte 1: Maximum Linear Velocity (Low Byte)
        Byte 2: Maximum Angular Velocity (High Byte), uint16, unit: 0.001 rad/s
        Byte 3: Maximum Angular Velocity (Low Byte)
        Byte 4: Maximum Linear Acceleration (High Byte), uint16, unit: 0.001 m/s²
        Byte 5: Maximum Linear Acceleration (Low Byte)
        Byte 6: Maximum Angular Acceleration (High Byte), uint16, unit: 0.001 rad/s²
        Byte 7: Maximum Angular Acceleration (Low Byte)
    '''
    def __init__(self, 
                 end_max_linear_vel: int = 0, 
                 end_max_angular_vel: int = 0, 
                 end_max_linear_acc: int = 0,
                 end_max_angular_acc: int = 0
                 ):
        self.end_max_linear_vel = end_max_linear_vel
        self.end_max_angular_vel = end_max_angular_vel
        self.end_max_linear_acc = end_max_linear_acc
        self.end_max_angular_acc = end_max_angular_acc

    def __str__(self):
        return (f"ArmMsgFeedbackCurrentEndVelAccParam(\n"
                f"  end_max_linear_vel: {self.end_max_linear_vel}\n"
                f"  end_max_angular_vel: {self.end_max_angular_vel}\n"
                f"  end_max_linear_acc: {self.end_max_linear_acc }\n"
                f"  end_max_angular_acc: {self.end_max_angular_acc}\n"
                f")")

    def __repr__(self):
        return self.__str__()
