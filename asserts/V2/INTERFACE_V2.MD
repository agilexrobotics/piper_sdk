# Piper Interface V2 Documentation

## Class: C_PiperInterface_V2

Main interface class for controlling the Piper robotic arm.

Based on version V1.5-2 frimware and later

Inner class identifies instances based on `can_port`, preventing the creation of duplicate `C_PiperInterface_V2` instances with the same `can_port`.

### Constructor Parameters

- `can_name` (str, default="can0"): CAN port name
- `judge_flag` (bool, default=True): Determines if the CAN port is functioning correctly. When using a PCIe-to-CAN module, set to false.
- `can_auto_init` (bool, default=True): Determines if the CAN port is automatically initialized.
- `dh_is_offset` (int, default=0): Does the j1-j2 offset by 2° in the DH parameters?
  - 0: No offset
  - 1: Offset applied
- `start_sdk_joint_limit` (bool, default=True): Enable SDK joint limits
- `start_sdk_gripper_limit` (bool, default=True): Enable SDK gripper limits

### Connection Methods

#### get_connect_status

```python
def get_connect_status(self)
```

Get connection status

Used to feedback whether the ConnectPort function has been called, You need to call ConnectPort again for the function feedback to become `True`

`False` if DisconnectPort was called

#### ConnectPort

```python
def ConnectPort(can_init: bool = False, piper_init: bool = True, start_thread: bool = True)
```

Starts a thread to process data from the connected CAN port.

Parameters:

- `can_init`: CAN port init flag. Set to True after using DisconnectPort().
- `piper_init`: Execute the robot arm initialization function
- `start_thread`: Start the reading thread

#### DisconnectPort

```python
def DisconnectPort(thread_timeout=0.1)
```

Disconnects the port without blocking the main thread.

### Init Methods

```python
def PiperInit()
```

- Sends a command to query the maximum angular speed of joint motors.
- Sends a command to query the maximum acceleration limit of joint motors.
- Sends a command to query the robotic arm firmware.

### Control Methods

#### EmergencyStop

```python
def EmergencyStop(emergency_stop: Literal[0x00, 0x01, 0x02] = 0)
```

Emergency stop control command (CAN ID: 0x150)

Parameters:

- `emergency_stop`:
  - 0x00: Invalid
  - 0x01: Emergency stop
  - 0x02: Resume

#### ModeCtrl

```python
def ModeCtrl(ctrl_mode: Literal[0x00, 0x01] = 0x01,
            move_mode: Literal[0x00, 0x01, 0x02, 0x03] = 0x01,
            move_spd_rate_ctrl: int = 50,
            is_mit_mode: Literal[0x00, 0xAD, 0xFF] = 0x00)
```

Mode control command (CAN ID: 0x151)

Parameters:

- `ctrl_mode`:
  - 0x00: Standby mode
  - 0x01: CAN command control mode
- `move_mode`:
  - 0x00: MOVE P (Position)
  - 0x01: MOVE J (Joint)
  - 0x02: MOVE L (Linear)
  - 0x03: MOVE C (Circular)
- `move_spd_rate_ctrl`: Movement speed percentage (0-100)
- `is_mit_mode`:
  - 0x00: Position-velocity mode
  - 0xAD: MIT mode
  - 0xFF: Invalid

#### EnableArm

```python
def EnableArm(motor_num: Literal[1, 2, 3, 4, 5, 6, 7, 0xFF] = 7,
             enable_flag: Literal[0x01, 0x02] = 0x02)
```

Enable motor(s) command (CAN ID: 0x471)

Parameters:

- `motor_num`: Motor number [1-7], 7 represents all motors
- `enable_flag`: 0x02 for enable

#### DisableArm

```python
def DisableArm(motor_num: Literal[1, 2, 3, 4, 5, 6, 7, 0xFF] = 7,
              enable_flag: Literal[0x01, 0x02] = 0x01)
```

Disable motor(s) command (CAN ID: 0x471)

