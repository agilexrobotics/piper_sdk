# Piper SDK

![ubuntu](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)

Test:

| PYTHON                                                       | STATE                                               |
| ------------------------------------------------------------ | --------------------------------------------------- |
| ![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg) | ![Pass](https://img.shields.io/badge/Pass-blue.svg) |

This SDK is used to receive CAN data frames and process them into custom data types. It does not include data offset frames.

For detailed explanations of the specific interface functions, please refer to the [Interface README](./asserts/INTERFACE.MD).

For the protocol parsing section, refer to the [Protocol README](./asserts/PROTOCOL_V1.MD).

For the message section, refer to the [Msgs README](./asserts/MSGS.MD).

## Installation Instructions

### Install dependencies

```shell
pip3 install python-can
```

```shell
pip3 install piper_sdk
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

- **Use the `can_config.sh` **

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
# Read and Print Robotic Arm Messages. You need to install `piper_sdk` first.
from typing import (
    Optional,
)
from piper_sdk import *

if __name__ == "__main__":
    # Instantiate the Piper interface class
    piper = C_PiperInterface("can0")
    # Activate the CAN device connection
    piper.ConnectPort()
    while True:
        import time
        # Print the robotic arm joint angles and gripper messages
        print(piper.GetArmJointGripperMsgs())
        time.sleep(0.005)
        pass
```

## Control the robotic arm movement

```python
#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing import (
    Optional,
)
from piper_sdk import *

if __name__ == "__main__":
    # Instantiate the Piper interface class
    piper = C_PiperInterface("can0")
    # Activate the CAN connection
    piper.ConnectPort()
    # Enable all motors of the robotic arm
    piper.EnableArm(7)
    # Gripper control: Send position 0, torque 1N, control code 0x01, and do not set the current as the zero point
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

## Notes

- You need to activate the CAN device and set the correct baud rate before you can read messages from or control the robotic arm.
- The `C_PiperInterface` class can be instantiated with the active CAN route name, which can be obtained using `ifconfig`.

- 有时执行can发送，终端反馈`Message NOT sent`，是can模块没有成功连接设备，先检查模块与机械臂的连接状态，然后将机械臂断电后上电，再尝试发送