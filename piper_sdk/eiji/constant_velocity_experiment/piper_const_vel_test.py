#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import math
import os
import time
from datetime import datetime

from piper_sdk import C_PiperInterface_V2

DT = 0.002  # 2 ms

# User-editable defaults.
CAN_PORT = "can0"
TARGET_JOINT_ID = 2  # 1..6
HOME_POSE_RAD = [0.0, math.radians(60), 0.0, 0.0, 0.0, 0.0]
SPEED_LEVELS_RAD_S = [0.05, 0.06, 0.07, 0.08, 0.09]

# Feedback fields (latest SDK assumption).
ANGLE_FIELD = "pos"
TORQUE_FIELD = "effort"
ANGLE_SCALE = 1e-3
TORQUE_SCALE = 1e-3

RANGE_RAD = math.radians(4.0)
TRAVEL_HALF_RAD = RANGE_RAD / 2.0
RANGE_MARGIN_RAD = math.radians(0.2)

KP_HOLD = 30.0
KD_HOLD = 0.5
KP_TARGET = 30.0
KD_TARGET = 1.0
KP_STOP = 0.0
KD_STOP = 0.0

MOVEJ_SPD_PCT = 30
MIT_SPD_PCT = 100
MIT_SETTLE_SEC = 1.0
RETURN_HOME_SEC = 1.0
MOVEJ_TIMEOUT_SEC = 15.0
MOVE_OFFSET_TIMEOUT_SEC = 5.0

TORQUE_LIMIT_NM = 2.0
OMEGA_LIMIT_RAD_S = 1.5
PRINT_INTERVAL_SEC = 0.1


class ExperimentAbort(RuntimeError):
    pass


def clamp(value: float, v_min: float, v_max: float) -> float:
    return max(v_min, min(v_max, value))


def sleep_to(t_next: float) -> None:
    while True:
        now = time.perf_counter()
        dt = t_next - now
        if dt <= 0:
            return
        time.sleep(min(dt, 0.0005))


def repo_log_dir() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    return os.path.join(repo_root, "piper_logs", "constant_vel_experiments")


def read_highspd_q_tau(piper: C_PiperInterface_V2):
    hs = piper.GetArmHighSpdInfoMsgs()
    motor_infos = [
        hs.motor_1,
        hs.motor_2,
        hs.motor_3,
        hs.motor_4,
        hs.motor_5,
        hs.motor_6,
    ]
    angles_rad = []
    torques_nm = []
    for info in motor_infos:
        angles_rad.append(getattr(info, ANGLE_FIELD) * ANGLE_SCALE)
        torques_nm.append(getattr(info, TORQUE_FIELD) * TORQUE_SCALE)
    return angles_rad, torques_nm


def send_mit_all(
    piper: C_PiperInterface_V2,
    home_pose: list,
    target_id: int,
    pos_ref_target: float,
    vel_ref_target: float,
    kp_target: float,
    kd_target: float,
    t_ref_target: float,
) -> tuple:
    home_target = home_pose[target_id - 1]
    pos_ref_target = clamp(
        pos_ref_target,
        home_target - TRAVEL_HALF_RAD,
        home_target + TRAVEL_HALF_RAD,
    )
    vel_ref_target = clamp(vel_ref_target, -OMEGA_LIMIT_RAD_S, OMEGA_LIMIT_RAD_S)
    t_ref_target = clamp(t_ref_target, -TORQUE_LIMIT_NM, TORQUE_LIMIT_NM)

    for jid in range(1, 7):
        if jid == target_id:
            piper.JointMitCtrl(
                motor_num=jid,
                pos_ref=pos_ref_target,
                vel_ref=vel_ref_target,
                kp=kp_target,
                kd=kd_target,
                t_ref=t_ref_target,
            )
        else:
            piper.JointMitCtrl(
                motor_num=jid,
                pos_ref=home_pose[jid - 1],
                vel_ref=0.0,
                kp=KP_HOLD,
                kd=KD_HOLD,
                t_ref=0.0,
            )
    return pos_ref_target, vel_ref_target, t_ref_target


def soft_stop(
    piper: C_PiperInterface_V2,
    home_pose: list,
    target_id: int,
    duration: float = 0.5,
) -> None:
    t_start = time.perf_counter()
    t_next = t_start
    while time.perf_counter() - t_start < duration:
        for jid in range(1, 7):
            piper.JointMitCtrl(
                motor_num=jid,
                pos_ref=home_pose[jid - 1],
                vel_ref=0.0,
                kp=KP_STOP,
                kd=KD_STOP,
                t_ref=0.0,
            )
        t_next += DT
        sleep_to(t_next)

