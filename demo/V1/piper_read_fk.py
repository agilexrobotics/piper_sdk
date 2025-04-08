#!/usr/bin/env python3
# -*-coding:utf8-*-

from typing import (
    Optional,
)
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    while True:
        print(f"feedback:{piper.GetFK('feedback')}")
        print(f"control:{piper.GetFK('control')}")
        time.sleep(0.01)