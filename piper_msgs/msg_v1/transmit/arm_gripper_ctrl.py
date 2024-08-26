#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgGripperCtrl:
    '''
    夹爪发送消息
    '''
    def __init__(self, 
                 grippers_angle: int=0, 
                 grippers_effort: int=0, 
                 status_code: Literal[0x00,0x01,0x02,0x03]=0,
                 set_zero: Literal[0x00,0xAE]=0):
        """
        初始化 ArmMsgGripperCtrl 实例。

        :Byte 0 grippers_angle: int32, 单位 0.001°, 夹爪角度,以整数表示。
        :Byte 1
        :Byte 2
        :Byte 3
        :Byte 4 grippers_effort: uint16, 单位 0.001N/m, 夹爪扭矩,以整数表示。
        :Byte 5
        :Byte 6 status_code: uint8, 夹爪状态码，使能/失能/清除错误
                            0x00失能,0x01使能
                            0x03/0x02,使能清除错误,失能清除错误
        :Byte 6 set_zero: uint8, 设定当前位置为0点
        """
        if status_code not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"status_code 值 {status_code} 超出范围 [0x00, 0x01, 0x02, 0x03]")
        self.grippers_angle = grippers_angle
        self.grippers_effort = grippers_effort
        self.status_code = status_code
        self.set_zero = set_zero

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        :return: 格式化的字符串表示夹爪的角度、速度和状态码。
        """
        return (f"ArmMsgGripperCtrl(\n"
                f"  grippers_angle: {self.grippers_angle * 0.001:.3f},\n"
                f"  grippers_effort: {self.grippers_effort * 0.01:.2f},\n"
                f"  status_code: {self.status_code},\n"
                f"  set_zero: {self.set_zero}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
