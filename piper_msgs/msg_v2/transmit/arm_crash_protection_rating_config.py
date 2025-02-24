#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgCrashProtectionRatingConfig:
    '''
    msg_v2_transmit
    
    碰撞防护等级设置指令
    
    CAN ID:
        0x47A

    有效值 : 0~8

    等级 0 代表不检测碰撞； 6个关节可以独立设置

    Args:
        joint_1_protection_level: 关节1的碰撞等级设定
        joint_2_protection_level: 关节2的碰撞等级设定
        joint_3_protection_level: 关节3的碰撞等级设定
        joint_4_protection_level: 关节4的碰撞等级设定
        joint_5_protection_level: 关节5的碰撞等级设定
        joint_6_protection_level: 关节6的碰撞等级设定
    
    位描述:
    
        Byte 0: 1 号关节碰撞防护等级, uint8
        Byte 1: 2 号关节碰撞防护等级, uint8
        Byte 2: 3 号关节碰撞防护等级, uint8
        Byte 3: 4 号关节碰撞防护等级, uint8
        Byte 4: 5 号关节碰撞防护等级, uint8
        Byte 5: 6 号关节碰撞防护等级, uint8
        Byte 6: 保留
        Byte 7: 保留
    '''
    '''
    msg_v2_transmit
    
    End Effector Speed/Acceleration Parameter Setting Command

    CAN ID:
        0x47A

    Valid Values: 0~8
        Level 0 indicates no collision detection.
        Collision protection levels can be set independently for the six joints.

    Args:
        joint_1_protection_level: Collision protection level for Joint 1.
        joint_2_protection_level: Collision protection level for Joint 2.
        joint_3_protection_level: Collision protection level for Joint 3.
        joint_4_protection_level: Collision protection level for Joint 4.
        joint_5_protection_level: Collision protection level for Joint 5.
        joint_6_protection_level: Collision protection level for Joint 6.

    Bit Description:

        Byte 0: Collision protection level for Joint 1, uint8.
        Byte 1: Collision protection level for Joint 2, uint8.
        Byte 2: Collision protection level for Joint 3, uint8.
        Byte 3: Collision protection level for Joint 4, uint8.
        Byte 4: Collision protection level for Joint 5, uint8.
        Byte 5: Collision protection level for Joint 6, uint8.
        Byte 6: Reserved.
        Byte 7: Reserved.
    '''
    def __init__(self, 
                 joint_1_protection_level: int = 0xFF, 
                 joint_2_protection_level: int = 0xFF, 
                 joint_3_protection_level: int = 0xFF,
                 joint_4_protection_level: int = 0xFF,
                 joint_5_protection_level: int = 0xFF,
                 joint_6_protection_level: int = 0xFF
                 ):
        self.joint_1_protection_level = joint_1_protection_level
        self.joint_2_protection_level = joint_2_protection_level
        self.joint_3_protection_level = joint_3_protection_level
        self.joint_4_protection_level = joint_4_protection_level
        self.joint_5_protection_level = joint_5_protection_level
        self.joint_6_protection_level = joint_6_protection_level

    def __str__(self):
        return (f"ArmMsgCrashProtectionRatingConfig(\n"
                f"  joint_1_protection_level: {self.joint_1_protection_level},\n"
                f"  joint_2_protection_level: {self.joint_2_protection_level},\n"
                f"  joint_3_protection_level: {self.joint_3_protection_level},\n"
                f"  joint_4_protection_level: {self.joint_4_protection_level},\n"
                f"  joint_5_protection_level: {self.joint_5_protection_level},\n"
                f"  joint_6_protection_level: {self.joint_6_protection_level}\n"
                f")")

    def __repr__(self):
        return self.__str__()
