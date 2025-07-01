#!/usr/bin/env python3
import subprocess
import argparse

def interface_exists(name: str) -> bool:
    result = subprocess.run(['ip', 'link', 'show', name],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
    return result.returncode == 0

def is_physical_can(name: str) -> bool:
    try:
        output = subprocess.check_output(['ethtool', '-i', name], text=True)
        return "driver" in output.lower()
    except subprocess.CalledProcessError:
        return False

def is_vcan(name: str) -> bool:
    try:
        output = subprocess.check_output(['ip', '-d', 'link', 'show', name], text=True)
        return 'vcan' in output.lower()
    except subprocess.CalledProcessError:
        return False

def get_can_bitrate(name: str) -> str:
    try:
        output = subprocess.check_output(['ip', '-details', 'link', 'show', name], text=True)
        for line in output.splitlines():
            line = line.strip()
            if line.startswith("bitrate"):
                return line  # e.g., "bitrate 500000 sample-point 0.875"
        return "(未设置波特率)"
    except subprocess.CalledProcessError:
        return "(获取失败)"

def create_vcan(name: str, bitrate: int):
    if interface_exists(name):
        print(f"[✓] 接口 {name} 已存在，跳过创建")
        if is_physical_can(name):
            bitrate_info = get_can_bitrate(name)
            print(f"[i] 当前波特率信息: {bitrate_info}")
        elif is_vcan(name):
            print(f"[i] {name} 是虚拟 CAN 接口，无波特率设置")
        else:
            print(f"[❓] {name} 类型无法识别")
        return

    try:
        subprocess.run(['modprobe', 'vcan'], check=True)
        subprocess.run(['ip', 'link', 'add', 'dev', name, 'type', 'vcan'], check=True)
        subprocess.run(['ip', 'link', 'set', name, 'up'], check=True)
        print(f"[+] 成功创建虚拟 CAN 接口: {name}")
    except subprocess.CalledProcessError as e:
        print(f"[×] 创建失败: {e}")

def delete_vcan(name: str):
    if not interface_exists(name):
        print(f"[×] 接口 {name} 不存在，无法删除")
        return

    if is_physical_can(name):
        bitrate_info = get_can_bitrate(name)
        print(f"[⚠️] {name} 是实体 CAN 接口，跳过删除")
        print(f"[i] 当前波特率信息: {bitrate_info}")
        return
    elif not is_vcan(name):
        print(f"[❓] {name} 类型未知，为安全起见跳过删除")
        return

    try:
        subprocess.run(['ip', 'link', 'delete', name], check=True)
        print(f"[-] 已删除虚拟 CAN 接口: {name}")
    except subprocess.CalledProcessError as e:
        print(f"[×] 删除失败: {e}")

def main():
    parser = argparse.ArgumentParser(description="虚拟CAN接口管理工具")
    subparsers = parser.add_subparsers(dest='command', required=True)

    parser_create = subparsers.add_parser('create', help='创建虚拟 CAN 接口')
    parser_create.add_argument('--can_name', required=True)
    parser_create.add_argument('--bitrate', type=int, default=500000, help='波特率（用于显示，不影响虚拟 CAN）')

    parser_delete = subparsers.add_parser('delete', help='删除虚拟 CAN 接口')
    parser_delete.add_argument('--can_name', required=True)

    args = parser.parse_args()

    if args.command == 'create':
        create_vcan(args.can_name, args.bitrate)
    elif args.command == 'delete':
        delete_vcan(args.can_name)

if __name__ == '__main__':
    main()
