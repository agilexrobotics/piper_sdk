#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意 demo 无法直接运行，需要 pip 安装 sdk 后才能运行
# V3 版本 SDK
# 首次上电后直接读取不会反馈 IK 关节消息，需要先切到 MOVE P 并发送末端位姿控制指令。
# After power-on, IK joint feedback is available only after MOVE P mode and an end-pose command are sent.
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V3()
    piper.ConnectPort()

    while not piper.EnablePiper():
        time.sleep(0.01)

    factor = 1000
    position = [67.0, 0.0, 215.0, 0.0, 85.0, 0.0]
    X = round(position[0] * factor)
    Y = round(position[1] * factor)
    Z = round(position[2] * factor)
    RX = round(position[3] * factor)
    RY = round(position[4] * factor)
    RZ = round(position[5] * factor)

    # Trigger IK joint feedback. Once triggered, the arm keeps publishing it.
    piper.MotionCtrl_2(0x01, 0x00, 100, 0x00)
    piper.EndPoseCtrl(X, Y, Z, RX, RY, RZ)

    while True:
        print(piper.GetArmIKJointMsgs())
        time.sleep(0.005)
