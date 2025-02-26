# 使用双臂摇操作

[EN](double_piper(EN).MD)

## 1 硬件设置流程

- 示意图

![ ](./wire_connection.PNG)

1. 单独将其中一个机械臂设定为主动臂，另一条设定为从动臂(如demo)，然后将两个机械臂下电
2. 将两个机械臂共同连接在一个can模块上，令主从臂的can连接
3. 先将从动臂上电，然后将主动臂上电，稍等几秒，即可进行遥操作
4. 如未成功，请查看can线是否连接正常，尝试重新断电上电

## 2 读取主从臂数据

详见SDK中接口函数文档

[Interface_V1 README](./V1/INTERFACE_V1.MD) <br> [Interface_V2 README](./V2/INTERFACE_V2.MD)

这里只作简要

### 2.1 读取主动臂消息

`GetArmJointMsgs`、`GetArmGripperMsgs`用来获取从动机械臂关节消息和夹爪消息(原始消息)

`GetArmJointCtrl`、`GetArmGripperCtrl`用来获取主动机械臂关节消息和夹爪消息(原始消息)

### 2.2 控制从臂

`MotionCtrl_2`用来设定控制指令模式，以关节模式举例

```python
# 0x01设定can指令控制模式；0x01设定关节控制模式；50设定机械臂运动速度
piper.MotionCtrl_2(0x01, 0x01, 50)
```

`JointCtrl`用来控制六个关节

`GripperCtrl`用来控制夹爪

注意！！！：**控制从臂的时候，需要将主臂和从臂断开，可以将主臂的航插拔掉，再执行控制从臂程序，否则就算执行了程序，由于主臂也一直在发送控制从臂指令，会出现从臂失控现象**
