#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgFeedBackIKJointStates():
    '''
    msg_v3_feedback

    IK Joint Angle Feedback for Piper Arm, in 0.001 Degrees

    CAN ID:
        0x2AA、0x2AB、0x2AC

    Args:
        ik_joint_1: Feedback ik angle of joint 1, in 0.001 degrees.
        ik_joint_2: Feedback ik angle of joint 2, in 0.001 degrees.
        ik_joint_3: Feedback ik angle of joint 3, in 0.001 degrees.
        ik_joint_4: Feedback ik angle of joint 4, in 0.001 degrees.
        ik_joint_5: Feedback ik angle of joint 5, in 0.001 degrees.
        ik_joint_6: Feedback ik angle of joint 6, in 0.001 degrees.
    '''
    def __init__(self,
                 ik_joint_1: int = 0,
                 ik_joint_2: int = 0,
                 ik_joint_3: int = 0,
                 ik_joint_4: int = 0,
                 ik_joint_5: int = 0,
                 ik_joint_6: int = 0):
        self.ik_joint_1 = ik_joint_1
        self.ik_joint_2 = ik_joint_2
        self.ik_joint_3 = ik_joint_3
        self.ik_joint_4 = ik_joint_4
        self.ik_joint_5 = ik_joint_5
        self.ik_joint_6 = ik_joint_6

    def __str__(self):
        # 将角度乘以0.001，并保留三位小数
        joint_angles = [
            ("IK Joint 1", self.ik_joint_1),
            ("IK Joint 2", self.ik_joint_2),
            ("IK Joint 3", self.ik_joint_3),
            ("IK Joint 4", self.ik_joint_4),
            ("IK Joint 5", self.ik_joint_5),
            ("IK Joint 6", self.ik_joint_6)
        ]

        # 生成格式化字符串，保留三位小数
        formatted_angles = "\n".join([f"{name}:{angle}" for name, angle in joint_angles])

        return f"ArmMsgFeedBackIKJointStates:\n{formatted_angles}"

    def __repr__(self):
        return self.__str__()