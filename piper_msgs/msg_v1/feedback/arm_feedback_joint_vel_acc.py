#!/usr/bin/env python3
# -*-coding:utf8-*-
import math
from typing_extensions import (
    Literal,
)
class ArmMsgFeedbackJointVelAcc:
    '''
    反馈各个关节当前末端速度/加速度

    0x481 ~ 0x486 代表 1~6 号关节

    :Byte 0: 末端线速度 H, uint16, 单位 0.001m/s
    :Byte 1: 末端线速度 L,
    :Byte 2: 末端角速度 H, uint16, 单位 0.001rad/s
    :Byte 3: 末端角速度 L,
    :Byte 4: 末端线加速度 H, uint16, 单位 0.001m/s^2
    :Byte 5: 末端线加速度 L
    :Byte 6: 末端角加速度 H, uint16, 单位 0.001rad/s^2
    :Byte 7: 末端角加速度 L
    '''
    def __init__(self, 
                 can_id:Literal[0,0x481,0x482,0x483,0x484,0x485,0x486]=0,
                 end_linear_vel:int=0, 
                 end_angular_vel:int=0, 
                 end_linear_acc: int=0,
                 end_angular_acc: int=0
                 ):
        """
        初始化 ArmMsgFeedbackJointVelAcc 实例。
        """
        if can_id not in [0,0x481,0x482,0x483,0x484,0x485,0x486]:
            raise ValueError(f"can_id 值 {can_id} 不在范围 [0x481,0x482,0x483,0x484,0x485,0x486]")
        self.can_id = can_id
        self.end_linear_vel = end_linear_vel
        self.end_angular_vel = end_angular_vel
        self.end_linear_acc = end_linear_acc
        self.end_angular_acc = end_angular_acc

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmMsgFeedbackJointVelAcc(\n"
                f"  can_id: {self.can_id},\n"
                f"  end_linear_vel: {self.end_linear_vel},\n"
                f"  end_angular_vel: {self.end_angular_vel },\n"
                f"  end_linear_acc: {self.end_linear_acc },\n"
                f"  end_angular_acc: {self.end_angular_acc}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()

class ArmMsgFeedbackAllJointVelAcc:
    '''
    反馈各个关节当前末端速度/加速度,为全部关节的消息

    0x481 ~ 0x486 代表 1~6 号关节

    :Byte 0: 末端线速度 H, uint16, 单位 0.001m/s
    :Byte 1: 末端线速度 L
    :Byte 2: 末端角速度 H, uint16, 单位 0.001rad/s
    :Byte 3: 末端角速度 L
    :Byte 4: 末端线加速度 H, uint16, 单位 0.001m/s^2
    :Byte 5: 末端线加速度 L
    :Byte 6: 末端角加速度 H, uint16, 单位 0.001rad/s^2
    :Byte 7: 末端角加速度 L
    '''
    def __init__(self, 
                 j1:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j2:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j3:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j4:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j5:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0),
                 j6:ArmMsgFeedbackJointVelAcc = ArmMsgFeedbackJointVelAcc(0,0,0,0,0)):
        """
        初始化 ArmMsgFeedbackAllJointVelAcc 实例。
        """
        self.j = [ArmMsgFeedbackJointVelAcc(0,0,0,0,0), j1, j2, j3, j4, j5, j6]
        self.joint = [ArmMsgFeedbackJointVelAcc() for _ in range(7)]
        self.joint[0] = ArmMsgFeedbackJointVelAcc(0,0,0,0,0)
    
    def assign(self):
        for i in range(1,7):
            if(self.j[i].can_id != 0):
                self.joint[i] = self.j[i]
    
    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"{self.joint[1]}\n"
                f"{self.joint[2]}\n"
                f"{self.joint[3]}\n"
                f"{self.joint[4]}\n"
                f"{self.joint[5]}\n"
                f"{self.joint[6]}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()