#!/usr/bin/env python3
# -*-coding:utf8-*-
#机械臂协议解析基类

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing_extensions import (
    Literal,
    LiteralString,
)

class C_PiperParserBase(ABC):
    '''
    Piper机械臂数据解析基类
    '''
    class ProtocolVersion(Enum):
        '''
        协议版本枚举,需要在派生类中指定
        '''
        ARM_PROTOCOL_UNKNOWN = auto()
        ARM_PROROCOL_V1 = auto()
        def __str__(self):
            return f"{self.name} (0x{self.value:X})"
        def __repr__(self):
            return f"{self.name}: 0x{self.value:X}"
    
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def DecodeMessage(self):
        '''
        解码消息,将can数据帧转为设定的类型
        '''
        pass
    
    @abstractmethod
    def EncodeMessage(self):
        '''
        将消息转为can数据帧
        
        只将输入数据转换为can数据的id和data, 没有为can message赋值channel、dlc、is_extended_id
        '''
        pass

    @abstractmethod
    def GetParserProtocolVersion(self):
        '''
        获取当前协议版本
        '''
        pass
    
    def ConvertToNegative_8bit(self, value: int, signed:bool=True) -> int:
        '''
        将输入的整数转换为8位整数。
        如果 signed 为 True,则转换为32位有符号整数。[-128, 127]
        如果 signed 为 False,则转换为32位无符号整数。[0, 255]
        '''
        # 范围检查
        if not (0 <= value <= 255):
            print("转换成8bit整数时出错:输入值超出 8 位无符号整数范围: [0, 255]")
        # 转换成 8 位无符号整数
        value &= 0xFF  # 将 value 转换成 8 位无符号整数
        if signed:
            if value & 0x80:  # 检查符号位
                value -= 0x100  # 如果符号位为 1，表示负数，需要减去 2^8
        return value

    def ConvertToNegative_int8_t(value: int) -> int:
        '''
        将输入的整数转换为8位有符号整数。
        范围: [-128, 127]
        '''
        # 范围检查
        if not (0 <= value <= 255):
            print("转换成8bit有符号整数时出错: 输入值超出范围: [0, 255]")
        # 转换成 8 位无符号整数
        value &= 0xFF  # 将 value 转换成 8 位无符号整数
        if value & 0x80:  # 检查符号位
            value -= 0x100  # 如果符号位为 1，表示负数，需要减去 2^8
        return value

    def ConvertToNegative_uint8_t(value: int) -> int:
        '''
        将输入的整数转换为8位无符号整数。
        范围: [0, 255]
        '''
        # 范围检查
        if not (0 <= value <= 255):
            print("转换成8bit无符号整数时出错: 输入值超出范围: [0, 255]")
        # 转换成 8 位无符号整数
        value &= 0xFF  # 将 value 转换成 8 位无符号整数
        return value

    def ConvertToNegative_16bit(self, value: int, signed:bool=True) -> int:
        '''
        将输入的整数转换为16位整数。
        如果 signed 为 True,则转换为32位有符号整数。[-32768, 32767]
        如果 signed 为 False,则转换为32位无符号整数。[0, 65535]
        '''
        # 范围检查
        if not (0 <= value <= 65535):
            print("转换成16bit整数时出错:输入值超出 16 位无符号整数范围: [0, 65535]")
        # 转换成 16 位无符号整数
        value &= 0xFFFF  # 将 value 转换成 16 位无符号整数
        if signed:
            if value & 0x8000:  # 检查符号位
                value -= 0x10000  # 如果符号位为 1，表示负数，需要减去 2^16
        return value
    
    def ConvertToNegative_int16_t(value: int) -> int:
        '''
        将输入的整数转换为16位有符号整数。
        范围: [-32768, 32767]
        '''
        # 范围检查
        if not (0 <= value <= 65535):
            print("转换成8bit有符号整数时出错: 输入值超出范围: [0, 65535]")
        # 转换成 8 位无符号整数
        value &= 0xFFFF  # 将 value 转换成 8 位无符号整数
        if value & 0x8000:  # 检查符号位
            value -= 0x10000  # 如果符号位为 1，表示负数，需要减去 2^8
        return value

    def ConvertToNegative_uint16_t(value: int) -> int:
        '''
        将输入的整数转换为16位无符号整数。
        范围: [0, 65535]
        '''
        # 范围检查
        if not (0 <= value <= 65535):
            print("转换成8bit无符号整数时出错: 输入值超出范围: [0, 65535]")
        # 转换成 8 位无符号整数
        value &= 0xFFFF  # 将 value 转换成 8 位无符号整数
        return value

    def ConvertToNegative_32bit(self, value:int, signed:bool=True):
        '''
        将输入的整数转换为32位整数。
        如果 signed 为 True,则转换为32位有符号整数。
        如果 signed 为 False,则转换为32位无符号整数。
        '''
        # 范围检查
        if not (0 <= value <= 4294967295):
            print("转换成32bit整数时出错:输入值超出 32 位无符号整数范围: [0, 4294967295]")
        # 转换成 32 位无符号整数
        value &= 0xFFFFFFFF  # 将 value 转换成 32 位无符号整数
        if signed:
            if value & 0x80000000:  # 检查符号位
                value -= 0x100000000  # 如果符号位为 1，表示负数，需要减去 2^32
        return value
    
    def ConvertToNegative_int32_t(value: int) -> int:
        '''
        将输入的整数转换为32位有符号整数。
        范围: [-2147483648, 2147483647]
        '''
        # 范围检查
        if not (0 <= value <= 4294967295):
            print("转换成8bit有符号整数时出错: 输入值超出范围: [0, 4294967295]")
        # 转换成 8 位无符号整数
        value &= 0xFFFFFFFF  # 将 value 转换成 8 位无符号整数
        if value & 0x80000000:  # 检查符号位
            value -= 0x100000000  # 如果符号位为 1，表示负数，需要减去 2^8
        return value

    def ConvertToNegative_uint32_t(value: int) -> int:
        '''
        将输入的整数转换为32位无符号整数。
        范围: [0, 4294967295]
        '''
        # 范围检查
        if not (0 <= value <= 4294967295):
            print("转换成8bit无符号整数时出错: 输入值超出范围: [0, 4294967295]")
        # 转换成 8 位无符号整数
        value &= 0xFFFFFFFF  # 将 value 转换成 8 位无符号整数
        return value

    def ConvertToList_8bit(self, value: int, signed: bool = True):
        '''
        将输入的整数转换为8位整数列表。
        根据signed参数判断是否将其视为带符号整数。
        超出范围时给出提示。
        '''
        if signed:
            if not -128 <= value <= 127:
                raise ValueError(f"输入的值 {value} 超出了8位有符号整数的范围 [-128, 127].")
            if value < 0:
                value = (value + 0x100) & 0xFF  # 转换为8位表示
            else:
                value &= 0xFF
        else:
            if not 0 <= value <= 255:
                raise ValueError(f"输入的值 {value} 超出了8位无符号整数的范围 [0, 255].")
            value &= 0xFF
        
        return [value]
    
    def ConvertToList_int8_t(self, value: int):
        if not -128 <= value <= 127:
            raise ValueError(f"输入的值 {value} 超出了8位有符号整数的范围 [-128, 127].")
        if value < 0:
            value = (value + 0x100) & 0xFF  # 转换为8位表示
        else:
            value &= 0xFF
        return [value]
    
    def ConvertToList_uint8_t(self, value: int):
        if not 0 <= value <= 255:
            raise ValueError(f"输入的值 {value} 超出了8位无符号整数的范围 [0, 255].")
        value &= 0xFF
        return [value]

    def ConvertToList_16bit(self, value: int, signed: bool = True):
        '''
        将输入的整数转换为16位整数列表。
        根据signed参数判断是否将其视为带符号整数。
        超出范围时给出提示。
        '''
        if signed:
            if not -32768 <= value <= 32767:
                raise ValueError(f"输入的值 {value} 超出了16位有符号整数的范围 [-32768, 32767].")
            if value < 0:
                value = (value + 0x10000) & 0xFFFF  # 转换为16位表示
            else:
                value &= 0xFFFF
        else:
            if not 0 <= value <= 65535:
                raise ValueError(f"输入的值 {value} 超出了16位无符号整数的范围 [0, 65535].")
            value &= 0xFFFF

        # 将结果拆分为两个uint8值
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF

        return [high_byte, low_byte]

    def ConvertToList_int16_t(self, value: int):
        if not -32768 <= value <= 32767:
            raise ValueError(f"输入的值 {value} 超出了16位有符号整数的范围 [-32768, 32767].")
        if value < 0:
            value = (value + 0x10000) & 0xFFFF  # 转换为16位表示
        else:
            value &= 0xFFFF
        # 将结果拆分为两个uint8值
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF
        return [high_byte, low_byte]
    
    def ConvertToList_uint16_t(self, value: int):
        if not 0 <= value <= 65535:
            raise ValueError(f"输入的值 {value} 超出了16位无符号整数的范围 [0, 65535].")
        value &= 0xFFFF
        # 将结果拆分为两个uint8值
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF
        return [high_byte, low_byte]

    def ConvertToList_32bit(self, value: int, signed: bool = True):
        '''
        将输入的整数转换为32位整数列表。
        根据signed参数判断是否将其视为带符号整数。
        超出范围时给出提示。
        '''
        if signed:
            if not -2147483648 <= value <= 2147483647:
                raise ValueError(f"输入的值 {value} 超出了32位有符号整数的范围 [-2147483648, 2147483647].")
            if value < 0:
                value = (value + 0x100000000) & 0xFFFFFFFF  # 转换为32位表示
            else:
                value &= 0xFFFFFFFF
        else:
            if not 0 <= value <= 4294967295:
                raise ValueError(f"输入的值 {value} 超出了32位无符号整数的范围 [0, 4294967295].")
            value &= 0xFFFFFFFF

        # 将结果拆分为四个uint8值
        byte_3 = (value >> 24) & 0xFF
        byte_2 = (value >> 16) & 0xFF
        byte_1 = (value >> 8) & 0xFF
        byte_0 = value & 0xFF

        return [byte_3, byte_2, byte_1, byte_0]

    def ConvertToList_int32_t(self, value: int):
        if not -2147483648 <= value <= 2147483647:
            raise ValueError(f"输入的值 {value} 超出了32位有符号整数的范围 [-2147483648, 2147483647].")
        if value < 0:
            value = (value + 0x100000000) & 0xFFFFFFFF  # 转换为32位表示
        else:
            value &= 0xFFFFFFFF
        # 将结果拆分为四个uint8值
        byte_3 = (value >> 24) & 0xFF
        byte_2 = (value >> 16) & 0xFF
        byte_1 = (value >> 8) & 0xFF
        byte_0 = value & 0xFF
        return [byte_3, byte_2, byte_1, byte_0]
    
    def ConvertToList_uint32_t(self, value: int):
        if not 0 <= value <= 4294967295:
            raise ValueError(f"输入的值 {value} 超出了32位无符号整数的范围 [0, 4294967295].")
        value &= 0xFFFFFFFF
        # 将结果拆分为四个uint8值
        byte_3 = (value >> 24) & 0xFF
        byte_2 = (value >> 16) & 0xFF
        byte_1 = (value >> 8) & 0xFF
        byte_0 = value & 0xFF
        return [byte_3, byte_2, byte_1, byte_0]

    def ConvertBytesToInt(self, bytes:bytearray, first_index:int, second_index:int, byteorder:Literal["little", "big"]='big'):
        '''
        将字节串转换为int类型,默认为大端对齐
        '''
        return int.from_bytes(bytes[first_index:second_index], byteorder=byteorder)