# Piper SDK

[CN](README.MD)

![ubuntu](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)

Test:

| PYTHON                                                       | STATE                                               |
| ------------------------------------------------------------ | --------------------------------------------------- |
| ![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg) | ![Pass](https://img.shields.io/badge/Pass-blue.svg) |

|Description |doc|
|---|---|
|Detailed description of the interface function.|[Interface README](./asserts/INTERFACE_V1(EN).MD)|
|Description of the protocol parsing section.|[Protocol README](./asserts/PROTOCOL_V1(EN).MD)|
|Description of the message section.|[Msgs README](./asserts/MSGS(EN).MD)|
|Piper DEMO|[DMEO](./asserts/SDK_DEMO(EN).MD)|

## Installation Instructions

### Install dependencies

```shell
pip3 install python-can
```

```shell
pip3 install piper_sdk
```

View piper_sdk Details, Such as Installation Path, Version, etc.

```shell
pip3 show piper_sdk
```

To uninstall

```shell
pip3 uninstall piper_sdk
```

### Install can tools

```shell
sudo apt update && sudo apt install can-utils ethtool
```

These two tools are used to configure the CAN module.

If you encounter the error `ip: command not found` while running the bash script, please install the `ip` command by running `sudo apt-get install iproute2`.

## Quick Start

### Enable CAN module

First, you need to set the shell script parameters.

#### Single Robotic Arm

##### PC with only one USB-to-CAN module inserted

- **Use the `can_activate.sh` script here**

Simply execute the script.

```bash
bash can_activate.sh can0 1000000
```

##### PC with Multiple USB-to-CAN Modules Inserted

- **Use the `can_activate.sh` script here**

Disconnect all CAN modules.

Only connect the CAN module linked to the robotic arm to the PC, then run the script.

```shell
sudo ethtool -i can0 | grep bus
```

and record the value of `bus-info`, for example, `1-2:1.0`.

**Note: The first inserted CAN module usually defaults to `can0`. If you do not find the CAN interface, you can use `bash find_all_can_port.sh` to check the CAN names corresponding to the USB addresses.**

Assuming the recorded `bus-info` value from the above operation is `1-2:1.0`, then run the command to check if the CAN device has been successfully activated.

```bash
bash can_activate.sh can_piper 1000000 "1-2:1.0"
```

**Note: This means that the CAN device connected to the USB port with hardware encoding `1-2:1.0` has been renamed to `can_piper`, set to a baud rate of 1,000,000, and activated.**

Then, run `ifconfig` to check if `can_piper` is listed. If it appears, the CAN module has been successfully configured.

#### Two Pairs of Robotic Arms (Four Arms)

For four robotic arms, which means two pairs of master-slave robotic arms:

- **Use the `can_config.sh`**
  
In the `can_config.sh` , the `EXPECTED_CAN_COUNT` parameter is usually set to `2`, as four robotic arms use two CAN modules.

Then, insert one of the two CAN modules (usually the one connected to the left arm) into the PC alone, and execute the script.

```shell
sudo ethtool -i can0 | grep bus
```

and record the `bus-info` value, for example, `1-2:1.0`.

Next, insert the second CAN module, ensuring that it is connected to a different USB port with the one used previously, and then run:

```shell
sudo ethtool -i can1 | grep bus
```

**Note: Generally, the first inserted CAN module defaults to `can0`, and the second one to `can1`. If the CAN interfaces are not found, use `bash find_all_can_port.sh` to check the CAN names corresponding to the USB addresses.**

Assuming the recorded `bus-info` values from the above operations are `1-2:1.0` and `1-4:1.0`, then replace the parameters inside the double quotes in `USB_PORTS["1-9:1.0"]="can_left:1000000"` with `1-2:1.0`.

Similarly, update the other one.

`USB_PORTS["1-5:1.0"]="can_right:1000000"` -> `USB_PORTS["1-4:1.0"]="can_right:1000000"`

**Note: This means that the CAN device connected to the USB port with hardware encoding `1-2:1.0` is renamed to `can_left`, set to a baud rate of 1,000,000, and activated.**

Then, run `bash can_config.sh` and check the terminal output to see if the activation was successful.

Afterward, run `ifconfig` to verify if `can_left` and `can_right` are listed. If they appear, the CAN modules have been successfully configured.

## Read robotic arm information

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
# 读取机械臂消息并打印,需要先安装piper_sdk
from typing import (
    Optional,
)
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    while True:
        import time
        # a.SearchMotorMaxAngleSpdAccLimit(1, 1)
        # a.ArmParamEnquiryAndConfig(1,0,2,0,3)
        # a.GripperCtrl(50000,1500,0x01)
        print(piper.GetArmJointMsgs())
        print(piper.GetArmGripperMsgs())
        time.sleep(0.005)
        pass
```

## arm reset

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行 you need to pip3 install piper_sdk and then you can run demo
# 设置机械臂重置，需要在mit或者示教模式切换为位置速度控制模式时执行 Arm reset. Need to be executed when MIT or teaching mode is switched to position speed control mode

from typing import (
    Optional,
)
import time
from piper_sdk import *

# 测试代码
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    piper.MotionCtrl_1(0x02,0,0)#恢复 recover
    piper.MotionCtrl_2(0, 0, 0, 0x00)#位置速度模式 postion&velocity mode
```

## Control the robotic arm movement

Note that if the robot arm has entered the teaching mode or MIT mode, a reset is required to switch the robot arm to the position speed mode.

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
# 注意demo无法直接运行，需要pip安装sdk后才能运行
from typing import (
    Optional,
)
import time
from piper_sdk import *

def enable_fun(piper:C_PiperInterface):
    '''
    使能机械臂并检测使能状态,尝试5s,如果使能超时则退出程序
    '''
    enable_flag = False
    # 设置超时时间（秒）
    timeout = 5
    # 记录进入循环前的时间
    start_time = time.time()
    elapsed_time_flag = False
    while not (enable_flag):
        elapsed_time = time.time() - start_time
        print("--------------------")
        enable_flag = piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_enable_status and \
            piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_enable_status
        print("使能状态:",enable_flag)
        piper.EnableArm(7)
        piper.GripperCtrl(0,1000,0x01, 0)
        print("--------------------")
        # 检查是否超过超时时间
        if elapsed_time > timeout:
            print("Timeout....")
            elapsed_time_flag = True
            enable_flag = True
            break
        time.sleep(1)
        pass
    if(elapsed_time_flag):
        print("The program automatically enables timeout, exit the program")
        exit(0)

if __name__ == "__main__":
    piper = C_PiperInterface("can0")
    piper.ConnectPort()
    piper.EnableArm(7)
    enable_fun(piper=piper)
    # piper.DisableArm(7)
    piper.GripperCtrl(0,1000,0x01, 0)
    factor = 57324.840764 #1000*180/3.14
    position = [0,0,0,0,0,0,0]
    count = 0
    while True:
        print(piper.GetArmStatus())
        import time
        count  = count + 1
        # print(count)
        if(count == 0):
            print("1-----------")
            position = [0,0,0,0,0,0,0]
        elif(count == 500):
            print("2-----------")
            position = [0.2,0.2,-0.2,0.3,-0.2,0.5,0.08]
        elif(count == 1000):
            print("1-----------")
            position = [0,0,0,0,0,0,0]
            count = 0
        
        joint_0 = round(position[0]*factor)
        joint_1 = round(position[1]*factor)
        joint_2 = round(position[2]*factor)
        joint_3 = round(position[3]*factor)
        joint_4 = round(position[4]*factor)
        joint_5 = round(position[5]*factor)
        joint_6 = round(position[6]*1000*1000)
        # piper.MotionCtrl_1()
        piper.MotionCtrl_2(0x01, 0x01, 50, 0x00)
        piper.JointCtrl(joint_0, joint_1, joint_2, joint_3, joint_4, joint_5)
        piper.GripperCtrl(abs(joint_6), 1000, 0x01, 0)
        piper.MotionCtrl_2(0x01, 0x01, 50, 0x00)
        time.sleep(0.005)
        pass
```

## Notes

- You need to activate the CAN device and set the correct baud rate before you can read messages from or control the robotic arm.
- The `C_PiperInterface` class can be instantiated with the active CAN route name, which can be obtained using `ifconfig`.

- Sometimes, when executing a CAN send operation, the terminal may display `Message NOT sent`. This indicates that the CAN module has not successfully connected to the device. First, check the connection between the module and the robotic arm. Then, power off and up the robotic arm, and try sending the message once more.
