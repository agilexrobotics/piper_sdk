#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgParamEnquiryAndConfig:
    '''
    机械臂参数查询与设置指令

    0x477

    :Byte 0: 参数查询, uint8, 查询末端 V/acc 参数:0x01
                            查询碰撞防护等级： 0x02
    :Byte 1: 参数设置, uint8, 设置末端 V/acc 参数为初始值: 0x01
    :Byte 2: 0x48X 报文反馈设置, uint8,   关闭周期反馈: 0x00
                                        开启周期反馈： 0x01
                                        开启后周期上报 1~6 号关节当前末端速度/加速度
    :Byte 3: 末端负载参数设置是否生效, uint8, 有效值 : 0xAE
    :Byte 4: 设置末端负载, uint8, 0x00 : 空载
                                0x01 : 半载
                                0x02 : 满载
    '''
    def __init__(self, 
                 param_enquiry:Literal[0x00, 0x01, 0x02]=0x00, 
                 param_setting: Literal[0x00, 0x01]=0, 
                 data_feedback_0x48x: Literal[0x00, 0x01, 0x02]=0x02,
                 end_load_param_setting_effective: Literal[0x00, 0xAE]=0,
                 set_end_load: Literal[0x00, 0x01, 0x02, 0x03]=0x03
                 ):
        """
        初始化 ArmMsgMotorAngleSpdLimitConfig 实例。

        机械臂参数查询与设置指令

        0x477

        :Byte 0: 参数查询, uint8, 查询末端 V/acc 参数:0x01
                                查询碰撞防护等级： 0x02
        :Byte 1: 参数设置, uint8, 设置末端 V/acc 参数为初始值: 0x01
        :Byte 2: 0x48X 报文反馈设置, uint8,   关闭周期反馈: 0x00
                                            开启周期反馈： 0x01
                                            开启后周期上报 1~6 号关节当前末端速度/加速度
        :Byte 3: 末端负载参数设置是否生效, uint8, 有效值 : 0xAE
        :Byte 4: 设置末端负载, uint8, 0x00 : 空载
                                    0x01 : 半载
                                    0x02 : 满载
        """
        if param_enquiry not in [0x00, 0x01, 0x02]:
            raise ValueError(f"param_enquiry 值 {param_enquiry} 超出范围 [0x00, 0x01, 0x02]")
        if param_setting not in [0x00, 0x01]:
            raise ValueError(f"param_setting 值 {param_setting} 超出范围 [0x00, 0x01]")
        if data_feedback_0x48x not in [0x00, 0x01, 0x02]:
            raise ValueError(f"data_feedback_0x48x 值 {data_feedback_0x48x} 超出范围 [0x00, 0x01, 0x02]")
        if end_load_param_setting_effective not in [0x00, 0xAE]:
            raise ValueError(f"end_load_param_setting_effective 值 {end_load_param_setting_effective} 超出范围 [0x00, 0xAE]")
        if set_end_load not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"set_end_load 值 {set_end_load} 超出范围 [0x00, 0x01, 0x02, 0x03]")
        self.param_enquiry = param_enquiry
        self.param_setting = param_setting
        self.data_feedback_0x48x = data_feedback_0x48x
        self.end_load_param_setting_effective = end_load_param_setting_effective
        self.set_end_load = set_end_load

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmMsgParamEnquiryAndConfig(\n"
                f"  param_enquiry: {self.param_enquiry},\n"
                f"  param_setting: {self.param_setting},\n"
                f"  data_feedback_0x48x: {self.data_feedback_0x48x},\n"
                f"  end_load_param_setting_effective: {self.end_load_param_setting_effective},\n"
                f"  set_end_load: {self.set_end_load}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
