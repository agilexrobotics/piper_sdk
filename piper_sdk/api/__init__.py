from .connection import PiperConnection
from .status import PiperStatus
from .motion import PiperMotion
from .gripper import PiperGripper
from .config import PiperConfig
from .safety import PiperSafety
from .system import PiperSystem

class PiperRobot(PiperConnection,
                 PiperStatus,
                 PiperMotion,
                 PiperGripper,
                 PiperConfig,
                 PiperSafety,
                 PiperSystem):
    """Main Piper Robot API class that combines all functionality modules
    
    This class inherits from all module classes to provide a unified interface
    for controlling the Piper robot. It includes:
    - Connection management
    - Status monitoring
    - Motion control
    - Gripper control
    - Configuration
    - Safety features
    - System information
    """
    pass

__all__ = ['PiperRobot']
