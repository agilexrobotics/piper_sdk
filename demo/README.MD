# Piper 机械臂sdk部分demo

[EN](README(EN).MD)

![ubuntu](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)

Test:

|PYTHON |STATE|
|---|---|
|![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

## 安装方法

### 安装依赖

```shell
pip3 install python-can
```

```shell
pip3 install piper_sdk
```

can模块激活说明[can README](./can_config.MD)

## demo说明

```shell
.
├── piper_disable.py
├── piper_enable.py
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
├── read_joint_state.py
└── read_piper_hardware.py
```

|文件 |说明|
|---|---|
|`piper_disable.py`|机械臂失能|
|`piper_enable.py`|机械臂使能|
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
|`read_joint_state.py`|读取关节角消息并打印|
|`read_piper_hardware.py`|读取机械臂主控固件版本|

注意：如果是在机械臂处于主动臂模式下，发送设置为从动臂指令后需要重新启动机械臂，机械臂才会切换到从动臂模式

## 使用双臂摇操作

### 硬件设置流程

- 示意图

![ ](./asserts/接线图.PNG)

1. 单独将其中一个机械臂设定为主动臂，另一条设定为从动臂(如上demo)，然后将两个机械臂下电
2. 将两个机械臂共同连接在一个can模块上，令主从臂的can连接
3. 先将从动臂上电，然后将主动臂上电，稍等几秒，即可进行遥操作
4. 如未成功，请查看can线是否连接正常，尝试重新断电上电

### 读取主从臂数据

详见SDK中interface说明，这里只作简要

#### 读取主动臂消息

`GetArmJointMsgs`、`GetArmGripperMsgs`这两个函数用来获取从动机械臂关节消息和夹爪消息(原始消息)

`GetArmJointCtrl`、`GetArmGripperCtrl`这两个函数用来获取主动机械臂关节消息和夹爪消息(原始消息)

#### 控制从臂

`MotionCtrl_2`用来设定控制指令模式，以关节模式举例

```python
# 0x01设定can指令控制模式；0x01设定关节控制模式；50设定机械臂运动速度
piper.MotionCtrl_2(0x01, 0x01, 50)
```

`JointCtrl`用来控制六个关节

`GripperCtrl`用来控制夹爪

注意！！！：**控制从臂的时候，需要将主臂和从臂断开，可以将主臂的航插拔掉，再执行控制从臂程序，否则就算执行了程序，由于主臂也一直在发送控制从臂指令，会出现从臂失控现象**
