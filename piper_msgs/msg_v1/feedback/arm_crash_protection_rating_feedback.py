#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgCrashProtectionRatingFeedback:
    '''
    末端速度/加速度参数反馈指令
    
    0x47B

    当前设定值 : 0~8

    等级 0 代表不检测碰撞； 6个关节可以独立设置

    :Byte 0: 1 号关节碰撞防护等级, uint8
    :Byte 1: 2 号关节碰撞防护等级, uint8
    :Byte 2: 3 号关节碰撞防护等级, uint8
    :Byte 3: 4 号关节碰撞防护等级, uint8
    :Byte 4: 5 号关节碰撞防护等级, uint8
    :Byte 5: 6 号关节碰撞防护等级, uint8
    :Byte 6: 保留
    :Byte 7: 保留
    '''
    def __init__(self, 
                 joint_1_protection_level:int=0, 
                 joint_2_protection_level:int=0, 
                 joint_3_protection_level: int=0,
                 joint_4_protection_level: int=0,
                 joint_5_protection_level: int=0,
                 joint_6_protection_level: int=0
                 ):
        """
        初始化 ArmMsgCrashProtectionRatingFeedback 实例。
        """
        self.joint_1_protection_level = joint_1_protection_level
        self.joint_2_protection_level = joint_2_protection_level
        self.joint_3_protection_level = joint_3_protection_level
        self.joint_4_protection_level = joint_4_protection_level
        self.joint_5_protection_level = joint_5_protection_level
        self.joint_6_protection_level = joint_6_protection_level

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmMsgCrashProtectionRatingFeedback(\n"
                f"  joint_1_protection_level: {self.joint_1_protection_level},\n"
                f"  joint_2_protection_level: {self.joint_2_protection_level},\n"
                f"  joint_3_protection_level: {self.joint_3_protection_level},\n"
                f"  joint_4_protection_level: {self.joint_4_protection_level},\n"
                f"  joint_5_protection_level: {self.joint_5_protection_level},\n"
                f"  joint_6_protection_level: {self.joint_6_protection_level}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
