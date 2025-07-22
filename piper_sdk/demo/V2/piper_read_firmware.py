#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 读取机械臂软件固件版本并打印
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    time.sleep(0.03) # 需要时间去读取固件反馈帧，否则会反馈-0x4AF
    print(piper.GetPiperFirmwareVersion())
    # while True:
    #     piper.SearchPiperFirmwareVersion()
    #     time.sleep(0.025)
    #     print(piper.GetPiperFirmwareVersion())
    