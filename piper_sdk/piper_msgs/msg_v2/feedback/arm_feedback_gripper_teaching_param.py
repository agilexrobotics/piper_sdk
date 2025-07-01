#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgFeedbackGripperTeachingPendantParam:
    '''
    msg_v2_feedback
    
    夹爪/示教器参数反馈指令(基于V1.5-2版本后)
    
    CAN ID:
        0x47E
    
    Args:
        teaching_range_per: 示教器行程系数反馈,[100~200]
        max_range_config: 夹爪/示教器最大控制行程限制值反馈,[0,70,100]
        teaching_friction: 示教器摩擦系数设置,范围[1, 10] ----- (基于V1.5-8版本及以后)
    
    位描述:
    
        Byte 0 示教器行程系数反馈, uint8 
            示教器行程系数反馈---100~200,单位(%)(默认100%)
            仅适用于设置主从臂的主臂，用于放大控制行程给从臂
        Byte 1 夹爪/示教器最大控制行程限制值反馈, uint8, 单位(mm)
            无效值---0
            小夹爪为---70mm
            大夹爪为---100mm
        Byte 2 示教器摩擦系数设置, uint8, 范围[1, 10] ----- (基于V1.5-8版本及以后)
        Byte 3 保留
        Byte 4 保留
        Byte 5 保留
        Byte 6 保留
        Byte 7 保留
    '''
    '''
    msg_v2_feedback
    
    Gripper/Teaching Pendant Parameter Feedback(Based on version V1.5-2 and later)

    CAN ID:
        0x47E

    Args:
        teaching_range_per: Teaching pendant stroke coefficient setting.[100~200]
        max_range_config: Maximum control stroke limit setting for the gripper/teaching pendant.[0,70,100]
        teaching_friction: Teaching pendant friction coefficient setting,range [1, 10].(Based on version V1.5-8 and later)

    Bit Description:
    
        Byte	Field	Type	Details
        Byte 0	Teaching range coefficient	uint8	Stroke coefficient setting: 100% to 200% (default: 100%).
                    Only applicable to the master arm in a master-slave setup to scale control range for the slave arm.
        Byte 1	Max control stroke limit	uint8	Invalid value: 0
                    Small gripper: 70 mm
                    Large gripper: 100 mm
        Byte 2	Teaching pendant friction coefficient setting, `uint8`, range [1, 10].(Based on version V1.5-8 and later)
        Byte 3	Reserved	-	Reserved for future use.
        Byte 4	Reserved	-	Reserved for future use.
        Byte 5	Reserved	-	Reserved for future use.
        Byte 6	Reserved	-	Reserved for future use.
        Byte 7	Reserved	-	Reserved for future use.
    '''
    def __init__(self, 
                 teaching_range_per: int = 0, 
                 max_range_config: int = 0,
                 teaching_friction: int = 0):
        self.teaching_range_per = teaching_range_per
        self.max_range_config = max_range_config
        self.teaching_friction = teaching_friction

    def __str__(self):
        return (f"ArmMsgFeedbackGripperTeachingPendantParam(\n"
                f"  teaching_range_per: {self.teaching_range_per}\n"
                f"  max_range_config: {self.max_range_config}\n"
                f"  teaching_friction: {self.teaching_friction}\n"
                f")")

    def __repr__(self):
        return self.__str__()
