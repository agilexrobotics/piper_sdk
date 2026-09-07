# 下个版本更新待办

本文档记录后续版本需要处理的已知事项。问题修复后请同步更新状态，后续新增任务可继续追加到列表中。

## 状态说明

- `[ ]` 未完成
- `[~]` 当前版本接受该风险，后续处理
- `[x]` 已完成

## 待办列表

1. `[~]` 修复 V3 MIT 底层消息默认值编码问题

   范围：
   `piper_sdk/piper_msgs/msg_v3/transmit/arm_joint_mit_ctrl.py`
   `piper_sdk/protocol/protocol_v3/piper_protocol_v3.py`

   问题：
   `ArmMsgJointMitCtrl_V3` 当前使用物理量形式的默认值，例如 `kd=0.8`。但 V3 协议编码器会直接对这些字段进行位移操作，底层调用方直接编码默认 `ArmMsgJointMitCtrl_V3` 时可能触发：

   ```text
   TypeError: unsupported operand type(s) for >>: 'float' and 'int'
   ```

   当前高层接口 `C_PiperInterface_V3.JointMitCtrl()` 会先将物理量转换为协议整数，再进入编码流程，因此正常高层调用路径暂时不会触发该问题。但底层 message/protocol API 不够可靠，后续需要统一默认值语义或在编码器中增加明确转换或校验。

   后续建议：
   - 明确 `ArmMsgJointMitCtrl_V3` 存储协议打包整数还是物理量。
   - 在编码器进行位操作前增加校验或转换。
   - 为直接编码底层 V3 MIT 消息增加回归测试。

2. `[~]` 分离顶层 `piper_sdk` 中的消息导入

   范围：
   `piper_sdk/__init__.py`
   `piper_sdk/piper_msgs/msg_v2/__init__.py`
   `piper_sdk/piper_msgs/msg_v3/__init__.py`

   问题：
   当前包需要兼顾向后兼容和 V3 协议访问。已有用户可能依赖 `import piper_sdk` 或 `from piper_sdk import *` 获取消息类型。随着 V3 功能扩展，在顶层混合导出 V2/V3 消息会导致名称冲突、隐式覆盖或默认协议行为不清晰。

   当前版本优先保证老用户代码尽量少改动，同时提供 V3 别名，例如 `PiperMessage_V3`、`ArmMsgType_V3`、`CanIDPiper_V3`。后续应更清晰地拆分消息类型导入，避免直接通过 `import piper_sdk` 暴露过多协议细节，也避免 V2/V3 同名类型相互覆盖。

   后续建议：
   - 仅在确有兼容性需求时保留 V2 默认导出。
   - 为 V2/V3 消息类型提供显式的版本化导入。
   - 在文档中推荐直接从 `piper_sdk.piper_msgs.msg_v2` 或 `piper_sdk.piper_msgs.msg_v3` 导入。
   - 为 `import piper_sdk`、`from piper_sdk import *` 和显式消息导入增加兼容性测试。

3. `[~]` 后续版本移除 Python 3.6 支持

   范围：
   `setup.py`

   问题：
   当前版本仍保留 `python_requires='>=3.6'` 以兼容旧环境。这需要维护类似 `typing_extensions` 按 Python 版本区分的依赖约束，也让包继续兼容已经停止维护的 Python 版本。

   后续建议：
   - 确定新的最低支持 Python 版本。
   - 更新 `setup.py` 中的 `python_requires`，不再支持 Python 3.6。
   - 同步更新分类器和依赖版本约束。
   - 在发布说明中记录移除 Python 3.6 支持。

4. `[~]` 隔离 V3 MIT 全关节消息默认对象

   范围：
   `piper_sdk/piper_msgs/msg_v3/transmit/arm_joint_mit_ctrl.py`

   问题：
   `ArmMsgAllJointMitCtrl_V3` 在默认参数中构造 `m1` 至 `m6`。Python 在函数定义时只创建一次这些对象，因此不同容器实例可能共享同一个可变关节消息对象。修改一个容器的关节消息可能影响另一个容器实例。

   此处的“容器”指保存 J1 至 J6 六个 MIT 关节消息的 `ArmMsgAllJointMitCtrl_V3` 实例。调用 `assign()` 后，容器的 `motor[1]` 至 `motor[6]` 会引用构造函数传入或默认创建的关节消息对象。由于默认对象在函数定义时只创建一次，多个未显式传入关节消息的容器可能引用同一对象。

   最小复现示例：

   ```python
   first = ArmMsgAllJointMitCtrl_V3()
   second = ArmMsgAllJointMitCtrl_V3()
   first.assign()
   second.assign()

   first.motor[1].kd = 123
   assert second.motor[1].kd == 123
   ```

   可能导致的问题：
   - 多个控制任务、线程或缓存分别创建全关节消息容器时，一个任务修改的关节参数可能污染另一个任务的待发送消息。
   - 复用容器时，上一轮控制遗留的 `pos_ref`、`vel_ref`、`kp`、`kd` 或 `t_ref` 可能意外进入后续控制报文。
   - 问题依赖创建和调用顺序，通常难以稳定复现，可能导致不同实例的日志与实际发送参数不一致，增加机械臂 MIT 控制排障难度。

   为兼容当前构造函数签名，本版本接受该风险且不修改实现。后续应避免在默认参数中创建可变消息对象，防止不同容器实例之间发生状态污染。

   后续建议：
   - 评估 `ArmMsgAllJointMitCtrl_V3` 的实际调用和外部兼容性需求；若未被依赖，后续版本可删除该全关节消息容器及其公开导出，避免维护未使用的聚合消息类型。
   - 将关节消息默认参数改为 `None`，并在构造函数内部为每个关节创建新消息。
   - 保持公开构造函数行为，同时确保每个容器拥有独立的关节消息对象。
   - 增加回归测试，验证一个容器的修改不会影响另一个容器。

5. `[~]` 校验 V3 MIT 位置参考值

   范围：
   `piper_sdk/interface/piper_interface_v3.py`

   问题：
   V3 MIT 当前会限幅 `vel_ref`、`kp`、`kd` 和 `t_ref`，但在转换为 16 位协议值前不会校验或限幅 `pos_ref`。越界的位置参考值可能在编码时被截断。

   为兼容当前调用行为，本版本暂不调整 `pos_ref`。后续需要明确位置越界时应拒绝请求还是限幅，并保持与其他 MIT 参数的行为一致。

   后续建议：
   - 在协议转换前校验 `pos_ref` 为有限数值且位于 `[-12.5, 12.5]`。
   - 明确并记录位置参考值越界时应抛出错误还是限幅。
   - 为 `pos_ref` 的边界与越界场景增加回归测试。
