# CHANGELOG(EN)

[Click to switch ZH](CHANGELOG(ZH).MD)
=============

Version 0.6.1
=============

Features
--------

- ✨ feat(can_encapsulation): Adds `dlc` and `is_extended_id` parameters to `SendCanMessage`
- ✨ feat(interface,piper_msgs): Adds CPV mode selection and comments
  - CPV mode can be switched using `ModeCtrl(0x01, 0x05)`

Bug Fixes
---------

None

Miscellaneous
---------

- 🧪 test(demo): Added a demo for setting the joint limit of a single motor, `piper_set_motor_angle_limit.py`
- 🧪 test(demo): Added a demo for setting the zero point of the robotic arm in CPV mode, `piper_set_joint_zero_cpv.py`
- 📃 docs(interface): Modified the comment for the bustype parameter in the CreateCanBus function
  - Modified the comments related to bustype in the `CreateCanBus` function to specify that the expected parameter is `'socketcan'` or `'slcan'`.
- 🧪 test(demo): Added three demos: moveJ, moveL, and moveP; synchronized the README in the demos.
  - Added a demo for `piper_ctrl_moveJ.py`, with the same content as `piper_ctrl_joint.py`;
  - Added a demo for `piper_ctrl_moveL.py`, which shows a robotic arm drawing a square;
  - Added a demo for `piper_ctrl_moveP.py`, with the same content as `piper_ctrl_end_pose.py`;
  - Synchronized the README content in the demos.

Version 0.6.0
=============

Features
--------

- ✨ feat(interface,can_encapsulation,demo): Added serial port CAN functionality (MAC support); Added some wrapper functions
  - Added serial port CAN reading functionality:
    - Gave `can_auto_init` a new meaning; when it is `False`, the CAN bus will not be initialized, and `CreateCanBus` needs to be called manually.
    - Added a check in `ConnectPort` to see if the CAN bus is None; if it is None, a ValueRrror error will be reported.
    - Modified the `Init` function in `can_encapsulation_v0_4_0` to add baud rate setting when creating the bus.
    - Added `piper_set_can.py` to `demo`.
  - Added some wrapper functions:
    - `GetMotorStates` is a wrapper function for `GetArmHighSpdInfoMsgs`, and the name has been changed to make its meaning clearer.
    - `GetDriverStates` is a wrapper function for `GetArmLowSpdInfoMsgs`, and the name has been changed to make its meaning clearer.
    - `ResetPiper` is a wrapper function for `MotionCtrl_1`, making the function of resetting the robotic arm a separate function.

Bug Fixes
---------

None

Miscellaneous
---------

- 📃 docs(Q&A.MD): Added explanations regarding the MIT protocol, clarifying the relationship between given torque and executed torque; added explanations regarding the value of motor feedback torque.
- 📃 docs(Q&A.MD): Added instructions on using serial port CAN in Q&A.MD
- 📃 docs(INTERFACE_V2.MD): Added descriptions of newly added functions in INTERFACE_V2.MD
- 📃 docs(asserts): Organized the images into the pictures folder

Version 0.5.0
=============

Features
--------

- ✨ feat(interface): Added abnormal data filtering for gripper travel, joint angle, and end-point data.
  - Abnormal data filtering is enabled by default. Use the `DisableFilterAbnormalData` function to disable it; use the `EnableFilterAbnormalData` function to enable it. The `isFilterAbnormalData` function returns True to indicate that the abnormal data filtering function is enabled.
  - The gripper travel filter is set to 150mm*1000;
  - The joint angle filter is set to 300 degrees*1000;
  - The end-point data xyz filter is set to 1m\*1000\*1000, and the rpy filter is set to 361 degrees*1000.
- ✨ feat(interface): Add the get function `GetCanBus` of the can class

Bug Fixes
---------

- 🐞 fix(msg, protocol, interface): Added command response feedback functionality, deprecating the previous version's set command response function.
  - Due to a protocol misunderstanding, the previous version's command response function was a send function, but the protocol actually uses a feedback message.
  - This update adds `GetRespInstruction`, a function for getting command response feedback, and `ClearRespSetInstruction`, a function for clearing stored command response messages. This function sets the timestamp variable in the command response feedback message to 0 and all other messages to -1.
  - Added the demo `piper_read_resp_instruction.py`.
  - The `SetInstructionResponse` function has been deprecated; calling it will generate a warning.

