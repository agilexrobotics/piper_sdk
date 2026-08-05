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
- `logger_level` (LogLevel, default=LogLevel.WARNING): Set the log level
- `log_to_file` (bool, default=False): Whether to enable the log writing function, True to enable, default to disable
- `log_file_path` (str, default=None): Set the path to write the log file, the default is the log folder under the sdk path

Note:

- The LogLevel definition is as follows:

  ```python
  class LogLevel(IntEnum):
      DEBUG = logging.DEBUG
      INFO = logging.INFO
      WARNING = logging.WARNING
      ERROR = logging.ERROR
      CRITICAL = logging.CRITICAL
      SILENT = 100
  ```

### Connection Methods

#### CreateCanBus

```python
def CreateCanBus(self, 
                  can_name:str, 
                  bustype="socketcan", 
                  expected_bitrate:int=1000000,
                  judge_flag:bool=False)
```

Create can related interfaces

Args:

- can_name: The name of the CAN port.
- bustype: The type of CAN bus, default is socket CAN.
- expected_bitrate: The expected bitrate for the CAN bus.
- judge_flag: Whether to check the CAN port during the instantiation of the class. In some cases, it should be set to False.

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

#### ResetPiper

```python
def ResetPiper()
```

The robot will immediately lose power and fall down, clearing all errors and internal flags.

#### ModeCtrl

```python
def ModeCtrl(ctrl_mode: Literal[0x00, 0x01] = 0x01,
            move_mode: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05] = 0x01,
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
  - 0x04: MOVE M (MIT) ---- Based on version V1.5-2 and later
  - 0x05: MOVE CPV ---- Based on version V1.8-1 and later
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

- `gripper_angle`: Gripper range, expressed as an integer, unit 0.001mm
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

#### GetCanBus

```python
def GetCanBus()
```

Return can encapsulation class, which contains some socketcan related functions

#### GetCanName

```python
def GetCanName()
```

Get the can port name currently read by current interface.

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
'''
Retrieves the current status of the robotic arm.

CAN ID:
  0x2A1

Returns
-------
time_stamp : float
  time stamp
Hz : float
  msg fps
arm_status : ArmMsgFeedbackStatus
  机械臂状态

  - ctrl_mode (int): Control Mode
      * 0x00 Standby mode
      * 0x01 CAN command control mode
      * 0x02 Teaching mode
  - arm_status (int): Robotic arm status
      * 0x00 normal
      * 0x01 Emergency Stop
      * 0x02 No solution
      * 0x03 singularity
      * 0x04 Target angle exceeds limit
      * 0x05 Abnormal joint communication
      * 0x06 Joint brake is not open
      * 0x07 The robotic arm collided
      * 0x08 Overspeed during drag teaching
      * 0x09 Abnormal joint condition
      * 0x0A Other abnormalities
      * 0x0B Teaching records
      * 0x0C Teaching execution
      * 0x0D Teaching pause
      * 0x0E Main control NTC overtemperature
      * 0x0F Release resistor NTC overtemperature
  - mode_feed (int): Mode Feedback
      * 0x00 MOVE P
      * 0x01 MOVE J
      * 0x02 MOVE L
      * 0x03 MOVE C
      * 0x04 MOVE M ---Based on V1.5-2 version
      * 0x05 MOVE_CPV ---Based on V1.6.5
  - teach_status (int): Teaching status
  - motion_status (int): Movement status
      * 0x00 Arrive at the designated point
      * 0x01 Did not reach the designated point
  - trajectory_num (int): Current running track point number
  - err_status (int): Fault status
  {
      * joint_1_angle_limit (bool): Whether the angle of joint 1 exceeds the limit, True means it exceeds the limit
      * joint_2_angle_limit (bool): Whether the angle of joint 2 exceeds the limit, True means it exceeds the limit
      * joint_3_angle_limit (bool): Whether the angle of joint 3 exceeds the limit, True means it exceeds the limit
      * joint_4_angle_limit (bool): Whether the angle of joint 4 exceeds the limit, True means it exceeds the limit
      * joint_5_angle_limit (bool): Whether the angle of joint 5 exceeds the limit, True means it exceeds the limit
      * joint_6_angle_limit (bool): Whether the angle of joint 6 exceeds the limit, True means it exceeds the limit
      * communication_status_joint_1 (bool): Is the communication of joint 1 abnormal. True means communication abnormal
      * communication_status_joint_2 (bool): Is the communication of joint 2 abnormal. True means communication abnormal
      * communication_status_joint_3 (bool): Is the communication of joint 3 abnormal. True means communication abnormal
      * communication_status_joint_4 (bool): Is the communication of joint 4 abnormal. True means communication abnormal
      * communication_status_joint_5 (bool): Is the communication of joint 5 abnormal. True means communication abnormal
      * communication_status_joint_6 (bool): Is the communication of joint 6 abnormal. True means communication abnormal
  }
'''
```

