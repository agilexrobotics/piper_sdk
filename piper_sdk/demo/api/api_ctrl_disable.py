from piper_sdk import Piper

# 测试代码
if __name__ == "__main__":
    piper = Piper("can0")
    piper.init()
    piper.disable_arm() # 运行后需运行两次使能才能正常控制