#!/usr/bin/env python3
# -*-coding:utf8-*-
# 本demo读取的是串口can消息
# 使用指定参数的can bus
# 注意，如果interface中的can_auto_init为False，需要先执行CreateCanBus初始化内部的__arm_can才能执行ConnectPort，否则会报错
# 如果使用pcie转can或者串口can模块，需要将judge_flag置为False，否则检测的是Linux系统下的socketcan模块
# 注意需要先赋予串口权限: sudo chmod 777 /dev/ttyACM0
# 正常帧率为3040左右(链接单条臂)
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2(can_auto_init=False)
    piper.CreateCanBus(can_name="/dev/ttyACM0",
                       bustype="slcan",
                       expected_bitrate=1000000,
                       judge_flag=False
                       )
    piper.ConnectPort(piper_init=False)
    while(True):
        print(f"all_fps: {piper.GetCanFps()}")
        time.sleep(0.01)
    