# Piper Robotic Arm SDK(V1) Demo

[中文](README.MD)

![ubuntu](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)

Test:

| PYTHON | STATE |
|---|---|
| ![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg) | ![Pass](https://img.shields.io/badge/Pass-blue.svg) |

## Installation Instructions

### Install Dependencies

Note: python-can >= 4.3.1

```shell
pip3 install python-can
```

```shell
pip3 install piper_sdk
```

Instructions for activating the CAN module [can README](./can_config.MD)

## Demo Overview

```shell
V1
├── motor_max_acc_limit_config.py
├── piper_disable.py
├── piper_enable.py
├── piper_end_pose.py
├── piper_gripper_ctrl.py
├── piper_gripper_zero_set.py
├── piper_init_default.py
├── piper_joint_ctrl.py
├── piper_master_config.py
├── piper_moveC.py
├── piper_read_arm_motor_max_acc_limit.py
├── piper_read_arm_motor_max_angle_spd.py
├── piper_read_end_pose.py
├── piper_reset.py
├── piper_set_mit.py
├── piper_slave_config.py
├── piper_status.py
├── piper_stop.py
├── read_gripper_status.py
├── read_joint_state.py
└── read_piper_hardware.py
```

| File | Description |
|---|---|
| `motor_max_acc_limit_config.py` | Set the maximum acceleration limit for individual joints' motors |
| `piper_disable.py` | Disable the robotic arm |
| `piper_enable.py` | Enable the robotic arm |
| `piper_end_pose.py` | Control the end effector of the robotic arm |
| `piper_gripper_ctrl.py` | Control the robotic arm's gripper |
| `piper_gripper_zero_set.py` | Set the gripper zero position |
| `piper_init_default.py` | Set default limits for all joints, maximum speeds, and accelerations |
| `piper_joint_ctrl.py` | Control the robotic arm's joints |
| `piper_master_config.py` | Set the robotic arm as the master arm |
| `piper_moveC.py` | Set the robotic arm as the circle mode |
| `piper_read_arm_motor_max_acc_limit.py` | Read the maximum acceleration limits of all motors |
| `piper_read_arm_motor_max_angle_spd.py` | Read the maximum speed limits of all motors |
| `piper_read_end_pose.py` | Read the end effector's pose |
| `piper_reset.py` | Reset the robotic arm; needs to be executed after setting to teach mode |
| `piper_set_mit.py` | Set the robotic arm to MIT mode, where it responds the fastest |
| `piper_slave_config.py` | Set the robotic arm as the slave arm |
| `piper_status.py` | Read the status of the robotic arm |
| `piper_stop.py` |The robotic arm stops with a slow descent, and it needs to be reset and re-enabled twice after use|
| `read_gripper_status.py` | Read the status of the gripper |
| `read_joint_state.py` | Read joint angle messages and print them |
| `read_piper_hardware.py` | Read the firmware version of the robotic arm's main controller |

**Note:** If the robotic arm is in master arm mode, after sending the command to set it to slave arm, the arm needs to be restarted for the switch to take effect.
