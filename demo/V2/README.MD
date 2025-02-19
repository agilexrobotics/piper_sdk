# Piper 机械臂sdk(V2)demo

[EN](README(EN).MD)

![ubuntu](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)

Test:

|PYTHON |STATE|
|---|---|
|![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

## 安装方法

### 安装依赖

注:python-can>=4.3.1

```shell
pip3 install python-can
```

注:piper_sdk>=0.1.9

```shell
pip3 install piper_sdk
```

can模块激活说明[can README](./can_config.MD)

## demo说明

```shell
V2
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
├── read_piper_hardware.py
├── V2_gripper_param_config.py
├── V2_installation_pos.py
├── V2_joint_mit_ctrl.py
└── V2_motor_max_spd_set.py
```

|文件 |说明|
|---|---|
|`motor_max_acc_limit_config.py`|电机单独设定某个关节电机的最大加速度限制|
|`piper_disable.py`|机械臂失能|
|`piper_enable.py`|机械臂使能|
|`piper_end_pose.py`|机械臂末端控制|
|`piper_gripper_ctrl.py`|机械臂夹爪控制|
|`piper_gripper_zero_set.py`|机械臂夹爪零点设定|
|`piper_init_default.py`|机械臂 设置全部关节限位、关节最大速度、关节加速度为默认值|
|`piper_joint_ctrl.py`|机械臂关节控制|
|`piper_master_config.py`|机械臂设置为主臂|
|`piper_moveC.py`|机械臂设置为主臂|
|`piper_read_arm_motor_max_acc_limit.py`|读取所有电机的最大加速度限制|
|`piper_read_arm_motor_max_angle_spd.py`|读取机械臂的所有电机的最大加速度限制|
|`piper_read_end_pose.py`|读取末端姿态|
|`piper_reset.py`|机械臂重置，需要在设定为示教模式后执行一次|
|`piper_set_mit.py`|设定机械臂为mit模式，这个模式下机械臂响应最快速|
|`piper_slave_config.py`|机械臂设置为从臂|
|`piper_status.py`|机械臂状态读取|
|`piper_stop.py`|机械臂停止缓慢下落，需要在使用后reset，并重新使能两次|
|`read_gripper_status.py`|机械臂夹爪状态读取|
|`read_joint_state.py`|读取关节角消息并打印|
|`read_piper_hardware.py`|读取机械臂主控固件版本|
|`V2_gripper_param_config.py`|V2版本夹爪参数设定|
|`V2_installation_pos.py`|V2版本设定安装位置为水平正装|
|`V2_joint_mit_ctrl.py`|V2版本sdk单独电机mit参数设定|
|`V2_motor_max_spd_set.py`|V2版本sdk电机单独设定某个关节电机的最大速度限制|

注意：如果是在机械臂处于主动臂模式下，发送设置为从动臂指令后需要重新启动机械臂，机械臂才会切换到从动臂模式
