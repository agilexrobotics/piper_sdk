#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# V2版本sdk
# 单独设定某个电机的最大加速度
# 注意这个指令是通过协议直接写入到驱动flash中，不可实时更新
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    piper.EnableArm(7)
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    # 5rad/s
    for i in range(1,7):
        piper.JointMaxAccConfig(i, 500)
        print(i)
        time.sleep(0.5) # 数据的写入需要时间，发送完上一帧设定指令，需要延时一会
    while True:
        piper.SearchAllMotorMaxAccLimit()
        print(piper.GetAllMotorMaxAccLimit())
        time.sleep(0.1)
    