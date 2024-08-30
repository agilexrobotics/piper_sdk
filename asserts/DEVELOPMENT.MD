# PIPER SDK 开发文档

本SDK用于接收can数据帧，然后处理为自定义数据类型

ps：有些地方略写，代码中有详细的中文注释，本文这里只是理清结构

## 文件结构

```shell
piper_sdk
├── piper_msgs
├── base
├── demo
├── hardware_port
├── __init__.py
├── interface
├── protocol
└── README.MD
```

底层交互：

与can路由进行数据交互

```shell
hardware_port
├── can_encapsulation.py
└── __init__.py
```

机械臂数据变量：

预留v2版本，为日后修改数据格式留出余量

```shell
piper_msgs
├── __init__.py
├── msg_v1
│   ├── arm_id_type_map.py
│   ├── arm_messages.py
│   ├── arm_msg_type.py
│   ├── can_id.py
│   ├── feedback
│   │   ├── arm_crash_protection_rating_feedback.py
│   │   ├── arm_end_pose.py
│   │   ├── arm_feedback_current_end_vel_acc_param.py
│   │   ├── arm_feedback_current_motor_angle_limit_max_spd.py
│   │   ├── arm_feedback_current_motor_max_acc_limit.py
│   │   ├── arm_feedback_joint_vel_acc.py
│   │   ├── arm_high_spd_feedback.py
│   │   ├── arm_joint_feedback.py
│   │   ├── arm_low_spd_feedback.py
│   │   ├── arm_status.py
│   │   ├── gripper_feedback.py
│   │   └── __init__.py
│   ├── __init__.py
│   └── transmit
│       ├── arm_circular_pattern.py
│       ├── arm_crash_protection_rating_config.py
│       ├── arm_end_vel_acc_param_config.py
│       ├── arm_gripper_ctrl.py
│       ├── arm_joint_config.py
│       ├── arm_joint_ctrl.py
│       ├── arm_light_ctrl.py
│       ├── arm_master_slave_config.py
│       ├── arm_motion_ctrl_1.py
│       ├── arm_motion_ctrl_2.py
│       ├── arm_motion_ctrl_cartesian.py
│       ├── arm_motor_angle_limit_max_spd_config.py
│       ├── arm_motor_enable_disable.py
│       ├── arm_param_enquiry_and_config.py
│       ├── arm_search_motor_max_angle_spd_acc_limit.py
│       ├── arm_set_instruction_response.py
│       └── __init__.py
└── msg_v2
```

机械臂协议解析：

暂为v1版本，为日后修改协议留出余量

```shell
protocol
├── piper_protocol_base.py
└── protocol_v1
    ├── piper_protocol_v1.py
    └── __init__.py
```

机械臂实际接口：

具体使用部分接口，抽象为具体功能函数，部分功能可能需要二次封装

```shell
interface
└── piper_interface.py
```

## interface解析

具体的接口函数的详细说明请看[Interface README](./INTERFACE.MD)

## protocol解析

具体的数据解析协议函数的详细说明请看[Protocol README](./PROTOCOL_V1.MD)
