#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意 demo 无法直接运行，需要 pip 安装 sdk 后才能运行
# V3 版本 SDK
# 设置安装位置为水平倒装
# Set the installation position to horizontal inverse.
from piper_sdk import *


if __name__ == "__main__":
    piper = C_PiperInterface_V3("can0")
    piper.ConnectPort()

    # installation_pos:
    #   0x00: invalid
    #   0x01: horizontal upright
    #   0x02: side mount left
    #   0x03: side mount right
    #   0x04: horizontal inverse
    piper.MotionCtrl_2(
        ctrl_mode=0x01,
        move_mode=0x01,
        move_spd_rate_ctrl=0,
        is_mit_mode=0x00,
        residence_time=0,
        installation_pos=0x04,
    )
