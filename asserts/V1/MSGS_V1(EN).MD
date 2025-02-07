# PIPER SDK msgs

[中文](MSGS_V1.MD)

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

`can_id.py` file is the enumeration class of all canids

`arm_msg_type.py` file is the enumeration class of all message types

`arm_id_type_map.py` file is the mapping map of canid and message type

`arm_messages.py` file is the summary of all custom message types, among which `PiperMessage` is the bridge between can message and abstract type

When reading data, filter out the corresponding message type according to canid and assign it to `PiperMessage`, parse the can frame from bytes type to the specified integer, and then assign it to the variable of the corresponding message type

When sending data, first create a variable of type `PiperMessage`, pass in the message type and the corresponding message class, then execute the protocol to parse it into a can frame and send it out

Directory `feedback` is all messages related to feedback

Directory `transmit` is all messages related to sending