Miscellaneous
---------

- 📃 docs(INTERFACE_V2.MD): Add Get class function comments and new function descriptions

Version 0.4.3
=============

Features
--------
None

Bug Fixes
---------
None

Miscellaneous
---------

- 🌈 style(arm_gripper_ctrl, arm_feedback_gripper): Modifies the gripper angle in the msg class to gripper travel, and changes the unit to mm instead of degrees.
- 🌈 style(kinematics/piper_fk.py): Adds unit annotations to the parameters of the forward function.
  - Adds unit annotations to the parameters and return data in the C_PiperForwardKinematics.CalFk function.
- 🧪 test(demo/V2/piper_ctrl_reset.py): Removes the mode setting in the reset demo.
- 🧪 test(demo/V2): Adds a tool coordinate system TCP offset and motor zero point setting demo.
  - demo/V2/piper_read_tcp_pose.py calculates the end point of the official Piper gripper.
  - demo/V2/piper_set_joint_zero.py sets the zero point of the Piper arm.
- 🦄 Refactor (piper_msgs/msg_v2): Modify the msg init structure and class import method.
  - In piper_msgs/msg_v2/feedback, add an import path for all classes in the init module. Similarly, in piper_msgs/msg_v2/transmit.
  - Modify piper_msgs/msg_v2/init.py to import required classes from the feedback and transmit submodules.
  - Modify piper_msgs/msg_v2/arm_messages.py to import classes from the feedback and transmit submodules.
- 📃 docs(readme): Added switching slave ARM example code to the readme;增加Jetson相关问题解决到Q&A中 
- 📃 docs(Q&A): Added Jetson related problem solving to Q&A
- 📃 docs(interface): Optimizing function annotations

Version 0.4.2
=============

Features
--------
None

Bug Fixes
---------

- Fixed an issue where the program would fail due to an arm status bit potentially receiving unexpected data. We've added an enumeration attribute, UNKNOWN (0xFF). When unexpected data is received, the variable is assigned the value UNKNOWN (0xFF).
- Fixed a bug where GetCanFps would still retrieve values ​​when the CAN module was connected alone without the arm.
- Fixed an issue in `demo/V2/piper_ctrl_moveC.py` that prevented the first MoveC after returning to zero.

Miscellaneous
---------
None

Version 0.4.1
=============

Features
--------

- `Interface` adds `GetCanName` function to get the can port name currently read by `interface`

Bug Fixes
---------
None

Miscellaneous
---------

- Modify the note about `Message NOT sent` in README to the prompt of log printing; modify the instructions about updating piper_sdk.

Version 0.4.0
=============

Features
--------

- Delete V1 version code
- Added the 191 return to zero instruction, which requires the robot firmware version to be 1.7-4 or above, and is defined as follows:

  ```python
  def ReqMasterArmMoveToHome(self, mode:Literal[0, 1, 2])
  '''
  mode (int): Request return-to-zero mode.

              0: Restore master-slave arm mode.

              1: Master arm return-to-zero.

              2: Master and slave arms return-to-zero together.
  '''
  ```

- Add can encapsulation file `can_encapsulation.py` and the revised version `can_encapsulation_v0_4_0.py` corresponding to the sdk version, add enum inside the class as the status feedback after the can function is executed, and modify the `__init__.py` of `hardware_port` and the way to import `C_STD_CAN` in the interface for this purpose
- Add the import of  `ArmMsgFeedbackStatusEnum` class in `__init__.py`
- Add log management (`piper_sdk/utils/logger_mag.py`) and add a fixed log path to store log files (`piper_sdk/log`)
- Add the formal parameters `logger_level`, `log_to_file`, `log_file_path` related to log in the interface
- Add the demo of `piper_set_log_level.py`
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

Bug fix
---------
None

Miscellaneous
---------

