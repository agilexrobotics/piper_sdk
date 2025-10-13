#!/usr/bin/env python3
# -*-coding:utf8-*-
"""
-------------------------------------------------
   File Name:    piper_read_tcp_pose.py
   Description:  测试TCP偏移
   Author:       Jack
   Date:         2025-08-15
   Version:      1.0
   License:      MIT License
-------------------------------------------------
"""
import math
import time
from piper_sdk import *


def apply_tool_offset(pose, tool_offset):
    '''
    计算TCP在基座系下的位置
    
    Args:
        pose: (X, Y, Z, RX, RY, RZ)
            X,Y,Z: 单位0.001mm
            RX,RY,RZ: 单位0.001度 (XYZ旋转顺序)
        tool_offset: (tool_x, tool_y, tool_z) 单位米
            在J6坐标系下工具中心点的坐标值 
        
    Returns:
        TCP_XYZ: (X_tcp, Y_tcp, Z_tcp) 单位0.001mm
    '''
    '''
    Calculate TCP position in base coordinate system
    
    Args:
        pose: Tuple (X, Y, Z, RX, RY, RZ)
            X,Y,Z: Position in 0.001mm units
            RX,RY,RZ: Rotation in 0.001 degrees (XYZ rotation order)
        tool_offset: Tuple (tool_x, tool_y, tool_z) in meters
            TCP coordinates in J6 coordinate system
        
    Returns:
        TCP_XYZ: Tuple (X_tcp, Y_tcp, Z_tcp) in 0.001mm units
    '''
    X, Y, Z, RX, RY, RZ = pose
    
    # Convert angles: 0.001 degrees → radians
    rx_rad = math.radians(RX / 1000.0)
    ry_rad = math.radians(RY / 1000.0)
    rz_rad = math.radians(RZ / 1000.0)
    
    # Precompute trig values
    cx, sx = math.cos(rx_rad), math.sin(rx_rad)
    cy, sy = math.cos(ry_rad), math.sin(ry_rad)
    cz, sz = math.cos(rz_rad), math.sin(rz_rad)
    
    # Compute rotation matrix (XYZ order: R = Rz * Ry * Rx)
    r00 = cy * cz
    r01 = sx * sy * cz - cx * sz
    r02 = cx * sy * cz + sx * sz
    
    r10 = cy * sz
    r11 = sx * sy * sz + cx * cz
    r12 = cx * sy * sz - sx * cz
    
    r20 = -sy
    r21 = sx * cy
    r22 = cx * cy
    
    # Convert tool offset: meters → 0.001mm
    tool_x_mm = tool_offset[0] * 1000000.0
    tool_y_mm = tool_offset[1] * 1000000.0
    tool_z_mm = tool_offset[2] * 1000000.0
    
    # Apply rotation to tool offset
    offset_x = r00 * tool_x_mm + r01 * tool_y_mm + r02 * tool_z_mm
    offset_y = r10 * tool_x_mm + r11 * tool_y_mm + r12 * tool_z_mm
    offset_z = r20 * tool_x_mm + r21 * tool_y_mm + r22 * tool_z_mm
    
    # Calculate TCP position with rounding
    return (
        round(X + offset_x),
        round(Y + offset_y),
        round(Z + offset_z)
    )


if __name__ == "__main__":
    # 初始化机械臂连接
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    
    # # 等待机械臂启用
    # while not piper.DisablePiper():
    #     time.sleep(0.01)
    
    # # 设置初始位置
    # piper.MotionCtrl_2(0x01, 0x01, 100, 0x00)
    # piper.JointCtrl(0,0,0,0,0,0)
    
    # 获取末端位姿并设置工具偏移
    end_pose = piper.GetArmEndPoseMsgs().end_pose
    tool_offset = (0, 0, 0.145)  # Z轴偏移145mm
    
    # 实时计算并显示TCP位置
    while True:
        pose = (
            end_pose.X_axis, 
            end_pose.Y_axis, 
            end_pose.Z_axis, 
            end_pose.RX_axis, 
            end_pose.RY_axis, 
            end_pose.RZ_axis
        )
        
        x_tcp, y_tcp, z_tcp = apply_tool_offset(pose, tool_offset)
        
        print("="*50)
        print("J6 Pos (0.001mm):")
        print(f" X: {pose[0]}, Y: {pose[1]}, Z: {pose[2]}")
        
        print("\nTCP Pos (0.001mm):")
        print(f" X: {x_tcp}, Y: {y_tcp}, Z: {z_tcp}\n")
        
        time.sleep(0.005)