# PIPER SDK Interface 使用文档

[EN](INTERFACE_V1(EN).MD)

本SDK用于接收can数据帧，然后处理为自定义数据类型

ps：有些地方略写，代码中有详细的中文注释，本文这里只是理清结构

## interface解析

`C_PiperInterface` 类初始化参数及成员变量说明

内类依照can_port识别实例，防止重复创建同can_port的interface实例

|形参|类型|说明|
| --- |------| --- |
|can_name|`str`|CAN 路由名称，指示从哪个 CAN 中收发数据。|
|judge_flag|`Bool`|是否在创建实例时判断can模块状态|
|can_auto_init|`Bool`|是否在创建实例时初始化can bus|

### 1.二次封装类

| 类  |说明                                                         |
| --- |------------------------------------------------------------ |
|`ArmStatus`|机械臂状态二次封装类，增加时间戳。|
|`ArmEndPose`|机械臂末端姿态二次封装类，增加时间戳。|
|`ArmJoint`|机械臂关节角度反馈二次封装类,增加时间戳。|
|`ArmGripper`|机械臂夹爪反馈二次封装类,增加时间戳。|
|`ArmMotorDriverInfoHighSpd`|机械臂电机驱动高速反馈信息类，增加时间戳。|
|`ArmMotorDriverInfoLowSpd`|机械臂电机驱动低速反馈信息类，增加时间戳。|
|`ArmMotorAngleLimitAndMaxVel`|当前电机限制角度/最大速度反馈信息类，增加时间戳。|
|`CurrentEndVelAndAccParam`|当前末端速度/加速度参数反馈信息类，增加时间戳。|
|`CrashProtectionLevelFeedback`|碰撞防护等级设置反馈指令信息类，增加时间戳。|
|`CurrentMotorMaxAccLimit`|当前电机最大加速度限制反馈信息类，增加时间戳。|
|`ArmJointCtrl`|机械臂关节角度控制消息类，增加时间戳。|
|`ArmGripperCtrl`|机械臂夹爪控制消息类，增加时间戳。|
|`ArmCtrlCode_151`|机械臂发送控制指令0x151的消息接收类，由主臂发送，增加时间戳。|
|`AllCurrentMotorMaxAccLimit`|机械臂关节所有关节电机的最大加速度限制。|
|`AllCurrentMotorAngleLimitMaxSpd`|机械臂关节所有关节电机的角度限制和最大速度|
|`ArmTimeStamp`|机械臂的时间戳类，包含各种反馈的时间戳。|

具体解释可以查看代码内注释

每个机械臂相关的类都有时间戳，如果是多条can帧才能获得的数据例如机械臂六个关节角，则会获取这些can帧的时间戳，并选取最大的一个作为该类的时间戳

### 2.类内变量解析

