#!/usr/bin/env python3
# -*-coding:utf8-*-
# 本demo读取的是串口can消息
# 使用指定参数的can bus
# 注意，如果interface中的can_auto_init为False，需要先执行CreateCanBus初始化内部的__arm_can才能执行ConnectPort，否则会报错
# 如果使用pcie转can或者串口can模块，需要将judge_flag置为False，否则检测的是Linux系统下的socketcan模块
# 注意需要先赋予串口权限: sudo chmod 777 /dev/ttyACM0
# 正常帧率为3040左右(链接单条臂)

# This demo reads serial CAN messages.
# Uses a CAN bus with specified parameters.
# Note that if `can_auto_init` in the interface is `False`,
#  you need to execute `CreateCanBus` to initialize the internal `__arm_can` before executing `ConnectPort`; 
# otherwise, an error will occur.
# If using a PCIe to CAN or serial CAN module, 
# you need to set `judge_flag` to `False`; 
# otherwise, it will detect the socketcan module under the Linux system.
# Note that you need to grant serial port permissions first: `sudo chmod 777 /dev/ttyACM0`
# The normal frame rate is around 3040 (connected to a single arm).
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    # 此处使用can_auto_init=False，手动创建can bus，该实例虽然会将can bus创建在__arm_can中，
    # 但不会自动执行ConnectPort，需要手动执行ConnectPort
    # 同时can_name虽然会被默认设置为can0，但不会被使用，实际使用的是CreateCanBus中指定的can_name
    # Here, `can_auto_init=False` is used to manually create the CAN bus. 
    # Although this instance will create the CAN bus in `__arm_can`, 
    # it will not automatically execute `ConnectPort`; you need to execute `ConnectPort` manually.
    # Also, although `can_name` will be set to `can0` by default, 
    # it will not be used. The actual `can_name` used is the one specified in `CreateCanBus`.
    piper = C_PiperInterface_V3(can_auto_init=False)
    piper.CreateCanBus(can_name="/dev/ttyACM0",
                       bustype="slcan",
                       expected_bitrate=1000000,
                       judge_flag=False
                       )
    piper.ConnectPort(piper_init=False)
    while(True):
        print(f"all_fps: {piper.GetCanFps()}")
        time.sleep(0.01)
