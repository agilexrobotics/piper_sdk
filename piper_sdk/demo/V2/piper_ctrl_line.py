#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface_V2("can0")
    piper.ConnectPort()
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    piper.GripperCtrl(0,1000,0x01, 0)
    factor = 1000
    position = [
                57.0, \
                0.0, \
                215.0, \
                0, \
                85.0, \
                0, \
                0]

    count = 0
    while True:
        print(piper.GetArmEndPoseMsgs())
        count  = count + 1
        if(count == 0):
            print("1-----------")
            position = [
                57.0, \
                0.0, \
                215.0, \
                0, \
                85.0, \
                0, \
                0]
        elif(count == 2):
            print("2-----------")
            position = [
                57.0, \
                0.0, \
                260.0, \
                0, \
                85.0, \
                0, \
                0]
        elif(count == 3):
            print("1-----------")
            position = [
                57.0, \
                0.0, \
                215.0, \
                0, \
                85.0, \
                0, \
                0]
            count = 0
        
        X = round(position[0]*factor)
        Y = round(position[1]*factor)
        Z = round(position[2]*factor)
        RX = round(position[3]*factor)
        RY = round(position[4]*factor)
        RZ = round(position[5]*factor)
        joint_6 = round(position[6]*factor)
        print(X,Y,Z,RX,RY,RZ)
        piper.MotionCtrl_2(0x01, 0x02, 100, 0x00)
        piper.EndPoseCtrl(X,Y,Z,RX,RY,RZ)
        piper.GripperCtrl(abs(joint_6), 1000, 0x01, 0)
        time.sleep(2)
    