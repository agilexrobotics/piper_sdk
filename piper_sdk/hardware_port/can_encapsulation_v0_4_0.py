#!/usr/bin/env python3
# -*-coding:utf8-*-
# can总线读取二次封装
# 反馈码为100开头，反馈码总长为000000
import can
from can.message import Message
import time
from threading import Timer
import subprocess
from typing import (
    Callable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)
from enum import IntEnum, auto

class C_STD_CAN():
    '''
    基础CAN数据帧的收发,内无线程创建,需要在类外调用的时候创建线程来循环read
    
    Args:
        channel_name: can的端口名称
        bustype: can总线类型,默认为socket can
        expected_bitrate: 预期can总线的波特率
        judge_flag: 是否在实例化该类时进行can端口判断,有些情况需要False 
        auto_init: 是否自动初始化can,也就是实例化can.interface.Bus
        callback_function: ReadCanMessage中的回调函数,应传入函数
    '''
    '''
    Basic CAN Frame Send/Receive with Thread Creation

    When calling outside the class, a thread needs to be created to continuously read the CAN data.

    Args:
        channel_name: The name of the CAN port.
        bustype: The type of CAN bus, default is socket CAN.
        expected_bitrate: The expected bitrate for the CAN bus.
        judge_flag: Whether to check the CAN port during the instantiation of the class. In some cases, it should be set to False.
        auto_init: Whether to automatically initialize the CAN bus (i.e., instantiate can.interface.Bus).
        callback_function: The callback function in ReadCanMessage, which should be passed as a function.
    '''
    class CAN_STATUS(IntEnum):
        # __del__
        DEL_CAN_BUS_CONNECT_SHUT_DOWN = 100001
        DEL_CAN_BUS_WAS_NOT_PROPERLY_INIT = auto()
        DEL_SHUTTING_DOWN_CAN_BUS_ERR = auto()
        INIT_CAN_BUS_IS_EXIST = auto()
        INIT_CAN_BUS_OPENED_SUCCESS = auto()
        INIT_CAN_BUS_OPENED_FAILED = auto()
        CLOSE_CAN_BUS_CONNECT_SHUT_DOWN = auto()
        CLOSE_CAN_BUS_WAS_NOT_PROPERLY_INIT = auto()
        CLOSE_SHUTTING_DOWN_CAN_BUS_ERR = auto()
        CLOSED_CAN_BUS_NOT_OPEN = auto()
        JUDGE_PASS = auto()
        READ_CAN_MSG_OK = auto()
        READ_CAN_MSG_TIMEOUT = auto()
        READ_CAN_MSG_FAILED = auto()
        READ_CAN_BUS_NOT_OK = auto()
        SEND_MESSAGE_SUCCESS = auto()
        SEND_MESSAGE_FAILED = auto()
        SEND_CAN_BUS_NOT_OK = auto()
        BUS_STATE_ACTIVE = auto()
        BUS_STATE_PASSIVE = auto()
        BUS_STATE_ERROR = auto()
        BUS_STATE_UNKNOWN = auto()
        CHECK_CAN_EXIST = auto()
        CHECK_CAN_UP = auto()
        CHECK_CAN_NOT_UP = auto()
        CAN_SOCKET_NOT_EXIST = auto()
        CAN_BITRATE_SUCCESS= auto()
        CAN_BITRATE_ERR= auto()
        def __str__(self):
            return f"{self.name} ({self.value})"
        def __repr__(self):
            return f"{self.name}: {self.value}"
    
    def __init__(self, 
                 channel_name:str="can0", 
                 bustype="socketcan", 
                 expected_bitrate:int=1000000,
                 judge_flag:bool=True, 
                 auto_init:bool=True,
                 callback_function: Callable = None) -> None:
        self.channel_name = channel_name
        self.bustype = bustype
        self.expected_bitrate = expected_bitrate
        self.rx_message:Optional[Message] = Message()   #创建消息接收类
        self.callback_function = callback_function  #接收回调函数
        self.bus = None
        if(judge_flag):
            self.JudgeCanInfo()
        if(auto_init):
            self.Init()#创建can总线交互
    
    def __del__(self):
        try:
            self.bus.shutdown()  # 关闭 CAN 总线
            return self.CAN_STATUS.DEL_CAN_BUS_CONNECT_SHUT_DOWN
        except AttributeError:
            return self.CAN_STATUS.DEL_CAN_BUS_WAS_NOT_PROPERLY_INIT
        except Exception as e:
            return self.CAN_STATUS.DEL_SHUTTING_DOWN_CAN_BUS_ERR
    
    def Init(self):
        '''初始化can总线
        '''
        '''Initialize the CAN bus.
        '''
        if self.bus is not None:
            # return True
            return self.CAN_STATUS.INIT_CAN_BUS_IS_EXIST
        try:
            self.bus = can.interface.Bus(channel=self.channel_name, bustype=self.bustype, bitrate=self.expected_bitrate)
            return self.CAN_STATUS.INIT_CAN_BUS_OPENED_SUCCESS
        except can.CanError as e:
            self.bus = None
            return self.CAN_STATUS.INIT_CAN_BUS_OPENED_FAILED

    def Close(self):
        '''关闭can总线
        '''
        '''Close the CAN bus.
        '''
        if self.bus is not None:
            try:
                self.bus.shutdown()  # 关闭 CAN 总线
                self.bus = None
                # return True
                return self.CAN_STATUS.CLOSE_CAN_BUS_CONNECT_SHUT_DOWN
            except AttributeError:
                return self.CAN_STATUS.CLOSE_CAN_BUS_WAS_NOT_PROPERLY_INIT
            except Exception as e:
                return self.CAN_STATUS.CLOSE_SHUTTING_DOWN_CAN_BUS_ERR
            # return 1
        else:
            return self.CAN_STATUS.CLOSED_CAN_BUS_NOT_OPEN
    
    def JudgeCanInfo(self):
        '''
        类初始化时是否检测基础信息
        '''
        '''
        Whether to check basic information during class initialization.
        '''
        # 检查 CAN 端口是否存在
        if self.is_can_socket_available(self.channel_name) is not self.CAN_STATUS.CHECK_CAN_EXIST:
            raise ValueError(f"CAN socket {self.channel_name} does not exist.")
        # 检查 CAN 端口是否 UP
        if self.is_can_port_up(self.channel_name) is not self.CAN_STATUS.CHECK_CAN_UP:
            raise RuntimeError(f"CAN port {self.channel_name} is not UP.")
        # 检查 CAN 端口的比特率
        actual_bitrate = self.get_can_bitrate(self.channel_name)
        if self.expected_bitrate is not None and not (actual_bitrate == self.expected_bitrate):
            raise ValueError(f"CAN port {self.channel_name} bitrate is {actual_bitrate} bps, expected {self.expected_bitrate} bps.")
        # return True
        return self.CAN_STATUS.JUDGE_PASS
    
    def GetBirtrate(self):
        return self.expected_bitrate

    def GetRxMessage(self) -> Message:
        return self.rx_message
    
    def GetCanPortName(self):
        return self.channel_name

    def ReadCanMessage(self):
        can_bus_status = self.is_can_bus_ok()
        if(can_bus_status == self.CAN_STATUS.BUS_STATE_ACTIVE):
            try:
                self.rx_message = self.bus.recv(1)
                if self.rx_message is None:
                    return self.CAN_STATUS.READ_CAN_MSG_TIMEOUT
                if self.rx_message and self.callback_function:
                    self.callback_function(self.rx_message) #回调函数处理接收的原始数据
                return self.CAN_STATUS.READ_CAN_MSG_OK
            except Exception as e:
                return self.CAN_STATUS.READ_CAN_MSG_FAILED
        else:
            return can_bus_status

    def SendCanMessage(self, arbitration_id, data, dlc=8, is_extended_id=False):
        '''can transmit

        Args:
            arbitration_id (_type_): _description_
            data (_type_): _description_ Defaults to 8.
            is_extended_id_ (bool, optional): _description_. Defaults to False.
        '''
        message = can.Message(channel=self.channel_name,
                              arbitration_id=arbitration_id, 
                              data=data, 
                              dlc=dlc,
                              is_extended_id=is_extended_id)
        if(self.is_can_bus_ok() == self.CAN_STATUS.BUS_STATE_ACTIVE):
            try:
                self.bus.send(message)
                # return True
                return self.CAN_STATUS.SEND_MESSAGE_SUCCESS
            # except can.CanError:
            #     return self.CAN_STATUS.SEND_MESSAGE_FAILED
            except Exception as e:
                return self.CAN_STATUS.SEND_MESSAGE_FAILED
        else:
            return self.CAN_STATUS.SEND_CAN_BUS_NOT_OK

    def is_can_bus_ok(self) -> bool:
        '''
        检查CAN总线状态是否正常。
        '''
        '''
        Check whether the CAN bus status is normal.
        '''
        if isinstance(self.bus, can.BusABC):
            bus_state = self.bus.state
        else: bus_state = None
        if bus_state == can.BusState.ACTIVE:
            # return True
            return self.CAN_STATUS.BUS_STATE_ACTIVE
        elif bus_state == can.BusState.PASSIVE:
            # return False
            return self.CAN_STATUS.BUS_STATE_PASSIVE
        elif bus_state == can.BusState.ERROR:
            # return False
            return self.CAN_STATUS.BUS_STATE_ERROR
        else:
            # return False
            return self.CAN_STATUS.BUS_STATE_UNKNOWN
    
    def is_can_socket_available(self, channel_name: str) -> bool:
        '''
        检查给定的 CAN 端口是否存在。
        '''
        '''
        Check if the given CAN port exists.
        '''
        try:
            with open(f"/sys/class/net/{channel_name}/operstate", "r") as file:
                state = file.read().strip()
                # return True
                return  self.CAN_STATUS.CHECK_CAN_EXIST
        except FileNotFoundError:
            # return False
            return  self.CAN_STATUS.CAN_SOCKET_NOT_EXIST
    
    def is_can_port_up(self, channel_name: str) -> bool:
        '''
        检查 CAN 端口是否为 UP 状态。
        '''
        '''
        Check if the CAN port is in the UP state.
        '''
        try:
            with open(f"/sys/class/net/{channel_name}/operstate", "r") as file:
                state = file.read().strip()
                if(state == "up"):
                    # return True
                    return  self.CAN_STATUS.CHECK_CAN_UP
                else: 
                    # return False
                    return  self.CAN_STATUS.CHECK_CAN_NOT_UP
        except FileNotFoundError:
            # return False
            return  self.CAN_STATUS.CAN_SOCKET_NOT_EXIST

    def get_can_ports(self) -> list:
        '''
        获取系统中所有可用的 CAN 端口。
        '''
        '''
        Get all available CAN ports in the system.
        '''
        import os
        can_ports = []
        for item in os.listdir('/sys/class/net/'):
            if 'can' in item:
                can_ports.append(item)
        return can_ports

    def can_port_info(self, channel_name: str) -> str:
        '''
        获取指定 CAN 端口的详细信息，包括状态、类型和比特率。
        '''
        '''
        Get detailed information about the specified CAN port, including status, type, and bit rate.
        '''
        try:
            with open(f"/sys/class/net/{channel_name}/operstate", "r") as file:
                state = file.read().strip()
            with open(f"/sys/class/net/{channel_name}/type", "r") as file:
                port_type = file.read().strip()
            bitrate = self.get_can_bitrate(channel_name)
            return f"CAN port {channel_name}: State={state}, Type={port_type}, Bitrate={bitrate} bps"
        except FileNotFoundError:
            return f"CAN port {channel_name} not found."

    def get_can_bitrate(self, channel_name: str) -> str:
        '''
        获取指定 CAN 端口的比特率。
        '''
        '''
        Get the bit rate of the specified CAN port.
        '''
        try:
            result = subprocess.run(['ip', '-details', 'link', 'show', channel_name],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    universal_newlines=True, check=True)  # Python 3.6
                                    # capture_output=True, text=True)
            output = result.stdout
            for line in output.split('\n'):
                if 'bitrate' in line:
                    return int(line.split('bitrate ')[1].split(' ')[0])
            return self.CAN_STATUS.CAN_BITRATE_SUCCESS
        except Exception as e:
            return self.CAN_STATUS.CAN_BITRATE_ERR, e

## 示例代码
# if __name__ == "__main__":
#     can_name = "can0"
#     try:
#         can_obj = C_STD_CAN(channel_name=can_name)
#         print("CAN bus initialized successfully.")
#         print(can_obj.get_can_ports())
#         print(can_obj.can_port_info(can_name))
#         print(can_obj.ReadCanMessage())
#         print(can_obj.GetRxMessage())
#         # print(can_obj.get_can_bitrate("can_name"))
#         print(f"{can_obj.CAN_STATUS.SEND_CAN_BUS_NOT_OK}")
#     except ValueError as e:
#         print(e)
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# if __name__ == "__main__":
#     can_name = "vcan0"
#     bus = C_STD_CAN(can_name, "socketcan", 1000000,False, True)
#     while True:
#         start_time = time.time()
#         # piper.SearchPiperFirmwareVersion()
#         bus.SendCanMessage(0x101, [0,0,0,0,0,0,0,0])
#         end_time = time.time()
#         cost_ms = (end_time - start_time) * 1000  # 转为毫秒
#         if(cost_ms > 1):
#             print(f"[MAX UPDATE] 最大执行耗时: {cost_ms:.3f} ms")
#         time.sleep(0.001)
#     bus.shutdown()