Parameters:

- `motor_num`: Motor number [1-7], 7 represents all motors
- `enable_flag`: 0x01 for disable

#### EndPoseCtrl

```python
def EndPoseCtrl(X: int, Y: int, Z: int, RX: int, RY: int, RZ: int)
```

End effector position control (CAN ID: 0x152, 0x153, 0x154)

Parameters:

- `X`: X-axis coordinate (0.001mm)
- `Y`: Y-axis coordinate (0.001mm)
- `Z`: Z-axis coordinate (0.001mm)
- `RX`: Rotation about X-axis (0.001 degrees)
- `RY`: Rotation about Y-axis (0.001 degrees)
- `RZ`: Rotation about Z-axis (0.001 degrees)

#### JointCtrl

```python
def JointCtrl(joint_1: int, joint_2: int, joint_3: int, joint_4: int, joint_5: int, joint_6: int)
```

Joint control command (CAN ID: 0x155, 0x156, 0x157)

Joint angle limits:

| Joint | Limit (rad) | Limit (degrees) |
|-------|-------------|-----------------|
| 1 | [-2.6179, 2.6179] | [-150.0, 150.0] |
| 2 | [0, 3.14] | [0, 180.0] |
| 3 | [-2.967, 0] | [-170, 0] |
| 4 | [-1.745, 1.745] | [-100.0, 100.0] |
| 5 | [-1.22, 1.22] | [-70.0, 70.0] |
| 6 | [-2.09439, 2.09439] | [-120.0, 120.0] |

Parameters (all in 0.001 degrees):

- `joint_1`: Joint 1 angle
- `joint_2`: Joint 2 angle
- `joint_3`: Joint 3 angle
- `joint_4`: Joint 4 angle
- `joint_5`: Joint 5 angle
- `joint_6`: Joint 6 angle

#### GripperCtrl

```python
def GripperCtrl(gripper_angle: int = 0,
               gripper_effort: int = 0,
               gripper_code: Literal[0x00, 0x01, 0x02, 0x03] = 0,
               set_zero: Literal[0x00, 0xAE] = 0)
```

Gripper control command (CAN ID: 0x159)

Parameters:

- `gripper_angle`: Gripper angle (0.001°)
- `gripper_effort`: Gripper torque (0.001 N/m, range 0-5000 corresponds to 0-5 N/m)
- `gripper_code`:
  - 0x00: Disable
  - 0x01: Enable
  - 0x02: Disable and clear error
  - 0x03: Enable and clear error
- `set_zero`:
  - 0x00: Invalid value
  - 0xAE: Set current position as zero point

#### MoveCAxisUpdateCtrl

```python
def MoveCAxisUpdateCtrl(instruction_num: Literal[0x00, 0x01, 0x02, 0x03] = 0x00)
```

MoveC mode coordinate point update command. Before using, switch the robotic arm mode to MoveC control mode.
This function must be used together with EndPoseCtrl.

Usage sequence:

1. First, use EndPoseCtrl to set the starting point, then call MoveCAxisUpdateCtrl(0x01).
2. Next, use EndPoseCtrl to set the middle point, then call MoveCAxisUpdateCtrl(0x02).
3. Finally, use EndPoseCtrl to set the endpoint, then call MoveCAxisUpdateCtrl(0x03).

Parameters:

- `instruction_num`: Instruction point number
  - 0x00: Invalid
  - 0x01: Start point
  - 0x02: Middle point
  - 0x03: End point

### Search Methods

#### SearchMotorMaxAngleSpdAccLimit

```python
def SearchMotorMaxAngleSpdAccLimit(motor_num: Literal[1, 2, 3, 4, 5, 6] = 1,
                                 search_content: Literal[0x01, 0x02] = 0x01)
```

Query motor angle/maximum speed/maximum acceleration limit command (CAN ID: 0x472)

Parameters:

- `motor_num`: Joint motor number [1-6]
- `search_content`: Query content type
  - 0x01: Query angle/speed limit
  - 0x02: Query acceleration limit

