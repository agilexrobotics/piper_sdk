#!/usr/bin/env python3
# -*-coding:utf8-*-
#机械臂协议解析基类

from abc import ABC, abstractmethod
from enum import Enum, auto
import ctypes
import struct
from typing_extensions import (
    Literal,
)
import can
from typing import (
    Optional,
    Union
)
from ..piper_msgs.msg_v2 import (
    PiperMessage as PiperMessageV2,
    ArmMessageMapping as ArmMessageMappingV2
)

from ..piper_msgs.msg_v1 import (
    PiperMessage as PiperMessageV1,
    ArmMessageMapping as ArmMessageMappingV1
)

class C_PiperParserBase(ABC):
    '''
    Piper机械臂数据解析基类
    '''
    '''
    Piper Robot Arm Data Parsing Base Class
    '''
    class ProtocolVersion(Enum):
        '''
        协议版本枚举,需要在派生类中指定
        '''
        '''
        Protocol Version Enumeration, needs to be specified in the derived class.
        '''
        ARM_PROROCOL_V1 = auto()
        ARM_PROROCOL_V2 = auto()
        ARM_PROTOCOL_UNKNOWN = auto()
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
        '''
        Decode the message, converting the CAN data frame into the specified type.
        '''
        pass
    
    @abstractmethod
    def EncodeMessage(self):
        '''
        将消息转为can数据帧
        
        只将输入数据转换为can数据的id和data, 没有为can message赋值channel、dlc、is_extended_id
        '''
        '''
        Convert the message into a CAN data frame.

        This function only converts the input data into the id and data of the CAN message, without assigning values to channel, dlc, or is_extended_id for the CAN message.
        '''
        pass

    @abstractmethod
    def GetParserProtocolVersion(self):
        '''
        获取当前协议版本
        '''
        '''
        Get the current protocol version.
        '''
        pass
    
    def ConvertToNegative_8bit(self, value: int, signed:bool=True) -> int:
        '''
        将输入的整数转换为8位整数。
        输入 value 范围:[0,255]
        如果 signed 为 True,则转换为8位有符号整数。[-128, 127]
        如果 signed 为 False,则转换为8位无符号整数。[0, 255]
        '''
        '''
        Convert the input integer to an 8-bit integer.
        input value range:[0,255]
        If signed is True, it will be converted to a 32-bit signed integer. [-128, 127]
        If signed is False, it will be converted to a 32-bit unsigned integer. [0, 255]
        '''
        # 范围检查
        if not (0 <= value <= 255):
            print("Error ConvertToNegative_8bit:  Input value exceeds the range [0, 255].")
        # 转换成 8 位无符号整数
        value &= 0xFF  # 将 value 转换成 8 位无符号整数
        if signed:
            if value & 0x80:  # 检查符号位
                value -= 0x100  # 如果符号位为 1，表示负数，需要减去 2^8
        return value

    def ConvertToNegative_int8_t(value: int) -> int:
        '''
        将输入的整数转换为8位有符号整数。
        输入 value 范围:[0,255]
        return范围: [-128, 127]
        '''
        '''
        Convert the input integer to an 8-bit signed integer.
        input value range:[0,255]
        return Range: [-128, 127]
        '''
        # 范围检查
        if not (0 <= value <= 255):
            print("Error ConvertToNegative_int8_t: Input value exceeds the range [0, 255].")
        # 转换成 8 位无符号整数
        value &= 0xFF  # 将 value 转换成 8 位无符号整数
        if value & 0x80:  # 检查符号位
            value -= 0x100  # 如果符号位为 1，表示负数，需要减去 2^8
        return value

    def ConvertToNegative_uint8_t(value: int) -> int:
        '''
        将输入的整数转换为8位无符号整数。
        输入 value 范围:[0,255]
        return 范围: [0, 255]
        '''
        '''
        Convert the input integer to an 8-bit unsigned integer.
        input value range:[0,255]
        return Range: [0, 255]
        '''
        # 范围检查
        if not (0 <= value <= 255):
            print("Error ConvertToNegative_uint8_t: Input value exceeds the range [0, 255].")
        # 转换成 8 位无符号整数
        value &= 0xFF  # 将 value 转换成 8 位无符号整数
        return value

    def ConvertToNegative_16bit(self, value: int, signed:bool=True) -> int:
        '''
        将输入的整数转换为16位整数。
        输入 value 范围:[0,65535]
        如果 signed 为 True,则转换为16位有符号整数。[-32768, 32767]
        如果 signed 为 False,则转换为16位无符号整数。[0, 65535]
        '''
        '''
        Convert the input integer to a 16-bit integer.
        input value range:[0,65535]
        If signed is True, it will be converted to a 16-bit signed integer. Range: [-32768, 32767]
        If signed is False, it will be converted to a 16-bit unsigned integer. Range: [0, 65535]
        '''
        # 范围检查
        if not (0 <= value <= 65535):
            print("Error ConvertToNegative_16bit: Input value exceeds the range [0, 65535].")
        # 转换成 16 位无符号整数
        value &= 0xFFFF  # 将 value 转换成 16 位无符号整数
        if signed:
            if value & 0x8000:  # 检查符号位
                value -= 0x10000  # 如果符号位为 1，表示负数，需要减去 2^16
        return value
    
    def ConvertToNegative_int16_t(value: int) -> int:
        '''
        将输入的整数转换为16位有符号整数。
        输入 value 范围:[0,65535]
        return 范围: [-32768, 32767]
        '''
        '''
        Convert the input integer to a 16-bit signed integer.
        input value range:[0,65535]
        return Range: [-32768, 32767]
        '''
        # 范围检查
        if not (0 <= value <= 65535):
            print("Error ConvertToNegative_int16_t: Input value exceeds the range [0, 65535].")
        # 转换成 8 位无符号整数
        value &= 0xFFFF  # 将 value 转换成 8 位无符号整数
        if value & 0x8000:  # 检查符号位
            value -= 0x10000  # 如果符号位为 1，表示负数，需要减去 2^8
        return value

    def ConvertToNegative_uint16_t(value: int) -> int:
        '''
        将输入的整数转换为16位无符号整数。
        输入 value 范围:[0,65535]
        return 范围: [0, 65535]
        '''
        '''
        Convert the input integer to a 16-bit unsigned integer.
        input value range:[0,65535]
        return Range: [0, 65535]
        '''
        # 范围检查
        if not (0 <= value <= 65535):
            print("Error ConvertToNegative_uint16_t: Input value exceeds the range [0, 65535].")
        # 转换成 8 位无符号整数
        value &= 0xFFFF  # 将 value 转换成 8 位无符号整数
        return value

    def ConvertToNegative_32bit(self, value:int, signed:bool=True):
        '''
        将输入的整数转换为32位整数。
        输入 value 范围:[0,4294967295]
        如果 signed 为 True,则转换为32位有符号整数。
        如果 signed 为 False,则转换为32位无符号整数。
        '''
        '''
        Convert the input integer to a 32-bit integer.
        input value range:[0,4294967295]
        If signed is True, it will be converted to a 32-bit signed integer.
        If signed is False, it will be converted to a 32-bit unsigned integer.
        '''
        # 范围检查
        if not (0 <= value <= 4294967295):
            print("Error ConvertToNegative_32bit: Input value exceeds the range [0, 4294967295].")
        # 转换成 32 位无符号整数
        value &= 0xFFFFFFFF  # 将 value 转换成 32 位无符号整数
        if signed:
            if value & 0x80000000:  # 检查符号位
                value -= 0x100000000  # 如果符号位为 1，表示负数，需要减去 2^32
        return value
    
    def ConvertToNegative_int32_t(value: int) -> int:
        '''
        将输入的整数转换为32位有符号整数。
        输入 value 范围:[0,4294967295]
        return范围: [-2147483648, 2147483647]
        '''
        '''
        Convert the input integer to a 32-bit signed integer.
        input value range:[0,4294967295]
        return Range: [-2147483648, 2147483647].
        '''
        # 范围检查
        if not (0 <= value <= 4294967295):
            print("Error ConvertToNegative_32bit: Input value exceeds the range [0, 4294967295].")
        # 转换成 8 位无符号整数
        value &= 0xFFFFFFFF  # 将 value 转换成 8 位无符号整数
        if value & 0x80000000:  # 检查符号位
            value -= 0x100000000  # 如果符号位为 1，表示负数，需要减去 2^8
        return value

    def ConvertToNegative_uint32_t(value: int) -> int:
        '''
        将输入的整数转换为32位无符号整数。
        输入 value 范围:[0,4294967295]
        return范围: [0, 4294967295]
        '''
        '''
        Convert the input integer to a 32-bit unsigned integer.
        input value range:[0,4294967295]
        return Range: [0, 4294967295].
        '''
        # 范围检查
        if not (0 <= value <= 4294967295):
            print("Error ConvertToNegative_32bit: Input value exceeds the range [0, 4294967295].")
        # 转换成 8 位无符号整数
        value &= 0xFFFFFFFF  # 将 value 转换成 8 位无符号整数
        return value

    def ConvertToList_8bit(self, value: int, signed: bool = True):
        '''
        将输入的整数转换为8位整数列表。
        根据signed参数判断是否将其视为带符号整数。
        超出范围时给出提示。
        '''
        '''
        Convert the input integer into an 8-bit integer list.
        The signed parameter determines whether it is treated as a signed integer.
        A warning will be given if the value exceeds the allowed range.
        '''
        if signed:
            if not -128 <= value <= 127:
                raise OverflowError(f"The input value {value} exceeds the range of an 8-bit signed integer [-128, 127].")
            value = ctypes.c_int8(value).value
            return list(struct.unpack("B", struct.pack(">b", value)))
        else:
            if not 0 <= value <= 255:
                raise OverflowError(f"The input value {value} exceeds the range of an 8-bit unsigned integer [0, 255].")
            return list(struct.unpack("B", struct.pack(">B", value)))
    
    def ConvertToList_int8_t(self, value: int):
        if not -128 <= value <= 127:
            raise OverflowError(f"输入的值 {value} 超出了8位有符号整数的范围 [-128, 127].")
        if value < 0:
            value = (value + 0x100) & 0xFF  # 转换为8位表示
        else:
            value &= 0xFF
        return [value]
    
    def ConvertToList_uint8_t(self, value: int):
        if not 0 <= value <= 255:
            raise OverflowError(f"输入的值 {value} 超出了8位无符号整数的范围 [0, 255].")
        value &= 0xFF
        return [value]

    def ConvertToList_16bit(self, value: int, signed: bool = True):
        '''
        将输入的整数转换为16位整数列表。
        根据signed参数判断是否将其视为带符号整数。
        超出范围时给出提示。
        '''
        '''
        Convert the input integer into a 16-bit integer list.
        The signed parameter determines whether it is treated as a signed integer.
        A warning will be given if the value exceeds the allowed range.
        '''
        if signed:
            if not -32768 <= value <= 32767:
                raise OverflowError(f"The input value {value} exceeds the range of a 16-bit signed integer [-32768, 32767].")
            value = ctypes.c_int16(value).value
            return list(struct.unpack("BB", struct.pack(">h", value)))
        else:
            if not 0 <= value <= 65535:
                raise OverflowError(f"The input value {value} exceeds the range of a 16-bit unsigned integer [0, 65535].")
            return list(struct.unpack("BB", struct.pack(">H", value)))

    def ConvertToList_int16_t(self, value: int):
        if not -32768 <= value <= 32767:
            raise OverflowError(f"输入的值 {value} 超出了16位有符号整数的范围 [-32768, 32767].")
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
            raise OverflowError(f"输入的值 {value} 超出了16位无符号整数的范围 [0, 65535].")
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
        '''
        Convert the input integer into a 32-bit integer list.
        The signed parameter determines whether it is treated as a signed integer.
        A warning will be given if the value exceeds the allowed range.
        '''
        if signed:
            if not -2147483648 <= value <= 2147483647:
                raise OverflowError(f"The input value {value} exceeds the range of a 32-bit signed integer [-2147483648, 2147483647].")
            value = ctypes.c_int32(value).value
            return list(struct.unpack("BBBB", struct.pack(">i", value)))
        else:
            if not 0 <= value <= 4294967295:
                raise OverflowError(f"The input value {value} exceeds the range of a 32-bit unsigned integer [0, 4294967295].")
            return list(struct.unpack("BBBB", struct.pack(">I", value)))

    def ConvertToList_int32_t(self, value: int):
        if not -2147483648 <= value <= 2147483647:
            raise OverflowError(f"输入的值 {value} 超出了32位有符号整数的范围 [-2147483648, 2147483647].")
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
            raise OverflowError(f"输入的值 {value} 超出了32位无符号整数的范围 [0, 4294967295].")
        value &= 0xFFFFFFFF
        # 将结果拆分为四个uint8值
        byte_3 = (value >> 24) & 0xFF
        byte_2 = (value >> 16) & 0xFF
        byte_1 = (value >> 8) & 0xFF
        byte_0 = value & 0xFF
        return [byte_3, byte_2, byte_1, byte_0]

    def FloatToUint(self,x_float:float, x_min:float, x_max:float, bits:int):
        '''
        浮点数转换为无符号整数
        用在mit模式透传控制单独关节电机驱动器模式
        '''
        '''
        Convert floating point number to unsigned integer
        Used in MIT mode pass-through control for individual joint motor driver mode
        '''
        span:float = x_max - x_min
        offset:float = x_min
        return int((x_float - offset) * (float((1<<bits)-1))/span)
    
    def ConvertBytesToInt(self, bytes:bytearray, first_index:int, second_index:int, byteorder:Literal["little", "big"]='big'):
        '''
        将字节串转换为int类型,默认为大端对齐
        '''
        '''
        Convert a byte string to an int type, with big-endian byte order by default.
        '''
        return int.from_bytes(bytes[first_index:second_index], byteorder=byteorder)
    
    #-------------------------------反馈-------------------------------------------

    PiperMessageType = Union[PiperMessageV1, PiperMessageV2]

    def _set_type(self, can_id, msg: PiperMessageType, version):
        mapping_cls = globals().get(f"ArmMessageMapping{version.upper()}", None)
        if mapping_cls:
            msg.type_ = mapping_cls.get_mapping(can_id=can_id)
    
    # 机械臂状态反馈,piper Status Feedback
    def ARM_STATUS_FEEDBACK(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_status_msgs.ctrl_mode = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
        msg.arm_status_msgs.arm_status = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,1,2),False)
        msg.arm_status_msgs.mode_feed = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,2,3),False)
        msg.arm_status_msgs.teach_status = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,3,4),False)
        msg.arm_status_msgs.motion_status = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5),False)
        msg.arm_status_msgs.trajectory_num = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
        msg.arm_status_msgs.err_code = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)

    # 机械臂末端位姿,piper End-Effector Pose
    def ARM_END_POSE_FEEDBACK_X_Y(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_end_pose.X_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_end_pose.Y_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    def ARM_END_POSE_FEEDBACK_Z_RX(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_end_pose.Z_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_end_pose.RX_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    def ARM_END_POSE_FEEDBACK_RY_RZ(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_end_pose.RY_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_end_pose.RZ_axis = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    # 关节角度反馈,Joint Angle Feedback
    def ARM_JOINT_FEEDBACK_12(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_joint_feedback.joint_1 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_joint_feedback.joint_2 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    def ARM_JOINT_FEEDBACK_34(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_joint_feedback.joint_3 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_joint_feedback.joint_4 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    def ARM_JOINT_FEEDBACK_56(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_joint_feedback.joint_5 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_joint_feedback.joint_6 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    # 夹爪反馈,Gripper Feedback
    def ARM_GRIPPER_FEEDBACK(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.gripper_feedback.grippers_angle = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.gripper_feedback.grippers_effort = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,4,6))
        msg.gripper_feedback.status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,6,7),False)

    # 驱动器信息高速反馈,High-Speed Driver Information Feedback
    def ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR1(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_high_spd_feedback_1.can_id = can_id
        msg.arm_high_spd_feedback_1.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
        msg.arm_high_spd_feedback_1.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_high_spd_feedback_1.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
    
    def ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR2(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_high_spd_feedback_2.can_id = can_id
        msg.arm_high_spd_feedback_2.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
        msg.arm_high_spd_feedback_2.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_high_spd_feedback_2.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    def ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR3(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_high_spd_feedback_3.can_id = can_id
        msg.arm_high_spd_feedback_3.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
        msg.arm_high_spd_feedback_3.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_high_spd_feedback_3.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    def ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR4(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_high_spd_feedback_4.can_id = can_id
        msg.arm_high_spd_feedback_4.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
        msg.arm_high_spd_feedback_4.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_high_spd_feedback_4.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    def ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR5(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_high_spd_feedback_5.can_id = can_id
        msg.arm_high_spd_feedback_5.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
        msg.arm_high_spd_feedback_5.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_high_spd_feedback_5.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    def ARM_INFO_HIGH_SPD_FEEDBACK_MOTOR6(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_high_spd_feedback_6.can_id = can_id
        msg.arm_high_spd_feedback_6.motor_speed = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2))
        msg.arm_high_spd_feedback_6.current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_high_spd_feedback_6.pos = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))

    # 驱动器信息低速反馈,Low-Speed Driver Information Feedback
    def ARM_INFO_LOW_SPD_FEEDBACK_MOTOR1(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_low_spd_feedback_1.can_id = can_id
        msg.arm_low_spd_feedback_1.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
        msg.arm_low_spd_feedback_1.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_low_spd_feedback_1.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
        msg.arm_low_spd_feedback_1.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
        msg.arm_low_spd_feedback_1.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)

    def ARM_INFO_LOW_SPD_FEEDBACK_MOTOR2(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_low_spd_feedback_2.can_id = can_id
        msg.arm_low_spd_feedback_2.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
        msg.arm_low_spd_feedback_2.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_low_spd_feedback_2.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
        msg.arm_low_spd_feedback_2.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
        msg.arm_low_spd_feedback_2.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)

    def ARM_INFO_LOW_SPD_FEEDBACK_MOTOR3(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_low_spd_feedback_3.can_id = can_id
        msg.arm_low_spd_feedback_3.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
        msg.arm_low_spd_feedback_3.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_low_spd_feedback_3.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
        msg.arm_low_spd_feedback_3.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
        msg.arm_low_spd_feedback_3.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)

    def ARM_INFO_LOW_SPD_FEEDBACK_MOTOR4(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_low_spd_feedback_4.can_id = can_id
        msg.arm_low_spd_feedback_4.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
        msg.arm_low_spd_feedback_4.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_low_spd_feedback_4.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
        msg.arm_low_spd_feedback_4.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
        msg.arm_low_spd_feedback_4.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)

    def ARM_INFO_LOW_SPD_FEEDBACK_MOTOR5(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_low_spd_feedback_5.can_id = can_id
        msg.arm_low_spd_feedback_5.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
        msg.arm_low_spd_feedback_5.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_low_spd_feedback_5.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
        msg.arm_low_spd_feedback_5.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
        msg.arm_low_spd_feedback_5.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
    
    def ARM_INFO_LOW_SPD_FEEDBACK_MOTOR6(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_low_spd_feedback_6.can_id = can_id
        msg.arm_low_spd_feedback_6.vol = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
        msg.arm_low_spd_feedback_6.foc_temp = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4))
        msg.arm_low_spd_feedback_6.motor_temp = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5))
        msg.arm_low_spd_feedback_6.foc_status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
        msg.arm_low_spd_feedback_6.bus_current = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
    
    def ARM_FEEDBACK_CURRENT_MOTOR_ANGLE_LIMIT_MAX_SPD(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_feedback_current_motor_angle_limit_max_spd.motor_num = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
        msg.arm_feedback_current_motor_angle_limit_max_spd.max_angle_limit = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,1,3))
        msg.arm_feedback_current_motor_angle_limit_max_spd.min_angle_limit = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,3,5))
        msg.arm_feedback_current_motor_angle_limit_max_spd.max_joint_spd = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,5,7),False)
    
    def ARM_FEEDBACK_CURRENT_END_VEL_ACC_PARAM(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_feedback_current_end_vel_acc_param.end_max_linear_vel = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,0,2),False)
        msg.arm_feedback_current_end_vel_acc_param.end_max_angular_vel = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,2,4),False)
        msg.arm_feedback_current_end_vel_acc_param.end_max_linear_acc = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,4,6),False)
        msg.arm_feedback_current_end_vel_acc_param.end_max_angular_acc = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,6,8),False)
    
    def ARM_CRASH_PROTECTION_RATING_FEEDBACK(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_crash_protection_rating_feedback.joint_1_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
        msg.arm_crash_protection_rating_feedback.joint_2_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,1,2),False)
        msg.arm_crash_protection_rating_feedback.joint_3_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,2,3),False)
        msg.arm_crash_protection_rating_feedback.joint_4_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,3,4),False)
        msg.arm_crash_protection_rating_feedback.joint_5_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5),False)
        msg.arm_crash_protection_rating_feedback.joint_6_protection_level = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,5,6),False)
    
    def ARM_FEEDBACK_CURRENT_MOTOR_MAX_ACC_LIMIT(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_feedback_current_motor_max_acc_limit.joint_motor_num = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
        msg.arm_feedback_current_motor_max_acc_limit.max_joint_acc = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,1,3),False)
    
    # 机械臂控制指令2,0x151
    def ARM_MOTION_CTRL_2(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_motion_ctrl_2.ctrl_mode = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
        msg.arm_motion_ctrl_2.move_mode = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,1,2),False)
        msg.arm_motion_ctrl_2.move_spd_rate_ctrl = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,2,3),False)
        msg.arm_motion_ctrl_2.mit_mode = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,3,4),False)
        msg.arm_motion_ctrl_2.residence_time = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,4,5),False)
    
    # 读取主臂发送的目标joint数值
    def ARM_JOINT_CTRL_12(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_joint_ctrl.joint_1 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_joint_ctrl.joint_2 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
    
    def ARM_JOINT_CTRL_34(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_joint_ctrl.joint_3 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_joint_ctrl.joint_4 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
    
    def ARM_JOINT_CTRL_56(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_joint_ctrl.joint_5 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_joint_ctrl.joint_6 = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,4,8))
    
    # 夹爪
    def ARM_GRIPPER_CTRL(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_gripper_ctrl.grippers_angle = self.ConvertToNegative_32bit(self.ConvertBytesToInt(can_data,0,4))
        msg.arm_gripper_ctrl.grippers_effort = self.ConvertToNegative_16bit(self.ConvertBytesToInt(can_data,4,6))
        msg.arm_gripper_ctrl.status_code = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,6,7),False)
        msg.arm_gripper_ctrl.set_zero = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,7,8),False)
    
    # 固件版本
    def ARM_FIRMWARE_READ(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.firmware_data = can_data
    
    # 夹爪/示教器参数反馈指令(基于V1.5-2版本后)
    def ARM_GRIPPER_TEACHING_PENDANT_PARAM_FEEDBACK(self, can_id, can_data, msg:PiperMessageType, version):
        self._set_type(can_id, msg, version)
        msg.arm_gripper_teaching_param_feedback.teaching_range_per = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,0,1),False)
        msg.arm_gripper_teaching_param_feedback.max_range_config = self.ConvertToNegative_8bit(self.ConvertBytesToInt(can_data,1,2),False)

    #-------------------------------控制-------------------------------------------
    def _encode_set_type(self, msg_type_, tx_can_frame: Optional[can.Message], msg:PiperMessageType, version):
        mapping_cls = globals().get(f"ArmMessageMapping{version.upper()}", None)
        if mapping_cls:
            # 获取对应的 arbitration_id 并设置
            tx_can_frame.arbitration_id = mapping_cls.get_mapping(msg_type=msg_type_)

    def PiperMsgMotionCtrl_1(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motion_ctrl_1.emergency_stop,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_1.track_ctrl,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_1.grag_teach_ctrl,False) + \
                            [0x00, 0x00, 0x00, 0x00, 0x00]
    def PiperMsgMotionCtrl_2_V1(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motion_ctrl_2.ctrl_mode,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_2.move_mode,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_2.move_spd_rate_ctrl,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_2.mit_mode,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_2.residence_time,False) + \
                            [0x00, 0x00, 0x00]
    def PiperMsgMotionCtrl_2_V2(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motion_ctrl_2.ctrl_mode,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_2.move_mode,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_2.move_spd_rate_ctrl,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_2.mit_mode,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_2.residence_time,False) + \
                            self.ConvertToList_8bit(msg.arm_motion_ctrl_2.installation_pos,False) + \
                            [0x00, 0x00]
    def PiperMsgMotionCtrlCartesian_1(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.X_axis) + \
                            self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.Y_axis)
    def PiperMsgMotionCtrlCartesian_2(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.Z_axis) + \
                            self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.RX_axis)
    def PiperMsgMotionCtrlCartesian_3(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.RY_axis) + \
                            self.ConvertToList_32bit(msg.arm_motion_ctrl_cartesian.RZ_axis)
    def PiperMsgJointCtrl_12(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_1) + \
                            self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_2)
    def PiperMsgJointCtrl_34(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_3) + \
                            self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_4)
    def PiperMsgJointCtrl_56(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_5) + \
                            self.ConvertToList_32bit(msg.arm_joint_ctrl.joint_6)
    def PiperMsgCircularPatternCoordNumUpdateCtrl(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_circular_ctrl.instruction_num,False) + \
                            [0, 0, 0, 0, 0, 0, 0]
    def PiperMsgGripperCtrl(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_32bit(msg.arm_gripper_ctrl.grippers_angle) + \
                            self.ConvertToList_16bit(msg.arm_gripper_ctrl.grippers_effort,False) + \
                            self.ConvertToList_8bit(msg.arm_gripper_ctrl.status_code,False) + \
                            self.ConvertToList_8bit(msg.arm_gripper_ctrl.set_zero,False)
    def PiperMsgMasterSlaveModeConfig(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_ms_config.linkage_config,False) + \
                            self.ConvertToList_8bit(msg.arm_ms_config.feedback_offset,False) + \
                            self.ConvertToList_8bit(msg.arm_ms_config.ctrl_offset,False) + \
                            self.ConvertToList_8bit(msg.arm_ms_config.linkage_offset,False) + \
                            [0, 0, 0, 0]
    def PiperMsgMotorEnableDisableConfig(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motor_enable.motor_num,False) + \
                            self.ConvertToList_8bit(msg.arm_motor_enable.enable_flag,False) + \
                            [0, 0, 0, 0, 0, 0]
    def PiperMsgSearchMotorMaxAngleSpdAccLimit(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_search_motor_max_angle_spd_acc_limit.motor_num,False) + \
                            self.ConvertToList_8bit(msg.arm_search_motor_max_angle_spd_acc_limit.search_content,False) + \
                            [0, 0, 0, 0, 0, 0]
    def PiperMsgMotorAngleLimitMaxSpdSet(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_motor_angle_limit_max_spd_set.motor_num,False) + \
                            self.ConvertToList_16bit(msg.arm_motor_angle_limit_max_spd_set.max_angle_limit) + \
                            self.ConvertToList_16bit(msg.arm_motor_angle_limit_max_spd_set.min_angle_limit) + \
                            self.ConvertToList_16bit(msg.arm_motor_angle_limit_max_spd_set.max_joint_spd,False) + \
                            [0]
    def PiperMsgJointConfig(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_joint_config.joint_motor_num,False) + \
                            self.ConvertToList_8bit(msg.arm_joint_config.set_motor_current_pos_as_zero,False) + \
                            self.ConvertToList_8bit(msg.arm_joint_config.acc_param_config_is_effective_or_not,False) + \
                            self.ConvertToList_16bit(msg.arm_joint_config.max_joint_acc,False) + \
                            self.ConvertToList_8bit(msg.arm_joint_config.clear_joint_err,False) + \
                            [0, 0]
    def PiperMsgInstructionResponseConfig(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_set_instruction_response.instruction_index,False) + \
                            self.ConvertToList_8bit(msg.arm_set_instruction_response.zero_config_success_flag,False) + \
                            [0, 0, 0, 0, 0, 0]
    def PiperMsgParamEnquiryAndConfig(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.param_enquiry,False) + \
                            self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.param_setting,False) + \
                            self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.data_feedback_0x48x,False) + \
                            self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.end_load_param_setting_effective,False) + \
                            self.ConvertToList_8bit(msg.arm_param_enquiry_and_config.set_end_load,False) + \
                            [0, 0, 0]
    def PiperMsgEndVelAccParamConfig(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_16bit(msg.arm_end_vel_acc_config.end_max_linear_vel,False) + \
                            self.ConvertToList_16bit(msg.arm_end_vel_acc_config.end_max_angular_vel,False) + \
                            self.ConvertToList_16bit(msg.arm_end_vel_acc_config.end_max_linear_acc,False) + \
                            self.ConvertToList_16bit(msg.arm_end_vel_acc_config.end_max_angular_acc,False)
    def PiperMsgCrashProtectionRatingConfig(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_1_protection_level,False) + \
                            self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_2_protection_level,False) + \
                            self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_3_protection_level,False) + \
                            self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_4_protection_level,False) + \
                            self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_5_protection_level,False) + \
                            self.ConvertToList_8bit(msg.arm_crash_protection_rating_config.joint_6_protection_level,False) + \
                            [0, 0]
    def PiperMsgGripperTeachingPendantParamConfig(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_8bit(msg.arm_gripper_teaching_param_config.teaching_range_per,False) + \
                            self.ConvertToList_8bit(msg.arm_gripper_teaching_param_config.max_range_config,False) + \
                            [0, 0, 0, 0, 0, 0]
    # 机械臂MIT单独控制电机
    def PiperMsgJointMitCtrl(self, msg_type_, msg:PiperMessageType, tx_can_frame: Optional[can.Message], version):
        self._encode_set_type(msg_type_, tx_can_frame, msg, version)
        tx_can_frame.data = self.ConvertToList_16bit(msg.arm_joint_mit_ctrl.pos_ref,False) + \
                            self.ConvertToList_8bit(((msg.arm_joint_mit_ctrl.vel_ref >> 4)&0xFF),False) + \
                            self.ConvertToList_8bit(((((msg.arm_joint_mit_ctrl.vel_ref&0xF)<<4)&0xF0) | 
                                                        ((msg.arm_joint_mit_ctrl.kp>>8)&0x0F)),False) + \
                            self.ConvertToList_8bit(msg.arm_joint_mit_ctrl.kp&0xFF,False) + \
                            self.ConvertToList_8bit((msg.arm_joint_mit_ctrl.kd>>4)&0xFF,False) + \
                            self.ConvertToList_8bit(((((msg.arm_joint_mit_ctrl.kd&0xF)<<4)&0xF0)|
                                                        ((msg.arm_joint_mit_ctrl.t_ref>>4)&0x0F)),False)
        crc = (tx_can_frame.data[0]^tx_can_frame.data[1]^tx_can_frame.data[2]^tx_can_frame.data[3]^tx_can_frame.data[4]^tx_can_frame.data[5]^ \
            tx_can_frame.data[6])&0x0F
        msg.arm_joint_mit_ctrl.crc = crc
        tx_can_frame.data = tx_can_frame.data + self.ConvertToList_8bit((((msg.arm_joint_mit_ctrl.t_ref<<4)&0xF0) | crc),False)
