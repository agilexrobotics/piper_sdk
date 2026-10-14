#!/usr/bin/env python3
# -*-coding:utf8-*-

from enum import unique

from ...core import IntEnumBase

class ArmMsgFeedbackGripperEnums_V3():
    @unique
    class CtrlMode(IntEnumBase):
        WIDTH = 0x00
        ANGLE = 0x01
        UNKNOWN = 0xFF

class ArmMsgFeedBackGripper_V3():
    '''
    msg_v3_feedback

    夹爪反馈消息

    CAN ID:
        0x2A8

    Args:
        grippers_val: 夹爪反馈数值, 以整数表示, 单位0.001 mm 或者 0.001 degree
        grippers_effort: 夹爪扭矩, 以整数表示, 单位 0.001N·m
        status_code: 夹爪状态码, 以整数表示
        mode: 夹爪控制模式, 0为行程, 1为角度

    位描述:

        Byte 0: 夹爪行程最高位, int32, 单位0.001 mm 或者 0.001 degree
        Byte 1:
        Byte 2:
        Byte 3:
        Byte 4: 夹爪扭矩 H, int16, 单位 0.001N·m
        Byte 5: 夹爪扭矩 L
        Byte 6: 状态码, uint8
            bit[0]      电源电压是否过低(0:正常 1:过低)
            bit[1]      电机是否过温(0:正常 1:过温)
            bit[2]      驱动器是否过流(0:正常 1:过流)
            bit[3]      驱动器是否过温(0:正常 1:过温)
            bit[4]      传感器状态(0:正常 1:异常)
            bit[5]      驱动器错误状态(0:正常 1:错误)
            bit[6]      驱动器使能状态(1:使能 0:失能)
            bit[7]      回零状态(0:没有回零 1:已经回零,或已经回过零)
        Byte 7: 夹爪控制模式, uint8
            0x00: 行程控制模式(默认)
            0x01: 角度控制模式
    '''
    '''
    msg_v3_feedback

    Gripper Feedback Message

    CAN ID:
        0x2A8

    Args:
        grippers_val: The gripper feedback value, represented as an integer. Unit is 0.001 mm in width mode or 0.001 degree in angle mode.
        grippers_effort: The torque of the gripper, represented as an integer.
        status_code: The status code of the gripper, represented as an integer.
        mode: The gripper control mode. 0x00 means width mode, 0x01 means angle mode.

    Bit Definitions:

        Byte Definitions:
        Byte 0: Gripper Value (Most Significant Byte), int32, unit: 0.001 mm or 0.001 degree
        Byte 1: Gripper Value (Second Most Significant Byte)
        Byte 2: Gripper Value (Second Least Significant Byte)
        Byte 3: Gripper Value (Least Significant Byte)
        Byte 4: Gripper Torque (High Byte), int16, unit: 0.001 N·m
        Byte 5: Gripper Torque (Low Byte)
        Byte 6: Status Code, uint8:
            bit[0]: Power voltage low (0: Normal, 1: Low)
            bit[1]: Motor over-temperature (0: Normal, 1: Over-temperature)
            bit[2]: Driver over-current (0: Normal, 1: Over-current)
            bit[3]: Driver over-temperature (0: Normal, 1: Over-temperature)
            bit[4]: Sensor status (0: Normal, 1: Abnormal)
            bit[5]: Driver error status (0: Normal, 1: Error)
            bit[6]: Driver enable status (1: Enabled, 0: Disabled)
            bit[7]: Zeroing status (0: Not zeroed, 1: Zeroed or previously zeroed)
        Byte 7: Control Mode, uint8:
            0x00: Width control mode (default)
            0x01: Angle control mode
    '''
    def __init__(self,
                 grippers_val: int = 0,
                 grippers_effort: int = 0,
                 status_code: int = 0,
                 mode: int = 0x00):
        self.grippers_val = grippers_val
        self.grippers_effort = grippers_effort
        self.foc_status = self.FOC_Status()
        self.status_code = status_code
        self._mode:ArmMsgFeedbackGripperEnums_V3.CtrlMode = ArmMsgFeedbackGripperEnums_V3.CtrlMode.match_value(mode)
        self.mode = self._mode

    @property
    def mode(self) -> ArmMsgFeedbackGripperEnums_V3.CtrlMode:
        return self._mode
    @mode.setter
    def mode(self, value:int):
        if isinstance(value, ArmMsgFeedbackGripperEnums_V3.CtrlMode):
            self._mode = value
        else:
            self._mode = ArmMsgFeedbackGripperEnums_V3.CtrlMode.match_value(value)

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
    def status_code(self):
        return self._status_code

    @status_code.setter
    def status_code(self, value: int):
        if not (0 <= value < 2**8):
            raise ValueError("status_code must be an 8-bit integer between 0 and 255.")
        self._status_code = value
        # Update foc_status based on the status_code bits
        self.foc_status.voltage_too_low = bool(value & (1 << 0))
        self.foc_status.motor_overheating = bool(value & (1 << 1))
        self.foc_status.driver_overcurrent = bool(value & (1 << 2))
        self.foc_status.driver_overheating = bool(value & (1 << 3))
        self.foc_status.sensor_status = bool(value & (1 << 4))
        self.foc_status.driver_error_status = bool(value & (1 << 5))
        self.foc_status.driver_enable_status = bool(value & (1 << 6))
        self.foc_status.homing_status = bool(value & (1 << 7))

    def __str__(self):
        return (f"ArmMsgFeedBackGripper(\n"
                f"  grippers_val: {self.grippers_val}, {self.grippers_val * 0.001:.3f},\n"
                f"  grippers_effort: {self.grippers_effort} \t {self.grippers_effort * 0.001:.3f},\n"
                f"  status_code: \n{self.foc_status},\n"
                f"  mode: \n{self.mode}\n"
                f")")

    def __repr__(self):
        return self.__str__()
