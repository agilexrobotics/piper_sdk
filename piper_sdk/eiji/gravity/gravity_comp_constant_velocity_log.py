#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import math
import os
import sys
import time
from datetime import datetime
from pathlib import Path
import numpy as np
from scipy.spatial.transform import Rotation as R

if __package__ in (None, ""):
    repo_root = Path(__file__).resolve().parents[3]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from piper_sdk import C_PiperInterface_V2
    from piper_sdk.eiji.emergency_hold_guard import EmergencyHoldGuard
    from piper_sdk.eiji.pinoccio.piper_pinocchio import PiperPinocchio
else:
    from piper_sdk import C_PiperInterface_V2
    from piper_sdk.eiji.emergency_hold_guard import EmergencyHoldGuard
    from ..pinoccio.piper_pinocchio import PiperPinocchio

# -----------------------------
# Parameters (edit as needed)
# -----------------------------
CAN_PORT = "can0"
TARGET_JOINT_ID = 2  # 1..6
TARGET_VELOCITY_RAD_S = 0.10
CONTROL_DURATION_S = 2.0
CONTROL_FREQUENCY_HZ = 200.0
RATIO = np.array([0.5, 0.5, 0.5, 2.5, 2.5, 2.5], dtype=float)

HOME_POSE_RAD = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
KP_TARGET = 350.0
KD_TARGET = 10.0
MOVEJ_SPEED_PERCENT = 30
MIT_SPEED_PERCENT = 100
TORQUE_LIMIT_NM = 18.0
KP_END_HOLD = 30.0
KD_END_HOLD = 0.8

def _read_joint_state(piper, joint_angles: np.ndarray, joint_velocities: np.ndarray | None = None):
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
        if joint_velocities is not None:
            joint_velocities[idx] = motor.motor_speed * 1e-3


