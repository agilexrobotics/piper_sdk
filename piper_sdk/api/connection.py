from typing import Optional
from .base import PiperBase

class PiperConnection(PiperBase):
    def connect(self, can_init: bool = False, piper_init: bool = True, start_thread: bool = True) -> bool:
        """Connect to the Piper robot
        
        Args:
            can_init (bool): Whether to initialize CAN
            piper_init (bool): Whether to initialize Piper
            start_thread (bool): Whether to start monitoring thread
            
        Returns:
            bool: True if connection successful
        """
        return self._interface.ConnectPort(can_init, piper_init, start_thread)
    
    def disconnect(self, thread_timeout: float = 0.1) -> None:
        """Disconnect from the Piper robot
        
        Args:
            thread_timeout (float): Timeout for thread termination
        """
        self._interface.DisconnectPort(thread_timeout)
        
    def is_connected(self) -> bool:
        """Check if connection is OK
        
        Returns:
            bool: True if connection is OK
        """
        return self._interface.isOk()
    
    def enable(self) -> bool:
        """Enable the Piper robot
        
        Returns:
            bool: True if enable successful
        """
        return self._interface.EnablePiper()
    
    def disable(self) -> bool:
        """Disable the Piper robot
        
        Returns:
            bool: True if disable successful
        """
        return self._interface.DisablePiper() 