Returns the current status of the robotic arm (CAN ID: 0x2A1)

#### GetArmEndPoseMsgs

```python
def GetArmEndPoseMsgs()
'''
Retrieves the end effector pose message of the robotic arm. Euler angle representation.

Returns
-------
time_stamp : float
Hz : float
end_pose : ArmMsgFeedBackEndPose

  - X_axis (int): X position, (in 0.001 mm)
  - Y_axis (int): Y position, (in 0.001 mm)
  - Z_axis (int): Z position, (in 0.001 mm)
  - RX_axis (int): RX orientation, (in 0.001 degrees)
  - RY_axis (int): RY orientation, (in 0.001 degrees)
  - RZ_axis (int): RZ orientation, (in 0.001 degrees)
'''
```

Returns the end effector pose (position -> in 0.001 mm and orientation -> in 0.001 degrees)

Manual unit conversion of data is required.

#### GetArmJointMsgs

```python
def GetArmJointMsgs()
'''
Retrieves the joint status message of the robotic arm.(in 0.001 degrees)

Returns
-------
time_stamp : float
Hz : float
joint_state : ArmMsgFeedBackJointStates

  - joint_1 (int): Feedback angle of joint 1, (in 0.001 degrees).
  - joint_2 (int): Feedback angle of joint 2, (in 0.001 degrees).
  - joint_3 (int): Feedback angle of joint 3, (in 0.001 degrees).
  - joint_4 (int): Feedback angle of joint 4, (in 0.001 degrees).
  - joint_5 (int): Feedback angle of joint 5, (in 0.001 degrees).
  - joint_6 (int): Feedback angle of joint 6, (in 0.001 degrees).
'''
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
'''
Retrieves the gripper status message of the robotic arm.

Returns
-------
time_stamp : float
  time stamp
Hz : float
  msg fps
gripper_state : ArmMsgFeedBackGripper

  - grippers_angle (int): The stroke of the gripper (in 0.001 mm).
  - grippers_effort (int): The torque of the gripper (in 0.001 N·m).
  - foc_status (int):  The status code of the gripper.
  {
      * voltage_too_low (bool): Power voltage low (False: Normal, True: Low)
      * motor_overheating (bool): Motor over-temperature (False: Normal, True: Over-temperature)
      * driver_overcurrent (bool): Driver over-current (False: Normal, True: Over-current)
      * driver_overheating (bool): Driver over-temperature (False: Normal, True: Over-temperature)
      * sensor_status (bool): Sensor status (False: Normal, True: Abnormal)
      * driver_error_status (bool): Driver error status (False: Normal, True: Error)
      * driver_enable_status (bool): Driver enable status (False: Disabled, True: Enabled)
      * homing_status (bool): Zeroing status (False: Not zeroed, True: Zeroed or previously zeroed)
  }
'''
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
'''
Retrieves the high-speed feedback message of the robotic arm.

Returns
-------
time_stamp : float
  time stamp
Hz : float
  msg fps
motor_x : ArmMsgFeedbackHighSpd

  - can_id (int): Current CAN ID, used to represent the joint number.
  - motor_speed (int): Motor Speed (in 0.001rad/s).
  - current (int): Motor  (in 0.001A).
  - pos (int): Motor Position (rad).
  - effort (int): Torque converted using a fixed coefficient, (in 0.001 N/m).
'''
```

Returns high-speed feedback including:

- Speed (rotation speed)
- Current(in 0.001 A)
- Position(in 0.001 rad)

Manual unit conversion of data is required.

#### GetMotorStates

