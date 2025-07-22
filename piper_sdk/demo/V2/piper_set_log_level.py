#!/usr/bin/env python3
# -*-coding:utf8-*
from piper_sdk import *
from piper_sdk.utils import global_area

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2(can_name="can0", logger_level=LogLevel.DEBUG, log_to_file=True)
    piper.ConnectPort()
    # 打印日志文件路径
    print("log file path:", LogManager.get_log_file_path(global_area))
    