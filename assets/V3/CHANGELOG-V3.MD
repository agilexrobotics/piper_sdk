# ChangeLog-V3

- **V3 is based on V2 and is intended for firmware/protocol versions that use the updated V3 message definitions.**
- **V3 keeps most V2 CAN IDs and data structures, but changes the MOVE M value and MIT control frame layout.**

## 1 Protocol Compatibility

V3 remains compatible with most V2 feedback, transmit, and parameter messages by reusing the V2 message classes where the protocol is unchanged.

V3 adds dedicated message classes only for fields that changed:

| Area | V2 | V3 |
|---|---|---|
| Motion control 2 `0x151` | `ArmMsgMotionCtrl_2` | `ArmMsgMotionCtrl_2_V3` |
| Arm status feedback `0x2A1` | `ArmMsgFeedbackStatus` | `ArmMsgFeedbackStatus_V3` |
| Gripper feedback `0x2A8` | `ArmMsgFeedBackGripper` | `ArmMsgFeedBackGripper_V3` |
| Gripper control `0x159` | `ArmMsgGripperCtrl` | `ArmMsgGripperCtrl_V3` |
| Joint MIT control `0x15A~0x15F` | `ArmMsgJointMitCtrl` | `ArmMsgJointMitCtrl_V3` |
| Parser | `C_PiperParserV2` | `C_PiperParserV3` |
| Interface | `C_PiperInterface_V2` | `C_PiperInterface_V3` |

## 2 Message Changes

### 2.1 `0x151` Motion Control 2

Byte 1 `move_mode` changes the MOVE M value.

| Value | V2 Meaning | V3 Meaning |
|---|---|---|
| `0x00` | MOVE P | MOVE P |
| `0x01` | MOVE J | MOVE J |
| `0x02` | MOVE L | MOVE L |
| `0x03` | MOVE C | MOVE C |
| `0x04` | MOVE M | Reserved/unsupported by V3 message validation |
| `0x05` | MOVE CPV | MOVE CPV |
| `0x06` | Not used by V2 | MOVE M, based on firmware V1.8-8 and later |

V3 validates `move_mode` through enum values from `ArmMsgMotionCtrl_2_V3.Enums.MotionMode`.

Byte 5 `installation_pos` add the Horizontal Inversion value.

| Value | V2 Meaning | V3 Meaning |
|---|---|---|
| `0x00` | Invalid value | Invalid value |
| `0x01` | Horizontal upright | Horizontal upright |
| `0x02` | Left-side mount | Left-side mount |
| `0x03` | Right-side mount | Right-side mount |
| `0x04` | Invalid value | Horizontal Inversion |

| Byte | Field | Type | V3 Values |
|---|---|---|---|
| 0 | `ctrl_mode` | `uint8` | `0x00`, `0x01`, `0x02`, `0x03`, `0x04`, `0x05`, `0x06`, `0x07`, `0xFF` through enum definitions |
| 1 | `move_mode` | `uint8` | `0x00`, `0x01`, `0x02`, `0x03`, `0x05`, `0x06`, `0xFF` through enum definitions |
| 2 | `move_spd_rate_ctrl` | `uint8` | `0~100` |
| 3 | `mit_mode` | `uint8` | `0x00`, `0xAD`, `0xFF` |
| 4 | `residence_time` | `uint8` | `0~255`, unit: s; `255` means trajectory termination |
| 5 | `installation_pos` | `uint8` | `0x00`, `0x01`, `0x02`, `0x03`, `0x04`, `0xFF` through enum definitions |
| 6 | Reserved | `uint8` | `0x00` |
| 7 | Reserved | `uint8` | `0x00` |

### 2.2 `0x2A1` Arm Status Feedback

Byte 2 `mode_feed` changes MOVE M feedback from `0x04` to `0x06`.

| Value | V3 Mode Feedback |
|---|---|
| `0x00` | MOVE P |
| `0x01` | MOVE J |
| `0x02` | MOVE L |
| `0x03` | MOVE C |
| `0x05` | MOVE CPV |
| `0x06` | MOVE M |
| `0xFF` | UNKNOWN |

`ArmMsgFeedbackStatus_V3` reuses the V2 status layout and overrides the `ModeFeed` enum so V3 feedback can be parsed consistently.

### 2.3 `0x15A~0x15F` Joint MIT Control

V3 changes the MIT control frame by removing the CRC nibble from byte 7 and using a wider torque reference field.

| Byte | Field | Description |
|---|---|---|
| 0 | `pos_ref[15:8]` | High 8 bits of position reference |
| 1 | `pos_ref[7:0]` | Low 8 bits of position reference |
| 2 | `vel_ref[11:4]` | High 8 bits of velocity reference |
| 3 | `vel_ref[3:0]`, `kp[11:8]` | Low 4 bits of velocity reference and high 4 bits of Kp |
| 4 | `kp[7:0]` | Low 8 bits of Kp |
| 5 | `kd[11:4]` | High 8 bits of Kd |
| 6 | `kd[3:0]`, `t_ref[11:8]` | Low 4 bits of Kd and high 4 bits of torque reference |
| 7 | `t_ref[7:0]` | Low 8 bits of torque reference |

V3 interface conversion ranges:

| Parameter | Range | Encoded Width |
|---|---|---|
| `pos_ref` | `[-12.5, 12.5]` | 16 bit |
| `vel_ref` | `[-45.0, 45.0]` | 12 bit |
| `kp` | `[0.0, 500.0]` | 12 bit |
| `kd` | `[-5.0, 5.0]` | 12 bit |
| `t_ref` | `[-16.0, 16.0]` | 12 bit |

## 3 Parser Changes

`C_PiperParserV3` inherits from `C_PiperParserV2` and overrides the transmit encoding for V3 message objects.

The parser reports `ProtocolVersion.ARM_PROROCOL_V3` through `GetParserProtocolVersion()`.

## 4 Interface Changes

V3 adds `C_PiperInterface_V3`, which inherits from `C_PiperInterface_V2` and replaces the parser with `C_PiperParserV3`.

The interface overrides these methods:

| Method | V3 Change |
|---|---|
| `GetCurrentInterfaceVersion()` | Returns `InterfaceVersion.INTERFACE_V3` |
| `MotionCtrl_2(...)` | Uses `ArmMsgMotionCtrl_2_V3`; MOVE M is `0x06` |
| `_JointMitCtrl(...)` | Uses 12-bit `t_ref` and the V3 MIT frame layout |
| `JointMitCtrl(...)` | Documents and applies the V3 torque range `[-16.0, 16.0]` |

All unchanged V2 methods remain available through inheritance.

## 5 Migration Notes

- Use `C_PiperInterface_V3` for V3 firmware/protocol behavior.
- Use `ModeCtrl(..., move_mode=0x06, is_mit_mode=0xAD)` or `MotionCtrl_2(..., move_mode=0x06, is_mit_mode=0xAD)` for V3 MOVE M.
- Do not use V2 MOVE M value `0x04` with V3 message classes.
- If reading arm status in V3, expect MOVE M feedback as `0x06`.
- If using MIT control, V3 accepts `t_ref` in `[-16.0, 16.0]` and encodes it as a 12-bit field.
