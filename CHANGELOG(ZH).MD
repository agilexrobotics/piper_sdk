# CHANGELOG(ZN)

[Click to switch EN](CHANGELOG.MD)
=============

Version 0.3.0
=============

特性
--------

- 增加interface形参`start_sdk_joint_limit`、`start_sdk_gripper_limit`，默认参数为`False`
- 增加`utils`路径，内含fps计算和四元数欧拉角计算工具（外旋sxyz）
  - 通过`quat_convert_euler`将四元数转换为欧拉角
  - 通过`euler_convert_quat`将欧拉角转换为四元数
- 增加 开启/关闭 sdk计算fk的函数`EnableFkCal`、`DisableFkCal`，`isCalFk`用来获取是否开启计算fk，然后通过`GetFK`函数读取，开启计算fk后读取线程会占用很高的cpu，请按需开启
- 增加获取`ConnectPort`函数调用状态的函数`get_connect_status`
- 降低interface中开启的`CanMonitor`线程的频率（20hz）以及存储帧率数值队列的长度（5）
- 帧率计算线程去掉窗口计算函数（过分占内存），改为每隔固定时间（0.1s）检测循环计数增量乘一个固定数值（10）来计算一秒内的数据帧率
- 在夹爪/示教器参数反馈命令（反馈和发送）中增加示教器摩擦系数参数
- 添加了`ModeCtrl`和`EmergencyStop`函数来设置模式和执行紧急停止（替代`MotionCtrl_1`和`MotionCtrl_2`）
- 将获取 CAN_ID=0x151 的臂模式控制命令的函数从`GetArmCtrlCode151`重命名为`GetArmModeCtrl`
- 增加机械臂状态反馈中的enum，当你使用demo里的`piper_read_status.py`来打印机械臂当前状态时，可以看到显式的格式化字符串表示当前机械臂的状态（实际变量的数值还是int）
- 将demo的文件重命名
- 在`C_STD_CAN` 类中初始化`rx_message`为`Message()`类型
- 修改了获取反馈信息时间戳的位置，从interface中获取当前系统时间修改到进入解码函数中获取时间戳，以增加数据时间戳的精准性
- 添加了 `piper_param_manager` 文件，其中包含角度和夹持器范围限制，并对反馈和控制消息应用约束
  - 使用interface中的形参来打开sdk限制功能：`piper = C_PiperInterface_V2("can0", start_sdk_joint_limit=True, start_sdk_gripper_limit=True)`
  - 如果反馈或控制消息超出设定的限制，则值将被限制在边界值内
  - 程序内已经存在了默认限制，要自定义配置限制范围，请使用 `SetSDKJointLimitParam` 和 `SetSDKGripperRangeParam` 函数设置软件约束
  
  请参阅demo中的 `piper_set_sdk_param.py` 文件以获取示例。
- 略微降低了关节限制，以防止在使用 math.degrees 将弧度转换为度数时超出机械臂的角度限制。新的限制如下：

  | joint_name |     limit(rad)       |    limit(angle)    |     limit(rad/s)   |
  |------------|----------------------|--------------------|--------------------|
  | joint1     |   [-2.6179, 2.6179]  |    [-150.0, 150.0] |      [0, 3.0]      |
  | joint2     |   [0, 3.14]          |    [0, 180.0]      |      [0, 3.0]      |
  | joint3     |   [-2.967, 0]        |    [-170, 0]       |      [0, 3.0]      |
  | joint4     |   [-1.745, 1.745]    |    [-100.0, 100.0] |      [0, 3.0]      |
  | joint5     |   [-1.22, 1.22]      |    [-70.0, 70.0]   |      [0, 3.0]      |
  | joint6     |   [-2.09439, 2.09439]|    [-120.0, 120.0] |      [0, 3.0]      |

  注意：弧度到度的转换系数为 57.2957795 (180/3.1415926)。