```python
def GetMotorStates()
'''
Retrieves the robot arm motor status message of the robotic arm.

Returns
-------
time_stamp : float
  time stamp
Hz : float
  msg fps
motor_x : ArmMsgFeedbackHighSpd

  - can_id (int): Current CAN ID, used to represent the joint number.
  - motor_speed (int): Motor Speed (in 0.001rad/s).
  - current (int): Motor  (in 0.001A).
  - pos (int): Motor Position (rad).
  - effort (int): Torque converted using a fixed coefficient, (in 0.001 N/m).
'''
```

#### GetArmLowSpdInfoMsgs

```python
def GetArmLowSpdInfoMsgs()
'''
Retrieves the low-speed feedback message of the robotic arm.

Returns
-------
time_stamp : float
  time stamp
Hz : float
  msg fps
motor_x : ArmMsgFeedbackLowSpd

  - can_id (int): CAN ID, representing the current motor number.
  - vol (int): Current driver voltage (in 0.1V).
  - foc_temp (int): Driver temperature (in 1℃).
  - motor_temp (int): Motor temperature (in 1℃).
  - foc_status (int): Driver status.
  {
      * voltage_too_low (bool): Power voltage low (False: Normal, True: Low)
      * motor_overheating (bool): Motor over-temperature (False: Normal, True: Over-temperature)
      * driver_overcurrent (bool): Driver over-current (False: Normal, True: Over-current)
      * driver_overheating (bool): Driver over-temperature (False: Normal, True: Over-temperature)
      * collision_status (bool): Collision protection status (False: Normal, True: Trigger protection)
      * driver_error_status (bool): Driver error status (False: Normal, True: Error)
      * driver_enable_status (bool): Driver enable status (False: Disabled, True: Enabled)
      * stall_status (bool): Stalling protection status (False: Normal, True: Trigger protection)
  }
  - bus_current (int): Current driver current (in 0.001A).
'''
```

Returns low-speed feedback including:

- Voltage(in 0.1 V)
- Driver temperature(in 1℃)
- Motor temperature(in 1℃)
- Driver status
- Bus current(in 0.001 A)

Manual unit conversion of data is required.

#### GetDriverStates

```python
def GetDriverStates()
'''
Retrieves the low-speed feedback message of the robotic arm.

Returns
-------
time_stamp : float
  time stamp
Hz : float
  msg fps
motor_x : ArmMsgFeedbackLowSpd

  - can_id (int): CAN ID, representing the current motor number.
  - vol (int): Current driver voltage (in 0.1V).
  - foc_temp (int): Driver temperature (in 1℃).
  - motor_temp (int): Motor temperature (in 1℃).
  - foc_status (int): Driver status.
  {
      * voltage_too_low (bool): Power voltage low (False: Normal, True: Low)
      * motor_overheating (bool): Motor over-temperature (False: Normal, True: Over-temperature)
      * driver_overcurrent (bool): Driver over-current (False: Normal, True: Over-current)
      * driver_overheating (bool): Driver over-temperature (False: Normal, True: Over-temperature)
      * collision_status (bool): Collision protection status (False: Normal, True: Trigger protection)
      * driver_error_status (bool): Driver error status (False: Normal, True: Error)
      * driver_enable_status (bool): Driver enable status (False: Disabled, True: Enabled)
      * stall_status (bool): Stalling protection status (False: Normal, True: Trigger protection)
  }
  - bus_current (int): Current driver current (in 0.001A).
'''
```

Returns low-speed feedback including:

- Voltage(in 0.1 V)
- Driver temperature(in 1℃)
- Motor temperature(in 1℃)
- Driver status
- Bus current(in 0.001 A)

Manual unit conversion of data is required.

#### GetArmEnableStatus

```python
def GetArmEnableStatus(self)->list:
'''
Get the robot arm enable status

Returns
-------
  list : bool
'''
```

Feedback the enable status of the six motors, return a list of length 6, variable type is bool, when True, it means the specified motor is enabled.

#### GetCurrentMotorAngleLimitMaxVel