#### SearchAllMotorMaxAngleSpd

```python
def SearchAllMotorMaxAngleSpd()
```

Query maximum angle/speed limits for all motors (CAN ID: 0x472)

#### SearchAllMotorMaxAccLimit

```python
def SearchAllMotorMaxAccLimit()
```

Query maximum acceleration limits for all motors (CAN ID: 0x472)

#### SearchPiperFirmwareVersion

```python
def SearchPiperFirmwareVersion()
```

Query Piper robotic arm firmware version (CAN ID: 0x4AF)

### Get Methods

#### GetCurrentInterfaceVersion

```python
def GetCurrentInterfaceVersion()
```

Returns the current interface version.

#### GetCurrentSDKVersion

```python
def GetCurrentSDKVersion()
```

Returns the current SDK version.

#### GetCurrentProtocolVersion

```python
def GetCurrentProtocolVersion()
```

Returns the current protocol version.

#### GetCanFps

```python
def GetCanFps()
```

Returns the frame rate of the robotic arm CAN module.

#### GetArmStatus

```python
def GetArmStatus()
```

Returns the current status of the robotic arm (CAN ID: 0x2A1)

#### GetArmEndPoseMsgs

```python
def GetArmEndPoseMsgs()
```

Returns the end effector pose (position -> in 0.001 mm and orientation -> in 0.001 degrees)

Manual unit conversion of data is required.

#### GetArmJointMsgs

```python
def GetArmJointMsgs()
```

Returns the joint angles (in 0.001 degrees)

Manual unit conversion of data is required.

#### GetFK

```python
def GetFK(mode: Literal["feedback", "control"] = "feedback")
```

**Note: Normal data will be obtained only after the `EnableFkCal` function is called, otherwise all data will be 0**

Returns the forward kinematics solution for each joint of the robotic arm.

Parameters:

- `mode`: Data source mode
  - "feedback": Get feedback data (default)
  - "control": Get control data

Returns:

- A 6x6 list containing the poses of joints 1-6 relative to the base_link
  - Each row represents a joint's pose (j1 to j6)
  - Each pose contains [X, Y, Z, RX, RY, RZ]
  - XYZ units are in 0.001mm
  - RX, RY, RZ units are in 0.001degrees
  - Index [-1] represents the pose of joint 6 relative to base_link

Manual unit conversion of data is required.

#### GetArmGripperMsgs

```python
def GetArmGripperMsgs()
```

Retrieve the robotic arm gripper status message.

Returns:

- `gripper_state`: Gripper status object
  - `grippers_angle`: int32, Gripper angle in 0.001°
  - `grippers_effort`: uint16, Gripper torque in 0.001N/m
  - `status_code`: uint8, Gripper status code

Manual unit conversion of data is required.

#### GetArmHighSpdInfoMsgs

```python
def GetArmHighSpdInfoMsgs()
```

Returns high-speed feedback including:

- Speed (rotation speed)
- Current(in 0.001 A)
- Position(in 0.001 rad)

Manual unit conversion of data is required.

#### GetArmLowSpdInfoMsgs

```python
def GetArmLowSpdInfoMsgs()
```

Returns low-speed feedback including:

- Voltage(in 0.1 V)
- Driver temperature(in 1℃)
- Motor temperature(in 1℃)
- Driver status
- Bus current(in 0.001 A)

Manual unit conversion of data is required.

#### GetCurrentMotorAngleLimitMaxVel

```python
def GetCurrentMotorAngleLimitMaxVel()
```

Returns the motor angle limit/maximum speed command (CAN ID: 0x473)

This includes:

- Maximum angle limit
- Minimum angle limit
- Maximum joint speed

This is the feedback message after sending the query command (0x472 Byte 1 = 0x01)

#### GetCurrentEndVelAndAccParam

```python
def GetCurrentEndVelAndAccParam()
```

