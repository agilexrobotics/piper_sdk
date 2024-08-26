#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgEndVelAccParamConfig:
    '''
    末端速度/加速度参数设置指令
    
    0x479

    :Byte 0: 末端最大线速度 H, uint16, 单位 0.001m/s
    :Byte 1: 末端最大线速度 L,
    :Byte 2: 末端最大角速度 H, uint16, 单位 0.001rad/s
    :Byte 3: 末端最大角速度 L,
    :Byte 4: 末端最大线加速度 H, uint16, 单位 0.001m/s^2
    :Byte 5: 末端最大线加速度 L
    :Byte 6: 末端最大角加速度 H, uint16, 单位 0.001rad/s^2
    :Byte 7: 末端最大角加速度 L
    '''
    def __init__(self, 
                 end_max_linear_vel:int=0, 
                 end_max_angular_vel:int=0, 
                 end_max_linear_acc: int=0,
                 end_max_angular_acc: int=0
                 ):
        """
        初始化 ArmMsgEndVelAccParamConfig 实例。

        末端速度/加速度参数设置指令
    
        0x479

        :Byte 0: 末端最大线速度 H, uint16, 单位 0.001m/s
        :Byte 1: 末端最大线速度 L,
        :Byte 2: 末端最大角速度 H, uint16, 单位 0.001rad/s
        :Byte 3: 末端最大角速度 L,
        :Byte 4: 末端最大线加速度 H, uint16, 单位 0.001m/s^2
        :Byte 5: 末端最大线加速度 L
        :Byte 6: 末端最大角加速度 H, uint16, 单位 0.001rad/s^2
        :Byte 7: 末端最大角加速度 L
        """
        self.end_max_linear_vel = end_max_linear_vel
        self.end_max_angular_vel = end_max_angular_vel
        self.end_max_linear_acc = end_max_linear_acc
        self.end_max_angular_acc = end_max_angular_acc

    def __str__(self):
        """
        返回对象的字符串表示，用于打印。
        """
        return (f"ArmMsgEndVelAccParamConfig(\n"
                f"  end_max_linear_vel: {self.end_max_linear_vel * 0.001:.3f},\n"
                f"  end_max_angular_vel: {self.end_max_angular_vel * 0.001:.3f},\n"
                f"  end_max_linear_acc: {self.end_max_linear_acc * 0.001:.3f},\n"
                f"  end_max_angular_acc: {self.end_max_angular_acc * 0.001:.3f}\n"
                f")")

    def __repr__(self):
        """
        返回对象的正式字符串表示，通常用于调试。

        :return: 对象的字符串表示，与 __str__ 相同。
        """
        return self.__str__()