- setup.py changed the author to Agilex
- Modified the function comments of the gripper, changed the angle to distance
- Modified the movec function comments, changed the typo "midpoint" to "end point"

Version 0.3.3
=============

Features
--------

- Modify the maximum torque of mit mode to 8 N.m

Bug Fixes
---------
None

Miscellaneous
---------
None

Version 0.3.2
=============

Features
--------
None

Bug Fixes
---------
None

Miscellaneous
---------

- Interface modified the import of hardware to import all in init instead of importing the specified class from the file;
- Interface added thread lock when creating an instance;
- Interface added error feedback when creating the C_STD_CAN class failed;
- Interface put the calculation of the fps count of the can bus at the beginning of the ReadCan thread loop;
- Interface optimized the judgment logic of executing the PiperInit function;
- SDK param modified demo to add the setting of formal parameters;
- Modified the import range of hardware to * instead of the specified C_STD_CAN;
- Optimized the init.py of msg v1 to be the same as v2;
- Added some comments

Version 0.3.0
=============

Features
--------

- Added interface parameters `start_sdk_joint_limit`, `start_sdk_gripper_limit`, the default parameter is `False`
- Added `utils` path, which contains tools for fps calculation and quaternion Euler angle calculation (external rotation sxyz)
  - Convert quaternion to Euler angle through `quat_convert_euler`
  - Convert Euler angle to quaternion through `euler_convert_quat`
- Added functions `EnableFkCal` and `DisableFkCal` to enable/disable sdk calculation fk. `isCalFk` is used to get whether to enable fk calculation, and then read it through `GetFK` function. After enabling fk calculation, the reading thread will occupy a high CPU, please enable it as needed
- Added function `get_connect_status` to get the call status of `ConnectPort` function
- Reduced the frequency (20hz) of `CanMonitor` thread enabled in the interface and the length of the queue for storing frame rate values ​​(5)
- Added the friction coefficient parameter of the teach pendant in the gripper/teach pendant parameter feedback command (feedback and send)
- Added `ModeCtrl` and `EmergencyStop` functions to set the mode and perform emergency stop (replace `MotionCtrl_1` and `MotionCtrl_2`)
- Will get CAN_ID=0x151 - Renamed the function of the arm mode control command from `GetArmCtrlCode151` to `GetArmModeCtrl`
- Added enum in the robot status feedback. When you use the `piper_read_status.py` in the demo to print the current status of the robot, you can see an explicit formatted string representing the current status of the robot (the actual variable value is still int)
- Renamed the demo file to be standardized
- Initialized `rx_message` to `Message()` type in the `C_STD_CAN` class
- Modified the location of obtaining the timestamp of the feedback information, from obtaining the current system time from the interface to obtaining the timestamp in the decoding function to increase the accuracy of the data timestamp
- Added the `piper_param_manager` file, which contains the angle and gripper range limits and applies constraints to feedback and control messages
  - Use the parameters in the interface to turn on the sdk limit function: `piper = C_PiperInterface_V2("can0", start_sdk_joint_limit=True, start_sdk_gripper_limit=True)`
  - If the feedback or control message exceeds the set limit, the value will be clamped within the boundary value
  - Default limits already exist in the program. To customize the configuration limit range, use the `SetSDKJointLimitParam` and `SetSDKGripperRangeParam` functions to set software constraints

  See the `piper_set_sdk_param.py` file in the demo for examples.
- Slightly reduced the joint limits to prevent exceeding the angle limit of the robot when converting radians to degrees using math.degrees. The new limits are as follows:

  | joint_name |     limit(rad)       |    limit(angle)    |     limit(rad/s)   |
  |------------|----------------------|--------------------|--------------------|
  | joint1     |   [-2.6179, 2.6179]  |    [-150.0, 150.0] |      [0, 3.0]      |
  | joint2     |   [0, 3.14]          |    [0, 180.0]      |      [0, 3.0]      |
  | joint3     |   [-2.967, 0]        |    [-170, 0]       |      [0, 3.0]      |
  | joint4     |   [-1.745, 1.745]    |    [-100.0, 100.0] |      [0, 3.0]      |
  | joint5     |   [-1.22, 1.22]      |    [-70.0, 70.0]   |      [0, 3.0]      |
  | joint6     |   [-2.09439, 2.09439]|    [-120.0, 120.0] |      [0, 3.0]      |

  Note: The conversion factor from radians to degrees is 57.2957795 (180/3.1415926).

