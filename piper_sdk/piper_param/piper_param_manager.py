import copy
from typing_extensions import (
    Literal,
)
from ..version import PiperSDKVersion

class C_PiperParamManager():
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
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
        '''
        if not hasattr(self, "PIPER_PARAM"):
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

    def SetJointLimitParam(self, 
                           joint_name: Literal["j1", "j2", "j3", "j4", "j5", "j6"],
                           min_val: float, 
                           max_val: float):
        if joint_name not in ["j1", "j2", "j3", "j4", "j5", "j6"]:
            raise ValueError(f'"joint_name" Value {joint_name} is not in ["j1", "j2", "j3", "j4", "j5", "j6"]')
        if max_val - min_val < 0:
            raise ValueError(f'max_val should be greater than min_val.')
        self.PIPER_PARAM["joint_limit"][joint_name] = [min_val, max_val]
    
    def SetGripperRangeParam(self,
                             min_val: float, 
                             max_val: float):
        if max_val - min_val < 0:
            raise ValueError(f'max_val should be greater than min_val.')
        self.PIPER_PARAM["gripper_range"] = [min_val, max_val]

# a = C_PiperParamManager()
# print( a.GetCurrentPiperParam())
# a.SetGripperRangeParam(-20000,30000)
# a.SetJointLimitParam("j1",-20000,30000)
# print( a.GetCurrentPiperParam())
# a.ResetDefaultParam()
# print( a.GetCurrentPiperParam())

# # ✅ 测试单例模式
# manager1 = C_PiperParamManager()
# manager2 = C_PiperParamManager()

# print(manager1 is manager2)  # ✅ True，确保是同一个实例

# # 修改 manager1 的参数
# manager1.SetGripperRangeParam(-500, 500)
# print(manager2.GetCurrentPiperParam())  # ✅ manager2 也受影响，说明是同一个实例

# # 复位参数
# manager2.ResetDefaultParam()
# print(manager1.GetCurrentPiperParam())  # ✅ manager1 也被复位，单例模式生效！