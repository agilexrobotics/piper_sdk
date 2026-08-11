# Next Update TODO / 下个版本更新待办

This document records known follow-up items for future releases. Keep the list updated as issues are fixed or new tasks are added.

本文档用于记录后续版本需要处理的已知事项。问题修复后请同步更新状态，后续新增任务也可以继续追加到列表中。

## Status Legend / 状态说明

- `[ ]` Todo / 未完成
- `[~]` Accepted for current release / 当前版本接受该风险，后续处理
- `[x]` Done / 已完成

## TODO List / 待办列表

1. `[~]` Fix V3 MIT low-level message default encoding / 修复 V3 MIT 底层消息默认值编码问题

   Scope / 范围:
   `piper_sdk/piper_msgs/msg_v3/transmit/arm_joint_mit_ctrl.py`
   `piper_sdk/protocol/protocol_v3/piper_protocol_v3.py`

   Problem / 问题:
   `ArmMsgJointMitCtrl_V3` currently uses physical-style default values, for example `kd=0.8`. However, the V3 protocol encoder directly performs bit-shift operations on these fields. If a low-level caller directly encodes a default `ArmMsgJointMitCtrl_V3`, it can raise:

   ```text
   TypeError: unsupported operand type(s) for >>: 'float' and 'int'
   ```

   当前高层接口 `C_PiperInterface_V3.JointMitCtrl()` 会先把物理量转换为协议整数，再进入编码流程，所以正常高层调用路径暂时不会触发该问题。但底层 message/protocol API 不够可靠，后续需要统一默认值语义或在 encoder 中增加明确转换/校验。

   Expected follow-up / 后续建议:
   - Decide whether `ArmMsgJointMitCtrl_V3` should store protocol-packed integers or physical values.
   - Add validation or conversion before bit operations in the encoder.
   - Add regression tests for direct low-level V3 MIT message encoding.

2. `[~]` Split message imports from top-level `piper_sdk` / 分离顶层 `piper_sdk` 中的 msg 导入

   Scope / 范围:
   `piper_sdk/__init__.py`
   `piper_sdk/piper_msgs/msg_v2/__init__.py`
   `piper_sdk/piper_msgs/msg_v3/__init__.py`

   Problem / 问题:
   The package currently needs to balance backward compatibility and V3 protocol access. Existing users may rely on `import piper_sdk` or `from piper_sdk import *` to access message types. As V3 grows, mixing V2 and V3 message exports at the top level can cause name conflicts, hidden overrides, or unclear default protocol behavior.

   当前版本优先保证老用户代码尽量少改动，同时提供 V3 alias，例如 `PiperMessage_V3`、`ArmMsgType_V3`、`CanIDPiper_V3`。后续应将 msg 类型导入拆分得更清晰，避免直接通过 `import piper_sdk` 暴露过多协议细节，也避免 V2/V3 同名类型互相覆盖。

   Expected follow-up / 后续建议:
   - Keep V2 default exports only if required for backward compatibility.
   - Provide explicit versioned imports for V2/V3 message types.
   - Document the recommended import style, for example importing from `piper_sdk.piper_msgs.msg_v2` or `piper_sdk.piper_msgs.msg_v3` directly.
   - Add compatibility tests for `import piper_sdk`, `from piper_sdk import *`, and explicit msg imports.

3. `[~]` Drop Python 3.6 support in a future release / 后续版本移除 Python 3.6 支持

   Scope / 范围:
   `setup.py`

   Problem / 问题:
   The current release still keeps `python_requires='>=3.6'` for compatibility. This requires dependency constraints such as the Python-version-specific `typing_extensions` requirement and keeps the package tied to an end-of-life Python version.

   当前版本仍保留 `python_requires='>=3.6'` 以兼容旧环境。这需要维护类似 `typing_extensions` 按 Python 版本区分的依赖约束，也让包继续兼容已经停止维护的 Python 版本。

   Expected follow-up / 后续建议:
   - Decide the new minimum supported Python version.
   - Update `python_requires` in `setup.py` to reject Python 3.6.
   - Update classifiers and dependency constraints to match the new minimum Python version.
   - Document the Python 3.6 support removal in the release notes.
