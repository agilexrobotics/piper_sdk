#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgGripperFeedBack:
    '''
    夹爪反馈消息
    '''
    def __init__(self, grippers_angle: int=0, grippers_effort: int=0, status_code: int=0):
        """
        初始化 ArmMsgGripperFeedBack 实例。

        :param grippers_angle: 夹爪角度，以整数表示。
        :param grippers_effort: 夹爪扭矩，以整数表示。
        :param status_code: 夹爪状态码，以整数表示。
        """
        self.grippers_angle = grippers_angle
        self.grippers_effort = grippers_effort
        self._status_code = status_code
        self.foc_status = self.FOC_Status()
    
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
        """
        返回对象的字符串表示，用于打印。

        :return: 格式化的字符串表示夹爪的角度、速度和状态码。
        """
        return (f"ArmMsgGripperFeedBack(\n"
                f"  grippers_angle: {self.grippers_angle}, {self.grippers_angle * 0.001:.3f},\n"
                f"  grippers_effort: {self.grippers_effort} \t {self.grippers_effort * 0.001:.2f},\n"
                f"  status_code: \n{self.foc_status}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
