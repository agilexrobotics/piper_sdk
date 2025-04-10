from typing import Optional, Literal
from ..interface.piper_interface_v2 import C_PiperInterface_V2

class PiperBase:
    def __init__(self, 
                 can_name: str = "can0",
                 judge_flag: bool = True,
                 can_auto_init: bool = True,
                 dh_is_offset: int = 0,
                 start_sdk_joint_limit: bool = True,
                 start_sdk_gripper_limit: bool = True) -> None:
        """Base class for Piper API
        
        Args:
            can_name (str): CAN port name
            judge_flag (bool): Determines if the CAN port is functioning correctly
            can_auto_init (bool): Determines if the CAN port is automatically initialized
            dh_is_offset (int): Does the j1-j2 offset by 2° in the DH parameters
            start_sdk_joint_limit (bool): Enable joint limits in SDK
            start_sdk_gripper_limit (bool): Enable gripper limits in SDK
        """
        self._interface = C_PiperInterface_V2(
            can_name=can_name,
            judge_flag=judge_flag,
            can_auto_init=can_auto_init,
            dh_is_offset=dh_is_offset,
            start_sdk_joint_limit=start_sdk_joint_limit,
            start_sdk_gripper_limit=start_sdk_gripper_limit
        ) 