Returns the end effector velocity and acceleration parameters (CAN ID: 0x478)

This includes:

- End effector linear velocity
- End effector angular velocity
- End effector linear acceleration
- End effector angular acceleration

This is the feedback message after sending the query command (0x477 Byte 0 = 0x01)

#### GetCrashProtectionLevelFeedback

```python
def GetCrashProtectionLevelFeedback()
```

Returns the collision protection level feedback (CAN ID: 0x47B)

This includes collision levels for joints 1-6 (values range from 0 to 8):

- 0: No collision detection
- 1-8: Detection levels with increasing thresholds

This is the feedback message after sending the query command (0x477 Byte 0 = 0x02)

#### GetGripperTeachingPendantParamFeedback

```python
def GetGripperTeachingPendantParamFeedback()
```

Returns the gripper/teaching pendant parameter feedback (CAN ID: 0x47E)

This includes:

- Teaching pendant travel coefficient
- Maximum control travel limit values for gripper/teaching pendant

This is the feedback message after sending the query command (0x477 Byte 0 = 0x04)

#### GetCurrentMotorMaxAccLimit

```python
def GetCurrentMotorMaxAccLimit()
```

Returns the current motor's maximum acceleration limit

This includes:

- Current motor number
- Maximum joint acceleration of the current motor

#### GetArmJointCtrl

```python
def GetArmJointCtrl()
```

Returns the joint control commands (CAN ID: 0x155, 0x156, 0x157)

Units are in 0.001 degrees

#### GetArmGripperCtrl

```python
def GetArmGripperCtrl()
```

Returns the gripper control command (CAN ID: 0x159)

#### GetArmModeCtrl

```python
def GetArmModeCtrl()
```

Returns the robotic arm mode control command (CAN ID: 0x151)

#### GetAllMotorMaxAccLimit

```python
def GetAllMotorMaxAccLimit()
```

Returns the maximum acceleration limits for all motors

#### GetAllMotorAngleLimitMaxSpd

```python
def GetAllMotorAngleLimitMaxSpd()
```

Returns the maximum limit angle, minimum limit angle, and maximum speed for all motors (m1-m6)

#### GetPiperFirmwareVersion

```python
def GetPiperFirmwareVersion()
```

Returns the Piper software firmware version

Success: Returns the corresponding string
Failure: Returns -0x4AF

#### isOk

```python
def isOk()
```

Returns whether the CAN data reading thread is functioning normally.

### Configuration Methods

#### EnableFkCal

```python
def EnableFkCal(self)
```

Enable forward kinematics calculations in SDK internal threads

#### DisableFkCal

```python
def DisableFkCal(self)
```

Disable forward kinematics calculations in SDK internal threads

#### isCalFk

```python
def isCalFk(self)
```

Whether the forward kinematics calculation is turned on, feedback `True` or `False`

#### MasterSlaveConfig

```python
def MasterSlaveConfig(linkage_config: int, feedback_offset: int, ctrl_offset: int, linkage_offset: int)
```

Sets the master/slave mode configuration (CAN ID: 0x470)

Parameters:

- `linkage_config` (int): The linkage setting command.
    0x00: Invalid
    0xFA: Set as teaching input arm
    0xFC: Set as motion output arm
- `feedback_offset` (int): The feedback command offset value.
    0x00: No offset / restore default
    0x10: Feedback command base ID shifts from 2Ax to 2Bx
    0x20: Feedback command base ID shifts from 2Ax to 2Cx
- `ctrl_offset` (int): The control command offset value.
    0x00: No offset / restore default
    0x10: Control command base ID shifts from 15x to 16x
    0x20: Control command base ID shifts from 15x to 17x
- `linkage_offset` (int): The linkage mode control target address offset value.
    0x00: No offset / restore default
    0x10: Control target address base ID shifts from 15x to 16x
    0x20: Control target address base ID shifts from 15x to 17x

#### MotorAngleLimitMaxSpdSet

