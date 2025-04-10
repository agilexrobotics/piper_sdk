from typing import Literal, Optional
from .base import PiperBase

class PiperMotion(PiperBase):
    def set_motion_mode(self, 
                       ctrl_mode: Literal[0x00, 0x01, 0x03, 0x04, 0x07] = 0x01,
                       move_mode: Literal[0x00, 0x01, 0x02, 0x03, 0x04] = 0x01,
                       speed_rate: int = 50,
                       mit_mode: Literal[0x00, 0xAD, 0xFF] = 0x00,
                       residence_time: int = 0,
                       installation_pos: Literal[0x00, 0x01, 0x02, 0x03] = 0x00):
        """Set motion control mode
        
        Args:
            ctrl_mode: Control mode (0x00: Stop, 0x01: Position, etc.)
            move_mode: Movement mode (0x00: Joint, 0x01: Linear, etc.)
            speed_rate: Movement speed rate (0-100)
            mit_mode: MIT mode flag
            residence_time: Residence time
            installation_pos: Installation position
        """
        return self._interface.MotionCtrl_2(
            ctrl_mode=ctrl_mode,
            move_mode=move_mode,
            move_spd_rate_ctrl=speed_rate,
            is_mit_mode=mit_mode,
            residence_time=residence_time,
            installation_pos=installation_pos
        )
    
    def move_joints(self, j1: int, j2: int, j3: int, j4: int, j5: int, j6: int):
        """Move robot to specified joint positions
        
        Args:
            j1-j6: Target joint angles in degrees
        """
        return self._interface.JointCtrl(j1, j2, j3, j4, j5, j6)
    
    def move_cartesian(self, x: int, y: int, z: int, rx: int, ry: int, rz: int):
        """Move robot to specified cartesian pose
        
        Args:
            x,y,z: Target position in mm
            rx,ry,rz: Target orientation in degrees
        """
        return self._interface.EndPoseCtrl(x, y, z, rx, ry, rz)
    
    def emergency_stop(self, mode: Literal[0x00, 0x01, 0x02] = 0x01):
        """Execute emergency stop
        
        Args:
            mode: Stop mode (0x00: Normal stop, 0x01: Emergency stop, 0x02: Clear emergency)
        """
        return self._interface.EmergencyStop(mode)
    
    def enable_motor(self, 
                    motor_num: Literal[1, 2, 3, 4, 5, 6, 7, 0xFF] = 7,
                    enable_flag: Literal[0x01, 0x02] = 0x02):
        """Enable specified motor
        
        Args:
            motor_num: Motor number (1-6, 7=gripper, 0xFF=all)
            enable_flag: Enable flag
        """
        return self._interface.EnableArm(motor_num, enable_flag)
    
    def disable_motor(self,
                     motor_num: Literal[1, 2, 3, 4, 5, 6, 7, 0xFF] = 7,
                     enable_flag: Literal[0x01, 0x02] = 0x01):
        """Disable specified motor
        
        Args:
            motor_num: Motor number (1-6, 7=gripper, 0xFF=all)
            enable_flag: Disable flag
        """
        return self._interface.DisableArm(motor_num, enable_flag)
    
    def mit_joint_control(self,
                         motor_num: int,
                         pos_ref: float,
                         vel_ref: float,
                         kp: float,
                         kd: float,
                         t_ref: float):
        """MIT mode joint control
        
        Args:
            motor_num: Motor number
            pos_ref: Position reference
            vel_ref: Velocity reference
            kp: Position gain
            kd: Velocity gain
            t_ref: Torque reference
        """
        return self._interface.JointMitCtrl(motor_num, pos_ref, vel_ref, kp, kd, t_ref) 