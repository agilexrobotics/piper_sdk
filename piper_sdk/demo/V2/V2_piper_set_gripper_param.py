#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# V2版本sdk
# 夹爪/示教器参数设置指令
# 第一次使用夹爪或者示教器时，需要设定一下这两个末端执行器参数，否则会出现数据没有反馈并且执行器无法控制的情况
# 一般情况下 GripperTeachingPendantParamConfig 函数第二个参数 max_range_config 是70
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    piper.GripperTeachingPendantParamConfig(100, 70, 1)
    piper.ArmParamEnquiryAndConfig(4)
    while True:
        print(piper.GetGripperTeachingPendantParamFeedback())
        time.sleep(0.05)
    