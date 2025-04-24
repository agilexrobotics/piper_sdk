#!/bin/bash
declare -A USB_PORTS 

# USB_PORTS["3-1.3:1.0"]="can_arm:1000000"
USB_PORTS["3-1.1:1.0"]="can_arm2:1000000"
USB_PORTS["3-1.2:1.0"]="can_arm2:1000000"
# USB_PORTS["3-1.5:1.0"]="can_arm1:1000000"

# Whether to ignore CAN quantity check (default false)
IGNORE_CHECK=false

# Parsing parameters
for arg in "$@"; do
    if [ "$arg" == "--ignore" ]; then
        IGNORE_CHECK=true
    fi
done

# Step 1: 打印 USB_PORTS 映射，同时检测是否存在重复目标名
echo "🔧 Checking USB_PORTS configuration:"
declare -A TARGET_NAMES_COUNT
LINE_NUM=0
HAS_DUPLICATE=false

for k in "${!USB_PORTS[@]}"; do
    LINE_NUM=$((LINE_NUM + 1))
    IFS=':' read -r name bitrate <<< "${USB_PORTS[$k]}"
    
    # 检查是否重复
    if [[ -n "${TARGET_NAMES_COUNT[$name]}" ]]; then
        echo "→ [$LINE_NUM] \"$k\"=\"${USB_PORTS[$k]}\"  ❌ Duplicate target CAN name: '$name'"
        HAS_DUPLICATE=true
    else
        echo "  [$LINE_NUM] \"$k\"=\"${USB_PORTS[$k]}\""
        TARGET_NAMES_COUNT["$name"]=1
    fi
done

if $HAS_DUPLICATE; then
    echo "❌ [ERROR]: Found duplicate target CAN interface name(s) above. Please resolve before proceeding."
    exit 1
fi

PREDEFINED_COUNT=${#USB_PORTS[@]}
CURRENT_CAN_COUNT=$(ip link show type can | grep -c "link/can")

if [ "$IGNORE_CHECK" = false ] && [ "$CURRENT_CAN_COUNT" -ne "$PREDEFINED_COUNT" ]; then
    echo "[WARN]: The detected number of CAN modules ($CURRENT_CAN_COUNT) does not match the expected number ($PREDEFINED_COUNT)."
    read -p "Do you want to continue? (y/N): " user_input
    case "$user_input" in
        [yY]|[yY][eE][sS])
            echo "Continue execution..."
            ;;
        *)
            echo "Exited."
            exit 1
            ;;
    esac
else
    echo "CAN quantity check ignored or matched, continuing..."
fi

# Load the gs_usb module
sudo modprobe gs_usb
if [ $? -ne 0 ]; then
    echo "[ERROR]: Unable to load gs_usb module."
    exit 1
fi

SUCCESS_COUNT=0  # Number of CAN interfaces successfully processed
FAILED_COUNT=0   # Expected number of interfaces that failed or were not processed

# Copy a list of USB_PORTS keys and mark each one for success
declare -A USB_PORT_STATUS
for k in "${!USB_PORTS[@]}"; do
    USB_PORT_STATUS["$k"]="pending"
done
# Handle multiple CAN modules
# Iterate over all CAN interfaces
SYS_INTERFACE=$(ip -br link show type can | awk '{print $1}')

echo -e "\n🔍 [INFO]: The following CAN interfaces were detected in the system:"
for iface in $SYS_INTERFACE; do
    echo "  - $iface"
done

echo -e "\n⚠️  [HINT]: Please make sure none of the above interface names conflict with the predefined names in your USB_PORTS config."

