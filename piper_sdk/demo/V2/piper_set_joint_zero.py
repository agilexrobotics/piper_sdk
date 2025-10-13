#!/usr/bin/env python3
# -*-coding:utf8-*-
"""
-------------------------------------------------
   File Name:    piper_set_joint_zero.py
   Description:  设置关节电机零点位置
   Author:       Jack
   Date:         2025-08-14
   Version:      1.0
   License:      MIT License
-------------------------------------------------
"""
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    time.sleep(0.1)
    print("设置过程输入'q'可以退出程序")
    print("During setup, enter 'q' to exit the program")
    print("设置零点前会对指定的电机失能，请保护好机械臂")
    print("Before setting zero position, the specified motor will be disabled. Please protect the robotic arm.")
    while( not piper.EnablePiper()):
        time.sleep(0.01)
    piper.ModeCtrl(0x01, 0x01, 30, 0x00)
    piper.JointCtrl(0, 0, 0, 0, 0, 0)
    piper.GripperCtrl(0, 1000, 0x01, 0)
    mode = -1
    while True:
        # 模式选择
        if mode == -1:
            print("\nStep 1: 请选择设置模式(0: 指定电机; 1: 顺序设置): ")
            print("Step 1: Select setting mode (0: Single motor; 1: Sequential setting): ")
            mode = input("> ")
            if mode == '0':
                mode = 0
            elif mode == '1':
                mode = 1
            elif mode == 'q':
                break
            else:
                mode = -1
        
        # 单电机设置
        elif mode == 0:
            print("\nStep 2: 输入需要设置零点的电机序号(1~7), 7代表所有电机: ")
            print("Step 2: Enter motor number to set zero (1~7), 7 represents all motors: ")
            motor_num = input("> ")
            if motor_num == 'q':
                mode = -1
                continue
            try:
                motor_num = int(motor_num)
                if motor_num < 1 or motor_num > 7:
                    print("Tip: 输入超出范围")
                    print("Tip: Input out of range")
                    continue
            except:
                print("Tip: 请输入整数")
                print("Tip: Please enter an integer")
                continue
            piper.DisableArm(motor_num)
            print(f"\nInfo: 第{motor_num}号电机失能成功，请手动纠正电机的零点位置")
            print(f"Info: Motor {motor_num} disabled successfully. Please manually adjust to zero position")
            
            print(f"\nStep 3: 回车设置第{motor_num}号电机零点: ")
            print(f"Step 3: Press Enter to set zero for motor {motor_num}: ")
            if input("(按回车继续/Press Enter) ") == 'q':
                mode = -1
                continue
            piper.JointConfig(motor_num, 0xAE)
            piper.EnableArm(motor_num)
            print(f"\nInfo: 第{motor_num}号电机零点设置成功")
            print(f"Info: Motor {motor_num} zero position set successfully")
        
        # 顺序设置
        elif mode == 1:
            print("\nStep 2: 输入从第几号电机开始设置(1~6): ")
            print("Step 2: Enter starting motor number (1~6): ")
            motor_num = input("> ")
            if motor_num == 'q':
                mode = -1
                continue
            try:
                motor_num = int(motor_num)
                if motor_num < 1 or motor_num > 6:
                    print("Tip: 输入超出范围")
                    print("Tip: Input out of range")
                    continue
            except:
                print("Tip: 请输入整数")
                print("Tip: Please enter an integer")
                continue
            for i in range(motor_num, 7):
                piper.DisableArm(i)
                print(f"\nInfo: 第{i}号电机失能成功，请手动纠正电机的零点位置")
                print(f"Info: Motor {i} disabled successfully. Please manually adjust to zero position")
                
                print(f"\nStep 3: 回车设置第{i}号电机零点: ")
                print(f"Step 3: Press Enter to set zero for motor {i}: ")
                if input("(按回车继续/Press Enter) ") == 'q':
                    mode = -1
                    break
                piper.JointConfig(i, 0xAE)
                piper.EnableArm(i)
                print(f"\nInfo: 第{i}号电机零点设置成功")
                print(f"Info: Motor {i} zero position set successfully")