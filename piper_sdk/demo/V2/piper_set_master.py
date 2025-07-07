#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 设置机械臂为主动臂，直接设置即可
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    piper.MasterSlaveConfig(0xFA, 0, 0, 0)
    