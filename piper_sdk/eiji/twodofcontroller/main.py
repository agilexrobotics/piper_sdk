import csv
import time
from datatime import datatime
import numpy as np
from piper_sdk import *
from piper_sdk.eiji.emergency_hold_guard import EmergencyHoldGuard
from piper_sdk.eiji.pinocchio.piper_pinocchio import PiperPinocchio
from scipy.spatial.transform import Rotation as R

"""各パラメータの設定"""
ratio = np.array([0.5, 0.5, 0.5, 2.5, 2.5, 2.5], dtype=float) # 関節トルク補正比率
can_port = "can0" # CAN ポート名


"""角度[rad]を読み取る関数"""
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

"""実験本体"""
def main():
    # ロボットアームモデルのURDFファイルパスを設定（エンドエフェクタの装着状態に合わせて変更）
    # urdf_path = "/home/piper/piper_sdk/piper_sdk/eiji/piper_description/urdf/piper_description.urdf"
    urdf_path = "/home/piper/piper_sdk/piper_sdk/eiji/piper_description/urdf/piper_no_gripper_description.urdf"
    # urdf_path = "/home/piper/piper_sdk/piper_sdk/eiji/piper_description/urdf/piper_description_with_teach.urdf"

    # piperのソルバーを初期化
    pin = PiperPinocchio(urdf_path)

    # 制御周波数
    control_frequency = 200.0
    control_period = 1.0 / control_frequency

    
    joint_ids = range(1, 7)

    # ロボットアームIFを初期化
    piper = C_PiperInterface_V2()
    piper.ConnectPort()  