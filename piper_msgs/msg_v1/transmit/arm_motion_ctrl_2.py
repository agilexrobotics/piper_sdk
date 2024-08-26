#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
class ArmMsgMotionCtrl_2():
    '''
    机械臂运动控制指令2

    0x151

    Byte 0 控制模式     uint8    0x00 待机模式
                                0x01 CAN 指令控制模式
                                0x02 示教模式
                                0x03 以太网控制模式
                                0x04 wifi 控制模式
                                0x07 离线轨迹模式
    Byte 1 MOVE模式     uint8    0x00 MOVE P
                                0x01 MOVE J
                                0x02 MOVE L
                                0x03 MOVE C
    Byte 2 运动速度百分比 uint8    0~100
    Byte 3 mit模式      uint8    0x00 位置速度模式
                                0xAD MIT模式
    Byte 4 离线轨迹点停留时间 uint8 0~255 单位 s
    '''
    def __init__(self, 
                 ctrl_mode:Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x07]=0x01, 
                 move_mode:Literal[0x00, 0x01, 0x02, 0x03]=0x01, 
                 move_spd_rate_ctrl:int=50,
                 mit_mode:Literal[0x00, 0xAD, 0xFF]=0x00,
                 residence_time:int=0):
        # 检查是否在有效范围内
        if ctrl_mode not in [0x00, 0x01, 0x02, 0x03, 0x04, 0x07]:
            raise ValueError(f"ctrl_mode 值 {ctrl_mode} 超出范围 [0x00, 0x01, 0x02, 0x03, 0x04, 0x07]")
        if move_mode not in [0x00, 0x01, 0x02, 0x03]:
            raise ValueError(f"move_mode 值 {move_mode} 超出范围 [0x00, 0x01, 0x02, 0x03]")
        if not (0<= move_spd_rate_ctrl <=100):
            raise ValueError(f"输入的值 {move_spd_rate_ctrl} 超出范围 [0, 100]")
        if mit_mode not in [0x00, 0xAD, 0xFF]:
            raise ValueError(f"mit_mode 值 {mit_mode} 超出范围 [0x00, 0xAD, 0xFF]")
        if not (0<= residence_time <=255):
            raise ValueError(f"输入的值 {residence_time} 超出范围 [0, 255]")
        self.ctrl_mode = ctrl_mode
        self.move_mode = move_mode
        self.move_spd_rate_ctrl = move_spd_rate_ctrl
        self.mit_mode = mit_mode
        self.residence_time = residence_time

    def __str__(self):
        dict_ = [
            (" ctrl_mode ", self.ctrl_mode),
            (" move_mode ", self.move_mode),
            (" move_spd_rate_ctrl ", self.move_spd_rate_ctrl),
            (" mit_mode ", self.mit_mode),
            (" residence_time ", self.residence_time)
        ]

        # 生成格式化字符串，保留三位小数
        formatted_ = "\n".join([f"{name}: {value}" for name, value in dict_])
        
        return f"ArmMsgMotionCtrl_2:\n{formatted_}"
    
    def __repr__(self):
        return self.__str__()