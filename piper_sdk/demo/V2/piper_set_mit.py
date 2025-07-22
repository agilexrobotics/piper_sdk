#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 设置机械臂为mit控制模式，这个模式下，机械臂相应最快
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    while True:
        piper.MotionCtrl_2(1, 1, 0, 0xAD)# 0xFC
        time.sleep(1)
    