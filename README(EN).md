# Piper SDK

[中文](README.MD)

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

This SDK is used for receiving CAN data frames and processing them into custom data types, without including data offset frames.

|Description |doc|
|---|---|
|Detailed description of the interface function.|[Interface README](./asserts/INTERFACE(EN).MD)|
|Description of the protocol parsing section.|[Protocol README](./asserts/PROTOCOL_V1(EN).MD)|
|Description of the message section.|[Msgs README](./asserts/MSGS(EN).MD)|
|Piper DEMO list|[DMEO](./asserts/SDK_DEMO(EN).MD)|
|Piper DEMO | [`piper_sdk/demo`](./demo/README.MD) |
| Master-Slave Configuration and Data Reading for Dual Arms | [double_piper](./asserts/double_piper.MD) |
| Open Source UI Using PyQT5 | [Piper_sdk_ui](https://github.com/agilexrobotics/Piper_sdk_ui.git) |
| Q&A | [Q&A](./asserts/Q&A.MD) |

## 1 Installation Instructions

### 1.1 Install dependencies

The python-can version should be higher than 3.3.4.

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

### 1.2 Install can tools

```shell
sudo apt update && sudo apt install can-utils ethtool
```

These two tools are used to configure the CAN module.

If you encounter the error `ip: command not found` while running the bash script, please install the `ip` command by running `sudo apt-get install iproute2`.

## 2 Quick Start

### 2.1 Enable CAN module

#### 2.1.1 Activate a single CAN module, **using the `can_activate.sh` script here**

##### 1) PC with only one USB-to-CAN module inserted

Simply execute the script.

```bash
bash can_activate.sh can0 1000000
```

##### 2) PC is connected to multiple USB-to-CAN modules, but only one CAN module is activated at a time

Note: This is for scenarios where both the robotic arm and the chassis are used simultaneously.

(1) Check the hardware address of the CAN module connected to the USB port.  

Unplug all CAN modules, then insert only the CAN module connected to the robotic arm into the PC and execute.

```shell
sudo ethtool -i can0 | grep bus
```

And record the value of `bus-info`, for example, `1-2:1.0`.

Note: **The CAN device inserted into the USB port with the hardware address `1-2:1.0` is renamed to `can_piper`, with a baud rate of 1000000, and is activated.**

(2) Activate the CAN device

Assuming the `bus-info` value recorded from the previous operation is `1-2:1.0`, execute:

```bash
bash can_activate.sh can_piper 1000000 "1-2:1.0"
```

Note: **This means that the CAN device connected to the USB port with hardware encoding `1-2:1.0` has been renamed to `can_piper`, set to a baud rate of 1,000,000, and activated.**

(3) Check if activation was successful.

Execute `ifconfig` to check if `can_piper` appears. If it does, the CAN module has been successfully configured.

#### 2.1.2 Activate multiple CAN modules simultaneously, **using the `can_config.sh` script here**

##### 1) Unplug and plug each CAN module one by one, and record the hardware address of each module corresponding to the USB port

In the `can_config.sh` script, the `EXPECTED_CAN_COUNT` parameter represents the number of CAN modules you want to activate. For this example, let's assume it is set to 2.

(1) Then, insert one of the CAN modules into the PC alone and execute.

```shell
sudo ethtool -i can0 | grep bus
```

and record the `bus-info` value, for example, `1-2:1.0`.

(2) Next, insert the next CAN module, making sure that it **cannot** be inserted into the same USB port as the previous CAN module, and then execute.

```shell
sudo ethtool -i can1 | grep bus
```

Note: **Generally, the first inserted CAN module defaults to `can0`, and the second one to `can1`. If the CAN interfaces are not found, use `bash find_all_can_port.sh` to check the CAN names corresponding to the USB addresses.**

##### 2) Predefine the USB ports, target interface names, and their bitrates

Assuming the `bus-info` values recorded from the previous operation are `1-2:1.0` and `1-4:1.0`, the `USB_PORTS["1-9:1.0"]="can_left:1000000"` should be updated as follows:

`USB_PORTS["1-2:1.0"]="can_left:1000000"`

`USB_PORTS["1-4:1.0"]="can_right:1000000"`

Note: **The CAN device inserted into the USB port with the hardware address `1-2:1.0` is renamed to `can_left`, with a baud rate of 1000000, and is activated.**

##### 3) Check the terminal output to see if activation was successful

Execute `bash can_config.sh`.

##### 4) Check if the CAN module was successfully configured

Execute `ifconfig` to check if `can_left` and `can_right` are listed. If they appear, it means the CAN modules have been successfully configured.

## Notes

- You need to activate the CAN device and set the correct baud rate before you can read messages from or control the robot arm.
- The `C_PiperInterface` interface class accepts the name of an activated CAN interface as an argument during instantiation. This name can be obtained via `ifconfig`.
- Sometimes when executing a CAN send operation, the terminal might display `Message NOT sent`. This indicates that the CAN module has not successfully connected to the device. First, check the connection between the module and the robot arm, then power cycle the robot arm (turn it off and then on), and try sending again.
- After creating an instance, the SDK interface will check if the built-in CAN module is activated. If you are using another CAN device, you can set the second parameter to `False`, for example: `piper = C_PiperInterface("can0", False)`.

## Contact Us

You can open an issue on GitHub.

You can also join our Discord at <https://discord.gg/wrKYTxwDBd>.
