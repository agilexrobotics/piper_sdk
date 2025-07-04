#!/usr/bin/env python3
# -*-coding:utf8-*-

from enum import Enum, auto

class PiperSDKVersion(Enum):
    PIPER_SDK_VERSION_0_2_19 = '0.2.19'
    PIPER_SDK_VERSION_0_2_20 = '0.2.20'
    PIPER_SDK_VERSION_0_3_0 = '0.3.0'
    PIPER_SDK_VERSION_0_3_1 = '0.3.1'
    PIPER_SDK_CURRENT_VERSION = PIPER_SDK_VERSION_0_3_1
    PIPER_SDK_VERSION_UNKNOWN = 'unknown'
    def __str__(self):
        return f"{self.name} ({self.value})"
    def __repr__(self):
        return f"{self.name}: {self.value}"