```python
def GetCurrentMotorAngleLimitMaxVel()
'''Retrieves the motor angle limit/maximum speed command.

This includes the following information:
  Maximum angle limit
  Minimum angle limit
  Maximum joint speed
This is the feedback message after actively sending a command.
Corresponds to the query for motor angle/maximum speed/maximum acceleration limit command 0x472,
with Byte 1 = 0x01

ArmParamEnquiryAndConfig(param_enquiry=0x01)

CAN ID:
  0x473

Returns
-------
time_stamp : float
  time stamp
current_motor_angle_limit_max_vel : ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd

  - motor_num (int): Joint motor serial number
  - max_angle_limit (int): Maximum angle limit, unit 0.1 degree
  - min_angle_limit (int): Minimum angle limit, unit 0.1 degree
  - max_joint_spd (int): Maximum joint speed, unit 0.001rad/s
'''
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
'''Retrieves the end effector velocity and acceleration parameters.

This includes the following information:
  End effector linear velocity
  End effector angular velocity
  End effector linear acceleration
  End effector angular acceleration
This is the feedback message after actively sending a command.
Corresponds to the robotic arm parameter query and setting command 0x477,
with Byte 0 = 0x01

ArmParamEnquiryAndConfig(param_enquiry=0x01)

CAN ID:
  0x478

Returns
-------
time_stamp : float
  time stamp
current_end_vel_acc_param : ArmMsgFeedbackCurrentEndVelAccParam

  - end_max_linear_vel (int): Maximum linear velocity at the end, unit 0.001m/s
  - end_max_angular_vel (int): Maximum angular velocity at the end, unit 0.001rad/s
  - end_max_linear_acc (int): Maximum linear acceleration at the end, unit 0.001m/s^2
  - end_max_angular_acc (int): Maximum angular acceleration at the end, unit 0.001rad/s^2
'''
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
'''Retrieves the collision protection level feedback.

This includes the following information:
  Collision level for joints 1-6 (values range from 0 to 8).
      0: No collision detection.
      1-8: Detection levels, where the threshold for collision detection increases progressively.
This is the feedback message after actively sending a command.
Corresponds to the robotic arm parameter query and setting command 0x477,
with Byte 0 = 0x02

ArmParamEnquiryAndConfig(param_enquiry=0x02)

CAN ID:
  0x47B

Returns
-------
time_stamp : float
crash_protection_level_feedback : ArmMsgFeedbackCrashProtectionRating

  - joint_1_protection_level (int): No. 1 joint collision protection level
  - joint_2_protection_level (int): No. 2 joint collision protection level
  - joint_3_protection_level (int): No. 3 joint collision protection level
  - joint_4_protection_level (int): No. 4 joint collision protection level
  - joint_5_protection_level (int): No. 5 joint collision protection level
  - joint_6_protection_level (int): No. 6 joint collision protection level
'''
```

Returns the collision protection level feedback (CAN ID: 0x47B)

This includes collision levels for joints 1-6 (values range from 0 to 8):

- 0: No collision detection
- 1-8: Detection levels with increasing thresholds

This is the feedback message after sending the query command (0x477 Byte 0 = 0x02)

#### GetGripperTeachingPendantParamFeedback

```python
def GetGripperTeachingPendantParamFeedback()
'''Gripper/Teaching Pendant Parameter Feedback Command
This includes the following information:
  Teaching pendant travel coefficient
  Maximum control travel limit values for gripper/teaching pendant
This is the feedback message after actively sending a command.
Corresponds to robotic arm parameter query and setting command 0x477, Byte 0 = 0x04
ArmParamEnquiryAndConfig(param_enquiry=0x04)

CAN ID:
  0x47E

Returns
-------
time_stamp : float
  time stamp
arm_gripper_teaching_param_feedback : ArmMsgFeedbackGripperTeachingPendantParam

  - teaching_range_per (int): 
    The stroke coefficient feedback of the teaching pendant is only applicable to the master arm when setting the master-slave arm. It is used to amplify the control stroke to the slave arm. The range is [100~200]
  - max_range_config (int): Gripper/teach pendant maximum control stroke limit value feedback, (0,70,100)
      Invalid value --- 0
      Small jaw: 70mm
      Large jaw: 100mm
  - teaching_friction (int): Teaching pendant friction coefficient setting, range [1, 10]
'''
```

Returns the gripper/teaching pendant parameter feedback (CAN ID: 0x47E)

This includes:

