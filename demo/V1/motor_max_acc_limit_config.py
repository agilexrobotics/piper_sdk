#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# V2版本sdk
# 单独设定某个电机的最大加速度
# 注意这个指令是通过协议直接写入到驱动flash中，不可实时更新

from typing import (
    Optional,
)
import time
from piper_sdk import *

def enable_fun(piper:C_PiperInterface, enable:bool):
    '''
    使能机械臂并检测使能状态,尝试5s,如果使能超时则退出程序
    '''
    enable_flag = False
    loop_flag = False
    # 设置超时时间（秒）
    timeout = 5
    # 记录进入循环前的时间
    start_time = time.time()
    elapsed_time_flag = False
    while not (loop_flag):
        elapsed_time = time.time() - start_time
        print(f"--------------------")
        enable_list = []
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_enable_status)
        enable_list.append(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_enable_status)
        if(enable):
            enable_flag = all(enable_list)
            piper.EnableArm(7)
            piper.GripperCtrl(0,1000,0x01, 0)
        else:
            enable_flag = any(enable_list)
            piper.DisableArm(7)
            piper.GripperCtrl(0,1000,0x02, 0)
        print(f"使能状态: {enable_flag}")
        print(f"--------------------")
        if(enable_flag == enable):
            loop_flag = True
            enable_flag = True
        else: 
            loop_flag = False
            enable_flag = False
        # 检查是否超过超时时间
        if elapsed_time > timeout:
            print(f"超时....")
            elapsed_time_flag = True
            enable_flag = False
            loop_flag = True
            break
        time.sleep(0.5)
    resp = enable_flag
    print(f"Returning response: {resp}")
    return resp

if __name__ == "__main__":
    piper = C_PiperInterface("can0")
    piper.ConnectPort()
    piper.EnableArm(7)
    enable_fun(piper=piper, enable=False)
    # 3rad/s
    piper.JointMaxAccConfig(1,500)
    time.sleep(0.5)
    piper.JointMaxAccConfig(2,500)
    time.sleep(0.5)
    piper.JointMaxAccConfig(3,500)
    time.sleep(0.5)
    piper.JointMaxAccConfig(4,500)
    time.sleep(0.5)
    piper.JointMaxAccConfig(5,500)
    time.sleep(0.5)
    piper.JointMaxAccConfig(6,500)
    while True:
        piper.SearchAllMotorMaxAccLimit()
        print(piper.GetAllMotorMaxAccLimit())
        time.sleep(0.1)