# PIPER SDK Interface User Manual

[中文](INTERFACE_V1.MD)

This SDK is used to receive CAN data frames and process them into a custom data type.

PS: Some parts are written in shorthand. The code contains detailed Chinese comments, and this document is only meant to clarify the structure.

## interface Analysis

`C_PiperInterface` : Explanation of Class Initialization Parameters and Member Variables

The inner class identifies instances based on can_port
to prevent duplicate creation of interface instances with the same can_port

|Variable|Type|Description|
| --- |------| --- |
| can_name      | `str`  | CAN route name, indicating from which CAN to send and receive data. |
| judge_flag   | `Bool` | Whether to check the CAN module status when creating an instance. |
| can_auto_init | `Bool` | Whether to initialize the CAN bus when creating an instance. |

### 1. Secondary encapsulation class

| Class |Description                                                         |
| --- |------------------------------------------------------------ |
|`ArmStatus`|Robotic arm state secondary encapsulation class, with added timestamp.|
|`ArmEndPose`| Robotic arm end-effector pose secondary encapsulation class, with added timestamp. |
|`ArmJoint`|Robotic arm joint angle feedback secondary encapsulation class, with added timestamp.|
|`ArmGripper`|Robotic arm gripper feedback secondary encapsulation class, with added timestamp.|
|`ArmMotorDriverInfoHighSpd`|Robotic arm motor driver high-speed feedback information class, with added timestamp.|
|`ArmMotorDriverInfoLowSpd`|Robotic arm motor driver low-speed feedback information class, with added timestamp.|
|`ArmMotorAngleLimitAndMaxVel`|Current motor limit angle/maximum speed feedback information class, with added timestamp.|
|`CurrentEndVelAndAccParam`|Current end-effector velocity/acceleration parameter feedback information class, with added timestamp.|
|`CrashProtectionLevelFeedback`|Collision protection level setting feedback command information class, with added timestamp.|
|`CurrentMotorMaxAccLimit`|Current motor maximum acceleration limit feedback information class, with added timestamp.|
|`ArmJointCtrl`|Robotic arm joint angle control message class, with added timestamp.|
|`ArmGripperCtrl`|Robotic arm gripper control message class, with added timestamp.|
|`ArmCtrlCode_151`|Robotic arm control command 0x151 message reception class, sent by the master arm, with added timestamp.|
|`AllCurrentMotorMaxAccLimit`|The maximum acceleration limit of all joint motors of the robot joints.|
|`AllCurrentMotorAngleLimitMaxSpd`|Angle limit and maximum speed of all joint motors of the robot arm joint|
|`ArmTimeStamp`|Robotic arm timestamp class, containing timestamps for various feedbacks.|

For a detailed explanation, please refer to the comments in the code.

Each robot-related class has a timestamp. If the data can only be obtained by multiple CAN frames, such as the six joint angles of the robot, the timestamps of these CAN frames will be obtained, and the largest one will be selected as the timestamp of the class.

### 2. In-class variable analysis

