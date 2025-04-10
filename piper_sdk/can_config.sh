#!/bin/bash

# 使用说明：

# 1.先决条件
#     需要在系统中安装 ip 工具和 ethtool 工具。
#     sudo apt install ethtool can-utils
#     确保 gs_usb 驱动已正确安装。

# 2.背景
#  本脚本旨在自动管理和重命名并激活 CAN（Controller Area Network）接口。
#  它检查系统中当前的 CAN 模块数量，并根据预定义的 USB 端口重命名 CAN 接口并激活。
#  这对于有多个 CAN 模块的系统，尤其是不同 CAN 模块需要特定名称的情况，非常有用。

# 3.主要功能
#  检查 CAN 模块数量：确保系统中检测到的 CAN 模块数量与预设的数量一致。
#  获取 USB 端口信息：通过 ethtool 获取每个 CAN 模块的 USB 端口信息。
#  验证 USB 端口：检查每个 CAN 模块的 USB 端口是否符合预定义的端口列表。
#  重命名 CAN 接口：根据预定义的 USB 端口，将 CAN 接口重命名为目标名称。

# 4.脚本配置说明
#   脚本中的关键配置项包括预期的 CAN 模块数量、默认的 CAN 接口名称和波特率设置：
#   1.预期的 CAN 模块数量：
#     EXPECTED_CAN_COUNT=1
#     这个值决定了系统中应该检测到的 CAN 模块数量。
#   2.单个can模块的时候默认的 CAN 接口名称：
#     DEFAULT_CAN_NAME="${1:-can0}"
#     可以通过命令行参数指定默认的 CAN 接口名称，如果不提供参数，默认为 can0。
#   3.单个 CAN 模块时的默认比特率：
#     DEFAULT_BITRATE="${2:-500000}"
#     可以通过命令行参数指定单个 CAN 模块时的比特率，如果不提供参数，默认为 500000。
#   4.多个 CAN 模块时的配置:
#     declare -A USB_PORTS
#     USB_PORTS["1-2:1.0"]="can_device_1:500000"
#     USB_PORTS["1-3:1.0"]="can_device_2:250000"
#     这里的键表示 USB 端口，值是接口名称和比特率，使用冒号分隔。

# 5.使用步骤
#  1.编辑脚本：
#   1. 修改预定义值：
#      - 预定义的 CAN 模块数量：EXPECTED_CAN_COUNT=2，可以修改为工控机上插入的can模块数量
#      - 如果只有一个can模块，设定完上面的参数可以直接跳过此处往后看
#      - (多个can模块)预定义的 USB 端口和目标接口名称：
#          先将某个can模块插入到预期的usb口，注意在初次配置时，每次在工控机上插入一个can模块
#          然后执行 sudo ethtool -i can0 | grep bus,并记录下 bus-info: 后面的参数
#          接着插入下一个can模块，注意不可以与上次can模块插入的usb口相同，然后重复执行上一步
#          (其实可以用一个can模块去插不同的usb，因为区分模块是根据usb地址来区分的)
#          所有模块都设计好所应该在的usb口并记录完成后，
#          根据实际情况修改 USB 端口（bus-info）和目标接口名称。
#          can_device_1:500000，前者为设定的can名称，后者为设定的波特率
#            declare -A USB_PORTS
#            USB_PORTS["1-2:1.0"]="can_device_1:500000"
#            USB_PORTS["1-3:1.0"]="can_device_2:250000"
#          需要修改的是USB_PORTS["1-3:1.0"]内双引号的内容，修改为上面记录的bus-info: 后面的参数
#   2.赋予脚本执行权限：
#       打开终端，导航到脚本所在目录，执行以下命令赋予脚本执行权限：
#       chmod +x can_config.sh
#   3.运行脚本：
#     使用 sudo 执行脚本，因为脚本需要管理员权限来修改网络接口：
#       1.单个 CAN 模块
#         1.可以通过命令行参数指定默认的 CAN 接口名称和比特率（默认为 can0 和 500000）：
#           sudo bash ./can_config.sh [CAN接口名称] [比特率]
#           例如，指定接口名称为 my_can_interface，比特率为 1000000：
#           sudo bash ./can_config.sh my_can_interface 1000000
#         2.可以通过指定的usb硬件地址来指定can名称
#           sudo bash ./can_config.sh [CAN接口名称] [比特率] [usb硬件地址]
#           例如，指定接口名称为 my_can_interface，比特率为 1000000，usb硬件地址为 1-3:1.0：
#           sudo bash ./can_config.sh my_can_interface 1000000 1-3:1.0
#           也就是将 1-3:1.0 usb地址的can设备指定名称为my_can_interface，比特率为 1000000
#       2.多个 CAN 模块
#         对于多个 CAN 模块，通过在脚本中设置 USB_PORTS 数组来指定每个 CAN 模块的接口名称和比特率。
#         无需额外参数，直接运行脚本：
#         sudo ./can_config.sh

# 注意事项

#     权限要求：
#         脚本需要使用 sudo 权限，因为网络接口的重命名和设置需要管理员权限。
#         确保你有足够的权限来运行该脚本。

