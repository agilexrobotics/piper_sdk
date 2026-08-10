#!/usr/bin/env python3
# -*-coding:utf8-*-
from typing_extensions import (
    Literal,
)
from enum import unique

from ...core import IntEnumBase

class ArmMsgGripperCtrl_V3:
    '''
    msg_v3_transmit

    Gripper Control Command

    CAN ID:
        0x159

    Args:
        grippers_val: Gripper val, unit: 0.001 mm or 0.001 degree.
        grippers_effort: Gripper torque, represented as an integer, unit: 0.001N·m. Range 0-5000, corresponds to 0-5 N·m
        status_code:
            - 0x00: disable/width
            - 0x01: enable/width
            - 0x02: disable/clear_err/width
            - 0x03: enable/clear_err/width
            - 0x04: disable/angle
            - 0x05: enable/angle
            - 0x06: disable/clear_err/angle
            - 0x07: enable/clear_err/angle
        set_zero: Set the current position as the zero point.
            0x00: Invalid;
            0xAE: Set zero.

    Bit Description:

        Byte 0-3 grippers_val: int32, unit: 0.001° or 0.001mm.
        Byte 4-5 grippers_effort: uint16, unit: 0.001N·m, represents the gripper torque.
        Byte 6 status_code: uint8, gripper status code for enable/disable/clear error.
            - 0x00: disable/width
            - 0x01: enable/width
            - 0x02: disable/clear_err/width
            - 0x03: enable/clear_err/width
            - 0x04: disable/angle
            - 0x05: enable/angle
            - 0x06: disable/clear_err/angle
            - 0x07: enable/clear_err/angle
        Byte 7 set_zero: uint8, flag to set the current position as the zero point.
            0x00: Invalid;
            0xAE: Set zero.
    '''
    class Enums:
        @unique
        class StatusCode(IntEnumBase):
            # disable / width
            DISABLE_WIDTH = 0x00

            # enable / width
            ENABLE_WIDTH = 0x01

            # disable / clear error / width
            DISABLE_CLEAR_ERR_WIDTH = 0x02

            # enable / clear error / width
            ENABLE_CLEAR_ERR_WIDTH = 0x03

            # disable / angle
            DISABLE_ANGLE = 0x04

            # enable / angle
            ENABLE_ANGLE = 0x05

            # disable / clear error / angle
            DISABLE_CLEAR_ERR_ANGLE = 0x06

            # enable / clear error / angle
            ENABLE_CLEAR_ERR_ANGLE = 0x07

            UNKNOWN = 0xFF

        @unique
        class SetZero(IntEnumBase):
            INVALID = 0x00
            SET_ZERO = 0xAE
            UNKNOWN = 0xFF

    def __init__(self,
                 grippers_val: int = 0,
                 grippers_effort: int = 0,
                 status_code: Literal[0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07] = 0,
                 set_zero: Literal[0x00, 0xAE] = 0):
        # if status_code not in [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]:
        #     raise ValueError(f"'status_code' Value {status_code} out of range [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07]")
        # if not (0 <= grippers_effort <= 5000):
        #     raise ValueError(f"'grippers_effort' Value {grippers_effort} out of range 0-5000")
        # if set_zero not in [0x00, 0xAE]:
        #     raise ValueError(f"'set_zero' Value {set_zero} out of range [0x00,0xAE]")
        self.grippers_val = grippers_val
        self.grippers_effort = grippers_effort
        self.status_code = status_code
        self.set_zero = set_zero

    def __str__(self):
        return (f"ArmMsgGripperCtrl(\n"
                f"  grippers_val: {self.grippers_val}, {self.grippers_val * 0.001:.3f},\n"
                f"  grippers_effort: {self.grippers_effort} \t {self.grippers_effort * 0.001:.3f},\n"
                f"  status_code: {self.status_code},\n"
                f"  set_zero: {self.set_zero}\n"
                f")")

    def __repr__(self):
        return self.__str__()
