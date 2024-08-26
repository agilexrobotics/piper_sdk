#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgStatus:
    '''
    机械臂状态
    '''
    
    def __init__(self):
        self._err_code = 0
        self.err_status = self.ErrStatus()
        self.ctrl_mode:int=0       #控制模式
        self.arm_status:int=0      #机械臂状态
        self.mode_feed:int=0       #模式反馈
        self.teach_status:int=0    #示教状态
        self.motion_status:int=0   #运动状态
        self.trajectory_num:int=0  #运动速度比率

    class ErrStatus:
        def __init__(self):
            self.joint_1_angle_limit = False
            self.joint_2_angle_limit = False
            self.joint_3_angle_limit = False
            self.joint_4_angle_limit = False
            self.joint_5_angle_limit = False
            self.joint_6_angle_limit = False
            self.communication_status_joint_1 = False
            self.communication_status_joint_2 = False
            self.communication_status_joint_3 = False
            self.communication_status_joint_4 = False
            self.communication_status_joint_5 = False
            self.communication_status_joint_6 = False
            
        def __str__(self):
            return (f" Joint 1 Angle Limit Status: {self.joint_1_angle_limit}\n"
                    f" Joint 2 Angle Limit Status: {self.joint_2_angle_limit}\n"
                    f" Joint 3 Angle Limit Status: {self.joint_3_angle_limit}\n"
                    f" Joint 4 Angle Limit Status: {self.joint_4_angle_limit}\n"
                    f" Joint 5 Angle Limit Status: {self.joint_5_angle_limit}\n"
                    f" Joint 6 Angle Limit Status: {self.joint_6_angle_limit}\n"
                    f" Joint 1 Communication Status: {self.communication_status_joint_1}\n"
                    f" Joint 2 Communication Status: {self.communication_status_joint_2}\n"
                    f" Joint 3 Communication Status: {self.communication_status_joint_3}\n"
                    f" Joint 4 Communication Status: {self.communication_status_joint_4}\n"
                    f" Joint 5 Communication Status: {self.communication_status_joint_5}\n"
                    f" Joint 6 Communication Status: {self.communication_status_joint_6}\n")

    @property
    def err_code(self):
        return self._err_code

    @err_code.setter
    def err_code(self, value: int):
        if not (0 <= value < 2**16):
            raise ValueError("err_code must be an 8-bit integer between 0 and 255.")
        self._err_code = value
        # Update err_status based on the err_code bits
        self.err_status.communication_status_joint_1 = bool(value & (1 << 0))
        self.err_status.communication_status_joint_2 = bool(value & (1 << 1))
        self.err_status.communication_status_joint_3 = bool(value & (1 << 2))
        self.err_status.communication_status_joint_4 = bool(value & (1 << 3))
        self.err_status.communication_status_joint_5 = bool(value & (1 << 4))
        self.err_status.communication_status_joint_6 = bool(value & (1 << 5))
        self.err_status.communication_status_joint_1 = bool(value & (1 << 8))
        self.err_status.communication_status_joint_2 = bool(value & (1 << 9))
        self.err_status.communication_status_joint_3 = bool(value & (1 << 10))
        self.err_status.communication_status_joint_4 = bool(value & (1 << 11))
        self.err_status.communication_status_joint_5 = bool(value & (1 << 12))
        self.err_status.communication_status_joint_6 = bool(value & (1 << 13))

    def __str__(self):
        return (f"Control Mode: {self.ctrl_mode}\n"
                f"Arm Status: {self.arm_status}\n"
                f"Mode Feed: {self.mode_feed}\n"
                f"Teach Status: {self.teach_status}\n"
                f"Motion Status: {self.motion_status}\n"
                f"Trajectory Num: {self.trajectory_num}\n"
                f"Error Code: {self._err_code}\n"
                f"Error Status: \n{self.err_status}\n")

    def __repr__(self):
        return self.__str__()