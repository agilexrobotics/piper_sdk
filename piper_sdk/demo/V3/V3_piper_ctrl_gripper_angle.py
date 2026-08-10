#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意 demo 无法直接运行，需要 pip 安装 sdk 后才能运行
# V3 版本 SDK
# 使用 V3 夹爪角度模式控制夹爪
# Control the gripper in V3 angle mode.
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V3("can0")
    piper.ConnectPort()

    while not piper.EnablePiper():
        time.sleep(0.01)

    # gripper_code:
    #   0x04: disable angle mode
    #   0x05: enable angle mode
    #   0x06: disable and clear error in angle mode
    #   0x07: enable and clear error in angle mode
    piper.GripperCtrl_V3(0, 1000, 0x06, 0x00)
    piper.GripperCtrl_V3(0, 1000, 0x05, 0x00)

    gripper_angle = 0
    count = 0
    while True:
        print(piper.GetArmGripperMsgs_V3())
        print(piper.GetArmGripperCtrl_V3())

        count += 1
        if count == 0:
            print("1-----------")
            gripper_angle = 0
        elif count == 300:
            print("2-----------")
            gripper_angle = 90 * 1000  # 90 degrees, unit: 0.001 degree
        elif count == 600:
            print("3-----------")
            gripper_angle = 0
            count = 0

        piper.GripperCtrl_V3(gripper_angle, 1000, 0x05, 0x00)
        time.sleep(0.005)
