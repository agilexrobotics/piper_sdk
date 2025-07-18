from ..utils import quat_convert_euler, euler_convert_quat
from ..interface.piper_interface_v2 import C_PiperInterface_V2
from ..piper_msgs.msg_v2 import ArmMsgFeedbackStatusEnum
from ..utils import *
from ..utils import logger, global_area
from typing import Tuple, Optional, Literal
import threading
import math

class Piper():
    _instances = {}  # 存储不同参数的实例
    _lock = threading.Lock()

    def __new__(cls, 
                can_name:str="can0"):
        """
        实现单例模式：
        - 相同 can_name参数，只会创建一个实例
        - 不同参数，允许创建新的实例
        """
        key = (can_name)  # 生成唯一 Key
        with cls._lock:
            if key not in cls._instances:
                instance = super().__new__(cls)  # 创建新实例
                instance._initialized = False  # 确保 init 只执行一次
                cls._instances[key] = instance  # 存入缓存
        return cls._instances[key]
    
    def __init__(self, 
                 can_name: str = "can0") -> None:
        if getattr(self, "_initialized", False): 
            return  # 避免重复初始化
        self.__local_area = self._instances
        self.logger = LogManager.get_logger(global_area, self.__local_area)
        self._interface:C_PiperInterface_V2
        self.__can_name = can_name

        # 有关interface的参数
        self.__can_validation: bool = True
        self.__can_auto_init: bool = True
        self.__dh_is_offset: int = 1
        self.__start_soft_joint_limit: bool = False
        self.__start_soft_gripper_limit: bool = False
        self.__log_level = LogLevel.WARNING
        self.__high_follow_mode = 0

        # 屏蔽控制输出
        self.__is_enable_ctrl = True

        # 夹爪有关参数
        self.__gripper_val = 0
        self.__effort = 0
        self.__enable_code = 0x02
    
    def init(self):
        self._interface = C_PiperInterface_V2(
            can_name=self.__can_name,
            judge_flag=self.__can_validation,
            can_auto_init=self.__can_auto_init,
            dh_is_offset=self.__dh_is_offset,
            start_sdk_joint_limit=self.__start_soft_joint_limit,
            start_sdk_gripper_limit=self.__start_soft_gripper_limit,
            logger_level=self.__log_level
        )
        return self._interface

    def init_can_validation_on(self):
        self.__can_validation: bool = True
    
    def init_can_validation_off(self):
        self.__can_validation: bool = False
    
    def get_can_validation_status(self):
        return self.__can_validation
    
    # def init_can_auto_init_on(self):
    #     self.__can_auto_init: bool = True
    
    # def init_can_auto_init_off(self):
    #     self.__can_auto_init: bool = False
    
    # def get_can_auto_init_status(self):
    #     return self.__can_auto_init
    
    def init_soft_joint_limit_on(self):
        self.__start_soft_joint_limit: bool = True
    
    def init_soft_joint_limit_off(self):
        self.__start_soft_joint_limit: bool = False

    def get_soft_joint_limit_status(self):
        return self.__start_soft_joint_limit

    def init_soft_gripper_limit_on(self):
        self.__start_soft_gripper_limit: bool = True

    def init_soft_gripper_limit_off(self):
        self.__start_soft_gripper_limit: bool = False

    def get_soft_gripper_limit_status(self):
        return self.__start_soft_gripper_limit
    
    def init_log_level(self, log_level:LogLevel = LogLevel.WARNING):
        self.__log_level = log_level
    
    def get_log_level(self):
        return self.__log_level

    def init_high_follow_mode_on(self):
        self.__high_follow_mode = 0xad
    
    def init_high_follow_mode_off(self):
        self.__high_follow_mode = 0
    
    def get_high_follow_mode_status(self):
        if self.__high_follow_mode == 0:
            return False
        else: return True
    
    def connect(self):
        self._interface.ConnectPort()
        return self._interface.get_connect_status()

    def enable_arm(self):
        self.enable_ctrl_output()
        return self._interface.EnablePiper()

    def disable_arm(self):
        self.disable_ctrl_output()
        status = self._interface.DisablePiper()
        self._interface.EmergencyStop(0x02)
        return status

    def enable_ctrl_output(self):
        self.__is_enable_ctrl = True
        return self.__is_enable_ctrl

    def disable_ctrl_output(self):
        self.__is_enable_ctrl = False
        return self.__is_enable_ctrl    
    
    def get_ctrl_output_status(self):
        return self.__is_enable_ctrl

    def move_to_home(self):
        # 只有在开启控制时才会下发控制指令
        if self.get_ctrl_output_status():
            # 若打开读取线程
            if self._interface.get_connect_status():
                enable_list = self._interface.GetArmEnableStatus()
                # 只有使能成功状态下才会发送控制消息
                if(all(enable_list)):
                    if(self._interface.GetArmStatus().arm_status.ctrl_mode == ArmMsgFeedbackStatusEnum.CtrlMode.TEACHING_MODE):
                        self.logger.warning("[move_to_home] Arm is in the TEACHING_MODE, please run disable_arm()")
                        return
                    self.__move_j((0.0,)*6, 30)
                # 检测到未使能，打印log
                else: 
                    self.logger.warning("[move_to_home] Arm is not enable!!!")
                    self.logger.warning("[move_to_home] Arm enable status is %s", enable_list)
            # 若没有打开读取线程，不检测使能状态直接发送控制消息
            else:
                self.__move_j((0.0,)*6, 30)

    def get_joint_states(self) -> Tuple[Tuple[float, float, float, float, float, float], float, float]:
        if self._interface.get_connect_status():
            tmp = self._interface.GetArmJointMsgs()
            result = (
                round(math.radians(tmp.joint_state.joint_1 / 1000), 6),
                round(math.radians(tmp.joint_state.joint_2 / 1000), 6),
                round(math.radians(tmp.joint_state.joint_3 / 1000), 6),
                round(math.radians(tmp.joint_state.joint_4 / 1000), 6),
                round(math.radians(tmp.joint_state.joint_5 / 1000), 6),
                round(math.radians(tmp.joint_state.joint_6 / 1000), 6),
            )
            return result, tmp.time_stamp, tmp.Hz
        else: 
            self.logger.warning("[get_joint_states] Read thread not opened")
            return (0.0,) * 6, 0.0, 0.0
        
    def get_gripper_states(self) -> Tuple[Tuple[float, float], float, float]:
        if self._interface.get_connect_status():
            tmp = self._interface.GetArmGripperMsgs()
            result = (
                round(tmp.gripper_state.grippers_angle / 1e6, 6),
                round(tmp.gripper_state.grippers_effort / 1000, 6),
            )
            return result, tmp.time_stamp, tmp.Hz
        else:
            self.logger.warning("[get_gripper_states] Read thread not opened")
            return (0.0) * 2, 0.0, 0.0
    
    def __move_j(self,
                    joint_states: Tuple[float, float, float, float, float, float], 
                    v:int):
        # 检查 joint_states 长度是否为6
        if len(joint_states) != 6:
            raise ValueError(f"[move_j] joint_states must contain 6 elements, got {len(joint_states)}")
        # 检查 v 是否是 [0, 100]
        if not isinstance(v, int) or v < 0 or v > 100:
            raise ValueError(f"[move_j] Speed v must be an int in [0,100], got {v}")
        # v = round(int(max(0, min(v, 100))))
        # 弧度 -> 度 -> 0.001度整数
        joint_cmd = [int(round(math.degrees(j) * 1000)) for j in joint_states]
        self._interface.ModeCtrl(0x01, 0x01, v, self.__high_follow_mode)
        self._interface.JointCtrl(
            joint_cmd[0],
            joint_cmd[1],
            joint_cmd[2],
            joint_cmd[3],
            joint_cmd[4],
            joint_cmd[5]
        )

    def move_j(self,
                    joint_states: Tuple[float, float, float, float, float, float], 
                    v:int):
        # 只有在开启控制时才会下发控制指令
        if self.get_ctrl_output_status():
            # 若打开读取线程
            if self._interface.get_connect_status():
                enable_list = self._interface.GetArmEnableStatus()
                # 只有使能成功状态下才会发送控制消息
                if(all(enable_list)):
                    if(self._interface.GetArmStatus().arm_status.ctrl_mode == ArmMsgFeedbackStatusEnum.CtrlMode.TEACHING_MODE):
                        self.logger.warning("[move_j] Arm is in the TEACHING_MODE, please run disable_arm()")
                        return
                    self.__move_j(joint_states, v)
                # 检测到未使能，打印log
                else: 
                    self.logger.warning("[move_j] Arm is not enable!!!")
                    self.logger.warning("[move_j] Arm enable status is %s", enable_list)
            # 若没有打开读取线程，不检测使能状态直接发送控制消息
            else:
                self.__move_j(joint_states, v)
    
    def get_end_pose_euler(self) -> Tuple[Tuple[float, float, float, float, float, float], float, float]:
        if self._interface.get_connect_status():
            tmp = self._interface.GetArmEndPoseMsgs()
            result = (
                round(tmp.end_pose.X_axis / 1000, 6),
                round(tmp.end_pose.Y_axis / 1000, 6),
                round(tmp.end_pose.Z_axis / 1000, 6),
                round(math.radians(tmp.end_pose.RX_axis / 1000), 6),
                round(math.radians(tmp.end_pose.RY_axis / 1000), 6),
                round(math.radians(tmp.end_pose.RZ_axis / 1000), 6),
            )
            return result, tmp.time_stamp, tmp.Hz
        else: 
            self.logger.warning("[get_end_pose_euler] Read thread not opened")
            return (0.0,) * 6
    
    def get_end_pose_quat(self) -> Tuple[float, float, float, float, float, float, float]:
        if self._interface.get_connect_status():
            tmp = self._interface.GetArmEndPoseMsgs()
            quat = euler_convert_quat(
                math.radians(tmp.end_pose.RX_axis / 1000),
                math.radians(tmp.end_pose.RY_axis / 1000),
                math.radians(tmp.end_pose.RZ_axis / 1000),
            )
            # quat = [round(q, 8) for q in quat]
            result = (
                round(tmp.end_pose.X_axis / 1000, 6),
                round(tmp.end_pose.Y_axis / 1000, 6),
                round(tmp.end_pose.Z_axis / 1000, 6),
                quat[0],
                quat[1],
                quat[2],
                quat[3],
            )
            return result, tmp.time_stamp, tmp.Hz
        else: 
            self.logger.warning("[get_end_pose_euler] Read thread not opened")
            return (0.0,) * 7

    def __move_p(self,
                    x: float,
                    y: float,
                    z: float,
                    rx: float,
                    ry: float,
                    rz: float,
                    v:int):
        # 检查 v 是否是 [0, 100]
        if not isinstance(v, int) or v < 0 or v > 100:
            raise ValueError(f"[move_p] Speed v must be an int in [0,100], got {v}")
        x = int(round(x * 1e6))
        y = int(round(y * 1e6))
        z = int(round(z * 1e6))
        rx = int(round(math.degrees(rx) * 1000))
        ry = int(round(math.degrees(ry) * 1000))
        rz = int(round(math.degrees(rz) * 1000))
        self._interface.ModeCtrl(0x01, 0x00, v, self.__high_follow_mode)
        self._interface.EndPoseCtrl(x, y, z, rx, ry, rz)

    def move_p_euler(self, 
                        x: float,
                        y: float,
                        z: float,
                        roll: float,
                        pitch: float,
                        yaw: float,
                        v:int):
        # 只有在开启控制时才会下发控制指令
        if self.get_ctrl_output_status():
            # 若打开读取线程
            if self._interface.get_connect_status():
                enable_list = self._interface.GetArmEnableStatus()
                # 只有使能成功状态下才会发送控制消息
                if(all(enable_list)):
                    self.__move_p(x, y, z, roll, pitch, yaw, v)
                # 检测到未使能，打印log
                else: 
                    self.logger.warning("[move_p] Arm is not enable!!!")
                    self.logger.warning("[move_p] Arm enable status is is %s", enable_list)
            # 若没有打开读取线程，不检测使能状态直接发送控制消息
            else:
                self.__move_p(x, y, z, roll, pitch, yaw, v)
    
    def move_p_quat(self, 
                        x: float,
                        y: float,
                        z: float,
                        qx: float,
                        qy: float,
                        qz: float,
                        qw: float,
                        v:int):
        # 只有在开启控制时才会下发控制指令
        if self.get_ctrl_output_status():
            roll, pitch, yaw = quat_convert_euler(qx, qy, qz, qw)
            # 若打开读取线程
            if self._interface.get_connect_status():
                enable_list = self._interface.GetArmEnableStatus()
                # 只有使能成功状态下才会发送控制消息
                if(all(enable_list)):
                    self.__move_p(x, y, z, roll, pitch, yaw, v)
                # 检测到未使能，打印log
                else: 
                    self.logger.warning("[move_j] Arm is not enable!!!")
                    self.logger.warning("[move_j] Arm enable status is is %s", enable_list)
            # 若没有打开读取线程，不检测使能状态直接发送控制消息
            else:
                self.__move_p(x, y, z, roll, pitch, yaw, v)
    
    def __move_l(self,
                    x: float,
                    y: float,
                    z: float,
                    rx: float,
                    ry: float,
                    rz: float,
                    v:int):
        # 检查 v 是否是 [0, 100]
        if not isinstance(v, int) or v < 0 or v > 100:
            raise ValueError(f"[move_l] Speed v must be an int in [0,100], got {v}")
        x = int(round(x * 1e6))
        y = int(round(y * 1e6))
        z = int(round(z * 1e6))
        rx = int(round(math.degrees(rx) * 1000))
        ry = int(round(math.degrees(ry) * 1000))
        rz = int(round(math.degrees(rz) * 1000))
        self._interface.ModeCtrl(0x01, 0x02, v, self.__high_follow_mode)
        self._interface.EndPoseCtrl(x, y, z, rx, ry, rz)

    def move_l_euler(self, 
                        x: float,
                        y: float,
                        z: float,
                        roll: float,
                        pitch: float,
                        yaw: float,
                        v:int):
        # 只有在开启控制时才会下发控制指令
        if self.get_ctrl_output_status():
            # 若打开读取线程
            if self._interface.get_connect_status():
                enable_list = self._interface.GetArmEnableStatus()
                # 只有使能成功状态下才会发送控制消息
                if(all(enable_list)):
                    self.__move_l(x, y, z, roll, pitch, yaw, v)
                # 检测到未使能，打印log
                else: 
                    self.logger.warning("[move_l] Arm is not enable!!!")
                    self.logger.warning("[move_l] Arm enable status is is %s", enable_list)
            # 若没有打开读取线程，不检测使能状态直接发送控制消息
            else:
                self.__move_l(x, y, z, roll, pitch, yaw, v)
    
    def move_l_quat(self, 
                        x: float,
                        y: float,
                        z: float,
                        qx: float,
                        qy: float,
                        qz: float,
                        qw: float,
                        v:int):
        # 只有在开启控制时才会下发控制指令
        if self.get_ctrl_output_status():
            roll, pitch, yaw = quat_convert_euler(qx, qy, qz, qw)
            # 若打开读取线程
            if self._interface.get_connect_status():
                enable_list = self._interface.GetArmEnableStatus()
                # 只有使能成功状态下才会发送控制消息
                if(all(enable_list)):
                    self.__move_p(x, y, z, roll, pitch, yaw, v)
                # 检测到未使能，打印log
                else: 
                    self.logger.warning("[move_j] Arm is not enable!!!")
                    self.logger.warning("[move_j] Arm enable status is is %s", enable_list)
            # 若没有打开读取线程，不检测使能状态直接发送控制消息
            else:
                self.__move_p(x, y, z, roll, pitch, yaw, v)

    def enable_gripper(self):
        self.__enable_code = 0x02
        self._interface.GripperCtrl(self.__gripper_val, self.__effort, self.__enable_code, 0)
        self.__enable_code = 0x01
        self._interface.GripperCtrl(self.__gripper_val, self.__effort, self.__enable_code, 0)
    
    def disable_gripper(self):
        self.__enable_code = 0x02
        self._interface.GripperCtrl(self.__gripper_val, self.__effort, self.__enable_code, 0)
    
    def set_gripper_effort(self, effort:float):
        self.__effort = effort
        # self._interface.GripperCtrl(self.__gripper_val, self.__effort, self.__enable_code, 0)
    
    def move_gripper(self, gripper_val:float, effort:float = None):
        self.__gripper_val = gripper_val
        if effort is None:
            self._interface.GripperCtrl(round(self.__gripper_val * 1e6), round(self.__effort * 1000), self.__enable_code, 0)
        else:
            self._interface.GripperCtrl(round(self.__gripper_val * 1e6), round(effort * 1000), self.__enable_code, 0)
    
