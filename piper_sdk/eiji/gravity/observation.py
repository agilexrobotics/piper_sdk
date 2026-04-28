from piper_sdk import *
import numpy as np

class Observation():
    def __init__(self):
        self.piper = C_PiperInterface_V2("can0")

    def obs(self):
        # observation
        piper = self.piper
        joint_angles = np.array([getattr(piper.GetArmHighSpdInfoMsgs(), f"motor_{i}").pos / 1e3 for i in range(1, 7)])
        joint_velocities = np.array([getattr(piper.GetArmHighSpdInfoMsgs(), f"motor_{i}").motor_speed / 1e3 for i in range(1, 7)])
        joint_torques = np.array([getattr(piper.GetArmHighSpdInfoMsgs(), f"motor_{i}").effort /1e3 for i in range(1, 7)])
        
        return joint_angles, joint_velocities, joint_torques