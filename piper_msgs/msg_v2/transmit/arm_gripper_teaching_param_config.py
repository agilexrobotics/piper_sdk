#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgGripperTeachingPendantParamConfig:
    '''
    msg_v2_transmit
    
    夹爪/示教器参数设置指令(基于V1.5-2版本后)
    
    CAN ID:
        0x47D
    
    Args:
        teaching_range_per: 示教器行程系数设置,[100~200]
        max_range_config: 夹爪/示教器最大控制行程限制值设置,[0,70,100]
    
    位描述:
    
        Byte 0: 示教器行程系数设置, uint8 
            示教器行程系数设置---100~200,单位(%)(默认100%)
            仅适用于设置主从臂的主臂，用于放大控制行程给从臂
        Byte 1: 夹爪/示教器最大控制行程限制值设置, uint8, 单位(mm)
            无效值---0
            小夹爪为---70mm
            大夹爪为---100mm
        Byte 2: 保留
        Byte 3: 保留
        Byte 4: 保留
        Byte 5: 保留
        Byte 6: 保留
        Byte 7: 保留
    '''
    '''
    msg_v2_transmit
    
    Gripper/Teaching Pendant Parameter Configuration Command(Based on version V1.5-2 and later)

    CAN ID:
        0x47D

    Args:
        teaching_range_per: Teaching pendant stroke coefficient setting.[100~200]
        max_range_config: Maximum control stroke limit setting for the gripper/teaching pendant.[0,70,100]

    Bit Description:
    
        Byte	Field	Type	Details
        Byte 0	Teaching range coefficient	uint8	- Stroke coefficient setting: 100% to 200% (default: 100%).
                    - Only applicable to the master arm in a master-slave setup to scale control range for the slave arm.
        Byte 1	Max control stroke limit	uint8	- Invalid value: 0
                    - Small gripper: 70 mm
                    - Large gripper: 100 mm
        Byte 2	Reserved	-	Reserved for future use.
        Byte 3	Reserved	-	Reserved for future use.
        Byte 4	Reserved	-	Reserved for future use.
        Byte 5	Reserved	-	Reserved for future use.
        Byte 6	Reserved	-	Reserved for future use.
        Byte 7	Reserved	-	Reserved for future use.
    '''
    def __init__(self, 
                 teaching_range_per: int = 100, 
                 max_range_config: Literal[0, 70, 100] = 0):
        if not (100 <= teaching_range_per <= 200):
            raise ValueError(f"'teaching_range_per' Value {teaching_range_per} out of range [100, 200]")
        if max_range_config not in [0, 70, 100]:
            raise ValueError(f"'max_range_config' Value {max_range_config} out of range [0,70,100]")
        self.teaching_range_per = teaching_range_per
        self.max_range_config = max_range_config

    def __str__(self):
        return (f"ArmMsgGripperTeachingPendantParamConfig(\n"
                f"  teaching_range_per: {self.teaching_range_per},\n"
                f"  max_range_config: {self.max_range_config},\n"
                f")")

    def __repr__(self):
        return self.__str__()
