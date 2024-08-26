#!/usr/bin/env python3
# -*-coding:utf8-*-

class ArmMsgMotionCtrlCartesian():
    '''
    机械臂运动控制直角坐标系指令

    0x152,0x153,0x154

    '''
    def __init__(self, X_axis: int=0, Y_axis: int=0, 
                 Z_axis: int=0, RX_axis: int=0, 
                 RY_axis: int=0, RZ_axis: int=0):
        self.X_axis = X_axis
        self.Y_axis = Y_axis
        self.Z_axis = Z_axis
        self.RX_axis = RX_axis
        self.RY_axis = RY_axis
        self.RZ_axis = RZ_axis

    def __str__(self):
        dict_ = [
            (" X_axis ", self.X_axis),
            (" Y_axis ", self.Y_axis),
            (" Z_axis ", self.Z_axis),
            (" RX_axis ", self.RX_axis),
            (" RY_axis ", self.RY_axis),
            (" RZ_axis ", self.RZ_axis)
        ]

        # 生成格式化字符串，保留三位小数
        formatted_ = "\n".join([f"{name}: {value}" for name, value in dict_])
        
        return f"ArmMsgMotionCtrlCartesian:\n{formatted_}"
    
    def __repr__(self):
        return self.__str__()