- 添加了`piper_set_load.py`demo，用于设置负载条件（空载/半载/满载）
- demo路径下增加了`detect_arm.py`用来在终端监测机械臂各种信息，注意这个文件未向后兼容

Bug修复
---------

- 修复了夹具反馈时间戳为`int`类型的问题。

其它
---------

- 修改了文件夹结构，将`fps.py`放到`utils`路径中，`monitor`路径将在下一版本后删除
- 重构了文档结构：
  - 大部分文档已用英文重写
  - 简化了文档，仅关注接口使用

Version 0.2.19
=============

特性
--------

None

Bug修复
---------

- 修复了异常电流反馈值。(高速 piper 消息)
  piper_sdk/piper_msgs/msg_v1/feedback/arm_high_spd_feedback.py
  piper_sdk/piper_msgs/msg_v2/feedback/arm_high_spd_feedback.py
  piper_sdk/protocol/protocol_v1/piper_protocol_v1.py
  piper_sdk/protocol/protocol_v2/piper_protocol_v2.py

其它
---------

None

Version 0.2.18
=============

特性
--------

- 在高速信息反馈中添加了`effort`反馈，单位为 0.001 N/m。
- 移除了`sh`脚本中的元素，以确保与`zsh`兼容。
- 添加了`interface_v1`，且不影响之前的版本，并将其保留用于后续更新。
- 在`__init__.py`中添加了类引用。
- 修复了`msg_v1/__init__.py`、`msg_v2/__init__.py`、`protocol/protocol_v2/piper_protocol_v2.py`和`arm_low_spd_feedback.py`中错误的注释。
-​​ 将`ArmMsgFeedbackCurrentMotorMaxAccLimit`类中`max_joint_acc`的单位描述更正为`0.001 rad/s^2`。
- 在接口文档中添加了固件版本说明。

Bug修复
---------

- 修改了 `pyproject.toml`，以便使用 `setup.py` 正确安装（之前的版本在 `project` 标签中缺少 `version` 字段，导致 `pip install.` 失败）。
- 修复了 `msg_v2` 中 `msg_type` 未使用 `auto` 赋值的问题。
- 修复了 `piper_sdk/__init__.py` 中缺少类引用导致的错误。
- 修复了 `protocol` 中将电机 2 的位置信息错误地赋值给电机 3 的错误。
- 修复了 `interface` 中高速反馈数据的时间戳错误地使用了低速反馈数据的时间戳的问题。

其它
---------

None

Version 0.2.17
=============

特性
--------

- 修改了 `piper_msgs/msg_v1(msg_v2)/feedback/arm_low_spd_feedback.py` 文件中 `foc_status` 的参数名称，共包含以下两个文件：
  - 将 `sensor_status` 重命名为 `collision_status`
  - 将 `homing_status` 重命名为 `stall_status`
- 为 `JointCtrl` 函数添加了类型检查（必须为 Python 的 int 类型）和取值范围检查（在关节限制范围内）
- 为 `EndPoseCtrl` 函数的输入值添加了类型检查（必须为 Python 的 int 类型）
- 修改了 `SearchAllMotorMaxAngleSpd` 和 `SearchAllMotorMaxAccLimit` 函数的注释，使其包含 CAN ID 描述
- 添加了用于设置和打印机械臂碰撞等级的演示文件 `piper_read_crash_protectation.py`
- 修改了 `arm_high_spd_feedback`，将 `motor_speed` 单位设置为 0.001 rad/s，将 `current` 单位设置为 0.001 A
- 修改了 shell 脚本。由于 `sh` 命令不支持 `==` 进行相等性比较，而 `bash` 支持，将其改为使用 `=` 进行相等性比较，令其可以被`zsh`使用

Bug修复
---------

None

其它
---------

None

Version 0.1.16
=============

特性
--------

