# Piper 机械臂 SDK使用说明

[EN](README(EN).MD)

|Ubuntu |STATE|
|---|---|
|![ubuntu18.04](https://img.shields.io/badge/Ubuntu-18.04-orange.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|
|![ubuntu20.04](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|
|![ubuntu22.04](https://img.shields.io/badge/Ubuntu-22.04-orange.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

Test:

|PYTHON |STATE|
|---|---|
|![python3.6](https://img.shields.io/badge/Python-3.6-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|
|![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|
|![python3.10](https://img.shields.io/badge/Python-3.10-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

本SDK用于接收can数据帧，然后处理为自定义数据类型，没有包括数据偏移帧

|说明 |文档|
|---|---|
|接口函数的详细说明|[Interface_V1 README](./asserts/V1/INTERFACE_V1.MD) <br> [Interface_V2 README](./asserts/V2/INTERFACE_V2.MD)|
|协议解析部分说明|[Protocol_V1 README](./asserts/V1/PROTOCOL_V1.MD) <br> [Protocol_V2 README](./asserts/V2/PROTOCOL_V2.MD)|
|消息部分说明|[Msgs_V1 README](./asserts/V1/MSGS_V1.MD) <br> [Msgs_V2 README](./asserts/V2/MSGS_V2.MD)|
|机械臂DEMO列举|[DMEO](./asserts/SDK_DEMO.MD)|
|机械臂DEMO|[`piper_sdk/demo/V1`](./demo/V1/README.MD) <br> [`piper_sdk/demo/V2`](./demo/V2/README.MD)|
|双臂的主从配置和读取数据|[double_piper](./asserts/double_piper.MD)|
|使用pyQT5的开源UI|[Piper_sdk_ui](<https://github.com/agilexrobotics/Piper_sdk_ui.git>)|
|Q&A|[Q&A](./asserts/Q&A.MD)|

## 1 软件安装方法

### 1.1 安装依赖

注: python-can版本应高于3.3.4

```shell
pip3 install python-can
```

```shell
pip3 install piper_sdk
```

查看`piper_sdk`细节，比如安装路径，版本等信息

```shell
pip3 show piper_sdk
```

0.0.x 为机械臂V1.5-2固件版本前的sdk支持

若要卸载

```shell
pip3 uninstall piper_sdk
```

### 1.2 安装can工具

```shell
sudo apt update && sudo apt install can-utils ethtool
```

这两个工具用于配置 CAN 模块

如果执行bash脚本出现`ip: command not found`，请安装ip指令，一般是`sudo apt-get install iproute2`

## 2 快速使用

### 2.1 使能can模块

#### 2.1.1 激活单个can模块, **此处使用`can_activate.sh`脚本**

##### 1) pc只插入一个usb转can模块

直接执行

```bash
bash can_activate.sh can0 1000000
```

##### 2) pc插入多个usb转can模块， 但每次只激活一个can模块

注： 此处用于同时使用机械臂和底盘的的情况

(1) 查看can模块插在usb端口的硬件地址。拔掉所有can模块，只将连接到机械臂的can模块插入PC，执行

```shell
sudo ethtool -i can0 | grep bus
```

并记录下`bus-info`的数值，例如`1-2:1.0`

注：**一般第一个插入的can模块会默认是can0，如果没有查询到can可以使用`bash find_all_can_port.sh`来查看刚才usb地址对应的can名称**

(2) 激活can设备。假设上面的操作记录的`bus-info`数值为`1-2:1.0`，执行：

```bash
bash can_activate.sh can_piper 1000000 "1-2:1.0"
```

注：**1-2:1.0硬件编码的usb端口插入的can设备，名字被重命名为can_piper，波特率为1000000，并激活**

(3) 检查是否激活成功

执行`ifconfig`查看是否有`can_piper`，如果有则can模块设置成功

#### 2.1.2 同时激活多个can模块，**此处使用`can_config.sh`脚本**

##### 1) 逐个拔插can模块并一一记录每个模块对应的usb口硬件地址

在`can_config.sh`中，`EXPECTED_CAN_COUNT`参数为想要激活的can模块数量，现在假设为2

(1) 然后can模块中的其中一个单独插入PC，执行

```shell
sudo ethtool -i can0 | grep bus
```

并记录下`bus-info`的数值例如`1-2:1.0`

(2) 接着插入下一个can模块，注意**不可以**与上次can模块插入的usb口相同，然后执行

```shell
sudo ethtool -i can1 | grep bus
```

注：**一般第一个插入的can模块会默认是can0，第二个为can1，如果没有查询到can可以使用`bash find_all_can_port.sh`来查看刚才usb地址对应的can名称**

##### 2) 预定义USB 端口、目标接口名称及其比特率

假设上面的操作记录的`bus-info`数值分别为`1-2:1.0`、`1-4:1.0`，则将下面的`USB_PORTS["1-9:1.0"]="can_left:1000000"`的中括号内部的双引号内部的参数换为`1-2:1.0`和`1-4:1.0`.

最终结果为：

`USB_PORTS["1-2:1.0"]="can_left:1000000"`

`USB_PORTS["1-4:1.0"]="can_right:1000000"`

注：**1-2:1.0硬件编码的usb端口插入的can设备，名字被重命名为can_left，波特率为1000000，并激活**

##### 3) 看终端输出是否激活成功

执行`bash can_config.sh`

##### 4) 查看can是否设置成功

执行`ifconfig`查看是不是有`can_left`和`can_right`

## 注意事项

- 需要先激活can设备，并且设置正确的波特率，才可以读取机械臂消息或者控制机械臂
- C_PiperInterface 接口类在实例化时可传入激活的can路由名称，这个名称可以通过`ifconfig`得到
- 有时执行can发送，终端反馈`Message NOT sent`，是can模块没有成功连接设备，先检查模块与机械臂的连接状态，然后将机械臂断电后上电，再尝试发送
- sdk的interface在创建实例后会检测是否激活自带的can模块，如果是其它can设备，可以将第二个形参设定为False，如：`piper = C_PiperInterface_V2("can0",False)`
- **机械臂的mit协议控制单关节电机为高级功能,使用时需注意,此协议的使用不当会导致机械臂损坏！！！**

## 联系我们

您可以在github上提issue

也可以加入discord<https://discord.gg/wrKYTxwDBd>
