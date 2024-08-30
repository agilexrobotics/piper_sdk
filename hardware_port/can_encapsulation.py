#!/usr/bin/env python3
# -*-coding:utf8-*-
# can总线读取二次封装
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

class C_STD_CAN():
    '''
    基础CAN数据帧的收发,内无线程创建,需要在类外调用的时候创建线程来循环read
    '''
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
        self.rx_message:Optional[Message]   #创建消息接收类
        self.callback_function = callback_function  #接收回调函数
        self.bus = None
        if(judge_flag):
            self.JudgeCanInfo()
        if(auto_init):
            self.Init()#创建can总线交互
        
    def __del__(self):
        try:
            self.bus.shutdown()  # 关闭 CAN 总线
            # print("CAN bus connection properly shut down.")
        except AttributeError:
            print("CAN bus connection was not properly initialized.")
        except Exception as e:
            print(f"Error occurred while shutting down CAN bus: {e}")
    
    def Init(self):
        """初始化can总线
        """
        if self.bus is not None:
            print("CAN bus is already open.")
            return
        try:
            self.bus = can.interface.Bus(channel=self.channel_name, bustype=self.bustype)
            print(self.channel_name,"bus opened successfully.")
        except can.CanError as e:
            print(f"Failed to open CAN bus: {e}")
            self.bus = None

    def Close(self):
        """关闭can总线
        """
        if self.bus is not None:
            try:
                self.bus.shutdown()  # 关闭 CAN 总线
                # print("CAN bus connection properly shut down.")
            except AttributeError:
                print("CAN bus connection was not properly initialized.")
                return -1
            except Exception as e:
                print(f"Error occurred while shutting down CAN bus: {e}")
                return -2
            self.bus = None
            # print("CAN bus closed successfully.")
            return 1
        else:
            print("CAN bus was not open.")
            return 0
    
    def JudgeCanInfo(self):
        '''
        类初始化时是否检测基础信息
        '''
        # 检查 CAN 端口是否存在
        if not self.is_can_socket_available(self.channel_name):
            raise ValueError(f"CAN socket {self.channel_name} does not exist.")
        print(self.channel_name, " is exist")
        # 检查 CAN 端口是否 UP
        if not self.is_can_port_up(self.channel_name):
            raise RuntimeError(f"CAN port {self.channel_name} is not UP.")
        print(self.channel_name, " is UP")
        # 检查 CAN 端口的比特率
        actual_bitrate = self.get_can_bitrate(self.channel_name)
        if self.expected_bitrate is not None and not (actual_bitrate == self.expected_bitrate):
            raise ValueError(f"CAN port {self.channel_name} bitrate is {actual_bitrate} bps, expected {self.expected_bitrate} bps.")
        print(self.channel_name, " bitrate is ", self.expected_bitrate)
    
    def GetBirtrate(self):
        return self.expected_bitrate

    def GetRxMessage(self):
        return self.rx_message

    def ReadCanMessage(self):
        if self.is_can_bus_ok():
            self.rx_message = self.bus.recv()
            if self.rx_message and self.callback_function:
                self.callback_function(self.rx_message) #回调函数处理接收的原始数据
        else:
            print("CAN bus is not OK, skipping message read")

    def SendCanMessage(self, arbitration_id, data):
        """can 发送

        Args:
            arbitration_id (_type_): _description_
            data (_type_): _description_
            is_extended_id_ (bool, optional): _description_. Defaults to False.
        """
        message = can.Message(channel=self.channel_name,
                              arbitration_id=arbitration_id, 
                              data=data, 
                              dlc=8,
                              is_extended_id=False)
        if self.is_can_bus_ok():
            try:
                self.bus.send(message)
                # print(message)
                # print(f"Message sent on {self.bus.channel_info}")
            except can.CanError:
                print(can.CanError,"Message NOT sent")
        else:
            print("CAN bus is not OK, cannot send message")

    def is_can_bus_ok(self) -> bool:
        """
        检查CAN总线状态是否正常。
        """
        bus_state = self.bus.state
        if bus_state == can.BusState.ACTIVE:
            # print("CAN bus state: ACTIVE - Bus is functioning normally")
            return True
        elif bus_state == can.BusState.PASSIVE:
            print("CAN bus state: PASSIVE - Warning level errors are occurring")
            return False  # 可以根据需要调整
        elif bus_state == can.BusState.ERROR:
            print("CAN bus state: ERROR - Communication may be impaired")
            return False
        else:
            print(f"Unknown CAN bus state: {bus_state}")
            return False
    
    def is_can_socket_available(self, channel_name: str) -> bool:
        """
        检查给定的 CAN 端口是否存在。
        """
        try:
            with open(f"/sys/class/net/{channel_name}/operstate", "r") as file:
                state = file.read().strip()
                return state == "up"
        except FileNotFoundError:
            return False

    def get_can_ports(self) -> list:
        """
        获取系统中所有可用的 CAN 端口。
        """
        import os
        can_ports = []
        for item in os.listdir('/sys/class/net/'):
            if 'can' in item:
                can_ports.append(item)
        return can_ports

    def can_port_info(self, channel_name: str) -> str:
        """
        获取指定 CAN 端口的详细信息，包括状态、类型和比特率。
        """
        try:
            with open(f"/sys/class/net/{channel_name}/operstate", "r") as file:
                state = file.read().strip()
            with open(f"/sys/class/net/{channel_name}/type", "r") as file:
                port_type = file.read().strip()
            bitrate = self.get_can_bitrate(channel_name)
            return f"CAN port {channel_name}: State={state}, Type={port_type}, Bitrate={bitrate} bps"
        except FileNotFoundError:
            return f"CAN port {channel_name} not found."

    def is_can_port_up(self, channel_name: str) -> bool:
        """
        检查 CAN 端口是否为 UP 状态。
        """
        try:
            with open(f"/sys/class/net/{channel_name}/operstate", "r") as file:
                state = file.read().strip()
                return state == "up"
        except FileNotFoundError:
            return False

    def get_can_bitrate(self, channel_name: str) -> str:
        """
        获取指定 CAN 端口的比特率。
        """
        try:
            result = subprocess.run(['ip', '-details', 'link', 'show', channel_name],
                                    capture_output=True, text=True)
            output = result.stdout
            for line in output.split('\n'):
                if 'bitrate' in line:
                    return int(line.split('bitrate ')[1].split(' ')[0])
            return "Unknown"
        except Exception as e:
            print(f"Error while getting bitrate: {e}")
            return "Unknown"

