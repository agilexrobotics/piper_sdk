# Agilex CAN Module Configuration Guide

## Install CAN Utilities

```shell
sudo apt update && sudo apt install can-utils ethtool
```

These two utilities are used to configure the CAN module.

If running a bash script results in `ip: command not found`,
please install the `ip` command, usually with:

```shell
sudo apt-get install iproute2
```

## Quick Usage

### Enable CAN Module

First, set up the shell script parameters properly.

#### Single Robotic Arm

##### PC with only one USB-to-CAN module inserted

- **Use the `can_activate.sh` script in this case.**

Simply execute:

```bash
bash can_activate.sh can0 1000000
```

##### PC with multiple USB-to-CAN modules inserted

- **Use the `can_activate.sh` script in this case.**

Unplug all CAN modules.

Insert only the CAN module connected to the robotic arm into the PC, then execute:

```shell
sudo ethtool -i can0 | grep bus
```

Record the `bus-info` value, e.g., `1-2:1.0`.

**Note:** Usually, the first inserted CAN module defaults to `can0`. If no CAN device is found, use `bash find_all_can_port.sh` to check the corresponding CAN name for the USB address.

Assuming the recorded `bus-info` value is `1-2:1.0`, execute the following command to check if the CAN device is successfully activated:

```bash
bash can_activate.sh can_piper 1000000 "1-2:1.0"
```

**Note:** This means that the CAN device inserted into the USB port with hardware encoding `1-2:1.0` is renamed to `can_piper`, set to a baud rate of `1000000`, and activated.

Then, run `ifconfig` to check if `can_piper` is listed. If it appears, the CAN module has been set up successfully.

#### Enabling Multiple CAN Modules Simultaneously

- **Use the `can_config.sh` script in this case.**

In `can_config.sh`, the `EXPECTED_CAN_COUNT` parameter represents the number of CAN modules to be activated. Assume this is set to `2`.

First, insert one CAN module into the PC and execute:

```shell
sudo ethtool -i can0 | grep bus
```

Record the `bus-info` value, e.g., `1-2:1.0`.

Next, insert another CAN module (ensure it is plugged into a different USB port than the previous one), then execute:

```shell
sudo ethtool -i can1 | grep bus
```

**Note:** Typically, the first inserted CAN module will be `can0`, and the second will be `can1`. If no CAN device is found, use `bash find_all_can_port.sh` to check the corresponding CAN name for the USB address.

Assume the recorded `bus-info` values are `1-2:1.0` and `1-4:1.0`.

Modify the script accordingly:

Replace:

```shell
USB_PORTS["1-9:1.0"]="can_left:1000000"
```

with:

```shell
USB_PORTS["1-2:1.0"]="can_left:1000000"
```

Similarly, replace:

```shell
USB_PORTS["1-5:1.0"]="can_right:1000000"
```

with:

```shell
USB_PORTS["1-4:1.0"]="can_right:1000000"
```

**Note:** This means that the CAN device inserted into the USB port with hardware encoding `1-2:1.0` is renamed to `can_left`, set to a baud rate of `1000000`, and activated.

Then, execute:

```bash
bash can_config.sh
```

Check the terminal output to verify if activation was successful.

Finally, run `ifconfig` to check if `can_left` and `can_right` appear. If they do, the CAN modules have been successfully set up.