```python
def MotorAngleLimitMaxSpdSet(motor_num: Literal[1, 2, 3, 4, 5, 6] = 1,
                           max_angle_limit: int = 0x7FFF,
                           min_angle_limit: int = 0x7FFF,
                           max_joint_spd: int = 0x7FFF)
```

Sets motor angle limit and maximum speed (CAN ID: 0x474)

Parameters:

- `motor_num`: Joint motor number (1-6)
- `max_angle_limit`: Maximum angle limit (0.1°, 0x7FFF for invalid)
- `min_angle_limit`: Minimum angle limit (0.1°, 0x7FFF for invalid)
- `max_joint_spd`: Maximum joint speed (0.001 rad/s, range [0, 3000], 0x7FFF for invalid)

Speed limits for each joint:

| Joint | Speed Limit (rad/s) |
|-------|-------------------|
| 1 | [0, 3.0] |
| 2 | [0, 3.0] |
| 3 | [0, 3.0] |
| 4 | [0, 3.0] |
| 5 | [0, 3.0] |
| 6 | [0, 3.0] |

#### MotorMaxSpdSet

```python
def MotorMaxSpdSet(motor_num: Literal[1, 2, 3, 4, 5, 6] = 6,
                  max_joint_spd: int = 3000)
```

Sets motor maximum speed (Based on V1.5-2 and later) (CAN ID: 0x474)

Parameters:

- `motor_num`: Motor number (1-6)
- `max_joint_spd`: Maximum joint speed (0.001 rad/s, range 0-3000, corresponding to 0-3 rad/s)

#### JointConfig

```python
def JointConfig(joint_num: Literal[1, 2, 3, 4, 5, 6, 7] = 7,
               set_zero: Literal[0x00, 0xAE] = 0,
               acc_param_is_effective: Literal[0x00, 0xAE] = 0,
               max_joint_acc: int = 500,
               clear_err: Literal[0x00, 0xAE] = 0)
```

Joint configuration command (CAN ID: 0x475)

Parameters:

- `joint_num`: Joint motor number (1-6, 7 for all joints)
- `set_zero`: Set current position as zero point (0xAE)
- `acc_param_is_effective`: Enable acceleration parameter (0xAE)
- `max_joint_acc`: Maximum joint acceleration (0.01 rad/s², range [0, 500] -> [0, 5.0 rad/s²])
- `clear_err`: Clear joint error code (0xAE)

#### JointMaxAccConfig

```python
def JointMaxAccConfig(joint_num: Literal[1, 2, 3, 4, 5, 6] = 1,
                     max_joint_acc: int = 500)
```

Sets maximum acceleration for a joint (CAN ID: 0x477)

Parameters:

- `joint_num`: Joint motor number (1-6)
- `max_joint_acc`: Maximum joint acceleration (0.01 rad/s², range [0, 500] -> [0, 5.0 rad/s²])

#### ArmParamEnquiryAndConfig

```python
def ArmParamEnquiryAndConfig(param_enquiry: Literal[0x00, 0x01, 0x02, 0x03, 0x04] = 0x00, 
                            param_setting: Literal[0x00, 0x01, 0x02] = 0x00, 
                            data_feedback_0x48x: Literal[0x00, 0x01, 0x02] = 0x00, 
                            end_load_param_setting_effective: Literal[0x00, 0xAE] = 0x00, 
                            set_end_load: Literal[0x00, 0x01, 0x02, 0x03] = 0x03)
```

Arm parameter enquiry and configuration command (CAN ID: 0x477)

Parameters:

- `param_enquiry` (int): Parameter enquiry.
  - 0x01 -> 0x478: Query end-effector velocity/acceleration
  - 0x02 -> 0x47B: Query collision protection level
  - 0x03: Query current trajectory index
  - 0x04 -> 0x47E: Query gripper/teaching pendant parameter index(Based on version V1.5-2 and later)

