# Piper Interface V3 Documentation

## Class: `C_PiperInterface_V3`

`C_PiperInterface_V3` is the V3 interface class for controlling the Piper robotic arm.

It inherits from `C_PiperInterface_V2`, keeps unchanged V2 APIs available, and overrides only the V3-specific parser, message, and control behavior.

For unchanged APIs, see [Interface_V2 README](../V2/INTERFACE_V2.MD).

For protocol and message differences, see [ChangeLog-V3](./CHANGELOG-V3.MD).

## Constructor

```python
def __init__(self,
             can_name: str = "can0",
             judge_flag: bool = True,
             can_auto_init: bool = True,
             dh_is_offset: int = 0x01,
             start_sdk_joint_limit: bool = False,
             start_sdk_gripper_limit: bool = False,
             logger_level: LogLevel = LogLevel.WARNING,
             log_to_file: bool = False,
             log_file_path = None) -> None
```

| Parameter | Default | Description |
|---|---|---|
| `can_name` | `"can0"` | CAN port name |
| `judge_flag` | `True` | Whether to check the CAN port. Set to `False` when using hardware that cannot be checked by the default method, such as some PCIe-to-CAN modules |
| `can_auto_init` | `True` | Whether to initialize the CAN port automatically |
| `dh_is_offset` | `0x01` | Whether the J1-J2 DH parameter has a 2 degree offset; `0` means no offset, `1` means offset applied |
| `start_sdk_joint_limit` | `False` | Whether to enable SDK-side joint limit protection |
| `start_sdk_gripper_limit` | `False` | Whether to enable SDK-side gripper range protection |
| `logger_level` | `LogLevel.WARNING` | SDK log level |
| `log_to_file` | `False` | Whether to write logs to a file |
| `log_file_path` | `None` | Log file path. When `None`, the default SDK log path is used |

## Version Methods

### `GetCurrentInterfaceVersion`

```python
def GetCurrentInterfaceVersion(self)
```

Returns `InterfaceVersion.INTERFACE_V3`.

### `GetCurrentProtocolVersion`

Inherited from V2. In V3 instances, it uses `C_PiperParserV3` and returns `ProtocolVersion.ARM_PROROCOL_V3`.

### `GetCurrentSDKVersion`

Inherited from V2. Returns the current SDK version enum.

## Connection Methods

Connection behavior is inherited from V2.

Common methods:

| Method | Description |
|---|---|
| `CreateCanBus(...)` | Create CAN bus objects manually |
| `ConnectPort(can_init=False, piper_init=True, start_thread=True)` | Connect and start receiving CAN data |
| `DisconnectPort(thread_timeout=0.1)` | Disconnect the CAN port and stop the receive thread |
| `get_connect_status()` | Read whether `ConnectPort` has been called successfully |
| `GetCanBus()` | Get the CAN bus wrapper |
| `GetCanName()` | Get the CAN port name |

## V3 Control Methods

### `MotionCtrl_2`

```python
def MotionCtrl_2(self,
                 ctrl_mode: Literal[0x00, 0x01, 0x03, 0x04, 0x07] = 0x01,
                 move_mode: Literal[0x00, 0x01, 0x02, 0x03, 0x06, 0x05] = 0x01,
                 move_spd_rate_ctrl: int = 50,
                 is_mit_mode: Literal[0x00, 0xAD, 0xFF] = 0x00,
                 residence_time: int = 0,
                 installation_pos: Literal[0x00, 0x01, 0x02, 0x03] = 0x00)
```

Sends robotic arm motion control command 2.

CAN ID: `0x151`.

| Parameter | Description | V3 Values |
|---|---|---|
| `ctrl_mode` | Control mode | `0x00` standby, `0x01` CAN command control, `0x03` Ethernet control, `0x04` Wi-Fi control, `0x07` offline trajectory |
| `move_mode` | MOVE mode | `0x00` MOVE P, `0x01` MOVE J, `0x02` MOVE L, `0x03` MOVE C, `0x05` MOVE CPV, `0x06` MOVE M |
| `move_spd_rate_ctrl` | Movement speed percentage | `0~100` |
| `is_mit_mode` | MIT switch | `0x00` position-speed mode, `0xAD` MIT mode, `0xFF` invalid |
| `residence_time` | Offline trajectory point residence time | `0~255`, unit: s; `255` means trajectory termination |
| `installation_pos` | Installation position | `0x00` invalid, `0x01` horizontal upright, `0x02` left-side mount, `0x03` right-side mount |

