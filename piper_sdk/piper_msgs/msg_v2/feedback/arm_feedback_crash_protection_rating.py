#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgFeedbackCrashProtectionRating:
    '''
    msg_v2_feedback
    
    碰撞防护等级反馈指令
    
    0x477 Byte 0 = 0x02 feedback
    
    CAN ID: 
        0x47B
    
    Args:
        joint_1_protection_level: 1号关节碰撞防护等级
        joint_2_protection_level: 2号关节碰撞防护等级
        joint_3_protection_level: 3号关节碰撞防护等级
        joint_4_protection_level: 4号关节碰撞防护等级
        joint_5_protection_level: 5号关节碰撞防护等级
        joint_6_protection_level: 6号关节碰撞防护等级
    
    设定值 : 0~8

    等级 0 代表不检测碰撞； 6个关节可以独立设置

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
    msg_v2_feedback
    
    Get the collision protection level feedback for each joint.

    0x477 Byte 0 = 0x02 feedback
    
    CAN ID: 
        0x47B

    Args:
        joint_1_protection_level (int): Collision protection level for joint 1 (0-8)
        joint_2_protection_level (int): Collision protection level for joint 2 (0-8)
        joint_3_protection_level (int): Collision protection level for joint 3 (0-8)
        joint_4_protection_level (int): Collision protection level for joint 4 (0-8)
        joint_5_protection_level (int): Collision protection level for joint 5 (0-8)
        joint_6_protection_level (int): Collision protection level for joint 6 (0-8)

    Level Description:
        0: No collision detection
        1-8: Collision detection thresholds increase (higher values represent more sensitive thresholds)

    Byte Description:

        Byte 0: Collision protection level for joint 1, uint8
        Byte 1: Collision protection level for joint 2, uint8
        Byte 2: Collision protection level for joint 3, uint8
        Byte 3: Collision protection level for joint 4, uint8
        Byte 4: Collision protection level for joint 5, uint8
        Byte 5: Collision protection level for joint 6, uint8
        Byte 6: Reserved
        Byte 7: Reserved
    '''
    def __init__(self, 
                 joint_1_protection_level: int = 0, 
                 joint_2_protection_level: int = 0, 
                 joint_3_protection_level: int = 0,
                 joint_4_protection_level: int = 0,
                 joint_5_protection_level: int = 0,
                 joint_6_protection_level: int = 0
                 ):
        self.joint_1_protection_level = joint_1_protection_level
        self.joint_2_protection_level = joint_2_protection_level
        self.joint_3_protection_level = joint_3_protection_level
        self.joint_4_protection_level = joint_4_protection_level
        self.joint_5_protection_level = joint_5_protection_level
        self.joint_6_protection_level = joint_6_protection_level

    def __str__(self):
        '''
        返回对象的字符串表示，用于打印。
        '''
        '''
        Return the string representation of the object for printing.
        '''
        return (f"ArmMsgFeedbackCrashProtectionRating(\n"
                f"  joint_1_protection_level: {self.joint_1_protection_level}\n"
                f"  joint_2_protection_level: {self.joint_2_protection_level}\n"
                f"  joint_3_protection_level: {self.joint_3_protection_level}\n"
                f"  joint_4_protection_level: {self.joint_4_protection_level}\n"
                f"  joint_5_protection_level: {self.joint_5_protection_level}\n"
                f"  joint_6_protection_level: {self.joint_6_protection_level}\n"
                f")")

    def __repr__(self):
        '''
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        '''
        '''
        Return the formal string representation of the object, typically used for debugging.
        
        :return: The string representation of the object, identical to `__str__`.
        '''
        return self.__str__()
