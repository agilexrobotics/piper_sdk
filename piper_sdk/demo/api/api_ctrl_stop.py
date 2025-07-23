from piper_sdk import Piper

# 测试代码
if __name__ == "__main__":
    piper = Piper("can0")
    interface = piper.init()
    interface.MotionCtrl_1(0x01,0,0)