V3 difference:

| Mode | V2 Value | V3 Value |
|---|---|---|
| MOVE M | `0x04` | `0x06` |

Example:

```python
from piper_sdk import C_PiperInterface_V3

piper = C_PiperInterface_V3("can0")
piper.ConnectPort()
piper.MotionCtrl_2(ctrl_mode=0x01, move_mode=0x06, move_spd_rate_ctrl=50, is_mit_mode=0xAD)
```

### `ModeCtrl`

```python
def ModeCtrl(ctrl_mode=0x01,
             move_mode=0x01,
             move_spd_rate_ctrl=50,
             is_mit_mode=0x00)
```

Inherited from V2 and internally calls `self.MotionCtrl_2(...)`. On a V3 instance, Python dispatches to V3 `MotionCtrl_2`, so V3 MOVE M should use `move_mode=0x06`.

Example:

```python
piper.ModeCtrl(ctrl_mode=0x01, move_mode=0x06, move_spd_rate_ctrl=50, is_mit_mode=0xAD)
```

### `JointMitCtrl`

```python
def JointMitCtrl(self,
                 motor_num: int,
                 pos_ref: float,
                 vel_ref: float,
                 kp: float,
                 kd: float,
                 t_ref: float)
```

Controls a single joint in MIT mode.

CAN IDs: `0x15A`, `0x15B`, `0x15C`, `0x15D`, `0x15E`, `0x15F`.

| Parameter | Description | V3 Range |
|---|---|---|
| `motor_num` | Motor index | `1~6` |
| `pos_ref` | Desired target position, unit: rad | `[-12.5, 12.5]` |
| `vel_ref` | Desired motor speed | `[-45.0, 45.0]` |
| `kp` | Proportional gain | `[0.0, 500.0]` |
| `kd` | Derivative gain | `[-5.0, 5.0]` |
| `t_ref` | Target torque reference | `[-16.0, 16.0]` |

V3 difference:

| Field | V2 | V3 |
|---|---|---|
| `t_ref` range | `[-8.0, 8.0]` | `[-16.0, 16.0]` |
| `t_ref` encoded width | 8 bit + CRC nibble in byte 7 | 12 bit, no CRC nibble in byte 7 |

Example:

```python
piper.MotionCtrl_2(ctrl_mode=0x01, move_mode=0x06, move_spd_rate_ctrl=50, is_mit_mode=0xAD)
piper.JointMitCtrl(motor_num=1, pos_ref=0.0, vel_ref=0.0, kp=10.0, kd=0.8, t_ref=0.0)
```

## V3 Message Classes

V3 imports most unchanged message classes from V2 and provides V3-specific classes for changed messages.

| Class | Purpose |
|---|---|
| `PiperMessage` from `piper_sdk.piper_msgs.msg_v3` | V3 message aggregate |
| `ArmMsgMotionCtrl_2` | V3 `0x151` motion control command |
| `ArmMsgFeedbackStatus` | V3 `0x2A1` arm status feedback |
| `ArmMsgFeedbackStatusEnum` | V3 feedback enum definitions |
| `ArmMsgJointMitCtrl` | V3 single-joint MIT control message |
| `ArmMsgAllJointMitCtrl` | V3 all-joint MIT control container |

## Inherited V2 APIs

The following commonly used V2 APIs are available in `C_PiperInterface_V3` unless noted otherwise:

