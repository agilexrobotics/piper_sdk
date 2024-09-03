# Piper 机械臂 SDK使用说明
[EN](README(EN).md)

![ubuntu](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)

Test:

|PYTHON |STATE|
|---|---|
|![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

本SDK用于接收can数据帧，然后处理为自定义数据类型,没有包括数据偏移帧

具体的接口函数的详细说明请看[Interface README](./asserts/INTERFACE.MD)

协议解析部分说明[Protocol README](./asserts/PROTOCOL_V1.MD)

消息部分说明[Msgs README](./asserts/MSGS.MD)

## 安装方法

### 安装依赖

```shell
pip3 install python-can
```

```shell
pip3 install piper_sdk
```

### 安装can工具

```shell
sudo apt update && sudo apt install can-utils ethtool
```

这两个工具用来配置can模块

如果执行bash脚本出现`ip: command not found`

请安装ip指令，一般是`sudo apt-get install iproute2`

## 快速使用

### 使能can模块

首先需要设置好shell脚本参数

#### 单条机械臂

##### pc只插入一个usb转can模块

- **此处使用`can_activate.sh`脚本**

直接执行

```bash
bash can_activate.sh can0 1000000
```

##### pc插入多个usb转can模块

- **此处使用`can_activate.sh`脚本**

拔掉所有can模块

只将连接到机械臂的can模块插入PC，执行

```shell
sudo ethtool -i can0 | grep bus
```

并记录下`bus-info`的数值例如`1-2:1.0`

ps:**一般第一个插入的can模块会默认是can0，如果没有查询到can可以使用`bash find_all_can_port.sh`来查看刚才usb地址对应的can名称**

假设上面的操作记录的`bus-info`数值为`1-2:1.0`

然后执行,查看can设备是否激活成功

```bash
bash can_activate.sh can_piper 1000000 "1-2:1.0"
```

ps:**此处的意思是，1-2:1.0硬件编码的usb端口插入的can设备，名字被重命名为can_piper，波特率为1000000，并激活**

然后执行`ifconfig`查看是否有`can_piper`，如果有则can模块设置成功

#### 两对机械臂(四条)

如果是四条机械臂，也就是两对主从机械臂

- **此处使用`can_config.sh`脚本**

在`can_config.sh`中，`EXPECTED_CAN_COUNT`参数一般设置为`2`，因为四条机械臂使用两个can模块

然后将两个can模块中的其中一个(一般第一个插入左臂所在的模块)单独插入PC，执行

```shell
sudo ethtool -i can0 | grep bus
```

并记录下`bus-info`的数值例如`1-2:1.0`

接着插入下一个can模块，注意不可以与上次can模块插入的usb口相同，然后执行

```shell
sudo ethtool -i can1 | grep bus
```

ps:**一般第一个插入的can模块会默认是can0，第二个为can1，如果没有查询到can可以使用`bash find_all_can_port.sh`来查看刚才usb地址对应的can名称**

假设上面的操作记录的`bus-info`数值分别为`1-2:1.0`、`1-4:1.0`

则将下面的`USB_PORTS["1-9:1.0"]="can_left:1000000"`的中括号内部的双引号内部的参数换为`1-2:1.0`

另一个同理

`USB_PORTS["1-5:1.0"]="can_right:1000000"` -> `USB_PORTS["1-4:1.0"]="can_right:1000000"`

ps:**此处的意思是，1-2:1.0硬件编码的usb端口插入的can设备，名字被重命名为can_left，波特率为1000000，并激活**

然后执行`bash can_config.sh`,查看终端输出是否激活成功

然后执行`ifconfig`查看是不是有`can_left`和`can_right`，如果有则can模块设置成功

## 读取机械臂消息

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 读取机械臂消息并打印,需要先安装piper_sdk
from typing import (
    Optional,
)
from piper_sdk import *

if __name__ == "__main__":
    # 实例化piper接口类
    piper = C_PiperInterface("can0")
    # 开启can设备连接
    piper.ConnectPort()
    while True:
        import time
        # 打印机械臂关节角度和夹爪消息
        print(piper.GetArmJointGripperMsgs())
        time.sleep(0.005)
        pass
```

## 控制机械臂运动

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing import (
    Optional,
)
from piper_sdk import *

if __name__ == "__main__":
    # 实例化piper接口类
    piper = C_PiperInterface("can0")
    # 开启can设备连接
    piper.ConnectPort()
    # 使能机械臂所有电机
    piper.EnableArm(7)
    # 夹爪控制，发送位置0，扭矩1N，控制码为0x01，不设置当前为零点
    piper.GripperCtrl(0,1000,0x01, 0)
    factor = 57324.840764 #1000*180/3.14
    position = [0,0,0,0,0,0,0]
    count = 0
    while True:
        import time
        count  = count + 1
        if(count == 0):
            position = [0,0,0,0,0,0,0]
        elif(count == 500):
            position = [0,0,0,0,0,0,0.005]
        elif(count == 1000):
            count = 0
        joint_0 = round(position[0]*factor)
        joint_1 = round(position[1]*factor)
        joint_2 = round(position[2]*factor)
        joint_3 = round(position[3]*factor)
        joint_4 = round(position[4]*factor)
        joint_5 = round(position[5]*factor)
        joint_6 = round(position[6]*1000*1000)
        piper.MotionCtrl_2(0x01, 0x01, 50)
        piper.JointCtrl(joint_0, joint_1, joint_2, joint_3, joint_4, joint_5)
        piper.GripperCtrl(abs(joint_6), 1000, 0x01, 0)
        piper.MotionCtrl_2(0x01, 0x01, 50)
        time.sleep(0.005)
        pass
```

## 注意事项

- 需要先激活can设备，并且设置正确的波特率，才可以读取机械臂消息或者控制机械臂
- C_PiperInterface 接口类在实例化时可传入激活的can路由名称，这个名称可以通过`ifconfig`得到
- 有时执行can发送，终端反馈`Message NOT sent`，是can模块没有成功连接设备，先检查模块与机械臂的连接状态，然后将机械臂断电后上电，再尝试发送
