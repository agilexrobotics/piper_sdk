import time, math
from piper_sdk import Piper

# 测试代码
if __name__ == "__main__":
    piper = Piper("can0")
    piper.init()
    piper.connect()
    while not piper.enable_arm():
        time.sleep(0.01)
    pos = [
                57.0 / 1000, \
                0.0, \
                215.0 / 1000, \
                0, \
                math.radians(85.0), \
                0, \
                0]
    count = 0
    while True:
        count  = count + 1
        if count == 0:
            print("1-----------")
            pos = [
                57.0 / 1000, \
                0.0, \
                215.0 / 1000, \
                0, \
                math.radians(85.0), \
                0, \
                0]
        elif count == 2:
            print("2-----------")
            pos = [
                57.0 / 1000, \
                0.0, \
                260.0 / 1000, \
                0, \
                math.radians(85.0), \
                0, \
                0]
        elif(count == 3):
            print("1-----------")
            pos = [
                57.0 / 1000, \
                0.0, \
                215.0 / 1000, \
                0, \
                math.radians(85.0), \
                0, \
                0]
            count = 0
        piper.move_l_euler(pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], 100)
        print(piper.get_end_pose_euler())
        time.sleep(2)