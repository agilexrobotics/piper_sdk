import time
from piper_sdk import Piper

# 测试代码
if __name__ == "__main__":
    piper = Piper("can0")
    piper.init()
    piper.connect()
    while not piper.enable_arm():
        time.sleep(0.01)
    print("使能成功!!!!")