#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行

from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V1()
    piper.ConnectPort(piper_init=False, start_thread=False)
    print(f'=====>> Piper Current Interface Version is {piper.GetCurrentInterfaceVersion()} <<=====')
    print(f'=====>> Piper Current Interface Version is {piper.GetCurrentInterfaceVersion().value} <<=====')
    print(f'=====>> Piper Current Protocol Version is {piper.GetCurrentProtocolVersion()} <<=====')
    print(f'=====>> Piper Current Protocol Version is {piper.GetCurrentProtocolVersion().value} <<=====')
    print(f'=====>> Piper Current SDK Version is {piper.GetCurrentSDKVersion()} <<=====')
    print(f'=====>> Piper Current SDK Version is {piper.GetCurrentSDKVersion().value} <<=====')

