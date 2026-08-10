#!/usr/bin/env python3
# -*-coding:utf8-*-

import argparse
import subprocess
from pathlib import Path


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="piper-can-activate",
        description="Activate one Piper USB-CAN module using the packaged can_activate.sh script.",
    )
    parser.add_argument(
        "can_name",
        nargs="?",
        default="can0",
        help="Target CAN interface name after activation. Default: can0.",
    )
    parser.add_argument(
        "bitrate",
        nargs="?",
        default="1000000",
        help="CAN bitrate. Default: 1000000.",
    )
    parser.add_argument(
        "--usb-port",
        dest="usb_port",
        help="USB hardware address, for example 3-1.4:1.0. Use this when multiple CAN modules are connected.",
    )
    return parser


def _script_path():
    return Path(__file__).resolve().parents[1] / "can_activate.sh"


def main():
    parser = _build_parser()
    try:
        import argcomplete
    except ImportError:
        argcomplete = None
    if argcomplete is not None:
        argcomplete.autocomplete(parser)

    args = parser.parse_args()
    script = _script_path()
    if not script.exists():
        parser.error("can_activate.sh not found in the installed piper_sdk package.")

    command = ["bash", str(script), args.can_name, args.bitrate]
    if args.usb_port:
        command.append(args.usb_port)
    raise SystemExit(subprocess.call(command))


if __name__ == "__main__":
    main()
