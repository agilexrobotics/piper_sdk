#!/bin/bash

# Default CAN name, the user can set it via command line argument
DEFAULT_CAN_NAME="${1:-can0}"

# Default bitrate for a single CAN module, the user can set it via command line argument
DEFAULT_BITRATE="${2:-1000000}"

# USB hardware address (optional parameter)
USB_ADDRESS="${3}"
echo "-------------------START-----------------------"
# Check if ethtool is installed
if ! dpkg -l | grep -q "ethtool"; then
    echo "\e[31mError: ethtool not found in the system.\e[0m"
    echo "Please install ethtool using the following command:"
    echo "sudo apt update && sudo apt install ethtool"
    exit 1
fi

# Check if can-utils is installed
if ! dpkg -l | grep -q "can-utils"; then
    echo "\e[31mError: can-utils not found in the system.\e[0m"
    echo "Please install can-utils using the following command:"
    echo "sudo apt update && sudo apt install can-utils"
    exit 1
fi

echo "ethtool and can-utils are both installed."

# Get the current number of CAN modules in the system
CURRENT_CAN_COUNT=$(ip link show type can | grep -c "link/can")

# Check if the current number of CAN modules matches the expected number
if [ "$CURRENT_CAN_COUNT" -ne "1" ]; then
    if [ -z "$USB_ADDRESS" ]; then
        # Iterate over all CAN interfaces
        for iface in $(ip -br link show type can | awk '{print $1}'); do
            # Use ethtool to get bus-info
            BUS_INFO=$(sudo ethtool -i "$iface" | grep "bus-info" | awk '{print $2}')
            
            if [ -z "$BUS_INFO" ]; then
                echo "Error: Cannot get bus-info information for interface $iface."
                continue
            fi
            
            echo "Interface $iface is plugged into USB port $BUS_INFO"
        done
        echo -e " \e[31mError: The number of CAN modules detected by the system ($CURRENT_CAN_COUNT) does not match the expected number (1).\e[0m"
        echo -e " \e[31mPlease add the USB hardware address parameter, e.g.: \e[0m"
        echo -e " bash can_activate.sh can0 1000000 1-2:1.0"
        echo "-------------------ERROR-----------------------"
        exit 1
    fi
fi

# Load the gs_usb module
# sudo modprobe gs_usb
# if [ $? -ne 0 ]; then
#     echo "Error: Unable to load gs_usb module."
#     exit 1
# fi

if [ -n "$USB_ADDRESS" ]; then
    echo "Detected USB hardware address parameter: $USB_ADDRESS"
    
    # Use ethtool to find the CAN interface corresponding to the USB hardware address
    INTERFACE_NAME=""
    for iface in $(ip -br link show type can | awk '{print $1}'); do
        BUS_INFO=$(sudo ethtool -i "$iface" | grep "bus-info" | awk '{print $2}')
        if [ "$BUS_INFO" == "$USB_ADDRESS" ]; then
            INTERFACE_NAME="$iface"
            break
        fi
    done
    
    if [ -z "$INTERFACE_NAME" ]; then
        echo "Error: Unable to find CAN interface corresponding to USB hardware address $USB_ADDRESS."
        exit 1
    else
        echo "Found interface $INTERFACE_NAME corresponding to USB hardware address $USB_ADDRESS"
    fi
else
    # Get the unique CAN interface
    INTERFACE_NAME=$(ip -br link show type can | awk '{print $1}')
    
    # Check if the interface name was retrieved
    if [ -z "$INTERFACE_NAME" ]; then
        echo "Error: Unable to detect CAN interface."
        exit 1
    fi
    BUS_INFO=$(sudo ethtool -i "$INTERFACE_NAME" | grep "bus-info" | awk '{print $2}')
    echo "Expected to configure a single CAN module, detected interface $INTERFACE_NAME, corresponding USB address is $BUS_INFO"
fi

# Check if the current interface is already activated
IS_LINK_UP=$(ip link show "$INTERFACE_NAME" | grep -q "UP" && echo "yes" || echo "no")

# Get the current bitrate of the interface
CURRENT_BITRATE=$(ip -details link show "$INTERFACE_NAME" | grep -oP 'bitrate \K\d+')

if [ "$IS_LINK_UP" == "yes" ] && [ "$CURRENT_BITRATE" -eq "$DEFAULT_BITRATE" ]; then
    echo "Interface $INTERFACE_NAME is already up, and the bitrate is $DEFAULT_BITRATE"
    
    # Check if the interface name matches the default name
    if [ "$INTERFACE_NAME" != "$DEFAULT_CAN_NAME" ]; then
        echo "Renaming interface $INTERFACE_NAME to $DEFAULT_CAN_NAME"
        sudo ip link set "$INTERFACE_NAME" down
        sudo ip link set "$INTERFACE_NAME" name "$DEFAULT_CAN_NAME"
        sudo ip link set "$DEFAULT_CAN_NAME" up
        echo "Interface renamed to $DEFAULT_CAN_NAME and reactivated."
    else
        echo "Interface name is already $DEFAULT_CAN_NAME"
    fi
else
    # If the interface is not activated or the bitrate is different, proceed with configuration
    if [ "$IS_LINK_UP" == "yes" ]; then
        echo "Interface $INTERFACE_NAME is up, but the bitrate is $CURRENT_BITRATE, which does not match the expected $DEFAULT_BITRATE."
    else
        echo "Interface $INTERFACE_NAME is not up or bitrate is not set."
    fi
    
    # Set the bitrate and activate the interface
    sudo ip link set "$INTERFACE_NAME" down
    sudo ip link set "$INTERFACE_NAME" type can bitrate $DEFAULT_BITRATE
    sudo ip link set "$INTERFACE_NAME" up
    echo "Interface $INTERFACE_NAME has been reconfigured to bitrate $DEFAULT_BITRATE and activated."
    
    # Rename the interface to the default name
    if [ "$INTERFACE_NAME" != "$DEFAULT_CAN_NAME" ]; then
        echo "Renaming interface $INTERFACE_NAME to $DEFAULT_CAN_NAME"
        sudo ip link set "$INTERFACE_NAME" down
        sudo ip link set "$INTERFACE_NAME" name "$DEFAULT_CAN_NAME"
        sudo ip link set "$DEFAULT_CAN_NAME" up
        echo "Interface renamed to $DEFAULT_CAN_NAME and reactivated."
    fi
fi

echo "-------------------OVER------------------------"
