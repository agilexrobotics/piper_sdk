#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 设定机械臂碰撞防护等级并打印
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0",False)
    piper.ConnectPort()
    # piper.CrashProtectionConfig(1,1,1,1,1,1)
    piper.CrashProtectionConfig(0,0,0,0,0,0)
    while True:
        piper.ArmParamEnquiryAndConfig(0x02, 0x00, 0x00, 0x00, 0x03)
        print(piper.GetCrashProtectionLevelFeedback())
        time.sleep(0.01)
    