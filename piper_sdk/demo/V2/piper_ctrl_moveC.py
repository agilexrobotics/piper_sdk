#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# piper机械臂圆弧模式demo
# 注意机械臂工作空间内不要有障碍

from typing import (
    Optional,
)
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    piper.GripperCtrl(0,1000,0x01, 0)
    # X:135.481
    piper.EndPoseCtrl(135481,9349,161129,178756,6035,-178440)
    piper.MoveCAxisUpdateCtrl(0x01)
    time.sleep(0.001)
    piper.EndPoseCtrl(222158,128758,142126,175152,-1259,-157235)
    piper.MoveCAxisUpdateCtrl(0x02)
    time.sleep(0.001)
    piper.EndPoseCtrl(359079,3221,153470,179038,1105,179035)
    piper.MoveCAxisUpdateCtrl(0x03)
    time.sleep(0.001)
    piper.MotionCtrl_2(0x01, 0x03, 30, 0x00)
    pass