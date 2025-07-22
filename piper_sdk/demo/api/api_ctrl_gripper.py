import time
from piper_sdk import Piper

# 测试代码
if __name__ == "__main__":
    piper = Piper("can0")
    piper.init()
    piper.connect()
    while not piper.enable_arm():
        time.sleep(0.01)
    piper.enable_gripper()
    piper.move_to_home()
    range = 0
    count = 0
    while True:
        count  = count + 1
        if(count == 0):
            print("1-----------")
            range = 0
        elif(count == 300):
            print("2-----------")
            range = 50 # 50mm
        elif(count == 600):
            print("1-----------")
            range = 0
            count = 0
        piper.move_gripper(range, 1)
        time.sleep(0.005)