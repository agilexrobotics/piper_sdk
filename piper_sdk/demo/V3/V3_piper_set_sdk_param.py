#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V3("can0",
                                start_sdk_gripper_limit=True,
                                start_sdk_joint_limit=True
                                )
    piper.ConnectPort()
    print(piper.GetSDKGripperAngleLimitParam())
    piper.SetSDKGripperAngleLimitParam(-180.0, 180.0)
    print(piper.GetSDKGripperAngleLimitParam())
