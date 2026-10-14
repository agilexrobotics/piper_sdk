#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意 demo 无法直接运行，需要 pip 安装 sdk 后才能运行
# V3 版本 SDK
# 首次上电后直接读取不会反馈 IK 关节消息，需要先切到 MOVE P 并发送末端位姿控制指令。
# After power-on, IK joint feedback is available only after MOVE P mode and an end-pose command are sent.
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V3(can_name="can0")
    piper.ConnectPort()

    while True:
        print(piper.GetArmIKJointMsgs())
        time.sleep(0.005)
