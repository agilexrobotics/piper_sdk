from piper_sdk import *
piper = C_PiperInterface()
piper.ConnectPort()
# reset arm
piper.MotionCtrl_1(0x02,0,0)
# 0x01 Set the can command control mode
# 0x01 Set the joint control mode to Joint control
# 50 Set the robot arm movement speed ratio
piper.MotionCtrl_2(0x01, 0x01, 50)
piper.EnableArm()
# Later call joint control and gripper control
# ...