from typing import Literal
from .base import PiperBase

class PiperGripper(PiperBase):
    def control(self,
                angle: int = 0,
                effort: int = 0,
                code: Literal[0x00, 0x01, 0x02, 0x03] = 0,
                set_zero: Literal[0x00, 0xAE] = 0):
        """Control the gripper
        
        Args:
            angle: Gripper angle
            effort: Gripper effort/force
            code: Control code
            set_zero: Zero position flag
        """
        return self._interface.GripperCtrl(
            gripper_angle=angle,
            gripper_effort=effort,
            gripper_code=code,
            set_zero=set_zero
        )
    
    def configure(self,
                 teaching_range: int = 100,
                 max_range: int = 70,
                 teaching_friction: int = 1):
        """Configure gripper parameters
        
        Args:
            teaching_range: Teaching range percentage
            max_range: Maximum range configuration
            teaching_friction: Teaching friction value
        """
        return self._interface.GripperTeachingPendantParamConfig(
            teaching_range_per=teaching_range,
            max_range_config=max_range,
            teaching_friction=teaching_friction
        )
    
    def get_range_limits(self):
        """Get gripper range limits
        
        Returns:
            tuple: (min_value, max_value)
        """
        return self._interface.GetSDKGripperRangeParam()
    
    def set_range_limits(self, min_val: float, max_val: float):
        """Set gripper range limits
        
        Args:
            min_val: Minimum range value
            max_val: Maximum range value
        """
        return self._interface.SetSDKGripperRangeParam(min_val, max_val) 