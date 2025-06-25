#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
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
    piper.GripperCtrl(0,1000,0x02, 0)
    piper.GripperCtrl(0,1000,0x01, 0)
    range = 0
    count = 0
    while True:
        print(piper.GetArmGripperMsgs())
        import time
        count  = count + 1
        if(count == 0):
            print("1-----------")
            range = 0
        elif(count == 300):
            print("2-----------")
            range = 50 * 1000 # 50mm
        elif(count == 600):
            print("3-----------")
            range = 0
            count = 0
        piper.GripperCtrl(abs(range), 1000, 0x01, 0)
        
        time.sleep(0.005)
        pass