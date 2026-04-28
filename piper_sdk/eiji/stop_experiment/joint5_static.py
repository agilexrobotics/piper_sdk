#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import math
import os
import time
from datetime import datetime
from piper_sdk import C_PiperInterface_V2

# ===== User params =====
CAN_PORT = "can0"
DT = 0.002  # 2 ms
RAMP_INTERVAL = 0.1  # 100 ms

# Breakaway detection (joint3)
BREAKAWAY_THRESH_RAD = math.radians(5.0)  # 5 deg

# Torque sweep (joint5)
TAU_START = 0.0
TAU_MAX   = 2.0      # start small
TAU_STEP  = 0.002    # Nm per ramp step
TAU_DIR   = -1        # +1 or -1 (run twice for both directions)

# MIT gains
KP_HOLD = 35.0
KD_HOLD = 0.5
KP_J5   = 0.0
KD_J5   = 0.0

# ===== Minimal field readers (latest SDK assumption) =====
def read_highspd_q_tau(piper: C_PiperInterface_V2):
    """
    Read joint positions (rad) and torques (Nm) from HighSpdInfo message.
    """
    hs = piper.GetArmHighSpdInfoMsgs()
    motor_infos = [
        hs.motor_1,
        hs.motor_2,
        hs.motor_3,
        hs.motor_4,
        hs.motor_5,
        hs.motor_6
    ]

    angles_rad = [info.pos * 1e-3 for info in motor_infos]
    torques_nm = [info.effort * 1e-3 for info in motor_infos]

    return angles_rad, torques_nm

def sleep_to(t_next: float):
    while True:
        t = time.perf_counter()
        dt = t_next - t
        if dt <= 0:
            return
        time.sleep(min(dt, 0.0005))

def main():
    piper = C_PiperInterface_V2(CAN_PORT)

    # 1. CANポートに接続
    print("CANポートに接続しています...")
    piper.ConnectPort()
    time.sleep(0.5) # 接続が安定するまで少し待機
    if not piper.isOk():
        print(f"CANポート '{CAN_PORT}' への接続に失敗しました。")
        return
    print("接続に成功しました。")
    # 2. アームを有効化(Enable)
    print("アームを有効化しています...")
    # EnablePiper()がTrueを返すまでループ
    while not piper.EnablePiper():
        time.sleep(0.01)
    print("アームが有効になりました。")
    time.sleep(1) # 安定するまで待機
    print("MOVE Jモードに設定しています...")
    piper.MotionCtrl_2(ctrl_mode=0x01, move_mode=0x01, move_spd_rate_ctrl=30)
    time.sleep(0.1)
    # 3. 初期角度に移動
    print("初期角度へ移動します...")
    piper.JointCtrl(0, 0, -26*1000, 0, -60*1000, 0)  # joint3 = -26 deg, joint5 =- 60 deg
    # アームが目標位置に到達するまで待機
    print("移動完了を待っています...")
    while piper.GetArmStatus().arm_status.motion_status != 0x00: # 0x00: 到達完了
        time.sleep(0.1)
    print("初期角度に到達しました。")
    time.sleep(2) # 2秒間停止


    # Read initial state (HighSpd)
    q0, _ = read_highspd_q_tau(piper)

    # Switch to MIT mode (common usage)
    piper.MotionCtrl_2(ctrl_mode=0x01, move_mode=0x04, move_spd_rate_ctrl=50, is_mit_mode=0xAD)
    time.sleep(3.0)
    log_data = []
    header = [
        "time_s", "joint1_angle_rad", "joint2_angle_rad", "joint3_angle_rad",
        "joint4_angle_rad", "joint5_angle_rad", "joint6_angle_rad",
        "joint1_torque_nm", "joint2_torque_nm", "joint3_torque_nm",
        "joint4_torque_nm", "joint5_torque_nm", "joint6_torque_nm",
        "joint5_cmd_tau_nm"
    ]
    log_data.append(header)

    tau_cmd = TAU_START
    t0 = time.perf_counter()
    t_next = t0
    t_last_ramp = t0
    while True:
        t = time.perf_counter()
        t_s = t - t0
        q, tau_fb = read_highspd_q_tau(piper)
        # Breakaway detection (joint5)
        if abs(q[4] - q0[4]) >= BREAKAWAY_THRESH_RAD:
            print(f"[INFO] breakaway: t={t_s:.3f}s, tau_cmd={tau_cmd:.3f} Nm, dq={q[4]-q0[4]:.4f} rad")
            break
        if abs(tau_cmd) > TAU_MAX:
            print(f"[WARN] reached TAU_MAX without breakaway: tau_cmd={tau_cmd:.3f} Nm")
            break
        # MIT control:
        # joint3: hold at -26 deg
        piper.JointMitCtrl(3, math.radians(-26.0), 0.0, KP_HOLD, KD_HOLD, 0.0)
        # Joint5: torque sweep
        piper.JointMitCtrl(5, 0.0, 0.0, KP_J5, KD_J5, tau_cmd)
        # Joints1,2,4,6: hold at 0 rd
        for jid in (1, 2, 4, 6):
            piper.JointMitCtrl(jid, 0.0, 0.0, KP_HOLD, KD_HOLD, 0.0)
        log_data.append([
            f"{t_s:.6f}",
            f"{q[0]:.6f}", f"{q[1]:.6f}", f"{q[2]:.6f}",
            f"{q[3]:.6f}", f"{q[4]:.6f}", f"{q[5]:.6f}",
            f"{tau_fb[0]:.6f}", f"{tau_fb[1]:.6f}", f"{tau_fb[2]:.6f}",
            f"{tau_fb[3]:.6f}", f"{tau_fb[4]:.6f}", f"{tau_fb[5]:.6f}",
            f"{tau_cmd:.6f}"
        ])
        # ramp update (every 100 ms)
        while (t - t_last_ramp) >= RAMP_INTERVAL:
            tau_cmd += TAU_DIR * TAU_STEP
            t_last_ramp += RAMP_INTERVAL
        # 2ms period
        t_next += DT
        sleep_to(t_next)

    try:
        piper.DisablePiper()
    except Exception:
        pass

    print("[DONE]")

    if len(log_data) > 1:
        save_dir = os.path.join(os.path.expanduser("~"), "piper_logs/static_experiments")
        os.makedirs(save_dir, exist_ok=True)
        filename = f"log_joint5_static_experiment_minus{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
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