- Teaching pendant travel coefficient
- Maximum control travel limit values for gripper/teaching pendant

This is the feedback message after sending the query command (0x477 Byte 0 = 0x04)

#### GetCurrentMotorMaxAccLimit

```python
def GetCurrentMotorMaxAccLimit()
'''Retrieves the current motor's maximum acceleration limit.

This includes the following information:
  Current motor number
  The maximum joint acceleration of the current motor

Returns
-------
time_stamp : float
  time stamp
current_motor_max_acc_limit : ArmMsgFeedbackCurrentMotorMaxAccLimit

  - joint_motor_num (int): Joint motor serial number
  - max_joint_acc (int): Maximum joint acceleration, unit 0.001rad/^2
'''
```

Returns the current motor's maximum acceleration limit

This includes:

- Current motor number
- Maximum joint acceleration of the current motor

#### GetArmJointCtrl

```python
def GetArmJointCtrl()
'''
Retrieves the 0x155, 0x156, and 0x157 control commands, which are joint control commands.(in 0.001 degrees)

Returns
-------
time_stamp : float
Hz : float
joint_ctrl : ArmMsgFeedBackJointStates

  - joint_1 (int): Feedback angle of joint 1, in 0.001 degrees.
  - joint_2 (int): Feedback angle of joint 2, in 0.001 degrees.
  - joint_3 (int): Feedback angle of joint 3, in 0.001 degrees.
  - joint_4 (int): Feedback angle of joint 4, in 0.001 degrees.
  - joint_5 (int): Feedback angle of joint 5, in 0.001 degrees.
  - joint_6 (int): Feedback angle of joint 6, in 0.001 degrees.
'''
```

Returns the joint control commands (CAN ID: 0x155, 0x156, 0x157)

Units are in 0.001 degrees

#### GetArmGripperCtrl

```python
def GetArmGripperCtrl()
'''
Retrieves the gripper control message using the 0x159 command.

Returns
-------
time_stamp : float
  time stamp
Hz : float
  msg fps
gripper_ctrl : ArmMsgGripperCtrl

  - grippers_angle (int): The stroke of the gripper (in 0.001 mm).
  - grippers_effort (int): Gripper torque, represented as an integer, unit: 0.001N·m.Range 0-5000 (corresponse 0-5N/m)
  - status_code (int): 
      0x00: Disabled;
      0x01: Enabled;
      0x03: Enable and clear errors;
      0x02: Disable and clear errors.
  - set_zero (int): Set the current position as the zero point.
      0x00: Invalid;
      0xAE: Set zero.
'''
```

Returns the gripper control command (CAN ID: 0x159)

#### GetArmModeCtrl

```python
def GetArmModeCtrl()
'''
Retrieves the 0x151 control command, which is the robotic arm mode control command.

Returns
-------
time_stamp : float
    time stamp
Hz : float
    msg fps
ctrl_151 : ArmMsgMotionCtrl_2

  - ctrl_mode (int): Control mode.
      * 0x00: Standby mode.
      * 0x01: CAN command control mode.
      * 0x03: Ethernet control mode.
      * 0x04: Wi-Fi control mode.
      * 0x07: Offline trajectory mode.
  - move_mode (int): MOVE mode.
      * 0x00: MOVE P (Position).
      * 0x01: MOVE J (Joint).
      * 0x02: MOVE L (Linear).
      * 0x03: MOVE C (Circular).
      * 0x04: MOVE M (MIT)
  - move_spd_rate_ctrl (int): Movement speed as a percentage.Range: 0~100.
  - mit_mode (int): MIT mode.
      * 0x00: Position-speed mode.
      * 0xAD: MIT mode.
      * 0xFF: Invalid.
  - residence_time (int): Hold time at offline trajectory points.
      Range: 0~255, unit: seconds.
  - installation_pos (int): Installation Position - Note: Wiring should face 
  {
      * 0x00: Invalid value
      * 0x01: Horizontal upright
      * 0x02: Left-side mount
      * 0x03: Right-side mount
  }
'''
```

Returns the robotic arm mode control command (CAN ID: 0x151)

#### GetAllMotorMaxAccLimit

