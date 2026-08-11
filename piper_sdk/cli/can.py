#!/usr/bin/env python3
# -*-coding:utf8-*-

import argparse
import subprocess
from pathlib import Path


def _script_path(script_name):
    return Path(__file__).resolve().parents[1] / script_name


def _run_script(parser, script_name, args):
    script = _script_path(script_name)
    if not script.exists():
        parser.error(f"{script_name} not found in the installed piper_sdk package.")
    raise SystemExit(subprocess.call(["/bin/sh", str(script)] + args))


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="piper-can",
        description="Find and activate Piper USB-CAN modules.",
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    find_parser = subparsers.add_parser(
        "find",
        help="List detected CAN interfaces and their USB hardware addresses.",
        description="List detected CAN interfaces and their USB hardware addresses.",
    )
    find_parser.set_defaults(func=_find)

    activate_parser = subparsers.add_parser(
        "activate",
        help="Activate one CAN interface.",
        description="Activate one Piper USB-CAN module.",
    )
    activate_parser.add_argument(
        "can_name",
        nargs="?",
        default="can0",
        help="Target CAN interface name after activation. Default: can0.",
    )
    activate_parser.add_argument(
        "bitrate",
        nargs="?",
        default="1000000",
        help="CAN bitrate. Default: 1000000.",
    )
    activate_parser.add_argument(
        "--usb-port",
        dest="usb_port",
        help="USB hardware address, for example 3-1.4:1.0. Use this when multiple CAN modules are connected.",
    )
    activate_parser.set_defaults(func=_activate)

    return parser


def _find(parser, args):
    _run_script(parser, "find_all_can_port.sh", [])


def _activate(parser, args):
    command_args = [args.can_name, args.bitrate]
    if args.usb_port:
        command_args.append(args.usb_port)
    _run_script(parser, "can_activate.sh", command_args)


def main():
    parser = _build_parser()
    try:
        import argcomplete
    except ImportError:
        argcomplete = None
    if argcomplete is not None:
        argcomplete.autocomplete(parser)

    args = parser.parse_args()
    args.func(parser, args)


if __name__ == "__main__":
    main()
