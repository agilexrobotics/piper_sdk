#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# piper机械臂直线模式demo
# 注意机械臂工作空间内不要有障碍
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    
    # 在XOY平面上画正方形
    # 切换至MOVEP模式，移动到初始位置
    piper.MotionCtrl_2(0x01, 0x00, 100, 0x00)
    piper.EndPoseCtrl(150000, -50000, 150000, -179900, 0, -179900)
    time.sleep(2)

    # 切换至MOVEL模式
    piper.MotionCtrl_2(0x01, 0x02, 100, 0x00)
    piper.EndPoseCtrl(150000, 50000, 150000, -179900, 0, -179900)
    time.sleep(2)

    piper.MotionCtrl_2(0x01, 0x02, 100, 0x00)
    piper.EndPoseCtrl(250000, 50000, 150000, -179900, 0, -179900)
    time.sleep(2)

    piper.MotionCtrl_2(0x01, 0x02, 100, 0x00)
    piper.EndPoseCtrl(250000, -50000, 150000, -179900, 0, -179900)
    time.sleep(2)

    piper.MotionCtrl_2(0x01, 0x02, 100, 0x00)
    piper.EndPoseCtrl(150000, -50000, 150000, -179900, 0, -179900)


    