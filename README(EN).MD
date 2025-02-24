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

This SDK is used to receive CAN data frames and then process them into custom data types, without including data offset frames.

|Description |doc|
|---|---|
|Detailed description of the interface function.|[Interface_V1 README](./asserts/V1/INTERFACE_V1.MD) <br> [Interface_V2 README](./asserts/V2/INTERFACE_V2.MD)|
|Description of the protocol parsing section.|[Protocol_V1 README](./asserts/V1/PROTOCOL_V1.MD) <br> [Protocol_V2 README](./asserts/V2/PROTOCOL_V2.MD)|
|Description of the message section.|[Msgs_V1 README](./asserts/V1/MSGS_V1.MD) <br> [Msgs_V2 README](./asserts/V2/MSGS_V2.MD)|
|Piper DEMO|[DMEO](./asserts/SDK_DEMO(EN).MD)|
|Robotic Arm DEMO| [`piper_sdk/demo/V1`](./demo/V1/README.MD) <br> [`piper_sdk/demo/V2`](./demo/V2/README.MD) |
|Master-slave configuration and data reading of dual arms| [double_piper](./asserts/double_piper.MD) |
| Open-source UI using PyQt5 | [Piper_sdk_ui](<https://github.com/agilexrobotics/Piper_sdk_ui.git>) |
|Q&A|[Q&A](./asserts/Q&A.MD)|

## 1 Software Installation Instructions

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

0.0.x provides SDK support for robotic arm firmware versions prior to V1.5-2.

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

- The CAN device must be activated and the correct baud rate set before reading messages from or controlling the robotic arm.
- The `C_PiperInterface` interface class can accept the activated CAN route name as a parameter when instantiated, which can be obtained using `ifconfig`.
- Sometimes when sending CAN messages, the terminal may show `Message NOT sent`. This indicates that the CAN module is not properly connected to the device. First, check the connection between the module and the robotic arm, then power cycle the robotic arm (turn it off and on) before attempting to send the message again.
- The SDK interface will check if the built-in CAN module is activated after creating an instance. If using another CAN device, you can set the second parameter to `False`, for example: `piper = C_PiperInterface_V2("can0", False)`.
- **The MIT protocol for controlling individual joints of the robotic arm is an advanced feature. Be cautious when using it, as improper use of this protocol may damage the robotic arm!!!**

## Contact Us

You can open an issue on GitHub.

Alternatively, you can join our Discord at <https://discord.gg/wrKYTxwDBd>
