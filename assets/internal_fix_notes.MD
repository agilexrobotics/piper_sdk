# Internal Fix Notes / 内部修复记录

## V3 Interface Singleton Reinitialization Guard / V3 接口单例重复初始化保护

Date / 日期: 2026-08-10

Scope / 范围: `piper_sdk/interface/piper_interface_v3.py`

### Problem / 问题

`C_PiperInterface_V3` 继承了 `C_PiperInterface_V2` 的单例行为。对于同一个 `can_name`，重复构造会返回同一个 Python 对象。

`C_PiperInterface_V3` inherits the singleton behavior from `C_PiperInterface_V2`. For the same `can_name`, repeated construction returns the same Python object.

`C_PiperInterface_V2.__init__()` 已经有初始化保护：

`C_PiperInterface_V2.__init__()` already has an initialization guard:

```python
if getattr(self, "_initialized", False):
    return
```

但是原来的 V3 构造函数在调用 `super().__init__()` 之后，会无条件重新初始化 V3 自己的运行时状态：

However, the original V3 constructor called `super().__init__()` and then unconditionally initialized V3-specific runtime state:

```python
self._parser = PiperParser()
self._arm_status_mtx = threading.Lock()
self._arm_status = self.ArmStatus()
self._arm_gripper_msgs_mtx = threading.Lock()
self._arm_gripper_msgs = self.ArmGripper()
self._arm_gripper_ctrl_msgs_mtx = threading.Lock()
self._arm_gripper_ctrl_msgs = self.ArmGripperCtrl()
self._arm_gripper_msgs_v3_mtx = threading.Lock()
self._arm_gripper_msgs_v3 = self.ArmGripper_V3()
self._arm_gripper_ctrl_msgs_v3_mtx = threading.Lock()
self._arm_gripper_ctrl_msgs_v3 = self.ArmGripperCtrl_V3()
self._arm_ik_joint_states_mtx = threading.Lock()
self._arm_ik_joint_states = self.ArmIKJointStates()
self.tx_msg = self.PiperMessage()
self.rx_msg = self.PiperMessage()
```

当同一个 V3 CAN 接口被重复构造时，V2 基类构造函数会正确提前返回，但 V3 构造函数会继续执行，从而替换 V3 的 parser、锁、缓存和消息对象。

When the same V3 CAN interface was constructed more than once, the V2 base constructor correctly returned early, but the V3 constructor continued and replaced the V3 parser, locks, caches, and message objects.

### Trigger Scenario / 触发场景

在同一个进程中，如果多个模块独立请求同一个 CAN 接口，就可能触发该问题：

This can happen in one process when multiple modules independently request the same CAN interface:

```python
piper1 = C_PiperInterface_V3("can0")
piper1.ConnectPort()

# Later, another module, service, monitor, or reconnect path does this:
# 之后，另一个模块、服务、监控逻辑或重连路径又执行：
piper2 = C_PiperInterface_V3("can0")
```

由于该类按 `can_name` 做单例，`piper1 is piper2` 为 true。第二次构造理论上应该是 no-op，但修复前会重置共享对象上的 V3 运行时状态。

Because the class is singleton-per-`can_name`, `piper1 is piper2` is true. The second construction should be a no-op, but before the fix it reset V3 runtime state on the shared object.

### Risk If Unfixed / 不修复的风险

这个问题在服务化、多模块或多线程使用中风险较高，虽然简单 demo 可能不容易暴露。

The issue is high risk for service-style, multi-module, or multi-threaded usage, even though simple demos may not expose it.

可能影响：

Possible effects:

- 缓存的反馈数据可能丢失，包括机械臂状态、V3 夹爪反馈和 IK 关节反馈。
- Cached feedback can be lost, including arm status, V3 gripper feedback, and IK joint feedback.
- `time_stamp` 和 `Hz` 字段可能意外回到默认值。
- `time_stamp` and `Hz` fields can unexpectedly return to default values.
- 接口运行期间，`rx_msg` 和 `tx_msg` 可能被替换。
- `rx_msg` and `tx_msg` can be replaced while the interface is running.
- 锁对象可能被替换，破坏读写线程之间原本预期的同步关系。
- Lock objects can be replaced, breaking the intended synchronization between reader and writer threads.
- V3 IK joint feedback 的 FPS 变量可能被重复注册或重置，具体取决于 `add_variable()` 的行为。
- FPS variables for V3 IK joint feedback can be registered repeatedly or reset, depending on `add_variable()` behavior.

最可能出现的是间歇性、难排查的问题：

The most likely symptoms are intermittent and hard to diagnose:

- 监控模块短暂读到默认反馈或旧反馈。
- A monitor briefly reads default or stale feedback.
- 重连路径清掉了刚接收到的状态。
- A reconnect path clears recently received state.
- Web/API 层重复构造接口对象，干扰已经运行中的控制对象。
- A web/API layer that constructs its own interface object disrupts an already running control object.
- 多线程代码看起来使用了锁，但重复初始化后不再同步到同一个锁对象。
- Multi-threaded code appears to use locks but no longer synchronizes on the same lock object after reinitialization.

### Fix / 修复方式

在 `C_PiperInterface_V3.__init__()` 顶部增加 V3 专用初始化保护：

Add a V3-specific initialization guard at the top of `C_PiperInterface_V3.__init__()`:

```python
if getattr(self, "_v3_initialized", False):
    return
```

只在所有 V3 专属状态完成初始化之后设置该标记：

Set the flag only after all V3-specific state has been initialized:

```python
self._v3_initialized = True
```

这样可以明确拆分生命周期职责：

This keeps the lifecycle responsibilities separate:

- V2 的 `_initialized` 保护基础 CAN/interface 状态。
- V2 `_initialized` protects base CAN/interface state.
- V3 的 `_v3_initialized` 保护 V3 parser、锁、缓存和消息对象。
- V3 `_v3_initialized` protects V3 parser, locks, caches, and message objects.

### Validation / 验证

该修复通过以下方式验证：

The fix was validated by:

- 使用 `py_compile` 编译 `piper_sdk/interface/piper_interface_v3.py`。
- Compiling `piper_sdk/interface/piper_interface_v3.py` with `py_compile`.
- 使用同一个测试 CAN 名称连续构造两次 `C_PiperInterface_V3`。
- Constructing `C_PiperInterface_V3` twice with the same test CAN name.
- 确认两个变量指向同一个对象。
- Confirming both variables point to the same object.
- 确认第二次构造后 `_parser`、V3 锁、`rx_msg` 和已缓存的 V3 状态都没有被替换或清空。
- Confirming `_parser`, V3 locks, `rx_msg`, and cached V3 state were preserved across the second construction.

### Notes / 备注

该修复不改变 CAN 协议行为、parser 行为或公开 API 用法，只是防止重复构造同一个 V3 单例实例时意外重置运行中状态。

This fix does not change CAN protocol behavior, parser behavior, or public API usage. It only prevents accidental state reset when the same V3 singleton instance is constructed repeatedly.