- 更正了夹爪打印数据的输出单位
- 统一了代码格式
- 增加了夹爪消息发送的数据限制：[0, 5000]，对应 [0, 5] N/m
- 增加了设置最大关节速度的数据限制：[0, 3000]，对应 [0, 3] rad/s
- 增加了设置最大关节加速度的数据限制：[0, 500]，对应 [0, 5] rad/s^2

Bug修复
---------

None

其它
---------

None

Version 0.1.15
=============

特性
--------

None

Bug修复
---------

* 修复了 CAN 发送函数中调用`is_can_bus_ok`导致`base_state`为 None 的问题

其它
---------

None

Version 0.1.14
=============

特性
--------

修改了 GetFK 函数，新增了一个 mode 参数，用于选择机械臂正向运动关节数据的来源。

mode 参数仅支持两个值：["feedback", "control"]。

mode 的默认值为 `"feedback"`。

Bug修复
---------

None

其它
---------

None

Version 0.1.13
=============

特性
--------

纠正 0.1.12 版本文档中的错误。

Bug修复
---------

None

其它
---------

None

Version 0.1.12
=============

特性
--------

### ChangeLog-V1

这里的V1版本代码，是属于0.1.x版本的代码

0.1.x版本代码与0.0.x代码区别较大，前者的V1是在后者基础上更新迭代

下文主要讲解0.1.x-V1版本代码和0.0.x代码的区别

#### 1 固件兼容

- **兼容新固件(V1.5-2版本前)协议，协议内容不赘述**

#### 2 interface

- **`C_PiperInterface`**

##### 2.1 特性

- 增加了类的条件实例化特性，条件为传入interface的`can_name`，如在循环中重复`piper=C_PiperInterface(can_name="can0")`，仅仅只会创建一次实例，之后的实例化会因为识别到已经重复创建了`can_name="can0"`实例而不会重复创建
- 类内增加了帧率计算，可以通过下面的`isOk`函数判断can传输是否正常，反馈值为True则表明数据正常传输，如果为False则说明数据断开
- 增加了正解，通过扩展DH参数来计算每个关节相对base_link的位姿，通过`GetFK`函数获取，反馈link1~link6的位姿，是一个6*6的列表，第-1位为link6的位姿

##### 2.2 函数

0.1.x-V1 相比 0.0.x 增加了一些函数，如下：

| 函数   | 类型 |说明                                                         |使用                | 参数                        |反馈       |
| ----- | ---- |------------------------------------------------------------ |-------------------|--------------------------- |--------|
|`GetCanFps`|Getter Method|获取can总线当前实时帧率|obj.GetArmStatus()|None|int|
|`GetFK`|Getter Method|获取机械臂每个关节控制信息和反馈信息的正解,XYZ单位为mm,RXRYRZ单位为度，反馈长度为6的float类型数据列表,代表 1-6 关节相对 base_link 的位姿|obj.GetFK()|mode:Literal["feedback", "control"]="feedback"|self.__link_fk|
|`isOk`|Getter Method|反馈can数据读取线程是否正常|obj.isOk()|None|self.__is_ok|
|`__CanMonitor`|Getter Method|can数据帧率检测|类内使用|None|None|
|`__UpdatePiperFeedbackFK`|Getter Method|更新piper反馈信息正解数据|类内使用|None|None|
|`__UpdatePiperCtrlFK`|Getter Method|更新piper控制信息正解数据|类内使用|None|None|

### 2 ChangeLog-V2

V2 基于 V1.5-2 及更高版本

此处 V1 和 V2 版本代码均基于 0.1.x 版本。

在 0.1.x 版本中，V2 与 V1 的区别在于协议。

0.1.x 版本的代码与 0.0.x 版本的代码有显著差异。

以下章节主要介绍 V2 与 V1 之间的区别。

#### 2.1 固件兼容

- **兼容新固件(V1.5-2版本后)协议，保留同时兼容上一版本固件**

##### 2.1.1 0x2A1 机械臂状态反馈

补充：