```python
def GetAllMotorMaxAccLimit()
'''Retrieves the maximum acceleration limits for all motors (m1-m6).

This is a response message, meaning the data will only be available after sending a request command.
The request command `self.SearchAllMotorMaxAccLimit()` has already been called in the `ConnectPort`.

Returns
-------
time_stamp : float
  time stamp

all_motor_max_acc_limit : ArmMsgFeedbackAllCurrentMotorMaxAccLimit

  - motor (ArmMsgFeedbackCurrentMotorMaxAccLimit): Current motor maximum acceleration limit
  {
      * joint_motor_num (int): Joint motor serial number
      * max_joint_acc (int): Maximum joint acceleration, unit 0.001rad/^2
  }
'''
```

Returns the maximum acceleration limits for all motors

#### GetAllMotorAngleLimitMaxSpd

```python
def GetAllMotorAngleLimitMaxSpd()
'''Retrieves the maximum limit angle, minimum limit angle, and maximum speed for all motors (m1-m6).

This is a response message, meaning the data will only be available after sending a request command.
The request command `self.SearchAllMotorMaxAngleSpd()` has already been called in the `ConnectPort`.

Returns
-------
time_stamp : float
  time stamp

all_motor_angle_limit_max_spd : ArmMsgFeedbackAllCurrentMotorAngleLimitMaxSpd

  - motor (ArmMsgFeedbackCurrentMotorAngleLimitMaxSpd): Current motor limit angle/maximum speed
  {
      * motor_num (int): Joint motor serial number
      * max_angle_limit (int): Maximum angle limit, unit 0.1 degree
      * min_angle_limit (int): Minimum angle limit, unit 0.1 degree
      * max_joint_spd (int): Maximum joint speed, unit 0.001rad/s
  }
'''
```

Returns the maximum limit angle, minimum limit angle, and maximum speed for all motors (m1-m6)

#### GetPiperFirmwareVersion

```python
def GetPiperFirmwareVersion()
```

Returns the Piper software firmware version

Success: Returns the corresponding string
Failure: Returns -0x4AF

#### GetRespInstruction

```python
def GetPiperFirmwareVersion()
'''
Sets the response for the instruction.

CAN ID: 0x476

Returns
-------
time_stamp : float
    time stamp

instruction_index (int): The response instruction index.
    This is derived from the last byte of the set instruction ID.
    For example, when responding to the 0x471 set instruction, this would be 0x71.

zero_config_success_flag (int): Flag indicating whether the zero point was successfully set.
    - 0x01: Zero point successfully set.
    - 0x00: Zero point set failed/not set.
    - This is only applicable when responding to a joint setting instruction that successfully sets motor N's current position as the zero point.
'''
```

#### isOk

```python
def isOk()
'''
Feedback on whether the CAN data reading thread is functioning normally

Returns
-------
bool: 
  True is normal
'''
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

#### EnableFilterAbnormalData

```python
def EnableFilterAbnormalData(self)
```

Enable filter abnormal data,joint data or end pose data

- The gripper travel filter is set to 150mm*1000;
- The joint angle filter is set to 300 degrees*1000;
- The end-point data xyz filter is set to 1m\*1000\*1000, and the rpy filter is set to 361 degrees*1000.

#### DisableFilterAbnormalData

```python
def DisableFilterAbnormalData(self)
```

Disable filter abnormal data,joint data or end pose data

#### isFilterAbnormalData

```python
def isFilterAbnormalData(self)
'''
Returns
-------
    bool: Whether to filter abnormal data, True to enable filtering
'''
```

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

#### ClearRespSetInstruction

```python
def GripperTeachingPendantParamConfig()
'''
Clear the SDK saved command response information.

Reset the command response to:
time_stamp = 0;
instruction_response.instruction_index = -1;
instruction_response.is_set_zero_successfully = -1
'''
```

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
- `t_ref`: Target torque ([-8.0, 8.0])

#### ReqMasterArmMoveToHome

```python
def ReqMasterArmMoveToHome(self, mode:Literal[0, 1, 2])
```

Request Master Arm Move to Home Command (Based on version V1.7-4 and later)

CAN ID:
    0x191

Parameters:

- `mode` (int): Request return-to-zero mode.
  - 0: Restore master-slave arm mode.
  - 1: Master arm return-to-zero.
  - 2: Master and slave arms return-to-zero together.

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
