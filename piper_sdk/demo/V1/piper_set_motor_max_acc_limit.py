#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# V2版本sdk
# 单独设定某个电机的最大加速度
# 注意这个指令是通过协议直接写入到驱动flash中，不可实时更新

from typing import (
    Optional,
)
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface("can0")
    piper.ConnectPort()
    while( not piper.EnablePiper()):
        pass
        time.sleep(0.01)
    # 3rad/s
    print(1)
    piper.JointMaxAccConfig(1,500)
    time.sleep(0.5)
    print(2)
    piper.JointMaxAccConfig(2,500)
    time.sleep(0.5)
    print(3)
    piper.JointMaxAccConfig(3,500)
    time.sleep(0.5)
    print(4)
    piper.JointMaxAccConfig(4,500)
    time.sleep(0.5)
    print(5)
    piper.JointMaxAccConfig(5,500)
    time.sleep(0.5)
    print(6)
    piper.JointMaxAccConfig(6,500)
    while True:
        piper.SearchAllMotorMaxAccLimit()
        print(piper.GetAllMotorMaxAccLimit())
        time.sleep(0.1)