#     脚本环境：
#         本脚本假设在 bash 环境下运行。确保你的系统使用 bash，而不是其他 Shell（如 sh）。
#         可以通过检查脚本的 Shebang 行（#!/bin/bash）确保使用 bash。

#     USB 端口信息：
#         确保你预定义的 USB 端口信息（bus-info）与实际系统中 ethtool 输出的信息一致。
#         使用命令 sudo ethtool -i can0、sudo ethtool -i can1 等检查每个 CAN 接口的 bus-info。

#     接口冲突：
#         确保目标接口名称（如 can_device_1、can_device_2）是唯一的，不与系统中其他现有接口名称冲突。
#         如果要修改 USB 端口和接口名称的对应关系，请根据实际情况调整 USB_PORTS 数组。
#-------------------------------------------------------------------------------------------------#

# 预定义的 CAN 模块数量
EXPECTED_CAN_COUNT=1

if [ "$EXPECTED_CAN_COUNT" -eq 1 ]; then
    # 默认的 CAN 名称，用户可以通过命令行参数设定
    DEFAULT_CAN_NAME="${1:-can0}"

    # 单个 CAN 模块时的默认比特率，用户可以通过命令行参数设定
    DEFAULT_BITRATE="${2:-1000000}"

    # USB 硬件地址（可选参数）
    USB_ADDRESS="${3}"
fi

# 预定义的 USB 端口、目标接口名称及其比特率（在多个 CAN 模块时使用）
if [ "$EXPECTED_CAN_COUNT" -ne 1 ]; then
    declare -A USB_PORTS 
    USB_PORTS["1-2:1.0"]="can_left:1000000"
    USB_PORTS["1-4:1.0"]="can_right:1000000"
fi

# 获取当前系统中的 CAN 模块数量
CURRENT_CAN_COUNT=$(ip link show type can | grep -c "link/can")

# 检查当前系统中的 CAN 模块数量是否符合预期
if [ "$CURRENT_CAN_COUNT" -ne "$EXPECTED_CAN_COUNT" ]; then
    echo "错误: 检测到的 CAN 模块数量 ($CURRENT_CAN_COUNT) 与预期数量 ($EXPECTED_CAN_COUNT) 不符。"
    exit 1
fi

# 加载 gs_usb 模块
sudo modprobe gs_usb
if [ $? -ne 0 ]; then
    echo "错误: 无法加载 gs_usb 模块。"
    exit 1
fi

# 判断是否只需要处理一个 CAN 模块
if [ "$EXPECTED_CAN_COUNT" -eq 1 ]; then
    if [ -n "$USB_ADDRESS" ]; then
        echo "检测到 USB 硬件地址参数: $USB_ADDRESS"
        
        # 使用 ethtool 查找与 USB 硬件地址对应的 CAN 接口
        INTERFACE_NAME=""
        for iface in $(ip -br link show type can | awk '{print $1}'); do
            BUS_INFO=$(sudo ethtool -i "$iface" | grep "bus-info" | awk '{print $2}')
            if [ "$BUS_INFO" = "$USB_ADDRESS" ]; then
                INTERFACE_NAME="$iface"
                break
            fi
        done
        
        if [ -z "$INTERFACE_NAME" ]; then
            echo "错误: 无法找到与 USB 硬件地址 $USB_ADDRESS 对应的 CAN 接口。"
            exit 1
        else
            echo "找到与 USB 硬件地址 $USB_ADDRESS 对应的接口: $INTERFACE_NAME"
        fi
    else
        # 获取唯一的 CAN 接口
        INTERFACE_NAME=$(ip -br link show type can | awk '{print $1}')
        
        # 检查是否获取到了接口名称
        if [ -z "$INTERFACE_NAME" ]; then
            echo "错误: 无法检测到 CAN 接口。"
            exit 1
        fi

        echo "预期只有一个 CAN 模块，检测到接口 $INTERFACE_NAME"
    fi

    # 检查当前接口是否已经激活
    IS_LINK_UP=$(ip link show "$INTERFACE_NAME" | grep -q "UP" && echo "yes" || echo "no")

    # 获取当前接口的比特率
    CURRENT_BITRATE=$(ip -details link show "$INTERFACE_NAME" | grep -oP 'bitrate \K\d+')

    if [ "$IS_LINK_UP" = "yes" ] && [ "$CURRENT_BITRATE" -eq "$DEFAULT_BITRATE" ]; then
        echo "接口 $INTERFACE_NAME 已经激活，并且比特率为 $DEFAULT_BITRATE"
        
        # 检查接口名称是否与默认的名称匹配
        if [ "$INTERFACE_NAME" != "$DEFAULT_CAN_NAME" ]; then
            echo "将接口 $INTERFACE_NAME 重命名为 $DEFAULT_CAN_NAME"
            sudo ip link set "$INTERFACE_NAME" down
            sudo ip link set "$INTERFACE_NAME" name "$DEFAULT_CAN_NAME"
            sudo ip link set "$DEFAULT_CAN_NAME" up
            echo "接口已重命名为 $DEFAULT_CAN_NAME，并重新激活。"
        else
            echo "接口名称已经是 $DEFAULT_CAN_NAME"
        fi
    else
        # 如果接口未激活或比特率不同，进行设置
        if [ "$IS_LINK_UP" = "yes" ]; then
            echo "接口 $INTERFACE_NAME 已经激活，但比特率为 $CURRENT_BITRATE，与设定的 $DEFAULT_BITRATE 不符。"
        else
            echo "接口 $INTERFACE_NAME 未激活或未设置比特率。"
        fi
        
        # 设置接口比特率并激活
        sudo ip link set "$INTERFACE_NAME" down
        sudo ip link set "$INTERFACE_NAME" type can bitrate $DEFAULT_BITRATE
        sudo ip link set "$INTERFACE_NAME" up
        echo "接口 $INTERFACE_NAME 已重新设置为比特率 $DEFAULT_BITRATE 并激活。"
        
        # 重命名接口为默认名称
        if [ "$INTERFACE_NAME" != "$DEFAULT_CAN_NAME" ]; then
            echo "将接口 $INTERFACE_NAME 重命名为 $DEFAULT_CAN_NAME"
            sudo ip link set "$INTERFACE_NAME" down
            sudo ip link set "$INTERFACE_NAME" name "$DEFAULT_CAN_NAME"
            sudo ip link set "$DEFAULT_CAN_NAME" up
            echo "接口已重命名为 $DEFAULT_CAN_NAME，并重新激活。"
        fi
    fi