- Added `piper_set_load.py` demo for setting load conditions (empty/half/full)
- Added `detect_arm.py` in the demo path to monitor various information of the robot arm in the terminal. Note that this file is not backward compatible

Bug Fixes
---------

- Fixed the issue where the gripper feedback timestamp was of type `int`.

Miscellaneous
---------

- Modified the folder structure, put `fps.py` into the `utils` path, the `monitor` path will be deleted after the next version
- Restructured the documentation:
  - Most of the documentation has been rewritten in English
  - Simplified the documentation to focus only on interface usage

Version 0.2.19
=============

Features
--------

None

Bug Fixes
---------

- Fixed abnormal current feedback values.(High speed piper msg)
  piper_sdk/piper_msgs/msg_v1/feedback/arm_high_spd_feedback.py
  piper_sdk/piper_msgs/msg_v2/feedback/arm_high_spd_feedback.py
  piper_sdk/protocol/protocol_v1/piper_protocol_v1.py
  piper_sdk/protocol/protocol_v2/piper_protocol_v2.py

Miscellaneous
---------

None

Version 0.2.18
=============

Features
--------

- Added `effort` feedback to high-speed information feedback, with a unit of 0.001 N/m.
- Removed elements in the `sh` script to ensure compatibility with `zsh`.
- Added `interface_v1` without affecting previous versions, reserving it for future updates.
- Added class references in `__init__.py`.
- Fixed incorrect comments in `msg_v1/__init__.py`, `msg_v2/__init__.py`, `protocol/protocol_v2/piper_protocol_v2.py`, and `arm_low_spd_feedback.py`.
- Corrected the unit description of `max_joint_acc` in the `ArmMsgFeedbackCurrentMotorMaxAccLimit` class to `0.001 rad/s^2`.
- Added firmware version descriptions in the interface documentation.

Bug Fixes
---------

- Modified `pyproject.toml` to allow proper installation using `setup.py` (the previous version was missing the `version` field in the `project` tag, causing `pip install .` to fail).
- Fixed the issue where `msg_type` in `msg_v2` was not assigned using `auto`.
- Fixed missing class references in `piper_sdk/__init__.py`, which caused errors.
- Fixed an error in `protocol` where the position information of motor 2 was incorrectly assigned to motor 3.
- Fixed an issue in `interface` where the timestamp for high-speed feedback data was mistakenly using the timestamp from low-speed feedback data.

Miscellaneous
---------

None

Version 0.2.17
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
- Modified the `arm_high_spd_feedback` to set the `motor_speed` unit to 0.001 rad/s and the `current` unit to 0.001 A.
- Modified the shell script. Since the `sh` command does not support `==` for equality comparison, but `bash` does, it is changed to use `=` for equality comparison so that it can be used by `zsh`

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

V1 based on version V1.5-1 and before

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

V2 based on version V1.5-2 and later

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

- Modified the CAN bus class to make its data reading part compatible with Python 3.6 in Ubuntu 18.04
- Updated protocol_base to simplify the function of converting values ​​to lists using struct and ctypes
- Added singleton mode support in the interface class
- Added thread protection to the `ConnectPort` function in the interface class
- Added a `DisconnectPort` function to the interface class to stop the data reading process
- Changed the `Update` function and some variables in the interface class to private variables
- Fixed incorrect comments to make it more readable
- Optimized the document structure and description
- Added the interface `SearchPiperFirmwareVersion` for querying the robot firmware, and the acquisition function is `GetPiperFirmwareVersion`
- Added many demos (such as moveC)

Bug Fixes
---------

- Corrected the spelling of "jonit" to "joint".
- Fixed the unit for setting maximum motor acceleration to 0.01 rad/s^2; added a new function `JointMaxAccConfig` to set the motor's maximum acceleration.

Miscellaneous
---------

None
