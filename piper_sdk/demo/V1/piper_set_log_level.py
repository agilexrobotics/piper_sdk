#!/usr/bin/env python3
# -*-coding:utf8-*
from piper_sdk import *
import time

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface(can_name="can0", logger_level=LogLevel.DEBUG)
    piper.ConnectPort()