| Variable | Type |Description                                                          |
| ----- | ---- |------------------------------------------------------------ |
|`__arm_can`|`C_STD_CAN`|The instantiation of classes in `can_encapsulation.py` serves as the hardware data reception layer, registering data processing callback functions.|
|`__piper_fk`|`C_PiperForwardKinematics`| Forward kinematics class for the robotic arm |
|`__parser`|`C_PiperParserBase`|Instantiation of the data protocol parsing class, currently using the V1 version protocol parsing. It serves as the base class for data parsing.|
|`__firmware_data`|`bytearray`|Firmware version string|
| `__fps_counter` | `C_FPSCounter` | CAN frame rate calculation |
| `__is_ok`       | `Bool`         | Whether there is still data on the CAN bus |
|`__arm_time_stamp`|`ArmTimeStamp`|The instantiation of the timestamp class is a private class of `C_PiperInterface_V2`. It handles timestamps for robotic arm variables that are composed of multiple CAN frames, such as joint angles.|
| `__link_feedback_fk` | `list[float]` | The forward kinematics position of all joint feedback information of the robotic arm |
| `__link_ctrl_fk`     | `list[float]` | The forward kinematics position of all joint control information of the robotic arm |
|`__arm_status`|`ArmStatus`|Instance of the robotic arm status message, containing the status information of the robotic arm.|
|`__arm_end_pose`|`ArmEndPose`|Instance of the robotic arm end-effector pose feedback message, containing the end-effector's pose information.|
|`__arm_joint_msgs`|`ArmJoint`|Instance of the robotic arm joint angle feedback message, containing status information for each joint.|
|`__arm_gripper_msgs`|`ArmGripper`|Instance of the robotic arm gripper feedback message, containing status information for each gripper.|
|`__arm_motor_info_high_spd`|`ArmMotorDriverInfoHighSpd`|Variable for high-speed feedback class of the robotic arm motor messages.|
|`__arm_motor_info_low_spd`|`ArmMotorDriverInfoLowSpd`|Variable for low-speed feedback class of the robotic arm motor messages.|
|`__feedback_current_motor_angle_limit_max_vel`|`ArmMotorAngleLimitAndMaxVel`|The variable is the feedback message after actively sending the CAN frame, used to read the current motor limit angles/maximum speed.|
|`__feedback_current_end_vel_acc_param`|`CurrentEndVelAndAccParam`|This variable is the feedback message after actively sending the CAN frame, used to read the current end velocity/acceleration parameters.|
|`__feedback_crash_protection_level`|`CrashProtectionLevelFeedback`|This variable is the feedback message after actively sending the CAN frame, used to read the collision protection level setting feedback command.|
|`__feedback_current_motor_max_acc_limit`|`CurrentMotorMaxAccLimit`|This variable is the feedback message after actively sending the CAN frame, used to read the current maximum acceleration limit of the motor.|
|`__arm_joint_ctrl_msgs`|`ArmJointCtrl`|The variable is used to read the joint angle messages sent from the master arm to the follower arm.|
|`__arm_gripper_ctrl_msgs`|`ArmGripperCtrl`|The variable is used to read the gripper messages sent from the master arm to the follower arm.|
|`__arm_ctrl_code_151`|`ArmCtrlCode_151`|The variable is used to read the 0x151 command messages sent from the master arm to the follower arm.|
|`__arm_all_motor_max_acc_limit`|`AllCurrentMotorMaxAccLimit`|The variable is the maximum acceleration limit message of all joint motors of the robot joint|
|`__arm_all_motor_angle_limit_max_spd`|`AllCurrentMotorAngleLimitMaxSpd`|Angle limit and maximum speed of all joint motors of the robot arm joint|
| `_initialized` | `Bool` | Flag to prevent duplicate instances within the class |

### 3. Function Analysis

