#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 读取机械臂消息并打印,需要先安装piper_sdk
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    print("1-----------")
    print(piper.GetRespInstruction())
    print("1-----------")
    piper.EnableArm()
    while True:
        print("------------")
        # print(piper.GetRespInstruction())
        piper.SetInstructionResponse()
        print("------------")
        if piper.GetRespInstruction().instruction_response.instruction_index == 0x71:
            # 捕获到设置指令0x471的应答时，等待3s后清除SDK保存的应答信息
            time.sleep(3)
            print("3-----------")
            piper.ClearRespSetInstruction()
        time.sleep(0.005)
    