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