Byte 2 模式反馈增加 0x04 MOVE M 反馈，为mit模式反馈

##### 2.1.2 0x151 模式控制协议

补充：

Byte 1 MOVE模式增加 0x04 MOVE M 指令，为mit模式设定

增加

Byte 5 安装位置设定

- 0x00 无效值
- 0x01水平正装
- 0x02侧装左
- 0x03侧装右  

注意接线朝后

##### 2.1.3 新增MIT控制指令

|机械臂关节1～6MIT控制指令|                                       |ID  0x15A ~ 0x15F|      len 8      |
|----------------------|---------------------------------------|-----------------|-----------------|
|        数据          |                  功能                  |        类型      |                 |
|       Byte 0        |  Pos_ref [bit15~bit8] 高8位            |       uint8     |                 |
|       Byte 1        |  Pos_ref [bit7~bit0]  低8位            |       uint8     |                 |
|       Byte 2        |  Vel_ref [bit11~bit4] 低12位           |       uint8     |                 |
|       Byte 3        |  Vel_ref [bit3~bit0] Kp [bit11~bit8]  |       uint8     |                 |
|       Byte 4        |  Kp [bit7~bit0]                       |       uint8     | Kp给定参考值：10  |
|       Byte 5        |  Kd [bit11~bit4]      低12位           |       uint8     | Kd给定参考值：0.8 |
|       Byte 6        |  Kd [bit3~bit0] T_ref [bit7~bit4]      |       uint8     |                 |
|       Byte 7        |  T_ref [bit3~bit0] CRC [bit3~bit0]     |       uint8     |                 |

##### 2.1.4 ID 0x474 电机角度限制/最大速度设置指令

增补无效值指令

|电机角度限制/最大速度设置指令|                                       |ID  0x474        |                           |
|------------------------|---------------------------------------|-----------------|---------------------------|
|          数据           |                  功能                 |        类型      |                           |
|       Byte 0           |  关节电机序号                           |       uint8     |值域1-6:1-6代表关节驱动器序号；|
|       Byte 1           |  最大角度限制 H                         |       uint16    |单位 0.1° **无效值：0x7FFF** |
|       Byte 2           |  最大角度限制 L                         |                 |                           |
|       Byte 3           |  最小角度限制 H                         |       uint16    |单位 0.1°**无效值：0x7FFF**  |
|       Byte 4           |  最小角度限制 L                         |                 |                           |
|       Byte 5           |  最大关节速度 H                         |       uint16    |单位 0.001rad/s**无效值：0x7FFF**|
|       Byte 6           |  最大关节速度 L                         |                 |                           |
|       Byte 7           |  保留                                  |                 |                           |

##### 2.1.5 ID 0x475 关节设置指令

增补无效值指令

|关节设置指令              |                                       |ID  0x475        |                                         |
|------------------------|---------------------------------------|-----------------|-----------------------------------------|
|          数据           |                  功能                 |        类型      |                                         |
|       Byte 0           |  关节电机序号                           |       uint8     |值域1-7:1-6代表关节驱动器序号；7代表全部关节电机|
|       Byte 1           |  设置N号电机当前位置为零点                |       uint8     |有效值 ：0xAE|
|       Byte 2           |  加速度参数设置是否生效                   |       uint8     |有效值 ：0xAE|
|       Byte 3           |  最大关节加速度 H                        |       uint16    |单位 0.001rad/s^2 **无效值：0x7FFF**|
|       Byte 4           |  最大关节加速度 L                        |                 |有效值 ：0xAE|
|       Byte 5           |  清除关节错误代码                        |       uint8     |                                         |
|       Byte 6           |  保留                                  |                 |                                         |
|       Byte 7           |  保留                                  |                 |                                         |

##### 2.1.6 ID 0x477 机械臂参数查询与设置指令

增补:

查询夹爪/示教器参数索引:0x04

