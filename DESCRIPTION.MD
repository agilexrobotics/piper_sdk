# Piper SDK

[![GitHub](https://img.shields.io/badge/GitHub-blue.svg)](https://github.com/agilexrobotics/piper_sdk)

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

0.0.x provides SDK support for robotic arm firmware versions prior to V1.5-2.

To uninstall

```shell
pip3 uninstall piper_sdk
```

## Notes

- The CAN device must be activated and the correct baud rate set before reading messages from or controlling the robotic arm.
- The `C_PiperInterface` interface class can accept the activated CAN route name as a parameter when instantiated.
- Sometimes when sending CAN messages, the terminal may show `Message NOT sent`. This indicates that the CAN module is not properly connected to the device. First, check the connection between the module and the robotic arm, then power cycle the robotic arm (turn it off and on) before attempting to send the message again.
- The SDK interface will check if the built-in CAN module is activated after creating an instance. If using another CAN device, you can set the second parameter to `False`, for example: `piper = C_PiperInterface_V2("can0", False)`.
- **The MIT protocol for controlling individual joints of the robotic arm is an advanced feature. Be cautious when using it, as improper use of this protocol may damage the robotic arm!!!**

## Contact Us

You can open an issue on GitHub.

Alternatively, you can join our Discord at <https://discord.gg/wrKYTxwDBd>
