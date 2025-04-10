#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 读取机械臂消息并打印,需要先安装piper_sdk
from typing import (
    Optional,
)
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    factor = 57.2957795 #1000*180/3.1415926
    # factor = 1
    while True:
        import time
        print(f"-------------------------------------------------------")
        print(f"j1: {piper.GetArmHighSpdInfoMsgs().motor_1.motor_speed*0.001*factor:.2f}")
        print(f"j2: {piper.GetArmHighSpdInfoMsgs().motor_2.motor_speed*0.001*factor:.2f}")
        print(f"j3: {piper.GetArmHighSpdInfoMsgs().motor_3.motor_speed*0.001*factor:.2f}")
        print(f"j4: {piper.GetArmHighSpdInfoMsgs().motor_4.motor_speed*0.001*factor:.2f}")
        print(f"j5: {piper.GetArmHighSpdInfoMsgs().motor_5.motor_speed*0.001*factor:.2f}")
        print(f"j6: {piper.GetArmHighSpdInfoMsgs().motor_6.motor_speed*0.001*factor:.2f}")
        print(f"=====================================================")
        time.sleep(0.1)
        pass
