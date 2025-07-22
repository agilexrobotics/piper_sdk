#!/usr/bin/env python3
# -*-coding:utf8-*-
# 当有多个机械臂的时候，可以创建多实例，通过识别can_port避免创建读取相同can端口的实例
# 注意需要多个can模块
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2("can_0")
    piper.ConnectPort(True)
    piper1 = C_PiperInterface_V2("can_1")
    piper1.ConnectPort(True)
    while True:
        print(piper.GetCanFps())
        time.sleep(1)
        pass
    