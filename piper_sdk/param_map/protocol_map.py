#!/usr/bin/env python3
# -*-coding:utf8-*-
from enum import IntEnum, auto

class EmergencyStopMode(IntEnum):
    """紧急停止模式"""

    NORMAL = 0x00  # 正常运行模式
    EMERGENCY_STOP = 0x01  # 急停模式
    CLEAR_STOP = 0x02  # 清除急停状态


class TrackCtrlMode(IntEnum):
    """轨迹控制模式"""

    IDLE = 0x00  # 停止/空闲
    INIT = 0x01  # 初始化
    START = 0x02  # 开始
    PAUSE = 0x03  # 暂停
    RESUME = 0x04  # 恢复
    CLEAR = 0x05  # 清除
    RESTART = 0x06  # 重新开始
    RESUME_FROM_PAUSE = 0x07  # 从暂停点继续
    TRACK_STOP = 0x08  # 停止轨迹


class GragTeachCtrlMode(IntEnum):
    """拖动示教控制模式"""

    IDLE = 0x00  # 停止/空闲
    START = 0x01  # 开始
    SAVE = 0x02  # 保存
    CLEAR = 0x03  # 清除
    TEACH_STOP = 0x04  # 停止示教
    START_AT_CURRENT_POS = 0x05  # 从当前位置开始
    SWITCH_TO_PRE_POINT = 0x06  # 切换到上一个点
    SWITCH_TO_NEXT_POINT = 0x07  # 切换到下一个点


class CtrlMode(IntEnum):
    """控制模式"""

    IDLE = 0x00  # 停止/空闲
    JOINT_CTRL = 0x01  # 关节控制
    MIN_JERK = 0x03  # 最小加加速度模式
    CARTESIAN_CTRL = 0x04  # 笛卡尔空间控制
    EXTERNAL_FORCE_CTRL = 0x07  # 外部力控制


class MoveMode(IntEnum):
    """运动模式"""

    IDLE = 0x00  # 停止/空闲
    JOINT_SPACE = 0x01  # 关节空间
    CARTESIAN_LINEAR = 0x02  # 笛卡尔空间线性
    CARTESIAN_CIRCULAR = 0x03  # 笛卡尔空间圆弧
    CARTESIAN_CONTINOUS = 0x04  # 笛卡尔空间连续


class MITMode(IntEnum):
    """MIT模式"""

    DISABLED = 0x00  # 禁用
    ENABLED = 0xAD  # 启用
    USER_DEFINED = 0xFF  # 用户自定义


class InstallationPosition(IntEnum):
    """安装位置"""

    DESKTOP = 0x00  # 桌面安装
    WALL = 0x01  # 墙面安装
    CEILING = 0x02  # 天花板安装
    ANGLE = 0x03  # 角度安装


class InstructionNum(IntEnum):
    """指令点序号（圆弧轨迹）"""

    INVALID = 0x00  # 无效
    START_POINT = 0x01  # 起点
    MID_POINT = 0x02  # 中点
    END_POINT = 0x03  # 终点


class GripperCode(IntEnum):
    """夹爪控制代码"""

    NORMAL = 0x00  # 正常控制
    MAX_FORCE = 0x01  # 最大力控制
    HOLD_POSITION = 0x02  # 保持位置
    OPEN_FULLY = 0x03  # 完全打开


class SetZeroFlag(IntEnum):
    """设置零点标志"""

    DISABLE = 0x00  # 禁用
    ENABLE = 0xAE  # 启用


class MotorNum(IntEnum):
    """电机编号"""

    MOTOR_1 = 1  # 电机1
    MOTOR_2 = 2  # 电机2
    MOTOR_3 = 3  # 电机3
    MOTOR_4 = 4  # 电机4
    MOTOR_5 = 5  # 电机5
    MOTOR_6 = 6  # 电机6
    GRIPPER = 7  # 夹爪
    ALL_MOTORS = 0xFF  # 所有电机


class EnableFlag(IntEnum):
    """使能标志"""

    DISABLE = 0x01  # 禁用
    ENABLE = 0x02  # 使能


class SearchContent(IntEnum):
    """搜索内容"""

    ANGLE_LIMIT_MAX_SPEED = 0x01  # 角度限制/最大速度
    MAX_ACCELERATION = 0x02  # 最大加速度


class InvalidValue(IntEnum):
    """无效值标志（V1.5-2版本后）"""

    INVALID = 0x7FFF  # 无效设定数值


class ParamEnquiry(IntEnum):
    """参数查询"""

    IDLE = 0x00  # 空闲
    END_VEL_ACC_PARAM = 0x01  # 末端速度/加速度参数
    JOINT_LIMIT_PARAM = 0x02  # 关节限制参数
    CRASH_PROTECTION_PARAM = 0x03  # 碰撞保护参数
    GRIPPER_TEACHING_PARAM = 0x04  # 夹爪/示教参数


class ParamSetting(IntEnum):
    """参数设置"""

    IDLE = 0x00  # 空闲
    END_VEL_ACC_PARAM = 0x01  # 末端速度/加速度参数初始值
    JOINT_LIMIT_PARAM = 0x02  # 所有关节限制及速度加速度默认值


class DataFeedback(IntEnum):
    """数据反馈"""

    IDLE = 0x00  # 空闲
    ENABLE = 0x01  # 启用
    DISABLE = 0x02  # 禁用


class EndLoadParamSetting(IntEnum):
    """末端负载参数设置"""

    DISABLE = 0x00  # 禁用
    ENABLE = 0xAE  # 启用


class SetEndLoad(IntEnum):
    """设置末端负载"""

    IDLE = 0x00  # 空闲
    LOAD_PARAM_1 = 0x01  # 负载参数1
    LOAD_PARAM_2 = 0x02  # 负载参数2
    ALL_LOAD_PARAM = 0x03  # 所有负载参数

class PiperParamMap:
    """参数映射类，提供对所有枚举的集中访问"""

    EmergencyStopMode = EmergencyStopMode
    TrackCtrlMode = TrackCtrlMode
    GragTeachCtrlMode = GragTeachCtrlMode
    CtrlMode = CtrlMode
    MoveMode = MoveMode
    MITMode = MITMode
    InstallationPosition = InstallationPosition
    InstructionNum = InstructionNum
    GripperCode = GripperCode
    SetZeroFlag = SetZeroFlag
    MotorNum = MotorNum
    EnableFlag = EnableFlag
    SearchContent = SearchContent
    InvalidValue = InvalidValue
    ParamEnquiry = ParamEnquiry
    ParamSetting = ParamSetting
    DataFeedback = DataFeedback
    EndLoadParamSetting = EndLoadParamSetting
    SetEndLoad = SetEndLoad
