# PIPER SDK msgs 说明文档

[EN](MSGS_V1(EN).MD)

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

`can_id.py` 文件为所有canid的枚举类

`arm_msg_type.py` 文件为所有消息类型的枚举类

`arm_id_type_map.py` 文件为canid和消息类型的映射map

`arm_messages.py` 文件为所有自定义消息类型的汇总，其中的`PiperMessage`是can消息和抽象类型的桥梁

读取数据时，根据canid筛选出对应的消息类型并赋给`PiperMessage`，将can帧从bytes类型解析为指定的整形，然后赋值到对应的消息类型的变量中

发送数据时，先创建一个`PiperMessage`类型的变量，传入消息类型和对应的消息类，然后执行协议解析为can帧并发送出去

目录 `feedback` 为所有有关反馈的消息

目录 `transmit` 为所有发送有关的消息
