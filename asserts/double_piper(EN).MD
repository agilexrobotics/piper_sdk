# Use two arm to remote control

[中文](double_piper.MD)

## 1 Hardware connection

- Diagram

![ ](../asserts/wire_connection.PNG)

1. Set one of the robotic arms as the master arm and the other as the slave arm (as shown in the demo above), then power off both robotic arms.
2. Connect the two robotic arms to a CAN module, and connect the CANs of the master and slave arms.
3. Power on the slave arm first, then the master arm, wait a few seconds, and then you can perform remote control.
4. If it fails, check whether the CAN line is connected properly, and try to power it off and on again.

## 2 Read the master-slave data

See the interface description in the SDK for details.

[Interface_V1 README](./V1/INTERFACE_V1.MD) <br> [Interface_V2 README](./V2/INTERFACE_V2.MD)

Here is just a brief description

### 2.1 Reading Master Arm Messages

The functions `GetArmJointMsgs` and `GetArmGripperMsgs` are used to obtain the slave robotic arm joint messages and gripper messages (raw messages).

The functions `GetArmJointCtrl` and `GetArmGripperCtrl` are used to obtain the master robotic arm joint messages and gripper messages (raw messages).

### 2.2 Control slave arm

`MotionCtrl_2` is used to set the control command mode, taking joint mode as an example.

```python
# 0x01 Set CAN command control mode. 0x01 Set joint control mode. 50 Set robotic arm movement speed.
piper.MotionCtrl_2(0x01, 0x01, 50)
```

`JointCtrl` is used to control six joints

`GripperCtrl` is used to control the gripper

Note!!!: **When controlling the slave arm, the master arm and the slave arm need to be disconnected. You can unplug the master arm's aviation plug and then run the slave arm control program. Otherwise, even if the program is executed, the slave arm will be out of control because the master arm is always sending slave arm control commands**