tim_stamp = time.time()
count = 0

def check_and_convert_to_negative(value):
    # 定义 32 位整数的范围
    INT32_MAX = 2**31 - 1
    INT32_MIN = -2**31

    # 判断是否超出范围
    # if value > INT32_MAX or value < INT32_MIN:
    #     print("Warning: Value is out of 32-bit range, which means it would overflow in C-like languages.")
    
    # 转换成 32 位有符号整数
    value &= 0xFFFFFFFF  # 将 value 转换成 32 位无符号整数

    if value & 0x80000000:  # 检查符号位
        value -= 0x100000000  # 如果符号位为 1，表示负数，需要减去 2^32

    return value
from typing_extensions import (
    Literal,
    LiteralString,
)

def ConvertBytesToInt(bytes:bytearray, first_index:int, second_index:int, byteorder:Literal["little", "big"]):
        return int.from_bytes(bytes[first_index:second_index], byteorder=byteorder)

def callback(rx:Optional[Message]):
    global tim_stamp
    global count
    if(rx.arbitration_id == 0x2A5):
        # if(abs(rx.timestamp - tim_stamp) > 1):
        #     tim_stamp = rx.timestamp
        #     print(count)
        #     count = 0
        # else:
        #     count = count + 1
        if len(rx.data) != 8:
            raise ValueError("CAN 数据帧长度必须为 8 字节")

        # 提取 byte0 到 byte3 (第一个数)
        # print(rx.data)
        number1 = check_and_convert_to_negative(ConvertBytesToInt(rx.data,0,4,'big'))  # 使用大端字节序
        # 提取 byte4 到 byte7 (第二个数)
        number2 = check_and_convert_to_negative(int.from_bytes(rx.data[4:8], byteorder='big'))  # 使用大端字节序
        print(number1,number2)
        # print(f"{rx.data.hex()}")
        pass

# a = C_STD_CAN(callback_function = callback)
# while True:
#     a.ReadCanMessage()


# 示例代码
# if __name__ == "__main__":
#     try:
#         can_obj = C_STD_CAN(channel_name="can0")
#         print("CAN bus initialized successfully.")
#         print(can_obj.get_can_ports())
#         print(can_obj.can_port_info("can0"))
#     except ValueError as e:
#         print(e)
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")