| 变量   | 类型 |说明                                                          |
| ----- | ---- |------------------------------------------------------------ |
|`__arm_can`|`C_STD_CAN`|`can_encapsulation.py` 中的类的实例化，为硬件接收数据层,注册数据处理回调函数|
|`__piper_fk`|`C_PiperForwardKinematics`|机械臂正解类|
|`__parser`|`C_PiperParserBase`|数据协议解析类实例化，当前为V1版本协议解析，类型为数据解析类的基类|
|`__firmware_data`|`bytearray`|固件版本字符串|
|`__fps_counter`|`C_FPSCounter`|can帧率计算|
|`__is_ok`|`Bool`|can总线是否还有数据|
|`__arm_time_stamp`|`ArmTimeStamp`|时间戳类的实例化，是`C_PiperInterface_V2`的私有类，是一些由多个can帧组合一起的机械臂变量的时间戳，例如关节角|
|`__link_feedback_fk`|`list[float]`|机械臂所有关节反馈信息的正解位置|
|`__link_ctrl_fk`|`list[float]`|机械臂所有关节控制信息的正解位置|
|`__arm_status`|`ArmStatus`|机械臂状态消息的实例，包含机械臂的状态信息。|
|`__arm_end_pose`|`ArmEndPose`|机械臂末端姿态反馈消息的实例，包含末端的姿态信息。|
|`__arm_joint_msgs`|`ArmJoint`|机械臂关节角度反馈消息的实例，包含各关节的状态信息。|
|`__arm_gripper_msgs`|`ArmGripper`|机械臂夹爪反馈消息的实例，包含各夹爪的状态信息。|
|`__arm_motor_info_high_spd`|`ArmMotorDriverInfoHighSpd`|变量为机械臂电机消息高速反馈类|
|`__arm_motor_info_low_spd`|`ArmMotorDriverInfoLowSpd`|变量为机械臂电机低速反馈类|
|`__feedback_current_motor_angle_limit_max_vel`|`ArmMotorAngleLimitAndMaxVel`|变量为主动发送can帧后的反馈消息，用来读取当前电机限制角度/最大速度|
|`__feedback_current_end_vel_acc_param`|`CurrentEndVelAndAccParam`|该变量为主动发送can帧后的反馈消息，用来读取当前末端速度/加速度参数|
|`__feedback_crash_protection_level`|`CrashProtectionLevelFeedback`|该变量为主动发送can帧后的反馈消息，用来读取碰撞防护等级设置反馈指令|
|`__feedback_current_motor_max_acc_limit`|`CurrentMotorMaxAccLimit`|该变量为主动发送can帧后的反馈消息，用来读取反馈当前电机最大加速度限制|
|`__arm_joint_ctrl_msgs`|`ArmJointCtrl`|变量为读取主动臂给从动臂发送的关节角消息|
|`__arm_gripper_ctrl_msgs`|`ArmGripperCtrl`|变量为读取主动臂给从动臂发送的夹爪消息|
|`__arm_ctrl_code_151`|`ArmCtrlCode_151`|变量为读取主动臂发送给从动臂的0x151指令消息|
|`__arm_all_motor_max_acc_limit`|`AllCurrentMotorMaxAccLimit`|变量为机械臂关节所有关节电机的最大加速度限制消息|
|`__arm_all_motor_angle_limit_max_spd`|`AllCurrentMotorAngleLimitMaxSpd`|机械臂关节所有关节电机的角度限制和最大速度|
|`_initialized`|`Bool`|类内防止重复实例标志位|

### 3.函数解析

