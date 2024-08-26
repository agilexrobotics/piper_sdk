#!/usr/bin/env python3
# -*-coding:utf8-*-
# 读取机械臂消息并打印,需要先安装piper_sdk
from typing import (
    Optional,
)
from piper_sdk import *


# 测试代码
if __name__ == "__main__":
    a = C_PiperInterface()
    a.ConnectPort()
    while True:
        import time
        # a.SearchMotorMaxAngleSpdAccLimit(1, 1)
        # a.ArmParamEnquiryAndConfig(1,0,2,0,3)
        # a.GripperCtrl(50000,1500,0x01)
        print(a.GetArmJointGripperMsgs())
        time.sleep(0.005)
        pass
