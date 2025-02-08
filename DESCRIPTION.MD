# Piper SDK 0.1.13

[![GitHub](https://img.shields.io/badge/GitHub-blue.svg)](https://github.com/agilexrobotics/piper_sdk)

|Ubuntu |STATE|
|---|---|
|![ubuntu18.04](https://img.shields.io/badge/Ubuntu-18.04-orange.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|
|![ubuntu20.04](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|
|![ubuntu22.04](https://img.shields.io/badge/Ubuntu-22.04-orange.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

Test:

|PYTHON |STATE|
|---|---|
|![python3.6](https://img.shields.io/badge/Python-3.6-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|
|![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|
|![python3.10](https://img.shields.io/badge/Python-3.10-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

## 1 Installation Instructions

### 1.1 Install dependencies

The python-can version should be higher than 3.3.4.

```shell
pip3 install python-can
```

```shell
pip3 install piper_sdk
```

View piper_sdk Details, Such as Installation Path, Version, etc.

```shell
pip3 show piper_sdk
```

0.0.x provides SDK support for robotic arm firmware versions prior to V1.5-2.

To uninstall

```shell
pip3 uninstall piper_sdk
```

## 2 ChangeLog

### 2.2 ChangeLog-V1

The V1 version code here is the code under version 0.1.x.

The code in version 0.1.x differs significantly from the code in version 0.0.x. The V1 version in the former is an update and iteration based on the latter.

The following sections mainly explain the differences between the 0.1.x-V1 version code and the 0.0.x version code.

#### 2.2.1 Firmware Compatibility

- **Compatible with new firmware (before version V1.5-2), the protocol content is not detailed here.**

#### 2.2.2 Interface

- **`C_PiperInterface`**

##### 1) Features

- Added conditional instantiation for the class. The condition is the `can_name` passed to the interface. For example, in a loop, repeatedly calling `piper = C_PiperInterface(can_name="can0")` will only create one instance. Subsequent instantiations will recognize that an instance with `can_name="can0"` has already been created and will not create a new one.
- The class now includes frame rate calculation. You can use the `isOk` function to check if CAN data transmission is normal. A True feedback indicates normal data transmission, while False indicates that the data has been disconnected.
- Added forward kinematics (FK) calculation. The pose of each joint relative to the base_link is calculated by extending the DH parameters. This can be obtained through the `GetFK` function, which returns the pose of link1 to link6 in a 6*6 list. The last element represents the pose of link6.

##### 2) Functions

Compared to version 0.0.x, version 0.1.x-V1 adds several functions as follows:

| Functio  | Type           | Description                                                 | Usage    | Parameters            | Feedback   |
| -------- | -------------- | ----------------------------------------------------------- | -------- | --------------------- | --------- |
| `GetCanFps`|Getter Method| Get the current real-time frame rate of the CAN bus. | obj.GetArmStatus()     | None | int |
| `GetFK`|Getter Method| Get the forward kinematics of each joint of the robot arm. XYZ is in mm, RXRYRZ is in degrees. It returns a list of 6 floats, representing the pose of joints 1-6 relative to base_link. | obj.GetFK() | None | self.__link_fk |
| `isOk`| Getter Method  | Check if the CAN data reading thread is functioning normally.   | obj.isOk() | None | self.__is_ok |
| `__CanMonitor`| Getter Method  | Monitor the CAN data frame rate. | Used internally in class | None | None |
| `__UpdatePiperFK`| Getter Method | Updates the Piper forward kinematics data. | Used internally in class | None | None |

### 2.3 ChangeLog-V2

The V1 and V2 version codes here are both under version 0.1.x.

In version 0.1.x, the difference between V2 and V1 is the protocol.

The code in version 0.1.x differs significantly from the code in version 0.0.x.

The following sections mainly explain the differences between V2 and V1.

#### 2.3.1 Firmware Compatibility

- **Compatible with new firmware (after version V1.5-2), while maintaining compatibility with the previous version firmware.**

##### 1) 0x2A1 Robot Arm Status Feedback

Additional information:

Byte 2 mode feedback now includes 0x04 MOVE M feedback, which corresponds to the MIT mode feedback.

##### 2) 0x151 Mode Control Protocol

Additional information:

Byte 1 MOVE mode now includes the 0x04 MOVE M instruction, which sets the MIT mode.

Added:

Byte 5 installation position settings:

- 0x00 Invalid value
- 0x01 Horizontal mounting (standard position)
- 0x02 Left side mounting
- 0x03 Right side mounting

Note: Ensure wiring faces backward.

##### 3) New MIT Control Commands

| Robot Arm Joint 1-6 MIT Control Command |                                       | ID  0x15A ~ 0x15F |      len 8      |
|----------------------------------------|---------------------------------------|------------------|-----------------|
|        Data                             |                  Function              |        Type      |                 |
|       Byte 0                            |  Pos_ref [bit15~bit8] High 8 bits      |       uint8      |                 |
|       Byte 1                            |  Pos_ref [bit7~bit0] Low 8 bits        |       uint8      |                 |
|       Byte 2                            |  Vel_ref [bit11~bit4] Low 12 bits      |       uint8      |                 |
|       Byte 3                            |  Vel_ref \[bit3 \~ bit0\] Kp \[bit11 \~ bit8\]  |       uint8      |                 |
|       Byte 4                            |  Kp [bit7~bit0]                       |       uint8      | Kp reference value: 10  |
|       Byte 5                            |  Kd [bit11~bit4] Low 12 bits          |       uint8      | Kd reference value: 0.8 |
|       Byte 6                            |  Kd \[bit3 \~ bit0\] T_ref \[bit7 \~ bit4\]      |       uint8      |                 |
|       Byte 7                            |  T_ref \[bit3 \~ bit0\] CRC \[bit3 \~ bit0\]     |       uint8      |                 |

##### 4) ID 0x474 Motor Angle Limit / Maximum Speed Setting Command

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

##### 5) ID 0x475 Joint Setting Command

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

##### 6) ID 0x477 Robot Arm Parameter Query and Setting Command

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

##### 7) ID 0x479 End-effector Speed/Acceleration Parameter Setting Command

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

##### 8) New ID 0x47D Gripper/Teach Pendant Parameter Setting Command

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

##### 9) New ID 0x47E Gripper/Teach Pendant Parameter Feedback Command

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

#### 2.3.2 interface

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

## Notes

- The CAN device must be activated and the correct baud rate set before reading messages from or controlling the robotic arm.
- The `C_PiperInterface` interface class can accept the activated CAN route name as a parameter when instantiated.
- Sometimes when sending CAN messages, the terminal may show `Message NOT sent`. This indicates that the CAN module is not properly connected to the device. First, check the connection between the module and the robotic arm, then power cycle the robotic arm (turn it off and on) before attempting to send the message again.
- The SDK interface will check if the built-in CAN module is activated after creating an instance. If using another CAN device, you can set the second parameter to `False`, for example: `piper = C_PiperInterface_V2("can0", False)`.
- **The MIT protocol for controlling individual joints of the robotic arm is an advanced feature. Be cautious when using it, as improper use of this protocol may damage the robotic arm!!!**

## Contact Us

You can open an issue on GitHub.

Alternatively, you can join our Discord at <https://discord.gg/wrKYTxwDBd>
