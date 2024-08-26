#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgCrashProtectionRatingConfig:
    '''
    末端速度/加速度参数设置指令
    
    0x47A

    有效值 : 0~8

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
                 jonit_1_protection_level:int=0xFF, 
                 jonit_2_protection_level:int=0xFF, 
                 jonit_3_protection_level: int=0xFF,
                 jonit_4_protection_level: int=0xFF,
                 jonit_5_protection_level: int=0xFF,
                 jonit_6_protection_level: int=0xFF
                 ):
        """
        初始化 ArmMsgCrashProtectionRatingConfig 实例。
        """
        self.jonit_1_protection_level = jonit_1_protection_level
        self.jonit_2_protection_level = jonit_2_protection_level
        self.jonit_3_protection_level = jonit_3_protection_level
        self.jonit_4_protection_level = jonit_4_protection_level
        self.jonit_5_protection_level = jonit_5_protection_level
        self.jonit_6_protection_level = jonit_6_protection_level

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmMsgCrashProtectionRatingConfig(\n"
                f"  jonit_1_protection_level: {self.jonit_1_protection_level},\n"
                f"  jonit_2_protection_level: {self.jonit_2_protection_level},\n"
                f"  jonit_3_protection_level: {self.jonit_3_protection_level},\n"
                f"  jonit_4_protection_level: {self.jonit_4_protection_level},\n"
                f"  jonit_5_protection_level: {self.jonit_5_protection_level},\n"
                f"  jonit_6_protection_level: {self.jonit_6_protection_level}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
