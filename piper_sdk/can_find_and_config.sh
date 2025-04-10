#!/bin/bash

# Usage: ./check_and_setup_can.sh <CAN_NAME> <BITRATE> <USB_ADDRESS> <TIMEOUT>

# 默认参数
CAN_NAME="${1:-can0}"
BITRATE="${2:-1000000}"
USB_ADDRESS="${3}"
TIMEOUT="${4:-120}"  # 超时时间，默认 120 秒

sudo -v

ROOT="$(dirname "$(readlink -f "$0")")"

if [ -z "$USB_ADDRESS" ]; then
    echo "错误: 需要提供 USB 硬件地址。"
    exit 1
fi

# 开始时间
START_TIME=$(date +%s)

# 超时标志
TIMED_OUT=false

echo "开始检查 USB 硬件地址 $USB_ADDRESS 是否有 CAN 设备..."

while true; do
    # 获取当前时间
    CURRENT_TIME=$(date +%s)
    ELAPSED_TIME=$((CURRENT_TIME - START_TIME))

    # 检查是否超时
    if [ "$ELAPSED_TIME" -ge "$TIMEOUT" ]; then
        echo "超时: 在 $TIMEOUT 秒内未找到 CAN 设备。"
        TIMED_OUT=true
        break
    fi

    # 查找是否有设备连接在指定的 USB 硬件地址
    DEVICE_FOUND=false
    for iface in $(ip -br link show type can | awk '{print $1}'); do
        BUS_INFO=$(sudo ethtool -i "$iface" | grep "bus-info" | awk '{print $2}')
        if [ "$BUS_INFO" = "$USB_ADDRESS" ]; then
            DEVICE_FOUND=true
            break
        fi
    done

    if [ "$DEVICE_FOUND" = "true" ]; then
        echo "找到 CAN 设备，调用配置脚本..."
        sudo bash $ROOT/can_activate.sh "$CAN_NAME" "$BITRATE" "$USB_ADDRESS"
        if [ $? -eq 0 ]; then
            echo "CAN 设备配置成功。"
            exit 0
        else
            echo "配置脚本执行失败。"
            exit 1
        fi
    fi

    echo "未找到 CAN 设备，等待并重试..."

    # 每 5 秒检查一次
    sleep 5
done

# 如果循环结束并且超时，输出超时信息
if [ "$TIMED_OUT" = "true" ]; then
    echo "未能在规定时间内找到 CAN 设备，脚本退出。"
    exit 1
fi
