#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 使能机械臂 注： 主臂模式下无法使能机械臂
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V3()
    piper.ConnectPort()
    time.sleep(0.1)
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    print("Enable successfully!!!!")
