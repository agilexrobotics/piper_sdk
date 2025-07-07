#!/usr/bin/env python3
# -*-coding:utf8-*
from piper_sdk import *
import time

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2(can_name="can0", logger_level=LogLevel.DEBUG,log_to_file=True)
    piper.ConnectPort()