for iface in $SYS_INTERFACE; do
    # Get bus-info using ethtool
    echo "--------------------------- $iface ------------------------------"
    BUS_INFO=$(sudo ethtool -i "$iface" | grep "bus-info" | awk '{print $2}')
    
    if [ -z "$BUS_INFO" ];then
        echo "[ERROR]: Unable to get bus-info information for interface '$iface'."
        continue
    fi
    
    echo "[INFO]: System interface '$iface' is plugged into USB port '$BUS_INFO'"
    # Check if bus-info is in the list of predefined USB ports
    if [ -n "${USB_PORTS[$BUS_INFO]}" ];then
        IFS=':' read -r TARGET_NAME TARGET_BITRATE <<< "${USB_PORTS[$BUS_INFO]}"
        
        # Check if the current interface is activated
        IS_LINK_UP=$(ip link show "$iface" | grep -q "UP" && echo "yes" || echo "no")

        # Get the bit rate of the current interface
        CURRENT_BITRATE=$(ip -details link show "$iface" | grep -oP 'bitrate \K\d+')
        
        if [ "$IS_LINK_UP" = "yes" ] && [ "$CURRENT_BITRATE" -eq "$TARGET_BITRATE" ]; then
            echo "[INFO]: Interface '$iface' is activated and bitrate is $TARGET_BITRATE"
            
            # Check if the interface name matches the target name
            if [ "$iface" != "$TARGET_NAME" ]; then
                echo "[INFO]: Rename interface '$iface' to '$TARGET_NAME'"
                sudo ip link set "$iface" down
                sudo ip link set "$iface" name "$TARGET_NAME"
                sudo ip link set "$TARGET_NAME" up
                echo "[INFO]: The interface was renamed to '$TARGET_NAME' and reactivated."
            else
                echo "[INFO]: The USB port '$BUS_INFO' interface name is already '$TARGET_NAME'"
            fi
        else
            if ip link show "$TARGET_NAME" &>/dev/null; then
                echo "[WARN]: Cannot rename '$iface' to '$TARGET_NAME' because interface '$TARGET_NAME' already exists."
                echo "[HINT]: Please check if another interface already occupies this name, or fix your USB_PORTS configuration."
                echo "-----------------------------------------------------------------"
                continue
            fi
            # if ip link show "$TARGET_NAME" &>/dev/null; then
            #     echo "[WARN]: Interface '$TARGET_NAME' already exists. Deleting to allow renaming."
            #     sudo ip link delete "$TARGET_NAME"
            # fi
            # If the interface is not active or the bit rate is different, set
            if [ "$IS_LINK_UP" = "yes" ]; then
                echo "[INFO]: Interface '$iface' is activated, but the bitrate $CURRENT_BITRATE does not match the set $TARGET_BITRATE."
            else
                echo "[INFO]: Interface '$iface' is not activated or the bitrate is not set."
            fi
            
            # Set the interface bit rate and activate it
            sudo ip link set "$iface" down
            sudo ip link set "$iface" type can bitrate $TARGET_BITRATE
            sudo ip link set "$iface" up
            echo "[INFO]: Interface '$iface' has been reset to bitrate $TARGET_BITRATE and activated."
            
            # Rename the interface to the target name
            if [ "$iface" != "$TARGET_NAME" ]; then
                echo "[INFO]: Rename interface $iface to '$TARGET_NAME'"
                sudo ip link set "$iface" down
                sudo ip link set "$iface" name "$TARGET_NAME"
                sudo ip link set "$TARGET_NAME" up
                echo "[INFO]: The interface was renamed to '$TARGET_NAME' and reactivated."
            fi
        fi
        SUCCESS_COUNT=$((SUCCESS_COUNT+1))
        USB_PORT_STATUS["$BUS_INFO"]="success"
    else
        # echo "↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓---err---↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓"
        echo "[ERROR]: The USB port '$BUS_INFO' of interface '$iface' was not found in the predefined USB_PORTS list."
        echo "[INFO]: Current predefined USB_PORTS configuration:"
        for k in "${!USB_PORTS[@]}"; do
            echo "        '$k'"
        done
        echo "[HINT]: Please check if the USB device is inserted into the correct port, or update the USB_PORTS config if needed."
        # echo "↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑---err---↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑"
    fi
    echo "-----------------------------------------------------------------"
done

# Calculation failed USB port
for k in "${!USB_PORT_STATUS[@]}"; do
    if [ "${USB_PORT_STATUS[$k]}" != "success" ]; then
        echo "❌ Expected CAN interface on USB port '$k' was not found or not activated."
        FAILED_COUNT=$((FAILED_COUNT+1))
    fi
done

# Final Tips
if [ "$SUCCESS_COUNT" -gt 0 ]; then
    echo "[RESULT]: ✅ $SUCCESS_COUNT expected CAN interfaces processed successfully."
else
    echo "[RESULT]: ❌ No USB interface matches the preset CAN configuration, please check whether the USB port is connected correctly."
fi

if [ "$FAILED_COUNT" -gt 0 ]; then
    echo "[RESULT]: 🚫 $FAILED_COUNT expected CAN interfaces failed to activate or were not found."
fi
