#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# JS模式关节控制demo: MOVE J(0x01) + MIT模式标志(0xAD), 机械臂以最快速度响应目标位置
# 警告: JS模式无平滑处理、无轨迹规划, 目标点跳变过大会产生剧烈机械冲击!
#       请像本demo一样高频流式下发连续的小幅目标点
import time
import math
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    factor = 57295.7795 #1000*180/3.1415926
    t = 0.0
    while True:
        # 以200Hz流式下发连续变化的目标点, 相邻目标点差值很小, 避免冲击
        j2 = 0.3 * (1 - math.cos(t))    # rad, 范围 [0, 0.6]
        j3 = -0.2 * (1 - math.cos(t))   # rad, 范围 [-0.4, 0]
        joint_2 = round(j2 * factor)
        joint_3 = round(j3 * factor)
        piper.MoveJS(0, joint_2, joint_3, 0, 0, 0)
        t += 0.005
        time.sleep(0.005)
