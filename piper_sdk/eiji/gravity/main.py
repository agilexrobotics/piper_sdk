#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import csv
import time
from datetime import datetime
from pathlib import Path
import numpy as np
from piper_sdk import *
from piper_sdk.eiji.emergency_hold_guard import EmergencyHoldGuard
from piper_sdk.eiji.pinocchio.piper_pinocchio import PiperPinocchio
from scipy.spatial.transform import Rotation as R

# 関節トルク補正比率（実機に合わせて調整）
ratio = np.array([0.5, 0.5, 0.5, 2.5, 2.5, 2.5], dtype=float)

def _read_joint_state(piper, joint_angles: np.ndarray):
    high_spd_msg = piper.GetArmHighSpdInfoMsgs()
    motors = (
        high_spd_msg.motor_1,
        high_spd_msg.motor_2,
        high_spd_msg.motor_3,
        high_spd_msg.motor_4,
        high_spd_msg.motor_5,
        high_spd_msg.motor_6,
    )
    for idx, motor in enumerate(motors):
        joint_angles[idx] = motor.pos * 1e-3


def _read_joint_effort(piper, joint_effort: np.ndarray):
    high_spd_msg = piper.GetArmHighSpdInfoMsgs()
    motors = (
        high_spd_msg.motor_1,
        high_spd_msg.motor_2,
        high_spd_msg.motor_3,
        high_spd_msg.motor_4,
        high_spd_msg.motor_5,
        high_spd_msg.motor_6,
    )
    for idx, motor in enumerate(motors):
        # SDK effort is current-converted torque in 0.001 N*m
        joint_effort[idx] = 2 * motor.effort * 1e-3 /  ratio[idx]


def main():
    # ロボットアームモデルのURDFファイルパスを設定（エンドエフェクタの装着状態に合わせて変更）
    # urdf_path = "/home/piper/piper_sdk/piper_sdk/eiji/piper_description/urdf/piper_description.urdf"
    urdf_path = "/home/piper/piper_sdk/piper_sdk/eiji/piper_description/urdf/piper_no_gripper_description.urdf"
    # urdf_path = "/home/piper/piper_sdk/piper_sdk/eiji/piper_description/urdf/piper_description_with_teach.urdf"

    # 逆運動学ソルバを初期化（重力補償計算用）
    pin = PiperPinocchio(urdf_path)

    # 制御周波数
    control_frequency = 200.0
    control_period = 1.0 / control_frequency

    
    joint_ids = range(1, 7)

    # ロボットアームIFを初期化
    piper = C_PiperInterface_V2()
    piper.ConnectPort()
    piper.EnablePiper()
    time.sleep(0.1)

    joint_angles = np.zeros(6, dtype=float)
    measured_torque = np.zeros(6, dtype=float)
    _read_joint_state(piper, joint_angles)

    # 世界座標系から基座座標系への回転行列を計算
    roll, pitch, yaw = 0, 0, 0
    R_world_base = R.from_euler('xyz', [roll, pitch, yaw], degrees=True).as_matrix()
    pin.set_base_orientation(R_world_base)

    log_dir = Path(__file__).resolve().parent.parent / "data"
    log_dir.mkdir(parents=True, exist_ok=True)
    csv_path = log_dir / f"log_gravity_cmd_torque_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    print("重力補償制御ループを開始します...")
    print(f"保存先CSV: {csv_path}")
    last_overrun_warn_time = 0.0
    try:
        with EmergencyHoldGuard(piper):
            with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([
                    "time_s",
                    "tau_cmd_j1", "tau_cmd_j2", "tau_cmd_j3",
                    "tau_cmd_j4", "tau_cmd_j5", "tau_cmd_j6",
                    "tau_meas_j1", "tau_meas_j2", "tau_meas_j3",
                    "tau_meas_j4", "tau_meas_j5", "tau_meas_j6",
                ])
                csv_file.flush()
                log_start_time = time.perf_counter()
                last_csv_flush_time = log_start_time

                while True:
                    start_time = time.perf_counter()

                    # 現在の関節角度を取得
                    _read_joint_state(piper, joint_angles)
                    # 重力補償トルクを計算
                    gravity_torque = pin.gravity_compensation(joint_angles)
                    actual_torque = np.full(6, np.nan, dtype=float)

                    now = time.perf_counter()
                    if now - last_csv_flush_time >= 1.0:
                        csv_file.flush()
                        last_csv_flush_time = now

                    # 重力補償トルクを適用
                    try:
                        piper.MotionCtrl_2(0x01, 0x04, 0, 0xAD)
                        actual_torque = np.clip(ratio * gravity_torque[:6], -18.0, 18.0)
                        for joint_id, torque in zip(joint_ids, actual_torque):
                            piper.JointMitCtrl(joint_id, 0, 0, 0, 0, float(torque))

                    except Exception as e:
                        print(f"重力補償の適用に失敗しました: {e}")

                    _read_joint_effort(piper, measured_torque)
                    writer.writerow([
                        time.perf_counter() - log_start_time,
                        *gravity_torque.tolist(),
                        *measured_torque.tolist(),
                    ])

                    # 制御周波数を維持
                    elapsed_time = time.perf_counter() - start_time
                    if elapsed_time < control_period:
                        time.sleep(control_period - elapsed_time)
                    else:
                        if now - last_overrun_warn_time >= 1.0:
                            print(f"警告: 制御ループが時間超過です {elapsed_time:.3f}s > {control_period:.3f}s")
                            last_overrun_warn_time = now
    except KeyboardInterrupt:
        print("\nユーザー中断により、重力補償を停止します")
    except Exception as e:
        print(f"プログラム実行中にエラーが発生しました: {e}")
    finally:
        try:
            piper.DisconnectPort()
        except Exception:
            pass


if __name__ == "__main__":
    main()
