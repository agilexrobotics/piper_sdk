#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgJointCtrl():
    '''
    机械臂腕部关节控制
    '''
    def __init__(self, joint_1: int=0, joint_2: int=0, 
                 joint_3: int=0, joint_4: int=0, 
                 joint_5: int=0, joint_6: int=0):
        self.joint_1 = joint_1
        self.joint_2 = joint_2
        self.joint_3 = joint_3
        self.joint_4 = joint_4
        self.joint_5 = joint_5
        self.joint_6 = joint_6

    def __str__(self):
        # 将角度乘以0.001，并保留三位小数
        joint_angles = [
            ("Joint_1", self.joint_1 * 0.001),
            ("Joint_2", self.joint_2 * 0.001),
            ("Joint_3", self.joint_3 * 0.001),
            ("Joint_4", self.joint_4 * 0.001),
            ("Joint_5", self.joint_5 * 0.001),
            ("Joint_6", self.joint_6 * 0.001)
        ]

        # 生成格式化字符串，保留三位小数
        formatted_angles = "\n".join([f"{name}: {angle:.3f}" for name, angle in joint_angles])
        
        return f"ArmMsgJointCtrl:\n{formatted_angles}"
    
    def __repr__(self):
        return self.__str__()