def main():
    if TARGET_JOINT_ID not in range(1, 7):
        raise ValueError("TARGET_JOINT_ID must be in [1, 6].")
    if len(HOME_POSE_RAD) != 6:
        raise ValueError("HOME_POSE_RAD must have 6 values.")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    urdf_path = os.path.join(
        script_dir, "piper_description", "urdf", "piper_no_gripper_description.urdf"
    )
    if not os.path.exists(urdf_path):
        raise FileNotFoundError(f"URDF が見つかりません: {urdf_path}")

    pin = PiperPinocchio(urdf_path)
    roll, pitch, yaw = 0, 0, 0
    R_world_base = R.from_euler('xyz', [roll, pitch, yaw], degrees=True).as_matrix()
    pin.set_base_orientation(R_world_base)

    piper = C_PiperInterface_V2(CAN_PORT)
    rows = []
    header = [
        "t_s",
        "q_ref_target_rad",
        "omega_ref_target_rad_s",
        "q_target_rad",
        "qd_target_rad_s",
        "tau_ff_target_nm",
        "tau_pd_target_nm",
        "tau_total_target_model_nm",
        "tau_total_target_actual_nm",
    ]
    rows.append(header)

    dt = 1.0 / CONTROL_FREQUENCY_HZ
    target_idx = TARGET_JOINT_ID - 1
    omega_ref = TARGET_VELOCITY_RAD_S
    joint_ids = range(1, 7)
    joint_angles = np.zeros(6, dtype=float)
    joint_velocities = np.zeros(6, dtype=float)
    q_ref_vec = np.zeros(6, dtype=float)
    qd_ref_vec = np.zeros(6, dtype=float)
    pd_input = np.zeros(6, dtype=float)

    try:
        piper = C_PiperInterface_V2(CAN_PORT)
        piper.ConnectPort()
        piper.EnablePiper()
        time.sleep(0.1)

        with EmergencyHoldGuard(piper, kp=KP_END_HOLD, kd=KD_END_HOLD, mit_speed_percent=MIT_SPEED_PERCENT):
            print("初期位置に移動")
            piper.MotionCtrl_2(ctrl_mode=0x01, move_mode=0x01, move_spd_rate_ctrl=MOVEJ_SPEED_PERCENT)
            initial_angles_mdeg = [int(pos * 180 / math.pi * 1000) for pos in HOME_POSE_RAD]
            piper.JointCtrl(*initial_angles_mdeg)

            print("MITモードに変更")
            piper.MotionCtrl_2(
                ctrl_mode=0x01,
                move_mode=0x04,
                move_spd_rate_ctrl=MIT_SPEED_PERCENT,
                is_mit_mode=0xAD,
            )
            time.sleep(0.2)

            _read_joint_state(piper, joint_angles, joint_velocities)
            q_ref_start = float(joint_angles[target_idx])

            # 一定周期のサンプル時刻と、その時刻に対応する目標角を事前生成する
            num_samples = max(1, int(round(CONTROL_DURATION_S * CONTROL_FREQUENCY_HZ)))
            sample_times = np.arange(num_samples, dtype=float) * dt
            q_ref_targets = q_ref_start + omega_ref * sample_times

            t0 = time.perf_counter()
            print(f"[INFO] Start logging ({num_samples} samples)")
            for q_ref_target in q_ref_targets:
                start_time = time.perf_counter()
                
                # 現在姿勢から重力補償トルクと慣性行列を計算する
                _read_joint_state(piper, joint_angles, joint_velocities)
                tau_ff = pin.gravity_compensation(joint_angles)
                mass_matrix = pin.mass_matrix(joint_angles)

                q_ref_vec[:] = joint_angles
                q_ref_vec[target_idx] = q_ref_target
                qd_ref_vec.fill(0.0)
                qd_ref_vec[target_idx] = omega_ref

                pd_input.fill(0.0)
                pd_input[target_idx] = (
                    KP_TARGET * (q_ref_vec[target_idx] - joint_angles[target_idx])
                    + KD_TARGET * (qd_ref_vec[target_idx] - joint_velocities[target_idx])
                )
                tau_pd = mass_matrix @ pd_input
                tau_total_model = tau_ff[:6] + tau_pd[:6]
                tau_total_actual = np.clip(RATIO * tau_total_model, -TORQUE_LIMIT_NM, TORQUE_LIMIT_NM)

                # MITモード指令をループ内で送る
                piper.MotionCtrl_2(
                    ctrl_mode=0x01,
                    move_mode=0x04,
                    move_spd_rate_ctrl=MIT_SPEED_PERCENT,
                    is_mit_mode=0xAD,
                )
                now = time.perf_counter()
                t_elapsed = now - t0
                
                for joint_id in joint_ids:
                    piper.JointMitCtrl(
                        motor_num=joint_id,
                        pos_ref=0.0,
                        vel_ref=0.0,
                        kp=0.0,
                        kd=0.0,
                        t_ref=float(tau_total_actual[joint_id - 1]),
                    )

                rows.append(
                    [
                        f"{t_elapsed:.6f}",
                        f"{q_ref_target:.6f}",
                        f"{omega_ref:.6f}",
                        f"{joint_angles[target_idx]:.6f}",
                        f"{joint_velocities[target_idx]:.6f}",
                        f"{tau_ff[target_idx]:.6f}",
                        f"{tau_pd[target_idx]:.6f}",
                        f"{tau_total_model[target_idx]:.6f}",
                        f"{tau_total_actual[target_idx]:.6f}",
                    ]
                )
                
                # 制御周期を維持
                t = time.perf_counter() - start_time
                sleep_time = dt - t
                if sleep_time > 0:
                    time.sleep(sleep_time)
    
            print("[INFO] Motion finished. Hold current pose and exit.")

    except KeyboardInterrupt:
        print("[INFO] KeyboardInterrupt: 終了時に現在角度保持を実行します。")
    except Exception as exc:
        print(f"[ERROR] 実験中に例外が発生: {exc}")
    finally:
        try:
            piper.DisconnectPort()
        except Exception:
            pass

        if len(rows) > 1:
            save_dir = os.path.abspath(os.path.join(script_dir, "..", "data"))
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(
                save_dir,
                f"log_gravity_comp_const_vel_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            )
            with open(save_path, "w", newline="", encoding="utf-8") as fp:
                writer = csv.writer(fp)
                writer.writerows(rows)
            print(f"[INFO] Saved: {save_path}")
        else:
            print("[INFO] 保存するログがありません。")


if __name__ == "__main__":
    main()