|关节设置指令              |                                       |ID  0x475        |                                         |
|------------------------|---------------------------------------|-----------------|-----------------------------------------|
|          数据           |                  功能                 |        类型      |                                         |
|       Byte 0           |  参数查询                              |       uint8     |查询末端V/acc参数：0x01 查询碰撞防护等级： 0x02 查询当前轨迹索引： 0x03 **查询夹爪/示教器参数索引:0x04**|
|       Byte 1           |  参数设置                              |       uint8     |设置末端V/acc参数为初始值：0x01 设置全部关节限位、关节最大速度、关节加速度为默认值： 0x02|
|       Byte 2           |  0x48X报文反馈设置                      |       uint8     |无效：0x00;开启周期反馈： 0x01;关闭周期反馈： 0x02;开启后周期上报1~6号关节当前末端速度/加速度|
|       Byte 3           |  末端负载参数设置是否生效                 |       uint8     |有效值 ：0xAE|
|       Byte 4           |  设置末端负载                           |       uint8     |0x00--空载; 0x01--半载; 0x02--满载|
|       Byte 5           |  保留                                  |       uint8     |                                         |
|       Byte 6           |  保留                                  |                 |                                         |
|       Byte 7           |  保留                                  |                 |                                         |

##### 2.1.7 ID 0x479 末端速度/加速度参数设置指令

增补无效值指令

|末端速度/加速度参数设置指令 |                                       |ID  0x479        |                                         |
|------------------------|---------------------------------------|-----------------|-----------------------------------------|
|          数据           |                  功能                 |        类型      |                                         |
|       Byte 0           |  末端最大线速度 H                       |       uint16    |单位 0.001m/s **无效值：0x7FFF**           |
|       Byte 1           |  末端最大线速度 L                       |                 |                                         |
|       Byte 2           |  末端最大角速度 H                       |       uint16    |单位 0.001rad/s **无效值：0x7FFF**         |
|       Byte 3           |  末端最大角速度 L                       |                 |                                         |
|       Byte 4           |  末端最大线加速度 H                      |      uint16     |单位 0.001m/s^2 **无效值：0x7FFF**         |
|       Byte 5           |  末端最大线加速度 L                      |                 |                                         |
|       Byte 6           |  末端最大角加速度 H                      |      uint16     |单位 0.001rad/s^2 **无效值：0x7FFF**       |
|       Byte 7           |  末端最大角加速度 L                      |                 |                                         |

##### 2.1.8 New ID 0x47D 夹爪/示教器参数设置指令

|夹爪/示教器参数设置指令     |                                       |ID  0x47D        |                                         |
|------------------------|---------------------------------------|-----------------|-----------------------------------------|
|          数据           |                  功能                 |        类型      |                                         |
|       Byte 0           |  示教器行程系数设置                      |       uint8     |示教器行程系数设置：100~200 单位 ：%（默认100%）仅适用于设置主从臂的主臂，用于放大控制行程给从臂|
|       Byte 1           |  夹爪/示教器最大控制行程限制值设置         |       uint8     |单位：mm; 无效值：0; 小夹爪为70mm; 大夹爪为100mm|
|       Byte 2           |  保留                                 |                 |                                           |
|       Byte 3           |  保留                                 |                 |                                           |
|       Byte 4           |  保留                                 |                 |                                           |
|       Byte 5           |  保留                                 |                 |                                           |
|       Byte 6           |  保留                                 |                 |                                           |
|       Byte 7           |  保留                                 |                 |                                           |

##### 2.1.9 New ID 0x47E 夹爪/示教器参数反馈指令

