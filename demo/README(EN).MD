# Piper sdk demo

[CN](README.MD)

![ubuntu](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)

Test:

|PYTHON |STATE|
|---|---|
|![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

## Install dependencies

```shell
pip3 install python-can
```

```shell
pip3 install piper_sdk
```

can activate instructions [can README](./can_config.MD)

## demo instruction

```shell
.
├── piper_disable.py        # 失能机械臂 Disable robotic arm
├── piper_enable.py         # 使能机械臂 Enable robotics arm
├── piper_joint_ctrl.py     # 机械臂关节控制 Arm joint control
├── piper_master_config.py  # 将机械臂设置为主动臂 Set the arm as a master arm
├── piper_slave_config.py   # 将机械臂设置为从动臂 Set the arm as a slave arm
└── read_joint_state.py     # 读取关节角消息并打印 Read and print joint state
```

Note: If the robot is in the master arm mode, you need to restart the robot after sending the command to set it as a slave arm, and the robot will switch to the slave arm mode.

## Use two arm to remote control

### Hardware connection

- Diagram

![ ](./asserts/接线图.PNG)

1. Set one of the robotic arms as the master arm and the other as the slave arm (as shown in the demo above), then power off both robotic arms.
2. Connect the two robotic arms to a CAN module, and connect the CANs of the master and slave arms.
3. Power on the slave arm first, then the master arm, wait a few seconds, and then you can perform remote control.
4. If it fails, check whether the CAN line is connected properly, and try to power it off and on again.

### Read the master-slave data

See the interface description in the SDK for details. Here is just a brief description

#### Reading Master Arm Messages

The functions `GetArmJointMsgs` and `GetArmGripperMsgs` are used to obtain the slave robotic arm joint messages and gripper messages (raw messages).

The functions `GetArmJointCtrl` and `GetArmGripperCtrl` are used to obtain the master robotic arm joint messages and gripper messages (raw messages).

#### Control slave arm

`MotionCtrl_2` is used to set the control command mode, taking joint mode as an example.

```python
# 0x01 Set CAN command control mode. 0x01 Set joint control mode. 50 Set robotic arm movement speed.
piper.MotionCtrl_2(0x01, 0x01, 50)
```

`JointCtrl` is used to control six joints

`GripperCtrl` is used to control the gripper

Note!!!: **When controlling the slave arm, the master arm and the slave arm need to be disconnected. You can unplug the master arm's aviation plug and then run the slave arm control program. Otherwise, even if the program is executed, the slave arm will be out of control because the master arm is always sending slave arm control commands**