| Function | Type |Description                                                         |Usage                | Parameter             |Return       |
| ----- | ---- |------------------------------------------------------------ |-------------------|--------------------------- |--------|
| `get_instance` | Getter Method | Get the current instance address | `obj.GetArmStatus()` | `can_name (str)`, `judge_flag (Bool)`, `can_auto_init (Bool)` | self@C_PiperInterface |
|`ConnectPort`|Start Method|This function is used to open the CAN message reading function. It calls the function to read CAN messages, creates a reading thread, and starts the thread.|Used to open the data processing thread after externally instantiating the class.|`can_init (Bool)`|None|
| `DisconnectPort` | Close Method | This function stops the CAN reading thread and closes CAN bus reading | After external instantiation of the class, stop reading | `can_init (Bool)` | None |
|`ParseCANFrame`|Getter Method| CAN protocol parsing function, used to process received CAN data frames, serves as the callback function for CAN message reception. |First, create a local variable, then call the decoding function in the protocol class. If decoding is successful, update the corresponding message in the private variable; each update function filters the current data type, and only the corresponding data type will be updated.|`rx_message: Optional[can.Message]`|None|
|`GetCanFps` | Getter Method | Get the current real-time frame rate of the CAN bus | `obj.GetArmStatus()` | None | int |
|`GetArmStatus`|Getter Method| Retrieve robotic arm status information. Use the mutex `__arm_status_mtx` to ensure thread safety. |obj.GetArmStatus()|None|self.__arm_status|
|`GetArmEndPoseMsgs`|Getter Method|Get messages regarding the end pose of the robotic arm. Use the mutex `__arm_end_pose_mtx` to ensure thread safety.|obj.GetArmEndPoseMsgs()|None|self.__arm_end_pose|
|`GetArmJointMsgs`|Getter Method|Get the status messages of the robotic arm joints. Use the mutex `__arm_joint_msgs_mtx` to ensure thread safety.|obj.GetArmJointMsgs()|None|self.__arm_joint_msgs|
| `GetFK` | Getter Method | Retrieves the forward kinematics solution for both control and feedback information of each joint of the robotic arm. XYZ units are in mm, and RXRYRZ units are in degrees. Returns a list of 6 float-type data representing the pose of joints 1-6 relative to the base_link. | `obj.GetFK()` | `mode: Literal["feedback", "control"] = "feedback"` | `self.__link_fk` |
|`GetArmGripperMsgs`|Getter Method|Get the status messages of the robotic arm gripper. Use the mutex `__arm_gripper_msgs_mtx` to ensure thread safety.|obj.GetArmGripperMsgs()|None|self.__arm_gripper_msgs|
|`GetArmHighSpdInfoMsgs`|Getter Method|Get messages regarding high-speed motion information of the robotic arm. Use the mutex `__arm_motor_info_high_spd_mtx` to ensure thread safety.|obj.GetArmHighSpdInfoMsgs()|None|self.__arm_motor_info_high_spd|
|`GetArmLowSpdInfoMsgs`|Getter Method|Get messages regarding low-speed motion information of the robotic arm. Use the mutex `__arm_motor_info_low_spd_mtx` to ensure thread safety.|obj.GetArmLowSpdInfoMsgs()|None|self.__arm_motor_info_low_spd|
|`GetCurrentMotorAngleLimitMaxVel`|Getter Method|Get the maximum angle limit value for the specified motor number. Use the mutex `__feedback_current_motor_angle_limit_max_vel_mtx` to ensure thread safety.|obj.GetCurrentMotorAngleLimitMaxVel()|None|self.__feedback_current_motor_angle_limit_max_vel|
|`GetCurrentEndVelAndAccParam`|Getter Method|Get feedback on the current end velocity and acceleration parameters of the robotic arm. Use the mutex `__feedback_current_end_vel_acc_param_mtx` to ensure thread safety.|obj.GetCurrentEndVelAndAccParam()|None|self.__feedback_current_end_vel_acc_param|
|`GetCrashProtectionLevelFeedback`|Getter Method|Get feedback information on the collision protection level. Use the mutex `__feedback_crash_protection_level_mtx` to ensure thread safety.|obj.GetCrashProtectionLevelFeedback()|None|self.__feedback_crash_protection_level|
|`GetCurrentMotorMaxAccLimit`|Getter Method|Get feedback on the current maximum acceleration limit of the motor. Use the mutex `__feedback_current_motor_max_acc_limit_mtx` to ensure thread safety.|obj.GetCurrentMotorMaxAccLimit()|None|self.__feedback_current_motor_max_acc_limit|
|`GetArmJointCtrl`|Getter Method|Get the joint angle control messages sent from the mater arm to the follower arm. Use the mutex `__arm_joint_ctrl_msgs_mtx` to ensure thread safety.|obj.GetArmJointCtrl()|None|self.__arm_joint_ctrl_msgs|
|`GetArmGripperCtrl`|Getter Method|Get the gripper control messages sent from the master arm to the follower arm. Use the mutex `__arm_gripper_ctrl_msgs_mtx` to ensure thread safety.|obj.GetArmJointCtrl()|None|self.__arm_gripper_ctrl_msgs|
|`GetArmCtrlCode151`|Getter Method|Get the status of control code 151 sent by the active arm. Use the mutex `__arm_ctrl_code_151_mtx` to ensure thread safety.|obj.GetArmCtrlCode151()|None|self.__arm_ctrl_code_151|
|`GetAllMotorMaxAccLimit`|Getter Method|Retrieve the maximum acceleration limit message for all joint motors of the robotic arm. Uses the mutex lock `__arm_all_motor_max_acc_limit_mtx` to ensure thread safety.|obj.GetAllMotorMaxAccLimit()|None|self.__arm_all_motor_max_acc_limit|
|`GetAllMotorAngleLimitMaxSpd`|Getter Method|Retrieve the angle limits and maximum speed for all joint motors of the robotic arm. Uses the mutex lock __arm_all_motor_angle_limit_max_spd_mtx to ensure thread safety.|obj.GetAllMotorAngleLimitMaxSpd()|None|self.__arm_all_motor_angle_limit_max_spd|
| `GetPiperFirmwareVersion` | Getter Method | Retrieves the firmware version of the Piper robotic arm's main controller, returning the firmware version as a string. | `obj.GetPiperFirmwareVersion()` | None | `firmware_version` |  
| `isOk` | Getter Method | Checks whether the CAN data reading thread is functioning properly. | `obj.isOk()` | None | `self.__is_ok` |  
| `__CanMonitor` | Getter Method | Monitors the CAN data frame rate. | Internal use only | None | None |  
|`UpdateArmStatus`|Getter Method|Update the robotic arm status.| Used within the class                                        | sg:PiperMessage                                              |self.__arm_status|
|`__UpdateArmEndPoseState`|Getter Method|Update the end pose state, unit is 0.001 mm.| Used within the class                                        |msg:PiperMessage|self.__arm_end_pose|
|`__UpdateArmJointState`|Getter Method|Update the joint state, joint angle unit is 0.001 degrees.|Used within the class|msg:PiperMessage|self.__arm_joint_msgs|
|`__UpdateArmGripperState`|Getter Method|Update the gripper state, gripper feedback stroke unit is 0.001 mm.|Used within the class|msg:PiperMessage|self.__arm_gripper_msgs|
|`__UpdateDriverInfoHighSpdFeedback`|Getter Method|Update high-speed driver information feedback.|Used within the class|msg:PiperMessage|self.__arm_motor_info_high_spd|
|`__UpdateDriverInfoLowSpdFeedback`|Getter Method|Update low-speed driver information feedback.|Used within the class|msg:PiperMessage|self.__arm_motor_info_low_spd|
|`__UpdateCurrentMotorAngleLimitMaxVel`|Getter Method|Feedback on the current motor angle limit/maximum speed.|Used within the class|msg:PiperMessage|self.__feedback_current_motor_angle_limit_max_vel|
|`__UpdateCurrentMotorMaxAccLimit`|Getter Method|Feedback on the current maximum acceleration limit of the motor.|Used within the class|msg:PiperMessage|self.__feedback_current_motor_max_acc_limit|
| `__UpdateAllCurrentMotorAngleLimitMaxVel` | Getter Method | Updates the maximum acceleration limit for all motors. | Internal use only | `msg: PiperMessage` | `self.__arm_all_motor_angle_limit_max_spd` |  
| `__UpdateAllCurrentMotorMaxAccLimit` | Getter Method | Updates the angle limits and maximum speed for all motors. | Internal use only | `msg: PiperMessage` | `self.__arm_all_motor_max_acc_limit` |  
|`__UpdateCurrentEndVelAndAccParam`|Getter Method|Feedback on the current end velocity/acceleration parameters.|Used within the class|msg:PiperMessage|self.__feedback_current_end_vel_acc_param|
|`__UpdateCrashProtectionLevelFeedback`|Getter Method|Feedback command for collision protection level settings.|Used within the class|msg:PiperMessage|self.__feedback_crash_protection_level|
|`__UpdateArmJointCtrl`|Getter Method|Update joint status (messages sent from the master arm).|Used within the class|msg:PiperMessage|self.__arm_joint_ctrl_msgs|
|`__UpdateArmGripperCtrl`|Getter Method|Update gripper status (messages sent from the master arm).|Used within the class|msg:PiperMessage|self.__arm_gripper_ctrl_msgs|
|`__UpdateArmCtrlCode151`|Getter Method|Update the control command 151 sent by the active arm.|Used within the class|msg:PiperMessage|self.__arm_ctrl_code_151|
|`__UpdatePiperFirmware`|Getter Method|Update by appending the characters received from the 4AF feedback after sending 4AF|Used within the class|msg:PiperMessage|self.__firmware_data|
| `__UpdatePiperFeedbackFK` | Getter Method | Updates the forward kinematics data for piper feedback information. | For internal class use only. | None | None |
| `__UpdatePiperCtrlFK`     | Getter Method | Updates the forward kinematics data for piper control information. | For internal class use only. | None | None |
|`MotionCtrl_1`|Ctrl Method| 0x150, can control emergency stop, trajectory transmission, and teach mode. |Called from outside the class|`emergency_stop (uint8)`, `track_ctrl (uint8)`, `grag_teach_ctrl (uint8)``emergency_stop (uint8)`,`track_ctrl (uint8)`, `grag_teach_ctrl (uint8)`|NoneNone|
|`MotionCtrl_2`|Ctrl MethodCtrl Method|0x151, can set control mode, MOVE mode, and motion speed. Each time before controlling the robotic arm's motion, this must be sent, otherwise the arm may not move.|Called from outside the class|`ctrl_mode (uint8)`, `move_mode (uint8)`, `move_spd_rate_ctrl (uint8)``ctrl_mode (uint8)`,`move_mode (uint8)`, `move_spd_rate_ctrl (uint8)`|NoneNone|
|`EndPoseCtrl`|Ctrl MethodCtrl Method|0x152, 0x153, 0x154, control the end position and posture of the robotic arm. This function consolidates the three functions below; note that the x, y, z values sent by this function are in units of 0.001 mm, and the rx, ry, rz values are in units of 0.001 degrees. For example, if the robotic arm needs to move 0.3 m in the x-axis direction, the data sent should be 0.3 \* 100 \* 1000 = 30000.|Called from outside the class|`X (int)`, `Y (int)`, `Z (int)`, `RX (int)`, `RY (int)`, `RZ (int)`,`X (int)`, `Y (int)`, `Z (int)`, `RX (int)`, `RY (int)`, `RZ (int)`|None|
|`__CartesianCtrl_XY`|Ctrl MethodCtrl Method|Control the XY axis motion of the robotic arm in Cartesian coordinates.|Called within the class (private)|`X (int)`, `Y (int)`|None|
|`__CartesianCtrl_ZRX`|Ctrl Method|Control the Z-axis and RX-axis movement of the robotic arm in Cartesian coordinates.|Called within the class (private)|`Z (int)`, `RX (int)`|None|
|`__CartesianCtrl_RYRZ`|Ctrl Method|Control the RY-axis and RZ-axis movement of the robotic arm in Cartesian coordinates.|Called within the class (private)|`RY (int)`, `RZ (int)`|None|
|`JointCtrl`|Ctrl Method|0x155, 0x156, 0x157, control the movement of the six joints of the robotic arm. Note that the values sent by this function are in units of 0.001 degrees. For example, to move joint 1 by 90 degrees (1.57 radians), the data sent should be 90 \* 1000. If using radians, it should be 1.57 \* 1000 \* (180/3.14).|Called from outside the class|`joint_1 (int)`, `joint_2 (int)`, `joint_3 (int)`, `joint_4 (int)`, `joint_5 (int)`, `joint_6 (int)`|None|
|`__JointCtrl_12`|Ctrl Method|Control the movement of joints 1 and 2 of the robotic arm.|Called within the class (private)|`joint_1 (int)`, `joint_2 (int)`|None|
|`__JointCtrl_34`|Ctrl Method|Control the movement of joints 3 and 4 of the robotic arm.|Called within the class (private)|`joint_3 (int)`, `joint_4 (int)`|None|
|`__JointCtrl_56`|Ctrl Method|Control the movement of joints 5 and 6 of the robotic arm.|Called within the class (private)|`joint_5 (int)`, `joint_6 (int)`|None|
| `MoveCAxisUpdateCtrl` | Ctrl Method | Controls the robotic arm in arc mode. It must be used in conjunction with `EndPoseCtrl`. `EndPoseCtrl` sets the target pose, while `MoveCAxisUpdateCtrl` executes the previously set target pose and updates the motion trajectory according to the given parameters. | External call | `instruction_num: int` | None |  
|`GripperCtrl`|Ctrl Method| 0x159 control the movement of the robotic arm's gripper. The gripper is adapted to the AGX end effector, and the gripper module is independently enabled. Note that the values sent by this function are in units of 0.001 mm. For example, to move the gripper by 50 mm, the data sent should be 50 * 1000 = 50000. |Called from outside the class|`gripper_angle (int)`, `gripper_effort (int)`, `gripper_code (int)`, `set_zero (int)`|None|
|`MasterSlaveConfig`|Ctrl Method|0x470, configure the master-slave mode of the robotic arm.|Called from outside the class|`linkage_config (int)`, `feedback_offset (int)`, `ctrl_offset (int)`, `linkage_offset (int)`|None|
|`DisableArm`|Ctrl Method|0x471, disable the motor. At this point, the specified motor loses power. If the robotic arm is in a non-zero position (e.g., joints 2 and 3 are raised), the arm will drop due to loss of power.|Called from outside the class|`motor_num (int)`, `enable_flag (int)`|None|
|`EnableArm`|Ctrl Method|0x471, enable the robotic arm's motor. At this point, the specified motor is powered on, and trying to move the joints by hand will not be possible.|Called from outside the class|`motor_num (int)`, `enable_flag (int)`|None|
|`SearchMotorMaxAngleSpdAccLimit`|Ctrl Method|0x472, query the angle, maximum speed, and maximum acceleration limits of the motor. This is a command for actively sending and then receiving a specified message. It can be modified by changing `search_content` to query specific content, with feedback for a single motor.|Called from outside the class|`motor_num (int)`, `search_content (int)`|None|
| `SearchAllMotorMaxAngleSpd` | Ctrl Method | Queries the maximum angle, minimum angle, and maximum speed of all motors. | External call | None | None |  
| `SearchAllMotorMaxAccLimit` | Ctrl Method | Queries the maximum acceleration limit of all motors. | External call | None | None |  
|`MotorAngleLimitMaxSpdSet`|Ctrl Method|Set the angle limit and maximum speed for the motor.|Called from outside the class|`motor_num (int)`, `max_angle_limit (int)`, `min_angle_limit (int)`, `max_joint_spd (int)`|None|
|`JointConfig`|Ctrl Method|Configure joint parameters.|Called from outside the class|`joint_num (int)`, `set_zero (int)`, `acc_param_is_effective (int)`, `max_joint_acc (int)`, `clear_err (int)`|None|
|`JointMaxAccConfig`|Ctrl Method|Set Joint Maximum Acceleration Command|Called from outside the class|`motor_num (int)`, `max_joint_acc (int)`|None|
|`SetInstructionResponse`|Ctrl Method|Set the instruction response.|Called from outside the class|`instruction_index (int)`, `zero_config_success_flag (int)`|None|
|`ArmParamEnquiryAndConfig`|Ctrl Method|Query and set robotic arm parameters.|Called from outside the class|`param_enquiry (int)`, `param_setting (int)`, `data_feedback_0x48x (int)`, `end_load_param_setting_effective (int)`, `set_end_load (int)`|None|
|`EndSpdAndAccParamSet`|Ctrl Method|Set the end speed and acceleration parameters of the robotic arm.|Called from outside the class|`end_max_linear_vel (int)`, `end_max_angular_vel (int)`, `end_max_linear_acc (int)`, `end_max_angular_acc (int)`|None|
|`CrashProtectionConfig`|Ctrl Method|Configure the collision protection level of the robotic arm.|Called from outside the class|`joint_1_protection_level (int)`, `joint_2_protection_level (int)`, `joint_3_protection_level (int)`, `joint_4_protection_level (int)`, `joint_5_protection_level (int)`, `joint_6_protection_level (int)`|None|
|`SearchPiperFirmwareVersion`|Ctrl Method|Query the main controller firmware version of the Piper robotic arm|Called outside the class|None|None|

**Note:**

All Update functions are used to read CAN data frames and update the parsed data into private variables. Since the variables are updated to private variables after acquiring and processing the messages, the values of these private variables need to be accessed using the class's Get functions.

Please note that all retrieved values are raw values.

The unit for the end-effector pose feedback of the robotic arm is 0.001 mm.

The unit for joint angle variables is 0.001 degrees.

The unit for the feedback travel of the gripper is 0.001 mm.

The unit for the feedback torque of the gripper is 0.001 N/m.

Therefore, unit conversion needs to be handled manually. For example, to obtain the current angle of the gripper, you need to divide the retrieved joint angle by 1000 to get the actual angle.
