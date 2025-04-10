from typing import Dict
from .base import PiperBase

class PiperSystem(PiperBase):
    def get_interface_version(self) -> str:
        """Get current interface version
        
        Returns:
            str: Interface version string
        """
        return self._interface.GetCurrentInterfaceVersion()
    
    def get_sdk_version(self) -> str:
        """Get current SDK version
        
        Returns:
            str: SDK version string
        """
        return self._interface.GetCurrentSDKVersion()
    
    def get_protocol_version(self) -> str:
        """Get current protocol version
        
        Returns:
            str: Protocol version string
        """
        return self._interface.GetCurrentProtocolVersion()
    
    def get_firmware_version(self) -> Dict:
        """Get Piper firmware version
        
        Returns:
            Dict: Firmware version information
        """
        return self._interface.GetPiperFirmwareVersion()
    
    def search_firmware_version(self):
        """Request firmware version update
        """
        return self._interface.SearchPiperFirmwareVersion()
    
    def arm_param_enquiry(self,
                         param_enquiry: int = 0x00,
                         param_setting: int = 0x00,
                         data_feedback: int = 0x00,
                         end_load_param_effective: int = 0x00,
                         set_end_load: int = 0x03):
        """Enquire and configure arm parameters
        
        Args:
            param_enquiry: Parameter enquiry type
            param_setting: Parameter setting type
            data_feedback: Data feedback type
            end_load_param_effective: End load parameter effectiveness
            set_end_load: End load setting type
        """
        return self._interface.ArmParamEnquiryAndConfig(
            param_enquiry=param_enquiry,
            param_setting=param_setting,
            data_feedback_0x48x=data_feedback,
            end_load_param_setting_effective=end_load_param_effective,
            set_end_load=set_end_load
        ) 