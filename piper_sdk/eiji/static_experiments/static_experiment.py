import numpy as np
import math
import matplotlib.pyplot as plt
from piper_sdk import *
import time
import csv
import os
from datetime import datetime
import pinocchio as pin

urdf_path = "/home/piper/piper_sdk/piper_description.urdf"
robot_model = pin.buildModelFromUrdf(urdf_path)
data = robot_model.createData()


T_stop = 2.0  # stopping time
Ts = 0.005  # sampling period

Position = [0, math.pi/6, -np.pi/3, 0, np.pi/6, -np.pi/6] 
Position_mdeg = [0, 30000, -60000, 0, 30000, -30000] # in mdeg

Kp = [8.0, 8.0, 8.0, 6.0, 7.0, 1.5]
Kd = [0.5, 0.5, 0.5, 0.3, 0.5, 0.2]

def main():
    # header for log data
    log_data = []
    header = ["time_s", "Hz", "joint1_angle_rad", "joint2_angle_rad", "joint3_angle_rad",
              "joint4_angle_rad", "joint5_angle_rad", "joint6_angle_rad",
              "joint1_torque_nm", "joint2_torque_nm", "joint3_torque_nm",
              "joint4_torque_nm", "joint5_torque_nm", "joint6_torque_nm",
              "joint1_rnea_torque_nm", "joint2_rnea_torque_nm", "joint3_rnea_torque_nm",
              "joint4_rnea_torque_nm", "joint5_rnea_torque_nm", "joint6_rnea_torque_nm"
             ]
    log_data.append(header)

    piper = C_PiperInterface_V2("can0")
    # connect to CAN port
    piper.ConnectPort()
    # enable piper
    while( not piper.EnablePiper()):
        time.sleep(0.1)
    
    # MoveJ mode
    piper.MotionCtrl_2(ctrl_mode=0x01, move_mode=0x01, move_spd_rate_ctrl=30)
    # Move to initial angle
    piper.JointCtrl(*Position_mdeg)
    # Wait until reach the target
    print("移動完了を待っています...")
    while piper.GetArmStatus().arm_status.motion_status != 0x00: # 0x00: 到達完了
        time.sleep(0.1)
    print("初期角度に到達しました。")
    time.sleep(3) # stop for 3 sec

    # MIT control mode
    piper.MotionCtrl_2(
        ctrl_mode=0x01,
        move_mode=0x04,
        move_spd_rate_ctrl=100,
        is_mit_mode=0xAD
    )
    time.sleep(1.0)  # wait for MIT mode to stabilize
    print("MIT制御モードに設定しました。")

    t = []
    i = 0
    while True:
        # read current state
        hs = piper.GetArmHighSpdInfoMsgs()
        motor_infos = [
            hs.motor_1,
            hs.motor_2,
            hs.motor_3,
            hs.motor_4,
            hs.motor_5,
            hs.motor_6
        ]
        t.append(hs.time_stamp)
        Hz = hs.Hz
        angles_rad = [info.pos * 1e-3 for info in motor_infos]
        torques_nm = [info.effort * 1e-3 for info in motor_infos]

        # calculate rnea torques
        q = np.zeros(robot_model.nv) # joint angles
        q[:6] = angles_rad # for 6 joints
        q[7:] = 0.0 # for the gripper joint
        qd = np.zeros(robot_model.nv) # joint velocities
        qdd = np.zeros(robot_model.nv) # joint accelerations
        tau_rnea = pin.rnea(robot_model, data, q, qd, qdd) # compute rnea torques

        # log data
        log_row = [t[i]] + [Hz]+ angles_rad + torques_nm + tau_rnea[:6].tolist()
        log_data.append(log_row)

        for joint_id in range(1, 7):
            # control command
            q_ref = Position[joint_id - 1]
            piper.JointMitCtrl(
                motor_num=joint_id,
                pos_ref=q_ref,
                vel_ref=0.0,
                kp=Kp[joint_id - 1],
                kd=Kd[joint_id - 1],
                t_ref=0.0
            )
        if t[i] - t[0] >= T_stop:
            print("実験終了。")
            break
        i += 1

        
    # Save log data to CSV
    if len(log_data) > 1:
        save_dir = os.path.join(os.path.expanduser("~"), "piper_logs/static_experiments")
        os.makedirs(save_dir, exist_ok=True)
        filename = f"static_experiment_follower_6_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        full_path = os.path.join(save_dir, filename)
        print(f"データを {full_path} に保存しています...")
        try:
            with open(full_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(log_data)
            print("保存が完了しました。")
        except IOError as e:
            print(f"ファイルへの書き込みに失敗しました: {e}")
    else:
        print("保存するデータがありません。")


if __name__ == "__main__":
    main()