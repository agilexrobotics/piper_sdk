import copy
import math
from typing_extensions import (
    Literal,
)
from ..version import PiperSDKVersion

class C_PiperParamManager():
    def __init__(self) -> None:
        '''
        |joint_name|     limit(rad)       |    limit(angle)    |
        |----------|     ----------       |     ----------     |
        |joint1    |   [-2.6179, 2.6179]  |    [-150.0, 150.0] |
        |joint2    |   [0, 3.14]          |    [0, 180.0]      |
        |joint3    |   [-2.967, 0]        |    [-170, 0]       |
        |joint4    |   [-1.745, 1.745]    |    [-100.0, 100.0] |
        |joint5    |   [-1.22, 1.22]      |    [-70.0, 70.0]   |
        |joint6    |   [-2.09439, 2.09439]|    [-120.0, 120.0] |

        Note:
            These are SDK-side software limit defaults used by
            C_PiperParamManager. SDK joint limits are disabled by default
            unless start_sdk_joint_limit=True. joint6 keeps the conservative
            legacy flange limit of +/-120 degrees for compatibility with older
            hardware/firmware. Newer robot presets may allow +/-180 degrees;
            see ROBOT_JOINT_LIMIT_PRESET_DEG in constants.py.
        '''
        self.__PIPER_PARAM_ORIGIN = {
            "joint_limit":{
                "j1": [-2.6179, 2.6179],
                "j2": [0, 3.14],
                "j3": [-2.967, 0],
                "j4": [-1.745, 1.745],
                "j5": [-1.22, 1.22],
                "j6": [-2.09439, 2.09439],
            },
            "gripper_range": [0.0, 0.07],
            "gripper_angle_limit": [-180.0, 180.0],
            "piper_sdk_version": PiperSDKVersion.PIPER_SDK_CURRENT_VERSION
        }
        self.PIPER_PARAM = copy.deepcopy(self.__PIPER_PARAM_ORIGIN)
    
    def ResetDefaultParam(self):
        self.PIPER_PARAM.update(copy.deepcopy(self.__PIPER_PARAM_ORIGIN))
    
    def GetPiperParamOrigin(self):
        return copy.deepcopy(self.__PIPER_PARAM_ORIGIN)
    
    def GetCurrentPiperParam(self):
        return copy.deepcopy(self.PIPER_PARAM)
    
    def GetCurrentPiperSDKVersion(self):
        return self.PIPER_PARAM["piper_sdk_version"]
    
    def GetJointLimitParam(self,
                           joint_name: Literal["j1", "j2", "j3", "j4", "j5", "j6"]):
        if joint_name not in ["j1", "j2", "j3", "j4", "j5", "j6"]:
            raise ValueError(f'"joint_name" Value {joint_name} is not in ["j1", "j2", "j3", "j4", "j5", "j6"]')
        return self.PIPER_PARAM["joint_limit"][joint_name][0], self.PIPER_PARAM["joint_limit"][joint_name][1]

    def GetGripperRangeParam(self):
        return self.PIPER_PARAM["gripper_range"][0], self.PIPER_PARAM["gripper_range"][1]

    def GetGripperAngleLimitParam(self):
        return self.PIPER_PARAM["gripper_angle_limit"][0], self.PIPER_PARAM["gripper_angle_limit"][1]

    def _ValidateFiniteNumber(self, name: str, value: float):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f'{name} should be an int or float.')
        if not math.isfinite(value):
            raise ValueError(f'{name} should be a finite number.')

    def SetJointLimitParam(self, 
                           joint_name: Literal["j1", "j2", "j3", "j4", "j5", "j6"],
                           min_val: float, 
                           max_val: float):
        if joint_name not in ["j1", "j2", "j3", "j4", "j5", "j6"]:
            raise ValueError(f'"joint_name" Value {joint_name} is not in ["j1", "j2", "j3", "j4", "j5", "j6"]')
        self._ValidateFiniteNumber("min_val", min_val)
        self._ValidateFiniteNumber("max_val", max_val)
        if max_val - min_val < 0:
            raise ValueError(f'max_val should be greater than min_val.')
        self.PIPER_PARAM["joint_limit"][joint_name] = [min_val, max_val]
    
    def SetGripperRangeParam(self,
                             min_val: float, 
                             max_val: float):
        self._ValidateFiniteNumber("min_val", min_val)
        self._ValidateFiniteNumber("max_val", max_val)
        if min_val < 0 or max_val < 0:
            raise ValueError(f'min_val and max_val should be non-negative.')
        if max_val - min_val < 0:
            raise ValueError(f'max_val should be greater than min_val.')
        self.PIPER_PARAM["gripper_range"] = [min_val, max_val]

    def SetGripperAngleLimitParam(self,
                                min_val: float, 
                                max_val: float):
        self._ValidateFiniteNumber("min_val", min_val)
        self._ValidateFiniteNumber("max_val", max_val)
        if max_val - min_val < 0:
            raise ValueError(f'max_val should be greater than min_val.')
        self.PIPER_PARAM["gripper_angle_limit"] = [min_val, max_val]

# a = C_PiperParamManager()
# print( a.GetCurrentPiperParam())
# a.SetGripperRangeParam(-20000,30000)
# a.SetJointLimitParam("j1",-20000,30000)
# print( a.GetCurrentPiperParam())
# a.ResetDefaultParam()
# print( a.GetCurrentPiperParam())

# # 参数管理器为普通实例，不同 interface 持有独立参数
# manager1 = C_PiperParamManager()
# manager2 = C_PiperParamManager()
# print(manager1 is manager2)  # False