| Category | Methods |
|---|---|
| Initialization | `PiperInit`, `EnableFkCal`, `DisableFkCal`, `EnableFilterAbnormalData`, `DisableFilterAbnormalData` |
| Basic control | `EmergencyStop`, `ResetPiper`, `EnableArm`, `DisableArm`, `EnablePiper`, `DisablePiper`, `EndPoseCtrl`, `JointCtrl`, `GripperCtrl` |
| MOVE helpers | `MoveCAxisUpdateCtrl`, `SearchMotorMaxAngleSpdAccLimit`, `SearchAllMotorMaxAngleSpd`, `SearchAllMotorMaxAccLimit` |
| Parameter setting | `MotorAngleLimitMaxSpdSet`, `MotorMaxSpdSet`, `JointConfig`, `JointMaxAccConfig`, `EndSpdAndAccParamSet`, `CrashProtectionConfig`, `GripperTeachingPendantParamConfig` |
| Master/slave | `MasterSlaveConfig`, `ReqMasterArmMoveToHome` |
| Query commands | `SearchPiperFirmwareVersion`, `ClearRespSetInstruction` |
| SDK limits | `GetSDKJointLimitParam`, `SetSDKJointLimitParam`, `GetSDKGripperRangeParam`, `SetSDKGripperRangeParam` |

## Getter Methods

Getter methods are inherited from V2 and return V3 message objects when the underlying message type is overridden by V3.

| Method | Description |
|---|---|
| `GetArmStatus()` | Returns arm status; in V3, `mode_feed` maps MOVE M to `0x06` |
| `GetArmEndPoseMsgs()` | Returns end-effector pose feedback |
| `GetArmJointMsgs()` | Returns joint feedback |
| `GetFK(mode="feedback")` | Returns FK result for feedback or control data |
| `GetArmGripperMsgs()` | Returns gripper feedback |
| `GetArmHighSpdInfoMsgs()` | Returns high-speed motor feedback |
| `GetMotorStates()` | Returns motor states from high-speed feedback |
| `GetArmLowSpdInfoMsgs()` | Returns low-speed motor feedback |
| `GetDriverStates()` | Returns driver states from low-speed feedback |
| `GetArmEnableStatus()` | Returns enable state for joints 1~6 |
| `GetCurrentMotorAngleLimitMaxVel()` | Returns current motor angle/speed limit feedback |
| `GetCurrentEndVelAndAccParam()` | Returns current end velocity/acceleration parameters |
| `GetCrashProtectionLevelFeedback()` | Returns collision protection level feedback |
| `GetGripperTeachingPendantParamFeedback()` | Returns gripper/teaching pendant parameter feedback |
| `GetCurrentMotorMaxAccLimit()` | Returns current motor max acceleration limit feedback |
| `GetArmJointCtrl()` | Returns joint control messages |
| `GetArmGripperCtrl()` | Returns gripper control messages |
| `GetArmCtrlCode151()` | Returns latest `0x151` control message |
| `GetArmModeCtrl()` | Returns current mode control message |
| `GetAllMotorMaxAccLimit()` | Returns all motor max acceleration limits |
| `GetAllMotorAngleLimitMaxSpd()` | Returns all motor angle/speed limits |
| `GetPiperFirmwareVersion()` | Returns firmware version data |
| `GetRespInstruction()` | Returns response instruction feedback |

## Migration From V2

Use these replacements when moving V2 code to V3:

| V2 Usage | V3 Usage |
|---|---|
| `C_PiperInterface_V2(...)` | `C_PiperInterface_V3(...)` |
| `move_mode=0x04` for MOVE M | `move_mode=0x06` for MOVE M |
| `t_ref` in `[-8.0, 8.0]` for MIT | `t_ref` in `[-16.0, 16.0]` for MIT |
| `ArmMsgFeedbackStatusEnum.ModeFeed.MOVE_M == 0x04` | `ArmMsgFeedbackStatusEnum.ModeFeed.MOVE_M == 0x06` |

Minimal V3 example:

```python
from piper_sdk import C_PiperInterface_V3

piper = C_PiperInterface_V3("can0")
piper.ConnectPort()
piper.EnableArm(7)
piper.MotionCtrl_2(ctrl_mode=0x01, move_mode=0x01, move_spd_rate_ctrl=50)
piper.JointCtrl(0, 0, 0, 0, 0, 0)
```
