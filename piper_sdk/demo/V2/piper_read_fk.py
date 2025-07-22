#!/usr/bin/env python3
# -*-coding:utf8-*-
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2(dh_is_offset=1)
    piper.ConnectPort()
    # 使用前需要使能
    piper.EnableFkCal()
    # 注意，由于计算在单一线程中十分耗费资源，打开后会导致cpu占用率上升接近一倍
    while True:
        # 反馈6个浮点数的列表，表示 1-6 号关节的位姿，-1表示joint6的位姿
        print(f"feedback:{piper.GetFK('feedback')[-1]}")
        print(f"control:{piper.GetFK('control')}")
        time.sleep(0.01)
    