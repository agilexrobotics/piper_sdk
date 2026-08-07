#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意 demo 无法直接运行，需要 pip 安装 sdk 后才能运行
# V3 版本 SDK
# 读取 V3 IK 关节反馈消息并打印
# Read and print V3 IK joint feedback messages.
import time
from piper_sdk import *


if __name__ == "__main__":
    piper = C_PiperInterface_V3()
    piper.ConnectPort()

    while True:
        print(piper.GetArmIKJointMsgs())
        time.sleep(0.005)
