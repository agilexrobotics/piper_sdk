#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# piper机械臂直线模式demo
# 注意机械臂工作空间内不要有障碍
import time
from piper_sdk import *

# piper(piper_h) initial end pose[mm, mm, mm, deg, deg, deg]: [56.127, 0.0, 213.266, 0.0, 85.0, 0.0]
# piper(piper_h) test end pose[mm, mm, mm, deg, deg, deg]: [56.127, 0.0, 258, 0.0, 85.0, 0.0]

# piper_l initial end pose[mm, mm, mm, deg, deg, deg]: [73.061, 0.0, 227.594, 0.0, 85.0, 0.0]
# piper_l test end pose[mm, mm, mm, deg, deg, deg]: [73.061, 0.0, 272.594, 0.0, 85.0, 0.0]

# piper_x initial end pose[mm, mm, mm, deg, deg, deg]: [96.897, 0.0, 216.827, -85.0, 0.0, -90.0]
# piper_x test end pose[mm, mm, mm, deg, deg, deg]: [96.897, 0.0, 261.827, -85.0, 0.0, -90.0]

# default piper
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
