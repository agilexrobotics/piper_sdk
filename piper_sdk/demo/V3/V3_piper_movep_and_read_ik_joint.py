#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意 demo 无法直接运行，需要 pip 安装 sdk 后才能运行
# V3 版本 SDK
# 首次上电后直接读取不会反馈 IK 关节消息，需要先切到 MOVE P 并发送末端位姿控制指令。
# After power-on, IK joint feedback is available only after MOVE P mode and an end-pose command are sent.
import time
from piper_sdk import *

# piper(piper_h) zero end pose[mm, mm, mm, deg, deg, deg]: [56.127, 0.0, 213.266, 0.0, 85.0, 0.0]
# piper(piper_h) initial end pose[mm, mm, mm, deg, deg, deg]: [56.127, 0.0, 215.0, 0.0, 85.0, 0.0]
# piper(piper_h) test end pose[mm, mm, mm, deg, deg, deg]: [56.127, 0.0, 258.0, 0.0, 85.0, 0.0]

# piper_l zero end pose[mm, mm, mm, deg, deg, deg]: [73.061, 0.0, 227.594, 0.0, 85.0, 0.0]
# piper_l initial end pose[mm, mm, mm, deg, deg, deg]: [73.061, 0.0, 237.594, 0.0, 85.0, 0.0]
# piper_l test end pose[mm, mm, mm, deg, deg, deg]: [73.061, 0.0, 272.594, 0.0, 85.0, 0.0]

# piper_x zero end pose[mm, mm, mm, deg, deg, deg]: [96.897, 0.0, 216.827, -85.0, 0.0, -90.0]
# piper_x initial end pose[mm, mm, mm, deg, deg, deg]: [96.897, 0.0, 226.827, -85.0, 0.0, -90.0]
# piper_x test end pose[mm, mm, mm, deg, deg, deg]: [96.897, 0.0, 261.827, -85.0, 0.0, -90.0]

# default piper
if __name__ == "__main__":
    piper = C_PiperInterface_V3(can_name="can0")
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
