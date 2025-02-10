# ChangeLog-V1

这里的V1版本代码，是属于0.1.x版本的代码

0.1.x版本代码与0.0.x代码区别较大，前者的V1是在后者基础上更新迭代

下文主要讲解0.1.x-V1版本代码和0.0.x代码的区别

## 1 固件兼容

- **兼容新固件(V1.5-2版本前)协议，协议内容不赘述**

## 2 interface

- **`C_PiperInterface`**

### 2.1 特性

- 增加了类的条件实例化特性，条件为传入interface的`can_name`，如在循环中重复`piper=C_PiperInterface(can_name="can0")`，仅仅只会创建一次实例，之后的实例化会因为识别到已经重复创建了`can_name="can0"`实例而不会重复创建
- 类内增加了帧率计算，可以通过下面的`isOk`函数判断can传输是否正常，反馈值为True则表明数据正常传输，如果为False则说明数据断开
- 增加了正解，通过扩展DH参数来计算每个关节相对base_link的位姿，通过`GetFK`函数获取，反馈link1~link6的位姿，是一个6*6的列表，第-1位为link6的位姿

### 2.2 函数

0.1.x-V1 相比 0.0.x 增加了一些函数，如下：

| 函数   | 类型 |说明                                                         |使用                | 参数                        |反馈       |
| ----- | ---- |------------------------------------------------------------ |-------------------|--------------------------- |--------|
|`GetCanFps`|Getter Method|获取can总线当前实时帧率|obj.GetArmStatus()|None|int|
|`GetFK`|Getter Method|获取机械臂每个关节控制信息和反馈信息的正解,XYZ单位为mm,RXRYRZ单位为度，反馈长度为6的float类型数据列表,代表 1-6 关节相对 base_link 的位姿|obj.GetFK()|mode:Literal["feedback", "control"]="feedback"|self.__link_fk|
|`isOk`|Getter Method|反馈can数据读取线程是否正常|obj.isOk()|None|self.__is_ok|
|`__CanMonitor`|Getter Method|can数据帧率检测|类内使用|None|None|
|`__UpdatePiperFeedbackFK`|Getter Method|更新piper反馈信息正解数据|类内使用|None|None|
|`__UpdatePiperCtrlFK`|Getter Method|更新piper控制信息正解数据|类内使用|None|None|