|夹爪/示教器参数反馈指令     |                                       |ID  0x47E        |                                         |
|------------------------|---------------------------------------|-----------------|-----------------------------------------|
|          数据           |                  功能                 |        类型      |                                         |
|       Byte 0           |  示教器行程系数反馈                      |       uint8     |示教器行程系数设置：100~200 单位 ：%（默认100%）仅适用于设置主从臂的主臂，用于放大控制行程给从臂|
|       Byte 1           |  夹爪/示教器最大控制行程限制值反馈         |       uint8     |单位：mm; 无效值：0; 小夹爪为70mm; 大夹爪为100mm|
|       Byte 2           |  保留                                 |                 |                                           |
|       Byte 3           |  保留                                 |                 |                                           |
|       Byte 4           |  保留                                 |                 |                                           |
|       Byte 5           |  保留                                 |                 |                                           |
|       Byte 6           |  保留                                 |                 |                                           |
|       Byte 7           |  保留                                 |                 |                                           |

#### 2.2 interface

- **保留V1版本`C_PiperInterface`，新增`C_PiperInterface_V2`**

将V2版本单独分出维护，虽然有一些重复代码，但是保证了版本之间的独立性，使用上并无太多差异

其中V2版本在V1基础上增加了函数，如下：

| 函数   | 类型 |说明                                                         |使用                | 参数                        |反馈       |
| ----- | ---- |------------------------------------------------------------ |-------------------|--------------------------- |--------|
|`GetGripperTeachingPendantParamFeedback`|Getter Method|获取夹爪/示教器参数反馈指令，包括示教器行程系数反馈、夹爪/示教器最大控制行程限制值反馈 为主动发送指令后反馈消息|obj.GetGripperTeachingPendantParamFeedback()|None|self.__feedback_gripper_teaching_pendant_param|
|`MotorMaxSpdSet`|Ctrl Method|设置电机最大速度。|类外调用|`motor_num (int)`, `max_joint_spd (int)`|None|
|`__JointMitCtrl`|Ctrl Method|0x15A,0x15B,0x15C,0x15D,0x15E,0x15F,机械臂关节1~6MIT控制指令|类内调用|`self,motor_num:int`,`pos_ref:float`,`vel_ref:float`,`kp:float`,`kd:float`,`t_ref:float`,`p_min:float=-12.5`,`p_max:float=12.5`,`v_min:float=-45.0`,`v_max:float=45.0`,`kp_min:float=0.0`,`kp_max:float=500.0`,`kd_min:float=-5.0`,`kd_max:float=5.0`,`t_min:float=-18.0`,`t_max:float=18.0`|None|
|`JointMitCtrl`|Ctrl Method|0x15A,0x15B,0x15C,0x15D,0x15E,0x15F,机械臂关节1~6MIT控制指令|类外调用|`self,motor_num:int`,`pos_ref:float`,`vel_ref:float`,`kp:float`,`kd:float`,`t_ref:float`|None|
|`GripperTeachingPendantParamConfig`|Ctrl Method|夹爪/示教器参数设置指令(基于V1.5-2版本后)|类外调用|`teaching_range_per:int=100`, `max_range_config:int=70`|None|

Bug修复
---------

None

其它
---------

None

Version 0.0.12
=============

特性
--------

- 修改了 CAN 总线类，使其数据读取部分兼容 Ubuntu 18.04 的 Python 3.6
- 更新了 protocol_base，简化了使用 struct 和 ctypes 将值转换为列表的函数
- 在接口类中添加了单例模式支持
- 为接口类中的 `ConnectPort` 函数添加了线程保护
- 为接口类中添加了 `DisconnectPort` 函数，用于停止数据读取过程
- 将接口类中的 `Update` 函数和一些变量更改为私有变量
- 修复了错误的注释，使其更具可读性
- 优化了文档结构和描述
- 添加了查询机械臂固件的接口`SearchPiperFirmwareVersion`，获取函数为`GetPiperFirmwareVersion`
- 添加了许多demo（例如 moveC）

Bug修复
---------

- 将`jonit`的拼写更正为`joint`。
- 将电机最大加速度的设置单位修正为 0.01 rad/s^2；新增函数`JointMaxAccConfig`用于设置电机的最大加速度。

其它
---------

None
