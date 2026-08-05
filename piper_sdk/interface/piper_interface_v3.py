#!/usr/bin/env python3
# -*-coding:utf8-*-

from can.message import Message
from typing_extensions import (
    Literal,
)
from typing import (
    Optional,
    Type
)
from ..hardware_port import *
from ..protocol.protocol_v3 import C_PiperParserV3 as PiperParser
from ..piper_msgs.msg_v3 import *
from ..piper_msgs.msg_v3 import ArmMsgType as ArmMsgType_V3
from ..piper_msgs.msg_v3 import CanIDPiper as CanIDPiper_V3
from ..piper_msgs.msg_v3 import PiperMessage as PiperMessage_V3
from ..kinematics import *
from ..utils import *
from ..utils import logger, global_area
from ..piper_param import *
from ..version import PiperSDKVersion
from .interface_version import InterfaceVersion

from .piper_interface_v2 import C_PiperInterface_V2

class C_PiperInterface_V3(C_PiperInterface_V2):
    '''
    Piper interface class
    
    Args:
        can_name(str): can port name
        judge_flag(bool): Determines if the CAN port is functioning correctly.
                        When using a PCIe-to-CAN module, set to false.
        can_auto_init(bool): Determines if the CAN port is automatically initialized.
        dh_is_offset([0,1] -> default 0x01): Does the j1-j2 offset by 2° in the DH parameters? 
                    0 -> No offset
                    1 -> Offset applied
        start_sdk_joint_limit(bool -> False):Whether to enable the software joint limit of SDK
        start_sdk_gripper_limit(bool -> False):Whether to enable the software gripper limit of SDK
    '''
    ArmMsgType = ArmMsgType_V3
    CanIDPiper = CanIDPiper_V3
    PiperMessage = PiperMessage_V3

    def __init__(self,
                    can_name:str="can0",
                    judge_flag=True,
                    can_auto_init=True,
                    # reconnect_after_disconnection:bool = False,
                    dh_is_offset: int = 0x01,
                    start_sdk_joint_limit: bool = False, 
                    start_sdk_gripper_limit: bool = False,
                    logger_level:LogLevel = LogLevel.WARNING,
                    log_to_file:bool = False,
                    log_file_path = None) -> None:
        super().__init__(
                    can_name,
                    judge_flag,
                    can_auto_init,
                    # reconnect_after_disconnection:bool = False,
                    dh_is_offset,
                    start_sdk_joint_limit, 
                    start_sdk_gripper_limit,
                    logger_level,
                    log_to_file,
                    log_file_path)
        self._parser: Type[PiperParser] = PiperParser()
        self.tx_msg = self.PiperMessage()
        self.rx_msg = self.PiperMessage()
        
    def GetCurrentInterfaceVersion(self):
        '''
        Returns
        -------
            current interface version
        '''
        return InterfaceVersion.INTERFACE_V3

    def MotionCtrl_2(self, 
                         ctrl_mode: Literal[0x00, 0x01, 0x03, 0x04, 0x07] = 0x01, 
                         move_mode: Literal[0x00, 0x01, 0x02, 0x03, 0x06, 0x05] = 0x01, 
                         move_spd_rate_ctrl: int = 50, 
                         is_mit_mode: Literal[0x00, 0xAD, 0xFF] = 0x00,
                         residence_time: int = 0,
                         installation_pos: Literal[0x00, 0x01, 0x02, 0x03] = 0x00):
            '''
            机械臂运动控制指令2
            
            CAN ID:
                0x151
            
            Args:
                ctrl_mode: 控制模式 uint8 
                    0x00 待机模式
                    0x01 CAN 指令控制模式
                    0x03 以太网控制模式
                    0x04 wifi 控制模式
                    0x07 离线轨迹模式
                move_mode: MOVE模式 uint8 
                    0x00 MOVE P
                    0x01 MOVE J
                    0x02 MOVE L
                    0x03 MOVE C
                    0x06 MOVE M ---基于V1.8-8版本后
                    0x05 MOVE CPV ---基于V1.8-1版本后
                move_spd_rate_ctrl 运动速度百分比 uint8
                    数值范围0~100 
                is_mit_mode: mit模式 uint8 
                    0x00 位置速度模式
                    0xAD MIT模式
                    0xFF 无效
                residence_time: 离线轨迹点停留时间 
                    uint8 0~254 ,单位: s;255:轨迹终止
                installation_pos: 安装位置 uint8 注意接线朝后 ---基于V1.5-2版本后
                        0x00 无效值
                        0x01 水平正装
                        0x02 侧装左
                        0x03 侧装右
            '''
            '''
            Sends the robotic arm motion control command (0x151).
            
            Args:
                ctrl_mode (int): The control mode.
                    0x00: Standby mode
                    0x01: CAN command control mode
                    0x03: Ethernet control mode
                    0x04: Wi-Fi control mode
                    0x07: Offline trajectory mode
                move_mode (int): The MOVE mode.
                    0x00: MOVE P (Position)
                    0x01: MOVE J (Joint)
                    0x02: MOVE L (Linear)
                    0x03: MOVE C (Circular)
                    0x06: MOVE M (MIT) ---- Based on version V1.8-8 and later
                    0x05: MOVE CPV ---- Based on version V1.8-1 and later
                move_spd_rate_ctrl (int): The movement speed percentage (0-100).
                is_mit_mode (int): The MIT mode.
                    0x00: Position-velocity mode
                    0xAD: MIT mode
                    0xFF: Invalid
                residence_time: Offline trajectory point residence time
                    uint8 0~254, unit: seconds; 255: trajectory termination
                installation_pos: Installation position uint8 (Pay attention to rear-facing wiring) --- Based on version V1.5-2 and later
                                0x00 Invalid value
                                0x01 Horizontal upright
                                0x02 Side mount left
                                0x03 Side mount right
            '''
            tx_can = Message()
            motion_ctrl_2 = ArmMsgMotionCtrl_2(ctrl_mode, move_mode, move_spd_rate_ctrl, is_mit_mode, residence_time, installation_pos)
            msg = self.tx_msg
            msg.type_ = self.ArmMsgType.PiperMsgMotionCtrl_2
            msg.arm_motion_ctrl_2 = motion_ctrl_2
            self._parser.EncodeMessage(msg, tx_can)
            feedback = self._arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
            if feedback is not self._arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
                self.logger.error("0x151 send failed: SendCanMessage(%s)", feedback)

    def _JointMitCtrl(self,motor_num:int,
                            pos_ref:float, vel_ref:float, kp:float, kd:float, t_ref:float,
                            p_min:float=-12.5,    p_max:float=12.5, 
                            v_min:float=-45.0,    v_max:float=45.0, 
                            kp_min:float=0.0,   kp_max:float=500.0, 
                            kd_min:float=-5.0,   kd_max:float=5.0,
                            t_min:float=-16.0,    t_max:float=16.0):
        '''
        机械臂关节1~6MIT控制指令
        
        CAN ID:
            0x15A,0x15B,0x15C,0x15D,0x15E,0x15F
        
        注意:p_min,p_max,v_min,v_max,kp_min,kp_max,kd_min,kd_max,t_min,t_max参数为固定,不要更改
        
        Args:
            motor_num:电机序号[1,6]
            pos_ref: 设定期望的目标位置
            vel_ref: 设定电机运动的速度
            kp: 比例增益,控制位置误差对输出力矩的影响
            kd: 微分增益,控制速度误差对输出力矩的影响
            t_ref: 目标力矩参考值,用于控制电机施加的力矩或扭矩
            p_min:位置最小值
            p_max:位置最大值
            v_min:速度最小值
            v_max:速度最大值
            kp_min:p参数最小值
            kp_max:p参数最大值
            kd_min:d参数最小值
            kd_max:d参数最大值
            t_min:扭矩参数最小值
            t_max:扭矩参数最大值
        '''
        pos_tmp = self._parser.FloatToUint(pos_ref, p_min, p_max, 16)
        vel_tmp = self._parser.FloatToUint(vel_ref, v_min, v_max, 12)
        kp_tmp = self._parser.FloatToUint(kp, kp_min, kp_max, 12)
        kd_tmp = self._parser.FloatToUint(kd, kd_min, kd_max, 12)
        t_tmp = self._parser.FloatToUint(t_ref, t_min, t_max, 12)
        tx_can = Message()
        mit_ctrl = ArmMsgJointMitCtrl(  pos_ref=pos_tmp, 
                                        vel_ref=vel_tmp,
                                        kp=kp_tmp, 
                                        kd=kd_tmp,
                                        t_ref=t_tmp)
        msg = self.tx_msg
        msg.arm_joint_mit_ctrl = mit_ctrl
        if(motor_num == 1):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_1
        elif(motor_num == 2):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_2
        elif(motor_num == 3):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_3
        elif(motor_num == 4):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_4
        elif(motor_num == 5):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_5
        elif(motor_num == 6):
            msg.type_ = self.ArmMsgType.PiperMsgJointMitCtrl_6
        else:
            raise ValueError(f"'motor_num' {motor_num} out of range 0-6.")
        self._parser.EncodeMessage(msg, tx_can)
        feedback = self._arm_can.SendCanMessage(tx_can.arbitration_id, tx_can.data)
        if feedback is not self._arm_can.CAN_STATUS.SEND_MESSAGE_SUCCESS:
            self.logger.error("JointMitCtrl send failed: SendCanMessage(%s)", feedback)
    
    def JointMitCtrl(self,motor_num:int,
                    pos_ref:float, vel_ref:float, kp:float, kd:float, t_ref:float):
        '''
        Robotic Arm Joint 1~6 MIT Control Command
        
        CAN IDs:
            0x15A, 0x15B, 0x15C, 0x15D, 0x15E, 0x15F
        
        Args:
            motor_num: Motor index, range [1, 6]
            pos_ref: Desired target position, unit: rad, range [-12.5, 12.5]
            vel_ref: Desired motor speed, range [-45.0, 45.0]
            kp: Proportional gain, controls the influence of position error on output torque, reference value: 10, range [0.0, 500.0]
            kd: Derivative gain, controls the influence of speed error on output torque, reference value: 0.8, range [-5.0, 5.0]
            t_ref: Target torque reference, controls the torque applied by the motor, range [-16.0, 16.0]
        '''
        '''
        机械臂关节1~6MIT控制指令
        
        CAN ID:
            0x15A,0x15B,0x15C,0x15D,0x15E,0x15F
        
        Args:
            motor_num:电机序号,[1,6]
            pos_ref: 设定期望的目标位置,单位rad,[-12.5,12.5]
            vel_ref: 设定电机运动的速度,[-45.0,45.0]
            kp: 比例增益,控制位置误差对输出力矩的影响,参考值---10,[0.0,500.0]
            kd: 微分增益,控制速度误差对输出力矩的影响,参考值---0.8,[-5.0,5.0]
            t_ref: 目标力矩参考值,用于控制电机施加的力矩或扭矩,[-16.0,16.0]
        '''
        self._JointMitCtrl(motor_num, pos_ref, vel_ref, kp, kd, t_ref)
