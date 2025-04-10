#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgParamEnquiryAndConfig:
    '''
    msg_v2_transmit
    
    机械臂参数查询与设置指令
    
    CAN ID:
        0x477
    
    Args:
        param_enquiry: 参数查询
        param_setting: 参数设置
        data_feedback_0x48x: 0x48X报文反馈设置
        end_load_param_setting_effective: 末端负载参数设置是否生效
        set_end_load: 设置末端负载
    
    位描述:

        Byte 0: uint8,参数查询,查询末端 V/acc
                0x01,查询末端 V/acc
                0x02,查询碰撞防护等级
                0x03,查询当前轨迹索引
                0x04,查询夹爪/示教器参数索引 ---- 基于V1.5-2版本后
        Byte 1: uint8,参数设置,
                设置末端 V/acc 参数为初始值: 0x01
                设置全部关节限位、关节最大速度、关节加速度为默认值: 0x02
        Byte 2: uint8,0x48X 报文反馈设置,
                无效:0x00
                关闭周期反馈: 0x01;
                开启周期反馈: 0x02;
                开启后周期上报 1~6 号关节当前末端速度/加速度
        Byte 3: uint8,末端负载参数设置是否生效,有效值 : 0xAE
        Byte 4: uint8,设置末端负载,
                0x00 : 空载;
                0x01 : 半载;
                0x02 : 满载;
                0x03 : 无效
    '''
    '''
    msg_v2_transmit
    
    Robot Arm Parameter Query and Setting Command

    CAN ID:
        0x477

    Args:
        param_enquiry: Parameter query.
        param_setting: Parameter setting.
        data_feedback_0x48x: 0x48X message feedback setting.
        end_load_param_setting_effective: Whether the end-load parameter setting is effective.
        set_end_load: Set the end load.

    Bit Description:

        Byte 0: uint8, parameter query, used to query end velocity/acceleration or collision protection level:
            0x01: Query end velocity/acceleration.
            0x02: Query collision protection level.
            0x03: Query the current trajectory index.
            0x04: Query gripper/teaching pendant parameter index (Based on version V1.5-2 and later)
        Byte 1: uint8, parameter setting, 
            set end velocity/acceleration parameters to initial values(0x01)
            Sets all joint limits, joint maximum speed, and joint acceleration to default values (0x02).
        Byte 2: uint8, 0x48X message feedback setting:
            0x00: Invalid.
            0x01: Disable periodic feedback.
            0x02: Enable periodic feedback (reports current end velocity/acceleration of joints 1~6).
        Byte 3: uint8, whether the end-load parameter setting is effective:
            Valid value: 0xAE.
        Byte 4: uint8, set the end load:
            0x00: No load.
            0x01: Half load.
            0x02: Full load.
            0x03: Invalid.
    '''
    def __init__(self, 
                 param_enquiry:Literal[0x00, 0x01, 0x02, 0x03, 0x04] = 0x00, 
                 param_setting: Literal[0x00, 0x01, 0x02] = 0, 
                 data_feedback_0x48x: Literal[0x00, 0x01, 0x02] = 0x00,
                 end_load_param_setting_effective: Literal[0x00, 0xAE] = 0,
                 set_end_load: Literal[0x00, 0x01, 0x02, 0x03] = 0x03
                 ):
        if param_enquiry not in [0x00, 0x01, 0x02, 0x03, 0x04]:
            raise ValueError(f"'param_enquiry' Value {param_enquiry} out of range [0x00, 0x01, 0x02, 0x03, 0x04]")
        if param_setting not in [0x00, 0x01, 0x02]:
            raise ValueError(f"'param_setting' Value {param_setting} out of range [0x00, 0x01, 0x02]")
        if data_feedback_0x48x not in [0x00, 0x01, 0x02]:
            raise ValueError(f"'data_feedback_0x48x' Value {data_feedback_0x48x} out of range [0x00, 0x01, 0x02]")
        if end_load_param_setting_effective not in [0x00, 0xAE]:
            raise ValueError(f"'end_load_param_setting_effective' Value {end_load_param_setting_effective} out of range [0x00, 0xAE]")
        if set_end_load not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"'set_end_load' Value {set_end_load} out of range [0x00, 0x01, 0x02, 0x03]")
        self.param_enquiry = param_enquiry
        self.param_setting = param_setting
        self.data_feedback_0x48x = data_feedback_0x48x
        self.end_load_param_setting_effective = end_load_param_setting_effective
        self.set_end_load = set_end_load

    def __str__(self):
        return (f"ArmMsgParamEnquiryAndConfig(\n"
                f"  param_enquiry: {self.param_enquiry},\n"
                f"  param_setting: {self.param_setting},\n"
                f"  data_feedback_0x48x: {self.data_feedback_0x48x},\n"
                f"  end_load_param_setting_effective: {self.end_load_param_setting_effective},\n"
                f"  set_end_load: {self.set_end_load}\n"
                f")")

    def __repr__(self):
        return self.__str__()
