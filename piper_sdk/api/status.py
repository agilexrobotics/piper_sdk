from typing import List, Optional
from .base import PiperBase

class PiperStatus(PiperBase):
    def get_arm_status(self):
        """Get the current status of the robot arm
        
        Returns:
            ArmStatus: Current arm status
        """
        return self._interface.GetArmStatus()
    
    def get_end_pose(self):
        """Get the current end pose of the robot
        
        Returns:
            ArmEndPose: Current end pose
        """
        return self._interface.GetArmEndPoseMsgs()
    
    def get_joint_states(self):
        """Get the current joint states
        
        Returns:
            ArmJoint: Current joint states
        """
        return self._interface.GetArmJointMsgs()
    
    def get_gripper_state(self):
        """Get the current gripper state
        
        Returns:
            ArmGripper: Current gripper state
        """
        return self._interface.GetArmGripperMsgs()
    
    def get_motor_high_speed_info(self):
        """Get high speed motor information
        
        Returns:
            ArmMotorDriverInfoHighSpd: High speed motor info
        """
        return self._interface.GetArmHighSpdInfoMsgs()
    
    def get_motor_low_speed_info(self):
        """Get low speed motor information
        
        Returns:
            ArmMotorDriverInfoLowSpd: Low speed motor info
        """
        return self._interface.GetArmLowSpdInfoMsgs()
    
    def get_enabled_status(self) -> List[bool]:
        """Get enabled status for each motor
        
        Returns:
            List[bool]: List of enabled status for each motor
        """
        return self._interface.GetArmEnableStatus()
    
    def get_forward_kinematics(self, mode: str = "feedback"):
        """Get forward kinematics result
        
        Args:
            mode (str): Either "feedback" or "control"
            
        Returns:
            dict: Forward kinematics result
        """
        return self._interface.GetFK(mode)
    
    def get_can_fps(self):
        """Get CAN bus frames per second
        
        Returns:
            float: CAN bus FPS
        """
        return self._interface.GetCanFps() 