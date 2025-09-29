# Q&A

## 1. First-time Use: Gripper/Teach Pendant Cannot Be Controlled and No Feedback

Note: **This feature is not available in the V1 version interface**

> The gripper/teach pendant are end effectors, hereafter referred to as end effectors.

In the new version, the gripper needs to have its stroke range set at the factory. If this is not set, you will experience issues where the feedback value is always zero, and control is not possible.

The V2 version interface and above should be used to set this.

1. Execute [piper_disable.py](../demo/V2/piper_disable.py) to disable the robotic arm. Note that disabling the arm will cut power to all motors immediately.
2. Execute [V2_gripper_param_config.py](../demo/V2/V2_gripper_param_config.py) to set the stroke range for the end effector.
3. Then, execute [read_gripper_status.py](../demo/V2/read_gripper_status.py) to check if the end effector provides any feedback.
4. If you find that the stroke data for the end effector is too large when closed, you can use [piper_gripper_zero_set.py](../demo/V2/piper_gripper_zero_set.py) to set the end effector’s zero position

## 2. Jetson Orin Nano cannot detect official CAN module

For Jetpack 6.0 and above, you need to use the command line Jetpack and then compile the `gs_usb` module into the kernel during the kernel compilation phase.

Reference Links:<https://forums.developer.nvidia.com/t/missing-gs-usb-kernel-module-for-jetpack-6/275287/7>

You need to add `CONFIG_CAN_GS_USB=m`, etc., that is, refer to the `defconfig.jetpack_5_1_2.txt` file, add what is missing in `defconfig.jetpack_6_0.txt`, complete the `gs_usb` module related to CAN, and then recompile the kernel.
