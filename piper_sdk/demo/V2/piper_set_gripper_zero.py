#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 夹爪设定零点demo
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    piper.GripperCtrl(0,1000,0x00, 0)
    time.sleep(1.5)
    piper.GripperCtrl(0,1000,0x00, 0xAE)
    