#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgEndVelAccParamConfig:
    '''
    msg_v2_transmit
    
    末端速度/加速度参数设置指令
    
    CAN ID:
        0x479

    Args:
        end_max_linear_vel: 末端最大线速度,0x7FFF为设定无效数值
        end_max_angular_vel: 末端最大角速度,0x7FFF为设定无效数值
        end_max_linear_acc: 末端最大线加速度,0x7FFF为设定无效数值
        end_max_angular_acc: 末端最大角加速度,0x7FFF为设定无效数值
    
    位描述:
    
        Byte 0: 末端最大线速度 H, uint16, 单位 0.001m/s, (基于V1.5-2版本后增加无效数值0x7FFF)
        Byte 1: 末端最大线速度 L,
        Byte 2: 末端最大角速度 H, uint16, 单位 0.001rad/s, (基于V1.5-2版本后增加无效数值0x7FFF)
        Byte 3: 末端最大角速度 L,
        Byte 4: 末端最大线加速度 H, uint16, 单位 0.001m/s^2, (基于V1.5-2版本后增加无效数值0x7FFF)
        Byte 5: 末端最大线加速度 L
        Byte 6: 末端最大角加速度 H, uint16, 单位 0.001rad/s^2, (基于V1.5-2版本后增加无效数值0x7FFF)
        Byte 7: 末端最大角加速度 L
    '''
    '''
    msg_v2_transmit
    
    End Effector Speed/Acceleration Parameter Setting Command

    CAN ID:
        0x479

    Args:
        end_max_linear_vel: Maximum linear velocity of the end effector.0x7FFF is defined as the invalid value.
        end_max_angular_vel: Maximum angular velocity of the end effector.0x7FFF is defined as the invalid value.
        end_max_linear_acc: Maximum linear acceleration of the end effector.0x7FFF is defined as the invalid value.
        end_max_angular_acc: Maximum angular acceleration of the end effector.0x7FFF is defined as the invalid value.

    Bit Description:

        Byte 0: High byte of maximum linear velocity, uint16, unit: 0.001m/s.(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
        Byte 1: Low byte of maximum linear velocity.
        Byte 2: High byte of maximum angular velocity, uint16, unit: 0.001rad/s.(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
        Byte 3: Low byte of maximum angular velocity.
        Byte 4: High byte of maximum linear acceleration, uint16, unit: 0.001m/s².(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
        Byte 5: Low byte of maximum linear acceleration.
        Byte 6: High byte of maximum angular acceleration, uint16, unit: 0.001rad/s².(Based on version V1.5-2 and later, the invalid value 0x7FFF is added.)
        Byte 7: Low byte of maximum angular acceleration.
    '''
    def __init__(self, 
                 end_max_linear_vel: int = 0, 
                 end_max_angular_vel: int = 0, 
                 end_max_linear_acc: int = 0,
                 end_max_angular_acc: int = 0
                 ):
        self.end_max_linear_vel = end_max_linear_vel
        self.end_max_angular_vel = end_max_angular_vel
        self.end_max_linear_acc = end_max_linear_acc
        self.end_max_angular_acc = end_max_angular_acc

    def __str__(self):
        return (f"ArmMsgEndVelAccParamConfig(\n"
                f"  end_max_linear_vel: {self.end_max_linear_vel * 0.001:.3f},\n"
                f"  end_max_angular_vel: {self.end_max_angular_vel * 0.001:.3f},\n"
                f"  end_max_linear_acc: {self.end_max_linear_acc * 0.001:.3f},\n"
                f"  end_max_angular_acc: {self.end_max_angular_acc * 0.001:.3f}\n"
                f")")

    def __repr__(self):
        return self.__str__()
