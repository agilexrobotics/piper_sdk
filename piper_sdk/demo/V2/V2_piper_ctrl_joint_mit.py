#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# V2版本sdk
# 单独设定某个电机的mit控制
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    
    while True:
        piper.MotionCtrl_2(0x01, 0x04, 0, 0xAD)
        piper.JointMitCtrl(6,-0.5,0,10,0.8,0)
        print(1)
        time.sleep(1)
        piper.MotionCtrl_2(0x01, 0x04, 0, 0xAD)
        piper.JointMitCtrl(6,0,0,10,0.8,0)
        print(2)
        time.sleep(1)
        piper.MotionCtrl_2(0x01, 0x04, 0, 0xAD)
        piper.JointMitCtrl(6,0.5,0,10,0.8,0)
        print(3)
        time.sleep(1)
    