from typing import Literal, Optional
from .base import PiperBase

class PiperConfig(PiperBase):
    def set_joint_limits(self,
                        joint_name: Literal["j1", "j2", "j3", "j4", "j5", "j6"],
                        min_val: float,
                        max_val: float):
        """Set joint limits
        
        Args:
            joint_name: Joint name (j1-j6)
            min_val: Minimum joint angle
            max_val: Maximum joint angle
        """
        return self._interface.SetSDKJointLimitParam(joint_name, min_val, max_val)
    
    def get_joint_limits(self,
                        joint_name: Literal["j1", "j2", "j3", "j4", "j5", "j6"]):
        """Get joint limits
        
        Args:
            joint_name: Joint name (j1-j6)
            
        Returns:
            tuple: (min_value, max_value)
        """
        return self._interface.GetSDKJointLimitParam(joint_name)
    
    def set_end_effector_params(self,
                               max_linear_vel: int,
                               max_angular_vel: int,
                               max_linear_acc: int,
                               max_angular_acc: int):
        """Set end effector velocity and acceleration parameters
        
        Args:
            max_linear_vel: Maximum linear velocity
            max_angular_vel: Maximum angular velocity
            max_linear_acc: Maximum linear acceleration
            max_angular_acc: Maximum angular acceleration
        """
        return self._interface.EndSpdAndAccParamSet(
            max_linear_vel,
            max_angular_vel,
            max_linear_acc,
            max_angular_acc
        )
    
    def set_motor_speed_limit(self,
                            motor_num: Literal[1, 2, 3, 4, 5, 6],
                            max_speed: int):
        """Set motor maximum speed
        
        Args:
            motor_num: Motor number (1-6)
            max_speed: Maximum speed value
        """
        return self._interface.MotorMaxSpdSet(motor_num, max_speed)
    
    def set_motor_acceleration_limit(self,
                                   motor_num: Literal[1, 2, 3, 4, 5, 6],
                                   max_acc: int = 500):
        """Set motor maximum acceleration
        
        Args:
            motor_num: Motor number (1-6)
            max_acc: Maximum acceleration value
        """
        return self._interface.JointMaxAccConfig(motor_num, max_acc)
    
    def configure_joint(self,
                       joint_num: Literal[1, 2, 3, 4, 5, 6, 7] = 7,
                       set_zero: Literal[0x00, 0xAE] = 0,
                       acc_param_effective: Literal[0x00, 0xAE] = 0,
                       max_acc: int = 500,
                       clear_err: Literal[0x00, 0xAE] = 0):
        """Configure joint parameters
        
        Args:
            joint_num: Joint number (1-6, 7=all)
            set_zero: Set zero position flag
            acc_param_effective: Acceleration parameter effectiveness flag
            max_acc: Maximum acceleration
            clear_err: Clear error flag
        """
        return self._interface.JointConfig(
            joint_num,
            set_zero,
            acc_param_effective,
            max_acc,
            clear_err
        ) 