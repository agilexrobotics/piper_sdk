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
    position = [0,0,0,0,0,0,0]
    count = 0
    while True:
        count  = count + 1
        if(count == 0):
            print("1-----------")
            position = [0,0,0,0,0,0,0]
        elif(count == 300):
            print("2-----------")
            position = [0.2,0.2,-0.2,0.3,-0.2,0.5,0.08]
        elif(count == 600):
            print("1-----------")
            position = [0,0,0,0,0,0,0]
            count = 0
        piper.move_j(position[:-1], 30)
        piper.move_gripper(position[-1], 1)
        print(piper.get_joint_states())
        time.sleep(0.005)