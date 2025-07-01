from typing import Tuple
import math
from typing_extensions import (
    Literal,
)

# 定义欧拉角顺序编码表
_AXES2TUPLE = {
    'sxyz': (0, 0, 0, 0),
    'rzyx': (0, 0, 0, 1),
}
axes = 'sxyz'
# 用于轴索引计算
_NEXT_AXIS = [1, 2, 0, 1]
# 设置浮点比较误差阈值
_EPS = 1e-10

def normalize_quat(qx, qy, qz, qw):
    norm = math.sqrt(qx**2 + qy**2 + qz**2 + qw**2)
    return qx / norm, qy / norm, qz / norm, qw / norm

def quat_convert_euler(qx: float, qy: float, qz: float, qw: float) -> Tuple[float, float, float]:
                    #    axes: Literal['sxyz', 'rzyx'] = 'sxyz') -> Tuple[float, float, float]:
    """
    将四元数 [x, y, z, w] 转换为欧拉角 (roll, pitch, yaw)。

    参数:
        x, y, z, w - 四元数各分量
        axes - 欧拉角轴顺序，支持 'sxyz' 或 'rzyx'

    返回:
        tuple(float, float, float): 欧拉角 (roll, pitch, yaw)，单位为弧度
    """
    
    # 轴顺序设置
    try:
        firstaxis, parity, repetition, frame = _AXES2TUPLE[axes.lower()]
    except (KeyError, AttributeError):
        raise ValueError(f"Unsupported axes specification: '{axes}'. "
                        f"Only 'sxyz' and 'rzyx' are currently supported.")
    # 轴索引对应 x=0, y=1, z=2
    # 获取轴顺序索引
    i = firstaxis
    j = _NEXT_AXIS[i + parity]
    k = _NEXT_AXIS[i - parity + 1]
    qx, qy, qz, qw = normalize_quat(qx, qy, qz, qw)
    # 矩阵 M[i][j] 表达方式：预先展开 3x3 旋转矩阵
    M = [[0.0] * 3 for _ in range(3)]
    M[0][0] = 1 - 2*(qy**2 + qz**2)
    M[0][1] =     2*(qx*qy - qz*qw)
    M[0][2] =     2*(qx*qz + qy*qw)
    M[1][0] =     2*(qx*qy + qz*qw)
    M[1][1] = 1 - 2*(qx**2 + qz**2)
    M[1][2] =     2*(qy*qz - qx*qw)
    M[2][0] =     2*(qx*qz - qy*qw)
    M[2][1] =     2*(qy*qz + qx*qw)
    M[2][2] = 1 - 2*(qx**2 + qy**2)

    # 计算欧拉角
    if repetition:
        sy = math.sqrt(M[i][j] ** 2 + M[i][k] ** 2)
        if sy > _EPS:
            ax = math.atan2(M[i][j], M[i][k])
            ay = math.atan2(sy, M[i][i])
            az = math.atan2(M[j][i], -M[k][i])
        else:
            ax = math.atan2(-M[j][k], M[j][j])
            ay = math.atan2(sy, M[i][i])
            az = 0.0
    else:
        cy = math.sqrt(M[i][i] ** 2 + M[j][i] ** 2)
        if cy > _EPS:
            ax = math.atan2(M[k][j], M[k][k])
            ay = math.atan2(-M[k][i], cy)
            az = math.atan2(M[j][i], M[i][i])
        else:
            ax = math.atan2(-M[j][k], M[j][j])
            ay = math.atan2(-M[k][i], cy)
            az = 0.0

    # 调整角度方向
    if parity:
        ax, ay, az = -ax, -ay, -az
    if frame:
        ax, az = az, ax

    return ax, ay, az

def euler_convert_quat(roll:float, pitch:float, yaw:float)->Tuple[float, float, float, float]:
    """
    将欧拉角（roll, pitch, yaw）转换为四元数。

    参数:
        roll  - 绕X轴旋转角（单位：弧度）
        pitch - 绕Y轴旋转角（单位：弧度）
        yaw   - 绕Z轴旋转角（单位：弧度）

    返回:
        list: 四元数 [x, y, z, w]
    """
    
    try:
        firstaxis, parity, repetition, frame = _AXES2TUPLE[axes.lower()]
    except (KeyError, AttributeError):
        raise ValueError(f"Unsupported axes specification: '{axes}'. "
                        f"Only 'sxyz' and 'rzyx' are currently supported.")
    # 轴索引对应 x=0, y=1, z=2
    # 获取轴顺序索引
    i = firstaxis
    j = _NEXT_AXIS[i + parity]
    k = _NEXT_AXIS[i - parity + 1]

    # 坐标系调整
    if frame:
        roll, yaw = yaw, roll
    if parity:
        pitch = -pitch

    # 角度减半
    roll *= 0.5
    pitch *= 0.5
    yaw *= 0.5

    # 三角函数
    c_roll = math.cos(roll)
    s_roll = math.sin(roll)
    c_pitch = math.cos(pitch)
    s_pitch = math.sin(pitch)
    c_yaw = math.cos(yaw)
    s_yaw = math.sin(yaw)

    cc = c_roll * c_yaw
    cs = c_roll * s_yaw
    sc = s_roll * c_yaw
    ss = s_roll * s_yaw

    # 初始化四元数 [x, y, z, w]
    q = [0.0, 0.0, 0.0, 0.0]

    if repetition:
        q[i] = c_pitch * (cs + sc)
        q[j] = s_pitch * (cc + ss)
        q[k] = s_pitch * (cs - sc)
        q[3] = c_pitch * (cc - ss)
    else:
        q[i] = c_pitch * sc - s_pitch * cs
        q[j] = c_pitch * ss + s_pitch * cc
        q[k] = c_pitch * cs - s_pitch * sc
        q[3] = c_pitch * cc + s_pitch * ss

    if parity:
        q[j] *= -1

    return q[0], q[1], q[2], q[3]  # [qx, qy, qz, qw]