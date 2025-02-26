
Version 0.2.16
=============

Features
--------

- Changed the parameter names of `foc_status` in `piper_msgs/msg_v1(msg_v2)/feedback/arm_low_spd_feedback.py` in two files:
  - Renamed `sensor_status` to `collision_status`
  - Renamed `homing_status` to `stall_status`
- Added type checking (must be of Python's int type) and value range checking (within joint limit range) for the `JointCtrl` function.
- Added type checking (must be of Python's int type) for the `EndPoseCtrl` function's input values
- Modified the comments in the `SearchAllMotorMaxAngleSpd` and `SearchAllMotorMaxAccLimit` functions to include CAN ID descriptions.
- Added a demo file to set and print the robotic arm's collision level `piper_read_crash_protectation.py`.

Bug Fixes
---------

None

Miscellaneous
---------

None

Version 0.1.16
=============

Features
--------

- Corrected the output unit for the gripper's printed data.
- Fixed some comments and provided clearer explanations.
- Unified the code formatting to maintain consistency.
- Added data limits for the gripper message sending: [0, 5000], corresponding to [0, 5] N/m.
- Added data limits for setting the maximum joint speed: [0, 3000], corresponding to [0, 3] rad/s.
- Added data limits for setting the maximum joint acceleration: [0, 500], corresponding to [0, 5] rad/s^2.

Bug Fixes
---------

None

Miscellaneous
---------

None

Version 0.1.15
=============

Features
--------

None

Bug Fixes
---------

* Fixed an issue in the CAN send function where calling `is_can_bus_ok` resulted in `base_state` being None(#23).

Miscellaneous
---------

None

Version 0.1.14
=============

Features
--------

Modified the GetFK function to include a mode parameter to choose the source of the robotic arm's forward kinematics joint data.

The mode parameter supports only two values: ["feedback", "control"].

The default value for mode is "feedback".

- 'feedback' -> Data from the robotic arm's feedback joint angle messages, corresponding to the data returned by the GetArmJointMsgs function.
- 'control' -> Data from the joint angle control messages sent in the robotic arm's master arm mode, corresponding to the data returned by the GetArmJointCtrl function.

Bug Fixes
---------

None

Miscellaneous
---------

None

Version 0.1.13
=============

Features
--------

Correct errors in the version 0.1.12 documentation.

Bug Fixes
---------

None

Miscellaneous
---------

None

Version 0.1.12
=============

Features
--------

### 1 ChangeLog-V1

The V1 version code here is the code under version 0.1.x.

The code in version 0.1.x differs significantly from the code in version 0.0.x. The V1 version in the former is an update and iteration based on the latter.

The following sections mainly explain the differences between the 0.1.x-V1 version code and the 0.0.x version code.

#### 1.1 Firmware Compatibility

- **Compatible with new firmware (before version V1.5-2), the protocol content is not detailed here.**

#### 1.2 Interface

- **`C_PiperInterface`**

##### 1.2.1 Interface Features

- Added conditional instantiation for the class. The condition is the `can_name` passed to the interface. For example, in a loop, repeatedly calling `piper = C_PiperInterface(can_name="can0")` will only create one instance. Subsequent instantiations will recognize that an instance with `can_name="can0"` has already been created and will not create a new one.
- The class now includes frame rate calculation. You can use the `isOk` function to check if CAN data transmission is normal. A True feedback indicates normal data transmission, while False indicates that the data has been disconnected.
- Added forward kinematics (FK) calculation. The pose of each joint relative to the base_link is calculated by extending the DH parameters. This can be obtained through the `GetFK` function, which returns the pose of link1 to link6 in a 6*6 list. The last element represents the pose of link6.

##### 1.2.2 Functions

Compared to version 0.0.x, version 0.1.x-V1 adds several functions as follows:

| Functio  | Type           | Description                                                 | Usage    | Parameters            | Feedback   |
| -------- | -------------- | ----------------------------------------------------------- | -------- | --------------------- | --------- |
| `GetCanFps`|Getter Method| Get the current real-time frame rate of the CAN bus. | obj.GetArmStatus()     | None | int |
| `GetFK`|Getter Method| Get the forward kinematics of each joint of the robot arm. XYZ is in mm, RXRYRZ is in degrees. It returns a list of 6 floats, representing the pose of joints 1-6 relative to base_link. | obj.GetFK() | None | self.__link_fk |
| `isOk`| Getter Method  | Check if the CAN data reading thread is functioning normally.   | obj.isOk() | None | self.__is_ok |
| `__CanMonitor`| Getter Method  | Monitor the CAN data frame rate. | Used internally in class | None | None |
| `__UpdatePiperFK`| Getter Method | Updates the Piper forward kinematics data. | Used internally in class | None | None |

### 2 ChangeLog-V2

The V1 and V2 version codes here are both under version 0.1.x.

In version 0.1.x, the difference between V2 and V1 is the protocol.

The code in version 0.1.x differs significantly from the code in version 0.0.x.

The following sections mainly explain the differences between V2 and V1.

#### 2.1 Firmware Compatibility

- **Compatible with new firmware (after version V1.5-2), while maintaining compatibility with the previous version firmware.**

##### 2.1.1 0x2A1 Robot Arm Status Feedback

Additional information:

Byte 2 mode feedback now includes 0x04 MOVE M feedback, which corresponds to the MIT mode feedback.

##### 2.1.2 0x151 Mode Control Protocol

Additional information:

Byte 1 MOVE mode now includes the 0x04 MOVE M instruction, which sets the MIT mode.

Added:

Byte 5 installation position settings:

- 0x00 Invalid value
- 0x01 Horizontal mounting (standard position)
- 0x02 Left side mounting
- 0x03 Right side mounting

Note: Ensure wiring faces backward.

##### 2.1.3 New MIT Control Commands

| Robot Arm Joint 1-6 MIT Control Command |                                       | ID  0x15A ~ 0x15F |      len 8      |
|----------------------------------------|---------------------------------------|------------------|-----------------|
|        Data                             |                  Function              |        Type      |                 |
|       Byte 0                            |  Pos_ref [bit15~bit8] High 8 bits      |       uint8      |                 |
|       Byte 1                            |  Pos_ref [bit7~bit0] Low 8 bits        |       uint8      |                 |
|       Byte 2                            |  Vel_ref [bit11~bit4] Low 12 bits      |       uint8      |                 |
|       Byte 3                            |  Vel_ref [bit3~bit0] Kp [bit11~bit8]  |       uint8      |                 |
|       Byte 4                            |  Kp [bit7~bit0]                       |       uint8      | Kp reference value: 10  |
|       Byte 5                            |  Kd [bit11~bit4] Low 12 bits          |       uint8      | Kd reference value: 0.8 |
|       Byte 6                            |  Kd [bit3~bit0] T_ref [bit7~bit4]      |       uint8      |                 |
|       Byte 7                            |  T_ref [bit3~bit0] CRC [bit3~bit0]     |       uint8      |                 |

##### 2.1.4 ID 0x474 Motor Angle Limit / Maximum Speed Setting Command

Additional invalid value command

| Motor Angle Limit / Maximum Speed Setting Command |                             | ID  0x474  |                           |
|---------------------------------------------------|-----------------------------|------------|---------------------------|
|          Data                                     |           Function          |    Type    |                           |
|       Byte 0                                      |  Joint Motor Serial Number  |    uint8   | Range 1-6: 1-6 represents joint actuator serial number; |
|       Byte 1                                      |  Maximum Angle Limit High   |    uint16  | Unit: 0.1° **Invalid value: 0x7FFF** |
|       Byte 2                                      |  Maximum Angle Limit Low    |            |                           |
|       Byte 3                                      |  Minimum Angle Limit High   |    uint16  | Unit: 0.1° **Invalid value: 0x7FFF** |
|       Byte 4                                      |  Minimum Angle Limit Low    |            |                           |
|       Byte 5                                      |  Maximum Joint Speed High   |    uint16  | Unit: 0.001 rad/s **Invalid value: 0x7FFF** |
|       Byte 6                                      |  Maximum Joint Speed Low    |            |                           |
|       Byte 7                                      |  Reserved                   |            |                           |

##### 2.1.5 ID 0x475 Joint Setting Command

Additional invalid value command

| Joint Setting Command |                                       | ID  0x475        |                                         |
|-----------------------|---------------------------------------|------------------|-----------------------------------------|
|          Data         |                  Function              |        Type      |                                         |
|       Byte 0          |  Joint Motor Serial Number             |       uint8      | Range 1-7: 1-6 represents joint actuator serial number; 7 represents all joint motors |
|       Byte 1          |  Set the current position of motor N as zero point |       uint8      | Valid value: 0xAE                       |
|       Byte 2          |  Acceleration parameter setting effectiveness |       uint8      | Valid value: 0xAE                       |
|       Byte 3          |  Maximum Joint Acceleration High       |       uint16     | Unit: 0.001 rad/s² **Invalid value: 0x7FFF** |
|       Byte 4          |  Maximum Joint Acceleration Low        |                  | Valid value: 0xAE                       |
|       Byte 5          |  Clear Joint Error Code                |       uint8      |                                         |
|       Byte 6          |  Reserved                              |                  |                                         |
|       Byte 7          |  Reserved                              |                  |                                         |

##### 2.1.6 ID 0x477 Robot Arm Parameter Query and Setting Command

Additional information:

Query gripper/teach pendant parameter index: 0x04

| Joint Setting Command |                                       | ID  0x475        |                                         |
|-----------------------|---------------------------------------|------------------|-----------------------------------------|
|          Data         |                  Function             |        Type      |                                         |
|       Byte 0          |  Parameter Query                      |       uint8      | Query end-effector V/acc parameters: 0x01, Query collision protection level: 0x02, Query current trajectory index: 0x03, **Query gripper/teach pendant parameter index: 0x04** |
|       Byte 1          |  Parameter Setting                    |       uint8      | Set end-effector V/acc parameters to initial values: 0x01, Set all joint limits, maximum joint speeds, and joint accelerations to default values: 0x02 |
|       Byte 2          |  0x48X Message Feedback Setting       |       uint8      | Invalid: 0x00; Enable periodic feedback: 0x01; Disable periodic feedback: 0x02; After enabling, periodic reporting of current end-effector speed/acceleration for joints 1-6 |
|       Byte 3          |  End-effector load parameter setting effectiveness |       uint8      | Valid value: 0xAE                       |
|       Byte 4          |  Set End-effector Load                |       uint8      | 0x00 -- No load; 0x01 -- Half load; 0x02 -- Full load |
|       Byte 5          |  Reserved                             |       uint8      |                                         |
|       Byte 6          |  Reserved                             |                  |                                         |
|       Byte 7          |  Reserved                             |                  |                                         |

##### 2.1.7 ID 0x479 End-effector Speed/Acceleration Parameter Setting Command

Additional invalid value command

| End-effector Speed/Acceleration Parameter Setting Command |                                       | ID  0x479        |                                         |
|-----------------------------------------------------------|---------------------------------------|------------------|-----------------------------------------|
|          Data                                             |                  Function             |       Type       |                                         |
|       Byte 0                                              |  Maximum Linear Speed High            |      uint16      | Unit: 0.001 m/s **Invalid value: 0x7FFF** |
|       Byte 1                                              |  Maximum Linear Speed Low             |                  |                                         |
|       Byte 2                                              |  Maximum Angular Speed High           |      uint16      | Unit: 0.001 rad/s **Invalid value: 0x7FFF** |
|       Byte 3                                              |  Maximum Angular Speed Low            |                  |                                         |
|       Byte 4                                              |  Maximum Linear Acceleration High     |      uint16      | Unit: 0.001 m/s² **Invalid value: 0x7FFF** |
|       Byte 5                                              |  Maximum Linear Acceleration Low      |                  |                                         |
|       Byte 6                                              |  Maximum Angular Acceleration High    |      uint16      | Unit: 0.001 rad/s² **Invalid value: 0x7FFF** |
|       Byte 7                                              |  Maximum Angular Acceleration Low     |                  |                                         |

##### 2.1.8 New ID 0x47D Gripper/Teach Pendant Parameter Setting Command

| Gripper/Teach Pendant Parameter Setting Command |                                       | ID  0x47D        |                                         |
|-------------------------------------------------|---------------------------------------|------------------|-----------------------------------------|
|          Data                                   |                  Function             |        Type      |                                         |
|       Byte 0                                    |  Teach Pendant Stroke Coefficient Setting |       uint8      | Teach pendant stroke coefficient setting: 100~200, Unit: % (default 100%), only applies to setting the main arm of the master-slave arms, used to amplify the control stroke for the slave arm |
|       Byte 1                                    |  Gripper/Teach Pendant Maximum Control Stroke Limit Setting |       uint8      | Unit: mm; Invalid value: 0; Small gripper: 70mm; Large gripper: 100mm |
|       Byte 2                                    |  Reserved                             |                  |                                         |
|       Byte 3                                    |  Reserved                             |                  |                                         |
|       Byte 4                                    |  Reserved                             |                  |                                         |
|       Byte 5                                    |  Reserved                             |                  |                                         |
|       Byte 6                                    |  Reserved                             |                  |                                         |
|       Byte 7                                    |  Reserved                             |                  |                                         |

##### 2.1.9 New ID 0x47E Gripper/Teach Pendant Parameter Feedback Command

| Gripper/Teach Pendant Parameter Feedback Command |                                       | ID  0x47E        |                                         |
|--------------------------------------------------|---------------------------------------|------------------|-----------------------------------------|
|          Data                                    |                  Function             |        Type      |                                         |
|       Byte 0                                     |  Teach Pendant Stroke Coefficient Feedback |       uint8      | Teach pendant stroke coefficient setting: 100~200, Unit: % (default 100%), only applies to setting the main arm of the master-slave arms, used to amplify the control stroke for the slave arm |
|       Byte 1                                     |  Gripper/Teach Pendant Maximum Control Stroke Limit Feedback |       uint8      | Unit: mm; Invalid value: 0; Small gripper: 70mm; Large gripper: 100mm |
|       Byte 2                                     |  Reserved                             |                  |                                         |
|       Byte 3                                     |  Reserved                             |                  |                                         |
|       Byte 4                                     |  Reserved                             |                  |                                         |
|       Byte 5                                     |  Reserved                             |                  |                                         |
|       Byte 6                                     |  Reserved                             |                  |                                         |
|       Byte 7                                     |  Reserved                             |                  |                                         |

#### 2.2 interface

- **Retain V1 version `C_PiperInterface`, add `C_PiperInterface_V2`**

The V2 version is maintained separately, although some code is duplicated, it ensures independence between versions, with minimal difference in usage.

In the V2 version, several functions have been added based on V1, as follows:

| Function   | Type |Description                                                         |Usage                | Parameters                        |Feedback       |
| ----- | ---- |------------------------------------------------------------ |-------------------|--------------------------- |--------|
|`GetGripperTeachingPendantParamFeedback`|Getter Method|Get gripper/teach pendant parameter feedback, including the teach pendant stroke coefficient feedback and the gripper/teach pendant maximum control stroke limit feedback after actively sending the command. |obj.GetGripperTeachingPendantParamFeedback()|None|self.__feedback_gripper_teaching_pendant_param|
|`MotorMaxSpdSet`|Ctrl Method|Set the maximum motor speed. |Called externally|`motor_num (int)`, `max_joint_spd (int)`|None|
|`__JointMitCtrl`|Ctrl Method|0x15A,0x15B,0x15C,0x15D,0x15E,0x15F,MIT control command for arm joints 1~6|Called externally|`self,motor_num:int`,`pos_ref:float`,`vel_ref:float`,`kp:float`,`kd:float`,`t_ref:float`,`p_min:float=-12.5`,`p_max:float=12.5`,`v_min:float=-45.0`,`v_max:float=45.0`,`kp_min:float=0.0`,`kp_max:float=500.0`,`kd_min:float=-5.0`,`kd_max:float=5.0`,`t_min:float=-18.0`,`t_max:float=18.0`|None|
|`JointMitCtrl`|Ctrl Method|0x15A,0x15B,0x15C,0x15D,0x15E,0x15F,MIT control command for arm joints 1~6|Called externally|`self,motor_num:int`,`pos_ref:float`,`vel_ref:float`,`kp:float`,`kd:float`,`t_ref:float`|None|
|`GripperTeachingPendantParamConfig`|Ctrl Method|Gripper/teach pendant parameter setting command (based on V1.5-2 version or later)|Called externally|`teaching_range_per:int=100`, `max_range_config:int=70`|None|

Bug Fixes
---------

None

Miscellaneous
---------

None

Version 0.0.12
=============

Features
--------

- Modified the CAN bus class to make the data reading section compatible with Ubuntu 18.04 and Python 3.6.
- Updated the protocol_base to simplify the function that converts values to a list by using struct and ctypes.
- Added singleton pattern support in the interface class.
- Added thread protection to the `ConnectPort` function in the interface class.
- Added a `DisconnectPort` function to the interface class to stop the data reading process.
- Changed the `Update` function and some variables in the interface class to private.
- Fixed erroneous comments to make them more readable.
- Optimized the document structure and descriptions.
- Added an interface to query the robotic arm's firmware.
- Added all demos (e.g., moveC).

Bug Fixes
---------

- Corrected the spelling of "jonit" to "joint".
- Fixed the unit for setting maximum motor acceleration to 0.01 rad/s^2; added a new function `JointMaxAccConfig` to set the motor's maximum acceleration.

Miscellaneous
---------

None
