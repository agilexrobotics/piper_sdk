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
        print(piper.GetRespInstruction())
        print("------------")
        if piper.GetRespInstruction().instruction_response.instruction_index == 0x71:
            # 捕获到设置指令0x471的应答时(使能机械臂发送的指令id为471)，等待3s后清除SDK保存的应答信息
            # When the response to the setting command 0x471 is captured (the command ID sent to enable the robot arm is 471), 
            # wait for 3 seconds and then clear the response information saved by the SDK
            time.sleep(3)
            print("3-----------")
            piper.ClearRespSetInstruction()
            print(piper.GetRespInstruction())
            exit(0)
        time.sleep(0.005)
    