- `param_setting` (int): Parameter setting.
  - 0x01: Set end effector velocity/acceleration parameters to initial values.
  - 0x02: Set all joint limits, joint maximum speed, and joint acceleration to default values.

- `data_feedback_0x48x` (int): 0x48X message feedback settings.
  - 0x00: Invalid.
  - 0x01: Disable periodic feedback.
  - 0x02: Enable periodic feedback.

When enabled, periodic reporting includes the current end effector speed/acceleration for joints 1-6.

- `end_load_param_setting_effective` (int): Whether the end load parameter setting is effective.
  - Valid value: 0xAE.

- `set_end_load` (int): Set end load.
  - 0x00: No load.
  - 0x01: Half load.
  - 0x02: Full load.
  - 0x03: Invalid.

#### EndSpdAndAccParamSet

```python
def EndSpdAndAccParamSet(max_linear_vel: int = 1000,
                        max_angular_vel: int = 1000,
                        max_linear_acc: int = 1000,
                        max_angular_acc: int = 1000)
```

Sets end effector velocity and acceleration parameters (CAN ID: 0x478)

Parameters:

- `max_linear_vel`: Maximum linear velocity (0.001 m/s)
- `max_angular_vel`: Maximum angular velocity (0.001 rad/s)
- `max_linear_acc`: Maximum linear acceleration (0.001 m/s²)
- `max_angular_acc`: Maximum angular acceleration (0.001 rad/s²)

#### CrashProtectionConfig

```python
def CrashProtectionConfig(joint_1_protection_level: int,
                        joint_2_protection_level: int,
                        joint_3_protection_level: int,
                        joint_4_protection_level: int,
                        joint_5_protection_level: int,
                        joint_6_protection_level: int)
```

Sets collision protection levels for each joint (CAN ID: 0x47A)

Parameters:

- `joint_X_protection_level`: Protection level for each joint (0-8)
  - 0: No collision detection
  - 1-8: Increasing detection thresholds

#### GripperTeachingPendantParamConfig

```python
def GripperTeachingPendantParamConfig(teaching_range_per: int = 100,
                                    max_range_config: int = 70,
                                    teaching_friction: int = 1)
```

Sets gripper/teaching pendant parameters (Based on V1.5-2 and later) (CAN ID: 0x47D)

Parameters:

- `teaching_range_per`: Teaching pendant travel range coefficient (100-200)
- `max_range_config`: Maximum control travel limit (0, 70, or 100)
- `teaching_friction`: Teaching friction parameter

### MIT Mode Control

#### JointMitCtrl

```python
def JointMitCtrl(motor_num: int,
                pos_ref: float,
                vel_ref: float,
                kp: float,
                kd: float,
                t_ref: float)
```

MIT (Model-based Impedance Tuning) control for joints (CAN ID: 0x15A-0x15F)

Parameters:

- `motor_num`: Motor number [1-6]
- `pos_ref`: Target position (rad, [-12.5, 12.5])
- `vel_ref`: Motor velocity ([-45.0, 45.0])
- `kp`: Proportional gain ([0.0, 500.0], reference: 10)
- `kd`: Derivative gain ([-5.0, 5.0], reference: 0.8)
- `t_ref`: Target torque ([-18.0, 18.0])

### SDK Parameter Methods

#### GetSDKJointLimitParam

```python
def GetSDKJointLimitParam(joint_name: Literal["j1", "j2", "j3", "j4", "j5", "j6"])
```

Get joint limit parameters from SDK

#### SetSDKJointLimitParam

```python
def SetSDKJointLimitParam(joint_name: Literal["j1", "j2", "j3", "j4", "j5", "j6"],
                        min_val: float,
                        max_val: float)
```

Set joint limit parameters in SDK

#### GetSDKGripperRangeParam

```python
def GetSDKGripperRangeParam()
```

Get gripper range parameters from SDK

#### SetSDKGripperRangeParam

```python
def SetSDKGripperRangeParam(min_val: float, max_val: float)
```

Set gripper range parameters in SDK
