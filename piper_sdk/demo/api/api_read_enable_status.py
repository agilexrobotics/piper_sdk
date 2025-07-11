import time
from piper_sdk import Piper
# 测试代码
if __name__ == "__main__":
    piper = Piper("can0")
    piper.init()
    piper.connect()
    enable_status = False
    while(True):
        print(piper.get_joint_states())
        time.sleep(1)
