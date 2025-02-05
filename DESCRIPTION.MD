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

## Notes

- You need to activate the CAN device and set the correct baud rate before you can read messages from or control the robot arm.
- The `C_PiperInterface` interface class accepts the name of an activated CAN interface as an argument during instantiation.
- Sometimes when executing a CAN send operation, the terminal might display `Message NOT sent`. This indicates that the CAN module has not successfully connected to the device. First, check the connection between the module and the robot arm, then power cycle the robot arm (turn it off and then on), and try sending again.
- After creating an instance, the SDK interface will check if the built-in CAN module is activated. If you are using another CAN device, you can set the second parameter to `False`, for example: `piper = C_PiperInterface("can0", False)`.

## Contact Us

You can open an issue on GitHub.

You can also join our Discord at <https://discord.gg/wrKYTxwDBd>.
