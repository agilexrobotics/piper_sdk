#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
import time
from piper_sdk import *

# piper(piper_h) initial end pose[mm, mm, mm, deg, deg, deg]: [56.127, 0.0, 213.266, 0.0, 85.0, 0.0]

# piper_l initial end pose[mm, mm, mm, deg, deg, deg]: [73.061, 0.0, 227.594, 0.0, 85.0, 0.0]

# piper_x initial end pose[mm, mm, mm, deg, deg, deg]: [96.897, 0.0, 216.827, -85.0, 0.0, -90.0]

if __name__ == "__main__":
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    while True:
        print(piper.GetArmEndPoseMsgs())
        time.sleep(0.01)
