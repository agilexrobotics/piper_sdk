#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
from typing import (
    Optional,
)
import time
from piper_sdk import *


def enable_fun(piper: C_PiperInterface):
    """
    使能机械臂并检测使能状态,尝试5s,如果使能超时则退出程序
    """
    enable_flag = False
    # 设置超时时间（秒）
    timeout = 5
    # 记录进入循环前的时间
    start_time = time.time()
    elapsed_time_flag = False
    while not (enable_flag):
        elapsed_time = time.time() - start_time
        print("--------------------")
        enable_flag = (
            piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_enable_status
            and piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_enable_status
            and piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_enable_status
            and piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_enable_status
            and piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_enable_status
            and piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_enable_status
        )
        print("使能状态:", enable_flag)
        piper.EnableArm(7)
        piper.GripperCtrl(0, 1000, 0x01, 0)
        print("--------------------")
        # 检查是否超过超时时间
        if elapsed_time > timeout:
            print("超时....")
            elapsed_time_flag = True
            enable_flag = True
            break
        time.sleep(1)
        pass
    if elapsed_time_flag:
        print("程序自动使能超时,退出程序")
        exit(0)


if __name__ == "__main__":
    piper = C_PiperInterface("can0")
    piper.ConnectPort()
    piper.EnableArm(7)
    enable_fun(piper=piper)
    # piper.DisableArm(7)
    piper.GripperCtrl(0, 1000, 0x01, 0)
    factor = 57324.840764  # 1000*180/3.14
    position = [0, 0, 0, 0, 0, 0, 0]
    count = 0
    while True:
        print(piper.GetArmStatus())
        import time

        count = count + 1
        # print(count)
        if count == 0:
            print("1-----------")
            position = [0, 0, 0, 0, 0, 0, 0]
        elif count == 500:
            print("2-----------")
            position = [0.2, 0.2, -0.2, 0.3, -0.2, 0.5, 0.08]
        elif count == 1000:
            print("1-----------")
            position = [0, 0, 0, 0, 0, 0, 0]
            count = 0

        joint_0 = round(position[0] * factor)
        joint_1 = round(position[1] * factor)
        joint_2 = round(position[2] * factor)
        joint_3 = round(position[3] * factor)
        joint_4 = round(position[4] * factor)
        joint_5 = round(position[5] * factor)
        joint_6 = round(position[6] * 1000 * 1000)
        # piper.MotionCtrl_1()
        piper.MotionCtrl_2(0x01, 0x01, 50, 0x00)
        piper.JointCtrl(joint_0, joint_1, joint_2, joint_3, joint_4, joint_5)
        piper.GripperCtrl(abs(joint_6), 1000, 0x01, 0)
        piper.MotionCtrl_2(0x01, 0x01, 50, 0x00)
        time.sleep(0.005)
        pass
