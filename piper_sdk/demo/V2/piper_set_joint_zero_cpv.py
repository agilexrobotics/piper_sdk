#!/usr/bin/env python3
# -*-coding:utf8-*-
"""
-------------------------------------------------
   File Name:    piper_set_joint_zero.py
   Description:  设置关节电机零点位置
   Author:       Jack
   Date:         2025-10-30
   Version:      2.0
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
    piper.MotionCtrl_2(0x01, 0x01, 30, 0x00)
    piper.JointCtrl(0, 0, 0, 0, 0, 0)
    piper.GripperCtrl(0, 1000, 0x01, 0)
    mode = -1
    while True:
        # 模式选择
        if mode == -1:
            print("\nStep 1: 请选择设置模式(0: 指定电机; 1: 顺序设置; 2: cpv模式校准零点): ")
            print("Step 1: Select setting mode (0: Single motor; 1: Sequential setting): ")
            mode = input("> ")
            if mode == '0':
                mode = 0
            elif mode == '1':
                mode = 1
            elif mode == '2':
                mode = 2
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
            time.sleep(0.1)
            piper.MotionCtrl_2(0x01, 0x01, 30, 0x00)
            time.sleep(0.1)
            piper.JointCtrl(0, 0, 0, 0, 0, 0)
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
                time.sleep(0.1)
                piper.MotionCtrl_2(0x01, 0x01, 30, 0x00)
                time.sleep(0.1)
                piper.JointCtrl(0, 0, 0, 0, 0, 0)
                print(f"\nInfo: 第{i}号电机零点设置成功")
                print(f"Info: Motor {i} zero position set successfully")
        
        elif mode == 2:
            print("\nStep 2: cpv模式(1: 校准j456电机; 2: 校准夹爪电机): ")
            cpv = input("> ")
            if cpv == 'q':
                mode = -1
                continue

            elif cpv == '1':
                for i in range(4, 7):
                    piper.DisableArm(i)

                if input("\nStep 3: j4顺时针旋转至限位，j5向上抬起至限位，j6对准中间凹槽: ") == 'q':
                    mode = -1
                    for i in range(4, 7):
                        piper.EnableArm(i)
                    time.sleep(0.1)
                    piper.MotionCtrl_2(0x01, 0x01, 30, 0x00)
                    time.sleep(0.1)
                    piper.JointCtrl(0, 0, 0, 0, 0, 0)
                    continue

                piper.MotionCtrl_2(0x01, 0x05)
                for i in range(4, 7):
                    id = 0x180 + i
                    data = [0x77, 0x65, 0x65, 0x65, 0x00, 0x00, 0x00]
                    piper.GetCanBus().SendCanMessage(id, data, 7)
                
                print("\n等待电机停止运动...")

            elif cpv == '2':
                piper.GripperCtrl(0, 1000, 0x00, 0)

                if input("\nStep 3: 捏紧夹爪，使其完全闭合: ") == 'q':
                    mode = -1
                    piper.GripperCtrl(0, 1000, 0x02, 0)
                    piper.GripperCtrl(0, 1000, 0x01, 0)
                    continue

                piper.MotionCtrl_2(0x01, 0x05)
                id = 0x180 + 7
                data = [0x77, 0x65, 0x65, 0x65, 0x00, 0x00, 0x00]
                piper.GetCanBus().SendCanMessage(id, data, 7)

                print("\n等待电机停止运动...")