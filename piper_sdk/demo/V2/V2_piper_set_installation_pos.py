#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# V2版本sdk
# 设定安装位置为水平正装
# 如需设定为侧装左/右
# MotionCtrl_2(0x01,0x01,0,0,0,0x02)
# MotionCtrl_2(0x01,0x01,0,0,0,0x03)
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    piper.MotionCtrl_2(0x01,0x01,0,0,0,0x01)  
    