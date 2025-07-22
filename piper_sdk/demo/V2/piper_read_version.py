#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2()
    piper.ConnectPort(piper_init=True, start_thread=True)
    time.sleep(0.1) # 需要时间去读取固件反馈帧，否则会反馈-0x4AF,如果不需要读取固件版本，可以不设置延时
    print(f'=====>> Piper Current Interface Version is {piper.GetCurrentInterfaceVersion()} <<=====')
    print(f'=====>> Piper Current Interface Version is {piper.GetCurrentInterfaceVersion().value} <<=====')
    print(f'=====>> Piper Current Protocol Version is {piper.GetCurrentProtocolVersion()} <<=====')
    print(f'=====>> Piper Current Protocol Version is {piper.GetCurrentProtocolVersion().value} <<=====')
    print(f'=====>> Piper Current SDK Version is {piper.GetCurrentSDKVersion()} <<=====')
    print(f'=====>> Piper Current SDK Version is {piper.GetCurrentSDKVersion().value} <<=====')
    # 只有当 ConnectPort(piper_init=True, start_thread=True) 时，才能读取到固件版本
    print(f'=====>> Piper Current Firmware Version is {piper.GetPiperFirmwareVersion()} <<=====')
    