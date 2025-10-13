# Piper 机械臂 SDK使用说明

[EN](README.MD)

|![ubuntu18.04](https://img.shields.io/badge/Ubuntu-18.04-orange.svg)|![ubuntu20.04](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)|![ubuntu22.04](https://img.shields.io/badge/Ubuntu-22.04-orange.svg)|
|---|---|---|
|![Pass](https://img.shields.io/badge/Pass-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

Test:

|![python3.6](https://img.shields.io/badge/Python-3.6-blue.svg)|![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg)|![python3.10](https://img.shields.io/badge/Python-3.10-blue.svg)|
|---|---|---|
|![Pass](https://img.shields.io/badge/Pass-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

本SDK用于接收can数据帧，然后处理为自定义数据类型，没有包括数据偏移帧

|说明 |文档|
|---|---|
|接口函数的详细说明|[Interface_V2 README](./asserts/V2/INTERFACE_V2.MD)|
|机械臂DEMO|[`piper_sdk/demo/V2`](./piper_sdk/demo/V2/README.MD)|
|双臂的主从配置和读取数据|[double_piper](./asserts/double_piper.MD)|
|使用pyQT5的开源UI|[Piper_sdk_ui](<https://github.com/agilexrobotics/Piper_sdk_ui.git>)|
|CHANGELOG|[CHANGELOG](./CHANGELOG.MD)|
|Q&A|[Q&A](./asserts/Q&A.MD)|

<details open>
  <summary><h2 style="display:inline">1 软件安装方法</h2></summary>
  <div>

### 1.1 安装依赖

注: python-can版本应高于3.3.4

```shell
pip3 install python-can
```

### 1.2 安装 piper_sdk

注意是否在conda环境里

```bash
which pip3
```

这里提供三种方法，任选其一即可

#### 1.2.1 从pypi仓库安装

```shell
pip3 install piper_sdk
```

#### 1.2.2 拉取github仓库后安装

```shell
git clone https://github.com/agilexrobotics/piper_sdk.git
cd piper_sdk
pip3 install .
```

#### 1.2.3 从github的realease里下载whl文件安装

注意下面的X为你要的realease版本

```shell
pip3 install piper_sdk-X.X.X-py3-none-any.whl 
```

### 1.3 查看 piper_sdk 细节

```shell
pip3 show piper_sdk
```

0.0.x 为机械臂V1.5-2固件版本前的sdk支持

### 1.4 卸载 piper_sdk

```shell
pip3 uninstall piper_sdk
```

### 1.5 更新 piper_sdk

这里提供三种方法，任选其一即可

#### 1.5.1 从pypi仓库更新

可以使用`--upgrade`来更新

```shell
pip3 install --upgrade piper_sdk
```

可以先卸载旧版本然后重新安装，注意存储库有可能未同步，这里默认是官方源

```shell
pip3 uninstall piper_sdk
pip3 install piper_sdk
```

#### 1.5.2 从github仓库更新

```shell
git clone https://github.com/agilexrobotics/piper_sdk.git
cd piper_sdk
pip3 install .
```

#### 1.5.3 从github的realease里下载whl文件更新

注意下面的X为你要的realease版本

```shell
pip3 install piper_sdk-X.X.X-py3-none-any.whl 
```

</div>
</details>

<details open>
  <summary><h2 style="display:inline">2 使用can模块</h2></summary>
  <div>

注意此处的can模块仅支持机械臂自带的can模块，不支持其它can模块

安装can工具

```shell
sudo apt update && sudo apt install can-utils ethtool
```

这两个工具用于配置 CAN 模块

如果执行bash脚本出现`ip: command not found`，请安装ip指令，一般是`sudo apt-get install iproute2`

### 2.1 寻找can模块

执行

```bash
bash find_all_can_port.sh
```

输入密码后，如果can模块插入了电脑，并被电脑检测到，输出类似如下：

```bash
Both ethtool and can-utils are installed.
Interface can0 is connected to USB port 3-1.4:1.0
```

如果有多个，输出类似如下：

```bash
Both ethtool and can-utils are installed.
Interface can0 is connected to USB port 3-1.4:1.0
Interface can1 is connected to USB port 3-1.1:1.0
```

有多少个can模块就会有多少行类似`Interface can1 is connected to USB port 3-1.1:1.0`的输出

其中`can1`是系统找到的can模块名字，`3-1.1:1.0`是该can模块所链接的usb端口

如果之前已经激活过can模块并其名为其它名字，这里假设名字为`can_piper`则输出如下

```bash
Both ethtool and can-utils are installed.
Interface can_piper is connected to USB port 3-1.4:1.0
Interface can0 is connected to USB port 3-1.1:1.0
```

如果没有检测到can模块，则只会输出如下：

```bash
Both ethtool and can-utils are installed.
```

### 2.2 激活单个can模块, **此处使用`can_activate.sh`脚本**

激活单个can模块的情况分两种，一种是电脑只链接了一个can模块，一种是多个can模块插入电脑但是只激活其中一个。

#### 2.2.1 pc只插入一个usb转can模块

直接执行

```bash
bash can_activate.sh can0 1000000
```

此处`can0`可以改为任意名字，`1000000`为波特率，不可更改

#### 2.2.2 pc插入多个usb转can模块， 但每次只激活一个can模块

注： 此处用于同时使用机械臂和底盘的的情况

(1) 查看can模块插在usb端口的硬件地址。拔掉所有can模块，只将连接到机械臂的can模块插入PC，执行

```shell
bash find_all_can_port.sh
```

并记录下`USB port`的数值，例如`3-1.4:1.0`

(2) 激活can设备。假设上面的`USB port`数值为`3-1.4:1.0`，执行：

```bash
bash can_activate.sh can_piper 1000000 "3-1.4:1.0"
```

解释：**3-1.4:1.0硬件编码的usb端口插入的can设备，名字被重命名为can_piper，设定波特率为1000000，并激活**

(3) 检查是否激活成功

执行`ifconfig`查看是否有`can_piper`，如果有则can模块设置成功

### 2.3 同时激活多个can模块，**此处使用`can_muti_activate.sh`脚本**

首先确定有多少个官方can模块被插入到电脑，这里假设是2

注：**若当前电脑插入了5个can模块，可以只激活指定的can模块**

#### 2.3.1 记录每个can模块对应的usb口硬件地址

逐个拔插can模块并一一记录每个模块对应的usb口硬件地址

在`can_muti_activate.sh`中，`USB_PORTS`参数中元素的数量为预激活的can模块数量，现假设为2

(1) 然后can模块中的其中一个单独插入PC，执行

```shell
bash find_all_can_port.sh
```

并记录下`USB port`的数值，例如`3-1.4:1.0`

(2) 接着插入下一个can模块，注意**不可以**与上次can模块插入的usb口相同，然后执行

```shell
bash find_all_can_port.sh
```

记录下第二个can模块的`USB port`的数值，例如`3-1.1:1.0`

注：**如果未曾激活过，则第一个插入的can模块会默认是can0，第二个为can1，若激活过，名字为之前激活过的名称**

#### 2.3.2 预定义USB 端口、目标接口名称及其比特率

假设上面的操作记录的`USB port`数值分别为`3-1.4:1.0`、`3-1.1:1.0`，则将下面的`USB_PORTS["1-9:1.0"]="can_left:1000000"`的中括号内部的双引号内部的参数换为`3-1.4:1.0`和`3-1.1:1.0`.

最终结果为：

```bash
USB_PORTS["3-1.4:1.0"]="can_left:1000000"
USB_PORTS["3-1.1:1.0"]="can_right:1000000"
```

解释：**3-1.4:1.0硬件编码的usb端口插入的can设备，名字被重命名为can_left，波特率为1000000，并激活**

#### 2.3.3 激活多个can模块

执行`bash can_muti_activate.sh`

#### 2.3.4 查看多个can模块是否设置成功

执行`ifconfig`查看是不是有`can_left`和`can_right`

</div>
</details>

<details open>
  <summary><h2 style="display:inline">3 简单开始</h2></summary>
  <div>

从一个最简单的读取机械臂关节角开始

```python
import time
# 导入piper_sdk模块
from piper_sdk import *

if __name__ == "__main__":
    # 实例化interface，形参的默认参数如下
    # can_name(str -> default 'can0'): can port name
    # judge_flag(bool -> default True): 创建该实例时是否开启判断can模块，若使用的是非官方模块，请将其设置False
    # can_auto_init(bool): 创建该实例时是否自动进行初始化来打开can bus，如果设置为False，请在ConnectPort参数中将can_init形参设置为True
    # dh_is_offset([0,1] -> default 0x01): 使用的dh参数是新版dh还是旧版dh，S-V1.6-3以前的为旧版，S-V1.6-3固件及以后的为新版，对应fk的计算
    #             0 -> old
    #             1 -> new
    # start_sdk_joint_limit(bool -> default False):是否开启SDK的关节角度限位，会对反馈消息和控制消息都做限制
    # start_sdk_gripper_limit(bool -> default False):是否开启SDK的夹爪位置限位，会对反馈消息和控制消息都做限制
    # logger_level(LogLevel -> default LogLevel.WARNING):设定log的日志等级
    #         参数有如下可选: 
    #               LogLevel.DEBUG
    #               LogLevel.INFO
    #               LogLevel.WARNING
    #               LogLevel.ERROR
    #               LogLevel.CRITICAL
    #               LogLevel.SILENT
    # log_to_file(bool -> default False):是否打开log写入文件功能，True则打开，默认关闭
    # log_file_path(str -> default False):设定log写入文件的路径，默认在sdk路径下的log文件夹
    piper = C_PiperInterface(can_name="can0",
                            judge_flag=False,
                            can_auto_init=True,
                            dh_is_offset=1,
                            start_sdk_joint_limit=False,
                            start_sdk_gripper_limit=False,
                            logger_level=LogLevel.WARNING,
                            log_to_file=False,
                            log_file_path=None)
    # 开启can收发线程
    piper.ConnectPort()
    # 循环打印消息，注意所有的消息第一帧都是默认数值，比如关节角消息第一帧的消息内容默认为0
    while True:
        print(piper.GetArmJointMsgs())
        time.sleep(0.005)# 200hz
```

注意，读取关节反馈需要机械臂处在从臂模式下，如果为主臂模式，机械臂是不会反馈该消息的

您可以使用以下代码切换到从臂

```python
from piper_sdk import *
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    piper.MasterSlaveConfig(0xFC, 0, 0, 0)
```

读取机械臂固件版本

```python
import time
from piper_sdk import *
if __name__ == "__main__":
    piper = C_PiperInterface("can0")
    piper.ConnectPort()
    time.sleep(0.03) # 需要时间去读取固件反馈帧，否则会反馈-0x4AF
    print(piper.GetPiperFirmwareVersion())
```

</div>
</details>

## 注意事项

- 需要先激活can设备，并且设置正确的波特率，才可以读取机械臂消息或者控制机械臂
- C_PiperInterface 接口类在实例化时可传入激活的can路由名称，这个名称可以通过`ifconfig`得到
- 执行can发送，终端反馈`SendCanMessage(SEND_MESSAGE_FAILED (100017))`，是can模块没有成功连接设备，先检查模块与机械臂的连接状态，然后将机械臂断电后上电，再尝试发送
- sdk的interface在创建实例后会检测是否激活自带的can模块，如果是其它can设备，可以将第二个形参设定为False，如：`piper = C_PiperInterface_V2("can0",False)`
- **机械臂的mit协议控制单关节电机为高级功能,使用时需注意,此协议的使用不当会导致机械臂损坏！！！**

## 联系我们

您可以在github上提issue

也可以加入discord<https://discord.gg/wrKYTxwDBd>