def hold_home_mit(
    piper: C_PiperInterface_V2,
    home_pose: list,
    target_id: int,
    duration: float,
    offset_rad: float = 0.0,
) -> None:
    t_start = time.perf_counter()
    t_next = t_start
    target_pos = home_pose[target_id - 1] + offset_rad
    while time.perf_counter() - t_start < duration:
        send_mit_all(
            piper=piper,
            home_pose=home_pose,
            target_id=target_id,
            pos_ref_target=target_pos,
            vel_ref_target=0.0,
            kp_target=KP_HOLD,
            kd_target=KD_HOLD,
            t_ref_target=0.0,
        )
        t_next += DT
        sleep_to(t_next)


def move_target_to_offset(
    piper: C_PiperInterface_V2,
    home_pose: list,
    target_id: int,
    offset_rad: float,
    timeout_sec: float = MOVE_OFFSET_TIMEOUT_SEC,
) -> None:
    target_pos = home_pose[target_id - 1] + offset_rad
    t_start = time.perf_counter()
    t_next = t_start
    while True:
        if time.perf_counter() - t_start > timeout_sec:
            raise ExperimentAbort("offset_move_timeout")
        send_mit_all(
            piper=piper,
            home_pose=home_pose,
            target_id=target_id,
            pos_ref_target=target_pos,
            vel_ref_target=0.0,
            kp_target=KP_TARGET,
            kd_target=KD_TARGET,
            t_ref_target=0.0,
        )
        q_rad, _ = read_highspd_q_tau(piper)
        if abs(q_rad[target_id - 1] - target_pos) <= RANGE_MARGIN_RAD:
            return
        t_next += DT
        sleep_to(t_next)


def run_constant_vel_segment(
    piper: C_PiperInterface_V2,
    log_rows: list,
    t0: float,
    home_pose: list,
    target_id: int,
    omega_abs: float,
    dir_sign: int,
    speed_index: int,
    start_offset_rad: float,
    end_offset_rad: float,
) -> None:
    omega_cmd = clamp(dir_sign * omega_abs, -OMEGA_LIMIT_RAD_S, OMEGA_LIMIT_RAD_S)
    start_pos = home_pose[target_id - 1] + start_offset_rad
    end_pos = home_pose[target_id - 1] + end_offset_rad
    min_pos = min(start_pos, end_pos)
    max_pos = max(start_pos, end_pos)
    pos_ref_target = start_pos

    t_prev = time.perf_counter()
    t_next = t_prev
    last_meas_t = None
    last_q_target = None
    last_print_t = None
    while True:
        now = time.perf_counter()
        dt = now - t_prev
        t_prev = now

        pos_ref_target += omega_cmd * dt
        pos_ref_target = clamp(
            pos_ref_target,
            min_pos,
            max_pos,
        )

        pos_ref_target, vel_ref_target, t_ref_target = send_mit_all(
            piper=piper,
            home_pose=home_pose,
            target_id=target_id,
            pos_ref_target=pos_ref_target,
            vel_ref_target=omega_cmd,
            kp_target=KP_TARGET,
            kd_target=KD_TARGET,
            t_ref_target=0.0,
        )

        q_rad, tau_nm = read_highspd_q_tau(piper)
        q_target = q_rad[target_id - 1]
        if last_meas_t is None:
            omega_meas = 0.0
        else:
            dt_meas = now - last_meas_t
            omega_meas = (q_target - last_q_target) / dt_meas if dt_meas > 0 else 0.0
        last_meas_t = now
        last_q_target = q_target
        if q_target < min_pos - RANGE_MARGIN_RAD:
            raise ExperimentAbort("range_exceeded_low")
        if q_target > max_pos + RANGE_MARGIN_RAD:
            raise ExperimentAbort("range_exceeded_high")

        phase = "vel_pos" if dir_sign > 0 else "vel_neg"
        if last_print_t is None or (now - last_print_t) >= PRINT_INTERVAL_SEC:
            print(
                f"[{phase}] idx={speed_index} cmd={omega_cmd:.3f} rad/s "
                f"meas={omega_meas:.3f} rad/s"
            )
            last_print_t = now
        log_rows.append(
            [
                f"{now - t0:.6f}",
                phase,
                speed_index,
                f"{omega_cmd:.6f}",
                dir_sign,
                f"{pos_ref_target:.6f}",
                f"{vel_ref_target:.6f}",
                f"{KP_TARGET:.3f}",
                f"{KD_TARGET:.3f}",
                f"{t_ref_target:.3f}",
            ]
            + [f"{v:.6f}" for v in q_rad]
            + [f"{v:.6f}" for v in tau_nm]
        )

        if end_pos >= start_pos and q_target >= end_pos - RANGE_MARGIN_RAD:
            return
        if end_pos < start_pos and q_target <= end_pos + RANGE_MARGIN_RAD:
            return

        t_next += DT
        sleep_to(t_next)


