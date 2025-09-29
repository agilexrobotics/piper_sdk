# Piper Robot Arm SDK User Manual

[ZH](README(ZH).MD)

|![ubuntu18.04](https://img.shields.io/badge/Ubuntu-18.04-orange.svg)|![ubuntu20.04](https://img.shields.io/badge/Ubuntu-20.04-orange.svg)|![ubuntu22.04](https://img.shields.io/badge/Ubuntu-22.04-orange.svg)|
|---|---|---|
|![Pass](https://img.shields.io/badge/Pass-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

Test:

|![python3.6](https://img.shields.io/badge/Python-3.6-blue.svg)|![python3.8](https://img.shields.io/badge/Python-3.8-blue.svg)|![python3.10](https://img.shields.io/badge/Python-3.10-blue.svg)|
|---|---|---|
|![Pass](https://img.shields.io/badge/Pass-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|![Pass](https://img.shields.io/badge/Pass-blue.svg)|

This SDK is used to receive CAN data frames and process them into custom data types, excluding data offset frames.

|Description | Documentation|
|---|---|
|Detailed description of interface functions|[Interface_V2 README](./asserts/V2/INTERFACE_V2.MD)|
|Robot Arm DEMO|[piper_sdk/demo/V2](./piper_sdk/demo/V2/README.MD)|
|Master-slave configuration and data reading for dual arms|[double_piper](./asserts/double_piper.MD)|
|Open-source UI using pyQT5|[Piper_sdk_ui](<https://github.com/agilexrobotics/Piper_sdk_ui.git>)|
|CHANGELOG|[CHANGELOG](./CHANGELOG.MD)|
|Q&A|[Q&A](./asserts/Q&A.MD)|

<details open>
  <summary><h2 style="display:inline">1 Software Installation Method</h2></summary>
  <div>

### 1.1 Install Dependencies

Note: The python-can version should be above 3.3.4

```shell
pip3 install python-can
```

### 1.2 Install piper_sdk

Note: Check if you are in a conda environment

```bash
which pip3
```

Three methods are provided, choose one.

#### 1.2.1 Install from pypi repository

```shell
pip3 install piper_sdk
```

#### 1.2.2 Clone the github repository and install

```shell
git clone https://github.com/agilexrobotics/piper_sdk.git
cd piper_sdk
pip3 install .
```

#### 1.2.3 Install from GitHub release by downloading the whl file

Note: Replace X with the release version you need

```shell
pip3 install piper_sdk-X.X.X-py3-none-any.whl
```

### 1.3 Check piper_sdk Details

```shell
pip3 show piper_sdk
```

0.0.x supports SDKs for robot arm firmware versions before V1.5-2

### 1.4 Uninstall piper_sdk

```shell
pip3 uninstall piper_sdk
```

### 1.5 Update piper_sdk

Three methods are provided, choose one.

#### 1.5.1 Update from pypi repository

You can use `--upgrade` to update

```shell
pip3 install --upgrade piper_sdk
```

You can uninstall the old version and then reinstall it. Note that the repository may not be synchronized. The default here is the official source

```shell
pip3 uninstall piper_sdk
pip3 install piper_sdk
```

#### 1.5.2 Update from GitHub repository

```shell
git clone https://github.com/agilexrobotics/piper_sdk.git
cd piper_sdk
pip3 install .
```

#### 1.5.3 Update by downloading the whl file from GitHub release

Note: Replace X with the release version you need

```shell
pip3 install piper_sdk-X.X.X-py3-none-any.whl
```

</div>
</details>

<details open>
  <summary><h2 style="display:inline">2 Use CAN Module</h2></summary>
  <div>

Note: The CAN module here only supports the robot arm's built-in CAN module, and does not support other CAN modules.

Install CAN tools

```bash
sudo apt update && sudo apt install can-utils ethtool
```

These two tools are used to configure the CAN module.

If executing the bash script shows `ip: command not found`, install the `ip` command by running `sudo apt-get install iproute2`

### 2.1 Find CAN Modules

Run the following command:

```bash
bash find_all_can_port.sh
```

Enter the password, and if the CAN module is inserted into the computer and detected, it will output something like:

```bash
Both ethtool and can-utils are installed.
Interface can0 is connected to USB port 3-1.4:1.0
```

If there are multiple modules, the output will look like this:

```bash
Both ethtool and can-utils are installed.
Interface can0 is connected to USB port 3-1.4:1.0
Interface can1 is connected to USB port 3-1.1:1.0
```

For each CAN module, there will be a corresponding output like `Interface can1 is connected to USB port 3-1.1:1.0`

Where `can1` is the name of the CAN module detected by the system, and `3-1.1:1.0` is the USB port it is connected to.

If the CAN module has already been activated with a different name, for example `can_piper`, the output will look like:

```bash
Both ethtool and can-utils are installed.
Interface can_piper is connected to USB port 3-1.4:1.0
Interface can0 is connected to USB port 3-1.1:1.0
```

If no CAN module is detected, only the following will be output:

```bash
Both ethtool and can-utils are installed.
```

### 2.2 Activate a Single CAN Module (use can_activate.sh script)

There are two situations for activating a single CAN module: one is when only one CAN module is connected to the PC, and the other is when multiple CAN modules are inserted, but only one is activated.

#### 2.2.1 PC has only one USB-to-CAN module connected

Simply execute:

```bash
bash can_activate.sh can0 1000000
```

Here, `can0` can be replaced with any name, and `1000000` is the baud rate, which cannot be changed.

#### 2.2.2 PC has multiple USB-to-CAN modules connected, but only one module is activated at a time

Note: This case applies when using both the robot arm and the chassis.

(1) Find the USB hardware address of the CAN module. Unplug all CAN modules and plug in only the one connected to the robot arm, then execute:

```shell
bash find_all_can_port.sh
```

Record the USB port value, for example, 3-1.4:1.0.

(2) Activate the CAN device. Assuming the USB port value is 3-1.4:1.0, run:

```bash
bash can_activate.sh can_piper 1000000 "3-1.4:1.0"
```

Explanation: **3-1.4:1.0 is the hardware-encoded USB port, and the CAN device inserted there is renamed as can_piper, with a baud rate of 1000000 and activated.**

(3) Check if activation was successful by running `ifconfig` to see if `can_piper` appears. If it does, the CAN module is configured successfully.

### 2.3 Activate Multiple CAN Modules Simultaneously (use can_muti_activate.sh script)

First, determine how many official CAN modules are plugged into the PC (assumed here as 2).

Note: **If the current computer has 5 CAN modules inserted, you can only activate the specified CAN module**

#### 2.3.1 Record the USB port hardware address of each CAN module

For each CAN module, unplug and reinsert it while recording the corresponding USB port address.

In the `can_muti_activate.sh` file, the `EXPECTED_CAN_COUNT` parameter should be set to the desired number of activated CAN modules (assumed here as 2).

(1) Plug in one CAN module and run:

```shell
bash find_all_can_port.sh
```

Record the `USB port` value, for example, `3-1.4:1.0`

(2) Plug in the next CAN module. Ensure **it is not inserted into the same USB port as the previous one** and run:

```shell
bash find_all_can_port.sh
```

Record the value of the second CAN module's `USB port`, for example `3-1.1:1.0`

Note: **If not previously activated, the first module will default to "can0," and the second will be "can1." If previously activated, the names will be the ones used before.**

#### 2.3.2 Predefine USB ports, target interface names, and their bitrates

Assume the recorded `USB port` values are `3-1.4:1.0` and `3-1.1:1.0`. Replace the values inside the brackets in `USB_PORTS["1-9:1.0"]="can_left:1000000"` with `3-1.4:1.0` and `3-1.1:1.0`.

The final result is:

```shell
USB_PORTS["3-1.4:1.0"]="can_left:1000000"
USB_PORTS["3-1.1:1.0"]="can_right:1000000"
```

Explanation: **3-1.4:1.0 is the hardware-encoded USB port, the CAN device inserted there is renamed to "can_left," with a baud rate of 1000000, and activated.**

#### 2.3.3 Activate multiple CAN modules

Run the script:

```bash
bash can_muti_activate.sh
```

#### 2.3.4 Check if multiple CAN modules were set up successfully

Run `ifconfig` to check if `can_left` and `can_right` are present.

</div>
</details>

<details open>
  <summary><h2 style="display:inline">3 Simple start</h2></summary>
  <div>

Start with the simplest way to read the joint angle of the robot arm

```python
import time
# Import piper_sdk module
from piper_sdk import *

if __name__ == "__main__":
    # Instantiate interface, the default parameters of the parameters are as follows
    #   can_name(str): can port name
    #   judge_flag(bool): Whether to enable the can module when creating this instance. 
    #                     If you use an unofficial module, please set it to False
    #   can_auto_init(bool): Whether to automatically initialize to open the can bus when creating this instance. 
    #                        If set to False, please set the can_init parameter to True in the ConnectPort parameter
    #   dh_is_offset([0,1] -> default 0x01): Whether the dh parameter used is the new version of dh or the old version of dh. 
    #                                       The old version is before S-V1.6-3, and the new version is after S-V1.6-3 firmware
    #           0 -> old
    #           1 -> new
    #   start_sdk_joint_limit(bool -> False): Whether to enable SDK joint angle limit, which will limit both feedback and control messages
    #   start_sdk_gripper_limit(bool -> False): Whether to enable SDK gripper position limit, which will limit both feedback and control messages
    #   logger_level(LogLevel -> default LogLevel.WARNING): Set the log level
    #         The following parameters are optional: 
    #               LogLevel.DEBUG
    #               LogLevel.INFO
    #               LogLevel.WARNING
    #               LogLevel.ERROR
    #               LogLevel.CRITICAL
    #               LogLevel.SILENT
    #   log_to_file(bool -> default False): Whether to enable the log writing function, True to enable, default to disable
    #   log_file_path(str -> default False): Set the path to write the log file, the default is the log folder under the sdk path
    piper = C_PiperInterface(can_name="can0",
                                judge_flag=False,
                                can_auto_init=True,
                                dh_is_offset=1,
                                start_sdk_joint_limit=False,
                                start_sdk_gripper_limit=False,
                                logger_level=LogLevel.WARNING,
                                log_to_file=False,
                                log_file_path=None)
    # Enable can send and receive threads
    piper.ConnectPort()
    # Loop and print messages. Note that the first frame of all messages is the default value. For example, the message content of the first frame of the joint angle message defaults to 0
    while True:
        print(piper.GetArmJointMsgs())
        time.sleep(0.005)# 200hz
```

Note that reading joint feedback requires the robot to be in slave mode. If it is in master mode, the robot will not respond.

You can use the following code to switch to slave mode.

```python
from piper_sdk import *
if __name__ == "__main__":
    piper = C_PiperInterface()
    piper.ConnectPort()
    piper.MasterSlaveConfig(0xFC, 0, 0, 0)
```

Read the robot firmware version

```python
import time
from piper_sdk import *

if __name__ == "__main__":
    piper = C_PiperInterface("can0")
    piper.ConnectPort()
    time.sleep(0.025) # It takes time to read the firmware feedback frame, otherwise -0x4AF will be fed back
    print(piper.GetPiperFirmwareVersion())
```

</div>
</details>

## Notes

- Ensure that CAN devices are activated and set to the correct baud rate before reading robot arm messages or controlling the robot arm.
- The `C_PiperInterface` class can accept the activated CAN interface name during instantiation, which can be obtained from `ifconfig`.
- If a message is not sent with the feedback `SendCanMessage(SEND_MESSAGE_FAILED (100017))` the CAN module might not be successfully connected. Check the connection and power cycle the robot arm before retrying.
- The SDK's interface will check if the built-in CAN module is activated after creating the instance. For other CAN devices, set the second parameter to False, for example: `piper = C_PiperInterface_V2("can0", False)`.
- **The MIT protocol for controlling individual joints is an advanced feature; misuse of this protocol can damage the robot arm!**

## Contact Us

You can raise issues on GitHub or join our Discord community: <https://discord.gg/wrKYTxwDBd>