| 函数   | 类型 |说明                                                         |使用                | 参数                        |反馈       |
| ----- | ---- |------------------------------------------------------------ |-------------------|--------------------------- |--------|
|`get_instance`|Getter Method|获取当前实例地址|bj.GetArmStatus()|`can_name (str)`, `judge_flag (Bool)`, `can_auto_init (Bool)`|self@C_PiperInterface|
|`ConnectPort`|Start Method|该函数为打开can消息读取函数，该函数调用读取can消息函数，并创建读取线程，打开线程|用来在外部实例化类后，打开数据处理线程，并且发送读取机械臂电机的最大加速度、关节限位和最大速度读取指令|`can_init (Bool)`|None|
|`DisconnectPort`|Close Method|该函数为停止can读取线程并关闭can总线读取|外部实例化类后，关闭读取|`can_init (Bool)`|None|
|`ParseCANFrame`|Getter Method|can协议解析函数，用来处理接收到的can数据帧，为can接收消息的回调函数|先创建局部变量，然后调用解析协议类中的解码函数如果解码成功，则更新对应的消息，更新到上述的私有变量中，每个更新数据函数都有筛选当前数据类型，对应的数据类型才会被更新|`rx_message: Optional[can.Message]`|None|
|`GetCanFps`|Getter Method|获取can总线当前实时帧率|obj.GetArmStatus()|None|int|
|`GetArmStatus`|Getter Method|获取机械臂状态信息。使用互斥锁`__arm_status_mtx`保证线程安全。|obj.GetArmStatus()|None|self.__arm_status|
|`GetArmEndPoseMsgs`|Getter Method|获取机械臂末端位置的消息。使用互斥锁`__arm_end_pose_mtx`保证线程安全。|obj.GetArmEndPoseMsgs()|None|self.__arm_end_pose|
|`GetArmJointMsgs`|Getter Method|获取机械臂关节的状态消息。使用互斥锁`__arm_joint_msgs_mtx`保证线程安全。|obj.GetArmJointMsgs()|None|self.__arm_joint_msgs|
|`GetFK`|Getter Method|获取机械臂每个关节控制信息和反馈信息的正解,XYZ单位为mm,RXRYRZ单位为度，反馈长度为6的float类型数据列表,代表 1-6 关节相对 base_link 的位姿|obj.GetFK()|mode:Literal["feedback", "control"]="feedback"|self.__link_fk|
|`GetArmGripperMsgs`|Getter Method|获取机械臂夹爪的状态消息。使用互斥锁`__arm_gripper_msgs_mtx`保证线程安全。|obj.GetArmGripperMsgs()|None|self.__arm_gripper_msgs|
|`GetArmHighSpdInfoMsgs`|Getter Method|获取机械臂高速运动信息的消息。使用互斥锁`__arm_motor_info_high_spd_mtx`保证线程安全。|obj.GetArmHighSpdInfoMsgs()|None|self.__arm_motor_info_high_spd|
|`GetArmLowSpdInfoMsgs`|Getter Method|获取机械臂低速运动信息的消息。使用互斥锁`__arm_motor_info_low_spd_mtx`保证线程安全。|obj.GetArmLowSpdInfoMsgs()|None|self.__arm_motor_info_low_spd|
|`GetCurrentMotorAngleLimitMaxVel`|Getter Method|获取当前指定电机编号的角度最大限制值。使用互斥锁`__feedback_current_motor_angle_limit_max_vel_mtx`保证线程安全。|obj.GetCurrentMotorAngleLimitMaxVel()|None|self.__feedback_current_motor_angle_limit_max_vel|
|`GetCurrentEndVelAndAccParam`|Getter Method|获取当前机械臂末端速度和加速度参数的反馈。使用互斥锁`__feedback_current_end_vel_acc_param_mtx`保证线程安全。|obj.GetCurrentEndVelAndAccParam()|None|self.__feedback_current_end_vel_acc_param|
|`GetCrashProtectionLevelFeedback`|Getter Method|获取碰撞保护等级的反馈信息。使用互斥锁`__feedback_crash_protection_level_mtx`保证线程安全。|obj.GetCrashProtectionLevelFeedback()|None|self.__feedback_crash_protection_level|
|`GetCurrentMotorMaxAccLimit`|Getter Method|获取当前电机最大加速度限制的反馈。使用互斥锁`__feedback_current_motor_max_acc_limit_mtx`保证线程安全。|obj.GetCurrentMotorMaxAccLimit()|None|self.__feedback_current_motor_max_acc_limit|
|`GetArmJointCtrl`|Getter Method|获取机械臂主动臂发给从臂的关节角控制消息。使用互斥锁`__arm_joint_ctrl_msgs_mtx`保证线程安全。|obj.GetArmJointCtrl()|None|self.__arm_joint_ctrl_msgs|
|`GetArmGripperCtrl`|Getter Method|获取机械臂主动臂发给从臂的夹爪控制消息。使用互斥锁`__arm_gripper_ctrl_msgs_mtx`保证线程安全。|obj.GetArmJointCtrl()|None|self.__arm_gripper_ctrl_msgs|
|`GetArmCtrlCode151`|Getter Method|获取机械臂控制码151的状态。使用互斥锁`__arm_ctrl_code_151_mtx`保证线程安全。|obj.GetArmCtrlCode151()|None|self.__arm_ctrl_code_151|
|`GetAllMotorMaxAccLimit`|Getter Method|获取机械臂控关节所有关节电机的最大加速度限制消息，使用互斥锁`__arm_all_motor_max_acc_limit_mtx`保证线程安全。|obj.GetAllMotorMaxAccLimit()|None|self.__arm_all_motor_max_acc_limit|
|`GetAllMotorAngleLimitMaxSpd`|Getter Method|获取机械臂控关节所有关节电机的角度限制和最大速度，使用互斥锁`__arm_all_motor_angle_limit_max_spd_mtx`保证线程安全。|obj.GetAllMotorAngleLimitMaxSpd()|None|self.__arm_all_motor_angle_limit_max_spd|
|`GetPiperFirmwareVersion`|Getter Method|获取piper机械臂的主控固件版本，反馈固件版本字符串|obj.GetPiperFirmwareVersion()|None|firmware_version|
|`isOk`|Getter Method|反馈can数据读取线程是否正常|obj.isOk()|None|self.__is_ok|
|`__CanMonitor`|Getter Method|can数据帧率检测|类内使用|None|None|
|`__UpdateArmStatus`|Getter Method|更新机械臂状态|类内使用|msg:PiperMessage|self.__arm_status|
|`__UpdateArmEndPoseState`|Getter Method|更新末端位姿状态，单位为0.001mm|类内使用|msg:PiperMessage|self.__arm_end_pose|
|`__UpdateArmJointState`|Getter Method|更新关节状态，关节角单位为0.001度|类内使用|msg:PiperMessage|self.__arm_joint_msgs|
|`__UpdateArmGripperState`|Getter Method|更新夹爪状态，夹爪反馈的行程单位为0.001mm|类内使用|msg:PiperMessage|self.__arm_gripper_msgs|
|`__UpdateDriverInfoHighSpdFeedback`|Getter Method|更新驱动器信息反馈（高速）|类内使用|msg:PiperMessage|self.__arm_motor_info_high_spd|
|`__UpdateDriverInfoLowSpdFeedback`|Getter Method|更新驱动器信息反馈（低速）|类内使用|msg:PiperMessage|self.__arm_motor_info_low_spd|
|`__UpdateCurrentMotorAngleLimitMaxVel`|Getter Method|更新当前电机限制角度/最大速度|类内使用|msg:PiperMessage|self.__feedback_current_motor_angle_limit_max_vel|
|`__UpdateCurrentMotorMaxAccLimit`|Getter Method|更新当前电机最大加速度限制|类内使用|msg:PiperMessage|self.__feedback_current_motor_max_acc_limit|
|`__UpdateAllCurrentMotorAngleLimitMaxVel`|Getter Method|更新所有电机最大加速度限制|类内使用|msg:PiperMessage|self.__arm_all_motor_angle_limit_max_spd|
|`__UpdateAllCurrentMotorMaxAccLimit`|Getter Method|更新所有电机角度限制和最大速度|类内使用|msg:PiperMessage|self.__arm_all_motor_max_acc_limit|
|`__UpdateCurrentEndVelAndAccParam`|Getter Method|更新当前末端速度/加速度参数|类内使用|msg:PiperMessage|self.__feedback_current_end_vel_acc_param|
|`__UpdateCrashProtectionLevelFeedback`|Getter Method|更新碰撞防护等级设置反馈指令|类内使用|msg:Pipe self.__UpdatePiperFK()rMessage|self.__feedback_crash_protection_level|
|`__UpdateArmJointCtrl`|Getter Method|更新关节状态（为主臂发送的消息）|类内使用|msg:PiperMessage|self.__arm_joint_ctrl_msgs|
|`__UpdateArmGripperCtrl`|Getter Method|更新夹爪状态（为主臂发送的消息）|类内使用|msg:PiperMessage|self.__arm_gripper_ctrl_msgs|
|`__UpdateArmCtrlCode151`|Getter Method|更新主臂发送的151控制指令|类内使用|msg:PiperMessage|self.__arm_ctrl_code_151|
|`__UpdatePiperFirmware`|Getter Method|更新发送4AF后，读取到的4AF反馈的字符并拼接|类内使用|msg:PiperMessage|self.__firmware_data|
|`__UpdatePiperFeedbackFK`|Getter Method|更新piper反馈信息正解数据|类内使用|None|None|
|`__UpdatePiperCtrlFK`|Getter Method|更新piper控制信息正解数据|类内使用|None|None|
|`MotionCtrl_1`|Ctrl Method|0x150,可以控制急停、轨迹传输及拖动示教模式。|类外调用|`emergency_stop (uint8)`,`track_ctrl (uint8)`, `grag_teach_ctrl (uint8)`|None|
|`MotionCtrl_2`|Ctrl Method|0x151,可以设置控制模式、MOVE模式及运动速度。每次控制机械臂运动之前都要发送一次，否则机械臂可能动不起来|类外调用|`ctrl_mode (uint8)`,`move_mode (uint8)`, `move_spd_rate_ctrl (uint8)`|None|
|`EndPoseCtrl`|Ctrl Method|0x152,0x153,0x154,控制机械臂的末端位置和姿态。是下面三个函数的汇总,需要注意的是，该函数发送出去的x、y、z数值单位为0.001mm,rx、ry、rz数值单位为0.001度,假如需要机械臂向x轴方向运行0.3m，则发送的数据应为0.3\*100\*1000=30000|类外调用|`X (int)`, `Y (int)`, `Z (int)`, `RX (int)`, `RY (int)`, `RZ (int)`|None|
|`__CartesianCtrl_XY`|Ctrl Method|控制机械臂笛卡尔坐标的XY轴运动。|类内调用(私有)|`X (int)`, `Y (int)`|None|
|`__CartesianCtrl_ZRX`|Ctrl Method|控制机械臂笛卡尔坐标的Z轴和RX轴运动。|类内调用(私有)|`Z (int)`, `RX (int)`|None|
|`__CartesianCtrl_RYRZ`|Ctrl Method|控制机械臂笛卡尔坐标的RY轴和RZ轴运动。|类内调用(私有)|`RY (int)`, `RZ (int)`|None|
|`JointCtrl`|Ctrl Method|0x155,0x156,0x157,控制机械臂的六个关节运动。需要注意的是，该函数发送出去的数值单位为0.001度,假如需要机械臂1号关节运动90度(1.57弧度)，则发送的数据为90*1000,如果是弧度，则1.57\*1000\*(180/3.14)|类外调用|`joint_1 (int)`, `joint_2 (int)`, `joint_3 (int)`, `joint_4 (int)`, `joint_5 (int)`, `joint_6 (int)`|None|
|`__JointCtrl_12`|Ctrl Method|控制机械臂1,2关节运动。|类内调用(私有)|`joint_1 (int)`, `joint_2 (int)`|None|
|`__JointCtrl_34`|Ctrl Method|控制机械臂3,4关节运动。|类内调用(私有)|`joint_3 (int)`, `joint_4 (int)`|None|
|`__JointCtrl_56`|Ctrl Method|控制机械臂5,6关节运动。|类内调用(私有)|`joint_5 (int)`, `joint_6 (int)`|None|
|`MoveCAxisUpdateCtrl`|Ctrl Method|机械臂圆弧模式控制，需要EndPoseCtrl配合使用。EndPoseCtrl发布目标位姿，MoveCAxisUpdateCtrl按照参数执行上一条 EndPoseCtrl() 设定的目标位姿，并更新运动轨迹。|类外调用|`instruction_num:int`|None|
|`GripperCtrl`|Ctrl Method|0x159控制机械臂夹爪的运动。夹爪适配agx的末端执行器，夹爪模块是独立使能,需要注意的是，该函数发送出去的数值单位为0.001mm,假如需要夹爪运动50mm，则发送的数据为50*1000=50000|类外调用|`gripper_angle (int)`, `gripper_effort (int)`, `gripper_code (int)`, `set_zero (int)`|None|
|`MasterSlaveConfig`|Ctrl Method|0x470,配置机械臂随动主从模式。|类外调用|`linkage_config (int)`, `feedback_offset (int)`, `ctrl_offset (int)`, `linkage_offset (int)`|None|
|`DisableArm`|Ctrl Method|0x471,失能电机。此时指定电机失去力，如果此时机械臂处于非零点位置，例如2号关节和3号关节抬起状态下，机械臂会直接失力掉下来|类外调用|`motor_num (int)`, `enable_flag (int)`|None|
|`EnableArm`|Ctrl Method|0x471,使能机械臂电机，此时指定的机械臂电机上电，用手尝试移动机械臂关节是无法移动的|类外调用|`motor_num (int)`, `enable_flag (int)`|None|
|`SearchMotorMaxAngleSpdAccLimit`|Ctrl Method|0x472,查询电机角度、最大速度及最大加速度限制。这是一个主动发送后反馈指定消息的指令，为应答式指令，可以通过修改`search_content`来查询指定的内容，反馈的内容是单个电机的|类外调用|`motor_num (int)`, `search_content (int)`|None|
|`SearchAllMotorMaxAngleSpd`|Ctrl Method|查询全部电机的电机最大角度/最小角度/最大速度指令|类外调用|None|None|
|`SearchAllMotorMaxAccLimit`|Ctrl Method|查询全部电机的最大加速度限制指令|类外调用|None|None|
|`MotorAngleLimitMaxSpdSet`|Ctrl Method|设置电机角度限制及最大速度。|类外调用|`motor_num (int)`, `max_angle_limit (int)`, `min_angle_limit (int)`, `max_joint_spd (int)`|None|
|`JointConfig`|Ctrl Method|配置关节参数。|类外调用|`joint_num (int)`, `set_zero (int)`, `acc_param_is_effective (int)`, `max_joint_acc (int)`, `clear_err (int)`|None|
|`JointMaxAccConfig`|Ctrl Method|设定关节最大加速度|类外调用|`motor_num (int)`, `max_joint_acc (int)`|None|
|`SetInstructionResponse`|Ctrl Method|设置指令应答。|类外调用|`instruction_index (int)`, `zero_config_success_flag (int)`|None|
|`ArmParamEnquiryAndConfig`|Ctrl Method|机械臂参数查询与设置。|类外调用|`param_enquiry (int)`, `param_setting (int)`, `data_feedback_0x48x (int)`, `end_load_param_setting_effective (int)`, `set_end_load (int)`|None|
|`EndSpdAndAccParamSet`|Ctrl Method|设置机械臂末端速度及加速度参数。|类外调用|`end_max_linear_vel (int)`, `end_max_angular_vel (int)`, `end_max_linear_acc (int)`, `end_max_angular_acc (int)`|None|
|`CrashProtectionConfig`|Ctrl Method|配置机械臂碰撞防护等级。|类外调用|`joint_1_protection_level (int)`, `joint_2_protection_level (int)`, `joint_3_protection_level (int)`, `joint_4_protection_level (int)`, `joint_5_protection_level (int)`, `joint_6_protection_level (int)`|None|
|`SearchPiperFirmwareVersion`|Ctrl Method|查询piper机械臂的主控固件版本|类外调用|None|None|

注意：

所有Update函数都是用来读取can数据帧后更新解析的数据到私有变量中的接口,由于获取消息并处理后的变量被更新到私有变量中，因此需要用类内的Get函数来获取私有变量的数值

注意获取的所有数值为原始数值

机械臂末端位姿反馈单位为0.001mm

关节角变量单位为0.001度

夹爪反馈的行程单位为0.001mm

夹爪反馈的扭矩单位为0.001N/m

因此需要自行处理单位问题，例如需要获取夹爪当前角度，需要将Get到的关节角度除以1000，才是获取到的真实角度