def main():
    if len(HOME_POSE_RAD) != 6:
        raise ValueError("HOME_POSE_RAD must have 6 elements.")
    if len(SPEED_LEVELS_RAD_S) != 5:
        raise ValueError("SPEED_LEVELS_RAD_S must have 5 elements.")
    if TARGET_JOINT_ID not in range(1, 7):
        raise ValueError("TARGET_JOINT_ID must be in 1..6.")
    home_pose = HOME_POSE_RAD

    piper = C_PiperInterface_V2(CAN_PORT)
    print("Connecting to CAN...")
    piper.ConnectPort()
    time.sleep(0.5)
    if not piper.isOk():
        raise RuntimeError(f"CAN port '{CAN_PORT}' connection failed.")

    print("Enabling Piper...")
    while not piper.EnablePiper():
        time.sleep(0.01)
    time.sleep(0.5)

    log_rows = []
    header = [
        "t_s",
        "phase",
        "speed_index",
        "omega_cmd_rad_s",
        "dir",
        "pos_ref_target",
        "vel_ref_target",
        "kp_target",
        "kd_target",
        "t_ref_target",
        "q1_rad",
        "q2_rad",
        "q3_rad",
        "q4_rad",
        "q5_rad",
        "q6_rad",
        "tau1_nm",
        "tau2_nm",
        "tau3_nm",
        "tau4_nm",
        "tau5_nm",
        "tau6_nm",
    ]
    log_rows.append(header)

    stop_reason = ""
    t0 = time.perf_counter()

    try:
        home_mdeg = [round(rad * 180.0 / math.pi * 1000.0) for rad in home_pose]
        piper.MotionCtrl_2(ctrl_mode=0x01, move_mode=0x01, move_spd_rate_ctrl=MOVEJ_SPD_PCT)
        piper.JointCtrl(*home_mdeg)
        # アームが目標位置に到達するまで待機
        print("移動完了を待っています...")
        while piper.GetArmStatus().arm_status.motion_status != 0x00: # 0x00: 到達完了
            time.sleep(0.1)
        print("初期角度に到達しました。")
        time.sleep(2) # stop for 2 sec

        piper.MotionCtrl_2(
            ctrl_mode=0x01,
            move_mode=0x04,
            move_spd_rate_ctrl=MIT_SPD_PCT,
            is_mit_mode=0xAD,
        )
        hold_home_mit(piper, home_pose, TARGET_JOINT_ID, MIT_SETTLE_SEC)

        for idx, omega in enumerate(SPEED_LEVELS_RAD_S):
            move_target_to_offset(piper, home_pose, TARGET_JOINT_ID, -TRAVEL_HALF_RAD)
            hold_home_mit(
                piper,
                home_pose,
                TARGET_JOINT_ID,
                RETURN_HOME_SEC,
                offset_rad=-TRAVEL_HALF_RAD,
            )
            run_constant_vel_segment(
                piper=piper,
                log_rows=log_rows,
                t0=t0,
                home_pose=home_pose,
                target_id=TARGET_JOINT_ID,
                omega_abs=omega,
                dir_sign=1,
                speed_index=idx,
                start_offset_rad=-TRAVEL_HALF_RAD,
                end_offset_rad=TRAVEL_HALF_RAD,
            )
            move_target_to_offset(piper, home_pose, TARGET_JOINT_ID, TRAVEL_HALF_RAD)
            hold_home_mit(
                piper,
                home_pose,
                TARGET_JOINT_ID,
                RETURN_HOME_SEC,
                offset_rad=TRAVEL_HALF_RAD,
            )
            run_constant_vel_segment(
                piper=piper,
                log_rows=log_rows,
                t0=t0,
                home_pose=home_pose,
                target_id=TARGET_JOINT_ID,
                omega_abs=omega,
                dir_sign=-1,
                speed_index=idx,
                start_offset_rad=TRAVEL_HALF_RAD,
                end_offset_rad=-TRAVEL_HALF_RAD,
            )

    except Exception as exc:
        stop_reason = str(exc)
        print(f"[ABORT] {stop_reason}")
    finally:
        try:
            piper.MotionCtrl_2(
                ctrl_mode=0x01,
                move_mode=0x04,
                move_spd_rate_ctrl=MIT_SPD_PCT,
                is_mit_mode=0xAD,
            )
        except Exception:
            pass
        try:
            soft_stop(piper, home_pose, TARGET_JOINT_ID)
        except Exception:
            pass
        try:
            while piper.DisablePiper():
                time.sleep(0.01)
        except Exception:
            pass

    if len(log_rows) > 1:
        save_dir = os.path.join(os.path.expanduser("~"), "piper_logs/constant_vel_experiments")
        os.makedirs(save_dir, exist_ok=True)
        filename = f"log_joint2_constant_vel_experiment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        full_path = os.path.join(save_dir, filename)
        print(f"データを {full_path} に保存しています...")
        try:
            with open(full_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(log_rows)
            print("保存が完了しました。")
        except IOError as e:
            print(f"ファイルへの書き込みに失敗しました: {e}")
    else:
        print("保存するデータがありません。")


if __name__ == "__main__":
    main()
