#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# piper机械臂圆弧模式demo
# 注意机械臂工作空间内不要有障碍
import time
from piper_sdk import *

# piper(piper_h) 1 end pose[mm, mm, mm, deg, deg, deg]: [135.481, 9.349, 161.129, 178.756, 6.035, -178.440]
# piper(piper_h) 2 end pose[mm, mm, mm, deg, deg, deg]: [222.158, 128.758, 142.126, 175.152, -1.259, -157.235]
# piper(piper_h) 3 end pose[mm, mm, mm, deg, deg, deg]: [359.079, 3.221, 153.470, 179.038, 1.105, 179.035]

# piper_l 1 end pose[mm, mm, mm, deg, deg, deg]: [135.481, 9.349, 161.129, 178.756, 6.035, -178.440]
# piper_l 2 end pose[mm, mm, mm, deg, deg, deg]: [222.158, 128.758, 142.126, 175.152, -1.259, -157.235]
# piper_l 3 end pose[mm, mm, mm, deg, deg, deg]: [359.079, 3.221, 153.470, 179.038, 1.105, 179.035]

# piper_x 1 end pose[mm, mm, mm, deg, deg, deg]: [135.481, 9.349, 161.129, 178.756, 6.035, -178.440]
# piper_x 2 end pose[mm, mm, mm, deg, deg, deg]: [222.158, 128.758, 142.126, 175.152, -1.259, -157.235]
# piper_x 3 end pose[mm, mm, mm, deg, deg, deg]: [359.079, 3.221, 153.470, 179.038, 1.105, 179.035]

# default piper
if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    piper.GripperCtrl(0,1000,0x01, 0)
    # 切换至MOVEC模式
    piper.MotionCtrl_2(0x01, 0x03, 30, 0x00)
    # X:135.481
    piper.EndPoseCtrl(135481,9349,161129,178756,6035,-178440)
    piper.MoveCAxisUpdateCtrl(0x01)
    time.sleep(0.001)
    piper.EndPoseCtrl(222158,128758,142126,175152,-1259,-157235)
    piper.MoveCAxisUpdateCtrl(0x02)
    time.sleep(0.001)
    piper.EndPoseCtrl(359079,3221,153470,179038,1105,179035)
    piper.MoveCAxisUpdateCtrl(0x03)
    time.sleep(0.001)
    piper.MotionCtrl_2(0x01, 0x03, 30, 0x00)
