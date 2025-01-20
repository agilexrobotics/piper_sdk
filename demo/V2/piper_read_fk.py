#!/usr/bin/env python3
# -*-coding:utf8-*-

from typing import (
    Optional,
)
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    while True:
        print(piper.GetFK())
        print(piper.GetArmEndPoseMsgs())
        # print(piper.GetArmJointMsgs())
        time.sleep(0.01)