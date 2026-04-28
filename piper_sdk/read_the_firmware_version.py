import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface("can0")
    piper.ConnectPort()
    time.sleep(0.025) # It takes time to read the firmware feedback frame, otherwise -0x4AF will be fed back
    print(piper.GetPiperFirmwareVersion())