else
    # 处理多个 CAN 模块

    # 检查 USB 端口和目标接口名称的数量是否与预期 CAN 模块数量匹配
    PREDEFINED_COUNT=${#USB_PORTS[@]}
    if [ "$EXPECTED_CAN_COUNT" -ne "$PREDEFINED_COUNT" ]; then
        echo "错误: 预设的 CAN 模块数量 ($EXPECTED_CAN_COUNT) 与预定义的 USB 端口数量 ($PREDEFINED_COUNT) 不匹配。"
        exit 1
    fi

    # 遍历所有 CAN 接口
    for iface in $(ip -br link show type can | awk '{print $1}'); do
        # 使用 ethtool 获取 bus-info
        BUS_INFO=$(sudo ethtool -i "$iface" | grep "bus-info" | awk '{print $2}')
        
        if [ -z "$BUS_INFO" ];then
            echo "错误: 无法获取接口 $iface 的 bus-info 信息。"
            continue
        fi
        
        echo "接口 $iface 插入在 USB 端口 $BUS_INFO"

        # 检查 bus-info 是否在预定义的 USB 端口列表中
        if [ -n "${USB_PORTS[$BUS_INFO]}" ];then
            IFS=':' read -r TARGET_NAME TARGET_BITRATE <<< "${USB_PORTS[$BUS_INFO]}"
            
            # 检查当前接口是否已经激活
            IS_LINK_UP=$(ip link show "$iface" | grep -q "UP" && echo "yes" || echo "no")

            # 获取当前接口的比特率
            CURRENT_BITRATE=$(ip -details link show "$iface" | grep -oP 'bitrate \K\d+')

            if [ "$IS_LINK_UP" = "yes" ] && [ "$CURRENT_BITRATE" -eq "$TARGET_BITRATE" ]; then
                echo "接口 $iface 已经激活，并且比特率为 $TARGET_BITRATE"
                
                # 检查接口名称是否与目标名称匹配
                if [ "$iface" != "$TARGET_NAME" ]; then
                    echo "将接口 $iface 重命名为 $TARGET_NAME"
                    sudo ip link set "$iface" down
                    sudo ip link set "$iface" name "$TARGET_NAME"
                    sudo ip link set "$TARGET_NAME" up
                    echo "接口已重命名为 $TARGET_NAME，并重新激活。"
                else
                    echo "接口名称已经是 $TARGET_NAME"
                fi
            else
                # 如果接口未激活或比特率不同，进行设置
                if [ "$IS_LINK_UP" = "yes" ]; then
                    echo "接口 $iface 已经激活，但比特率为 $CURRENT_BITRATE，与设定的 $TARGET_BITRATE 不符。"
                else
                    echo "接口 $iface 未激活或未设置比特率。"
                fi
                
                # 设置接口比特率并激活
                sudo ip link set "$iface" down
                sudo ip link set "$iface" type can bitrate $TARGET_BITRATE
                sudo ip link set "$iface" up
                echo "接口 $iface 已重新设置为比特率 $TARGET_BITRATE 并激活。"
                
                # 重命名接口为目标名称
                if [ "$iface" != "$TARGET_NAME" ]; then
                    echo "将接口 $iface 重命名为 $TARGET_NAME"
                    sudo ip link set "$iface" down
                    sudo ip link set "$iface" name "$TARGET_NAME"
                    sudo ip link set "$TARGET_NAME" up
                    echo "接口已重命名为 $TARGET_NAME，并重新激活。"
                fi
            fi
        else
            echo "错误: 未知的 USB 端口 $BUS_INFO 对应接口 $iface。"
            exit 1
        fi
    done
fi

echo "所有 CAN 接口已成功重命名并激活。"
