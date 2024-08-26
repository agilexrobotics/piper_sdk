#!/usr/bin/env python3
# -*-coding:utf8-*-
import math
from typing_extensions import (
    Literal,
)
class ArmLowSpdFeedback:
    '''
    驱动器信息高速反馈 0x6

    节点 ID: 0x1~0x06
    帧 ID :  0X261~0x266

    :Byte 0: 电压高八位, uint16, 当前驱动器电压单位: 0.1V
    :Byte 1: 电压低八位
    :Byte 2: 驱动器温度高八位, int16, 单位: 1℃
    :Byte 3: 驱动器温度低八位
    :Byte 4: 电机温度, int8, 单位: 1℃
    :Byte 5: 驱动器状态, uint8
        bit[0] 电源电压是否过低(0: 正常 1: 过低)
        bit[1] 电机是否过温(0: 正常 1: 过温)
        bit[2] 驱动器是否过流(0: 正常 1: 过流)
        bit[3] 驱动器是否过温(0: 正常 1: 过温)
        bit[4] 碰撞保护状态(0: 正常 1: 异常)-7.25修改,之前为传感器状态
        bit[5] 驱动器错误状态(0: 正常 1: 错误)
        bit[6] 驱动器使能状态(1: 使能 0: 失能)
        bit[7] 堵转保护状态(0: 没有回零 1:已经回零,或已经回过零)-7.25修改，之前为回零状态
    :Byte 6: 母线电流高八位, uint16, 当前驱动器电流单位: 0.001A
    :Byte 7: 母线电流低八位
    '''
    def __init__(self, 
                 can_id:Literal[0x000,0x261,0x262,0x263,0x264,0x264,0x265,0x266]=0,
                 vol:int=0, 
                 foc_temp:int=0, 
                 motor_temp: int=0,
                 foc_status: int=0,
                 bus_current: int=0,
                 ):
        """
        初始化 ArmLowSpdFeedback 实例。
        """
        if can_id not in [0x000,0x261,0x262,0x263,0x264,0x264,0x265,0x266]:
            raise ValueError(f"can_id 值 {can_id} 不在范围 [0x000,0x261,0x262,0x263,0x264,0x264,0x265,0x266]")
        self.can_id = can_id
        self.vol = vol
        self.foc_temp = foc_temp
        self.motor_temp = motor_temp
        self._foc_status_code = foc_status
        self.foc_status = self.FOC_Status()
        self.bus_current = bus_current

    class FOC_Status:
        def __init__(self):
            self.voltage_too_low  = False
            self.motor_overheating = False
            self.driver_overcurrent = False
            self.driver_overheating = False
            self.sensor_status = False
            self.driver_error_status = False
            self.driver_enable_status = False
            self.homing_status  = False
        def __str__(self): 
            return (f"    voltage_too_low : {self.voltage_too_low}\n"
                    f"    motor_overheating: {self.motor_overheating}\n"
                    f"    driver_overcurrent: {self.driver_overcurrent}\n"
                    f"    driver_overheating: {self.driver_overheating}\n"
                    f"    sensor_status: {self.sensor_status}\n"
                    f"    driver_error_status: {self.driver_error_status}\n"
                    f"    driver_enable_status: {self.driver_enable_status}\n"
                    f"    homing_status: {self.homing_status}\n"
                    )

    @property
    def foc_status_code(self):
        return self._foc_status_code

    @foc_status_code.setter
    def foc_status_code(self, value: int):
        if not (0 <= value < 2**8):
            raise ValueError("foc_status_code must be an 8-bit integer between 0 and 255.")
        self._foc_status_code = value
        # Update foc_status based on the foc_status_code bits
        self.foc_status.voltage_too_low = bool(value & (1 << 0))
        self.foc_status.motor_overheating = bool(value & (1 << 1))
        self.foc_status.driver_overcurrent = bool(value & (1 << 2))
        self.foc_status.driver_overheating = bool(value & (1 << 3))
        self.foc_status.sensor_status = bool(value & (1 << 4))
        self.foc_status.driver_error_status = bool(value & (1 << 5))
        self.foc_status.driver_enable_status = bool(value & (1 << 6))
        self.foc_status.homing_status = bool(value & (1 << 7))

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmLowSpdFeedback(\n"
                f"  can_id: {hex(self.can_id)},\n"
                f"  vol: {self.vol}, {self.vol*0.1:.1f}V,\n"
                f"  foc_temp: {self.foc_temp }C,\n"
                f"  motor_temp: {self.motor_temp }C,\n"
                f"  foc_status: \n{self.foc_status },\n"
                f"  bus_current: {self.bus_current}, {self.bus_current*0.001:.1f}A\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
