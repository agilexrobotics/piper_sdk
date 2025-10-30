#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# V2版本sdk
# 单独设定某个电机的关节限位
# 注意这个指令是通过协议直接写入到驱动flash中，不可实时更新
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    piper.EnableArm(7)
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    
    piper.MotorAngleLimitMaxSpdSet(1, 1500, -1500)
    piper.MotorAngleLimitMaxSpdSet(2, 1800, 0)
    piper.MotorAngleLimitMaxSpdSet(3, 0, -1700)
    piper.MotorAngleLimitMaxSpdSet(4, 1000, -1000)
    piper.MotorAngleLimitMaxSpdSet(5, 700, -700)
    piper.MotorAngleLimitMaxSpdSet(6, 1700, -1700)

    while True:
        print(piper.GetAllMotorAngleLimitMaxSpd())
        time.sleep(0.1)
    