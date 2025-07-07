#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# V2版本sdk
# 单独设定某个电机的最大速度
# 注意这个指令是通过协议直接写入到驱动flash中，不可实时更新，如果需要动态调整速度，请使用位置速度模式中的速度百分比
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    # 3rad/s
    for i in range(1,7):
        piper.MotorMaxSpdSet(i, 3000)
        time.sleep(0.1)
    while True:
        piper.SearchAllMotorMaxAngleSpd()
        print(piper.GetAllMotorAngleLimitMaxSpd())
        time.sleep(0.01)
    