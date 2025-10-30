# Piper Robotic Arm SDK (V2) Demo

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

Note: piper_sdk >= 0.1.9

```shell
pip3 install piper_sdk
```

Instructions for activating the CAN module [can README](../../asserts/can_config.MD)

## Demo Overview

| File | Description |
|---|---|
|[`piper_ctrl_disable.py`](./piper_ctrl_disable.py)|Disable the robotic arm.|
|[`piper_ctrl_enable.py`](./piper_ctrl_enable.py)|Enable the robotic arm.|
|[`piper_ctrl_end_pose.py`](./piper_ctrl_end_pose.py)|Control the end-effector of the robotic arm.|
|[`piper_ctrl_go_zero.py`](./piper_ctrl_go_zero.py)|Control the robotic arm to the zero position.|
|[`piper_ctrl_gripper.py`](./piper_ctrl_gripper.py)|Control the robotic arm gripper.|
|[`piper_ctrl_joint.py`](./piper_ctrl_joint.py)|Control the robotic arm joints.|
|[`piper_ctrl_line.py`](./piper_ctrl_line.py)|Control the robotic arm in line motion mode.|
|[`piper_ctrl_moveC.py`](./piper_ctrl_moveC.py)|Set the robotic arm to circular motion mode.|
|[`piper_ctrl_moveJ.py`](./piper_ctrl_moveJ.py)|Control the joint movement of the robotic arm.|
|[`piper_ctrl_moveL.py`](./piper_ctrl_moveL.py)|Control the robotic arm to draw a square on the XOY plane.|
|[`piper_ctrl_moveP.py`](./piper_ctrl_moveP.py)|Control the movement of the robotic arm's end effector.|
|[`piper_ctrl_reset.py`](./piper_ctrl_reset.py)|Reset the robotic arm. This must be executed once after setting it to teaching mode.|
|[`piper_ctrl_stop.py`](./piper_ctrl_stop.py)|Stop the robotic arm and allow it to descend slowly. After use, reset and re-enable twice before resuming normal control.|
|[`piper_read_all_fps.py`](./piper_read_all_fps.py)|Read the frequency of specified robotic arm data.|
|[`piper_read_arm_motor_max_acc_limit.py`](./piper_read_arm_motor_max_acc_limit.py)|Read the maximum acceleration limits of all motors.|
|[`piper_read_arm_motor_max_angle_spd.py`](./piper_read_arm_motor_max_angle_spd.py)|Read the maximum angle and speed limits of all robotic arm motors.|
|[`piper_read_crash_protectation.py`](./piper_read_crash_protectation.py)|Read the robotic arm's collision protection level.|
|[`piper_read_end_pose.py`](./piper_read_end_pose.py)|Read the end-effector pose.|
|[`piper_read_firmware.py`](./piper_read_firmware.py)|Read the main controller firmware version of the robotic arm.|
|[`piper_read_fk.py`](./piper_read_fk.py)|Read the forward kinematics solution for each joint.|
|[`piper_read_gripper_status.py`](./piper_read_gripper_status.py)|Read the status of the robotic arm gripper.|
|[`piper_read_high_msg.py`](./piper_read_high_msg.py)|Read high-speed messages from the robotic arm.|
|[`piper_read_joint_ctrl.py`](./piper_read_joint_ctrl.py)|Read and print joint control messages.|
|[`piper_read_joint_state.py`](./piper_read_joint_state.py)|Read and print joint state messages.|
|[`piper_read_low_msg.py`](./piper_read_low_msg.py)|Read low-speed messages from the robotic arm.|
|[`piper_read_mode_ctrl_canid_151.py`](./piper_read_mode_ctrl_canid_151.py)|Read the current mode control message from CAN ID 151.|
|[`piper_read_mode_ctrl.py`](./piper_read_mode_ctrl.py)|Read the current mode control message from CAN ID 151.|
|[`piper_read_resp_instruction.py`](./piper_read_resp_instruction.py)|Read the current instruction of the robotic arm.|
|[`piper_read_status.py`](./piper_read_status.py)|Read the current status of the robotic arm.|
|[`piper_read_tcp_pose.py`](./piper_read_tcp_pose.py)|Read the tool center point (TCP) pose.|
|[`piper_read_version.py`](./piper_read_version.py)|Read the software version of each module in the robotic arm SDK.|
|[`piper_set_can.py`](./piper_set_can.py)|Set the CAN bus parameters for the robotic arm.|
|[`piper_set_gripper_zero.py`](./piper_set_gripper_zero.py)|Set the zero position of the robotic arm gripper.|
|[`piper_set_init_default.py`](./piper_set_init_default.py)|Set all joint limits, maximum joint speeds, and joint accelerations to default values.|
|[`piper_set_joint_zero_cpv.py`](./piper_set_joint_zero_cpv.py)|Set the joint motor zero-point position (including zero-point learning calibration in CPV mode).|
|[`piper_set_joint_zero.py`](./piper_set_joint_zero.py)|Set the zero position of the robotic arm joints.|
|[`piper_set_load.py`](./piper_set_load.py)|Set the end load parameters for the robotic arm.|
|[`piper_set_log_level.py`](./piper_set_log_level.py)|Set the log level for the robotic arm SDK.|
|[`piper_set_master.py`](./piper_set_master.py)|Set the robotic arm as the master arm.|
|[`piper_set_mit.py`](./piper_set_mit.py)|Set the robotic arm to MIT mode, which provides the fastest response.|
|[`piper_set_motor_angle_limit.py`](./piper_set_motor_angle_limit.py)|Set the angle limits for individual joint motors.|
|[`piper_set_motor_max_acc_limit.py`](./piper_set_motor_max_acc_limit.py)|Set the maximum acceleration limit for individual joint motors.|
|[`piper_set_sdk_param.py`](./piper_set_sdk_param.py)|Set SDK parameters for joint and gripper limits.|
|[`piper_set_slave.py`](./piper_set_slave.py)|Set the robotic arm as the slave arm.|
|[`piper_test_interface_disconnect.py`](./piper_test_interface_disconnect.py)|Test the interface disconnect functionality.|
|[`piper_test_multi_interface_instance.py`](./piper_test_multi_interface_instance.py)|Test multiple interface instances.|
|[`V2_piper_ctrl_joint_mit.py`](./V2_piper_ctrl_joint_mit.py)|Control individual joints in MIT mode.|
|[`V2_piper_ctrl_motor_max_spd.py`](./V2_piper_ctrl_motor_max_spd.py)|Set maximum speed limits for individual joint motors.|
|[`V2_piper_read_gripper_param_feedback.py`](./V2_piper_read_gripper_param_feedback.py)|Read gripper parameter feedback.|
|[`V2_piper_set_gripper_param.py`](./V2_piper_set_gripper_param.py)|Set gripper parameters.|
|[`V2_piper_set_installation_pos.py`](./V2_piper_set_installation_pos.py)|Set the installation position to horizontal upright.|

**Note:** If the robotic arm is in master arm mode, after sending the command to set it to slave arm mode, the arm needs to be restarted for the change to take effect.
