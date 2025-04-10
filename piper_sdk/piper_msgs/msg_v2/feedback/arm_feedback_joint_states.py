#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgFeedBackJointStates():
    '''
    msg_v2_feedback
    
    机械臂关节角度反馈,单位0.001度
    
    CAN ID: 
        0x2A5、0x2A6、0x2A7
    
    Args:
        joint_1: 关节1反馈角度
        joint_2: 关节2反馈角度
        joint_3: 关节3反馈角度
        joint_4: 关节4反馈角度
        joint_5: 关节5反馈角度
        joint_6: 关节6反馈角度
    '''
    '''
    msg_v2_feedback
    
    Joint Angle Feedback for Robotic Arm, in 0.001 Degrees
    
    CAN ID: 
        0x2A5、0x2A6、0x2A7
    
    Args:
        joint_1: Feedback angle of joint 1, in 0.001 degrees.
        joint_2: Feedback angle of joint 2, in 0.001 degrees.
        joint_3: Feedback angle of joint 3, in 0.001 degrees.
        joint_4: Feedback angle of joint 4, in 0.001 degrees.
        joint_5: Feedback angle of joint 5, in 0.001 degrees.
        joint_6: Feedback angle of joint 6, in 0.001 degrees.
    '''
    def __init__(self, 
                 joint_1: int = 0, 
                 joint_2: int = 0, 
                 joint_3: int = 0, 
                 joint_4: int = 0, 
                 joint_5: int = 0, 
                 joint_6: int = 0):
        self.joint_1 = joint_1
        self.joint_2 = joint_2
        self.joint_3 = joint_3
        self.joint_4 = joint_4
        self.joint_5 = joint_5
        self.joint_6 = joint_6

    def __str__(self):
        # 将角度乘以0.001，并保留三位小数
        joint_angles = [
            ("Joint 1", self.joint_1),
            ("Joint 2", self.joint_2),
            ("Joint 3", self.joint_3),
            ("Joint 4", self.joint_4),
            ("Joint 5", self.joint_5),
            ("Joint 6", self.joint_6)
        ]

        # 生成格式化字符串，保留三位小数
        formatted_angles = "\n".join([f"{name}:{angle}" for name, angle in joint_angles])
        
        return f"ArmMsgFeedBackJointStates:\n{formatted_angles}"
    
    def __repr__(self):
        return self.__str__()