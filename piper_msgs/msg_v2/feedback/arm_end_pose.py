#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgEndPoseFeedBack():
    '''
    msg_v2_feedback
    
    机械臂末端姿态反馈,单位0.001mm
    
    CAN ID: 
        0x152、0x153、0x154
    
    Args:
        X_axis: X坐标
        Y_axis: Y坐标
        Z_axis: Z坐标
        RX_axis: RX角度
        RY_axis: RY角度
        RZ_axis: RZ角度
    '''
    '''
    msg_v2_feedback
    
    End-Effector Pose Feedback for the Robotic Arm, unit: 0.001 mm.
    
    CAN ID: 
        0x152、0x153、0x154
    
    Args:
        X_axis: X-coordinate.
        Y_axis: Y-coordinate.
        Z_axis: Z-coordinate.
        RX_axis: Rotation angle around the X-axis (RX).
        RY_axis: Rotation angle around the Y-axis (RY).
        RZ_axis: Rotation angle around the Z-axis (RZ).
    '''
    def __init__(self, 
                 X_axis: int = 0, 
                 Y_axis: int = 0, 
                 Z_axis: int = 0, 
                 RX_axis: int = 0, 
                 RY_axis: int = 0, 
                 RZ_axis: int = 0):
        self.X_axis = X_axis
        self.Y_axis = Y_axis
        self.Z_axis = Z_axis
        self.RX_axis = RX_axis
        self.RY_axis = RY_axis
        self.RZ_axis = RZ_axis

    def __str__(self):
        # 将角度乘以0.001，并保留三位小数
        end_pose = [
            (" X_axis ", self.X_axis, self.X_axis * 0.001),
            (" Y_axis ", self.Y_axis, self.Y_axis * 0.001),
            (" Z_axis ", self.Z_axis, self.Z_axis * 0.001),
            (" RX_axis ", self.RX_axis, self.RX_axis * 0.001),
            (" RY_axis ", self.RY_axis, self.RY_axis * 0.001),
            (" RZ_axis ", self.RZ_axis, self.RZ_axis * 0.001)
        ]

        # 生成格式化字符串，保留三位小数
        formatted_ = "\n".join([f"{name}: {pose}, {pose_f:.3f}" for name, pose, pose_f in end_pose])
        
        return f"ArmMsgEndPoseFeedBack:\n{formatted_}"
    
    def __repr__(self):
        return self.__str__()