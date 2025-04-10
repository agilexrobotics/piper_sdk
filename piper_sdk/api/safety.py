from typing import Literal
from .base import PiperBase

class PiperSafety(PiperBase):
    def set_collision_protection(self,
                               j1_level: int,
                               j2_level: int,
                               j3_level: int,
                               j4_level: int,
                               j5_level: int,
                               j6_level: int):
        """Set collision protection levels for all joints
        
        Args:
            j1_level: Joint 1 protection level
            j2_level: Joint 2 protection level
            j3_level: Joint 3 protection level
            j4_level: Joint 4 protection level
            j5_level: Joint 5 protection level
            j6_level: Joint 6 protection level
        """
        return self._interface.CrashProtectionConfig(
            j1_level, j2_level, j3_level,
            j4_level, j5_level, j6_level
        )
    
    def get_collision_protection_feedback(self):
        """Get collision protection level feedback
        
        Returns:
            CrashProtectionLevelFeedback: Current protection levels
        """
        return self._interface.GetCrashProtectionLevelFeedback()
    
    def emergency_stop(self, mode: Literal[0x00, 0x01, 0x02] = 0x01):
        """Execute emergency stop
        
        Args:
            mode: Stop mode
                0x00: Normal stop
                0x01: Emergency stop
                0x02: Clear emergency
        """
        return self._interface.EmergencyStop(mode)
    
    def motion_control(self,
                      emergency_stop: Literal[0x00, 0x01, 0x02] = 0,
                      track_ctrl: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08] = 0,
                      grag_teach_ctrl: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07] = 0):
        """Control motion safety parameters
        
        Args:
            emergency_stop: Emergency stop control
            track_ctrl: Track control mode
            grag_teach_ctrl: Drag teaching control mode
        """
        return self._interface.MotionCtrl_1(
            emergency_stop=emergency_stop,
            track_ctrl=track_ctrl,
            grag_teach_ctrl=grag_teach_ctrl
        ) 