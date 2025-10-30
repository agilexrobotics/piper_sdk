#!/usr/bin/env python3
# -*-coding:utf8-*-

from enum import Enum, auto

class PiperSDKVersion(Enum):
    PIPER_SDK_VERSION_0_2_19 = '0.2.19'
    PIPER_SDK_VERSION_0_2_20 = '0.2.20'
    PIPER_SDK_VERSION_0_3_0 = '0.3.0'
    PIPER_SDK_VERSION_0_3_2 = '0.3.2'
    PIPER_SDK_VERSION_0_3_3 = '0.3.3'
    PIPER_SDK_VERSION_0_4_0 = '0.4.0'
    PIPER_SDK_VERSION_0_4_1 = '0.4.1'
    PIPER_SDK_VERSION_0_4_2 = '0.4.2'
    PIPER_SDK_VERSION_0_4_3 = '0.4.3'
    PIPER_SDK_VERSION_0_5_0 = '0.5.0'
    PIPER_SDK_VERSION_0_6_0 = '0.6.0'
    PIPER_SDK_VERSION_0_6_1 = '0.6.1'
    PIPER_SDK_CURRENT_VERSION = PIPER_SDK_VERSION_0_6_1
    PIPER_SDK_VERSION_UNKNOWN = 'unknown'
    def __str__(self):
        return f"{self.name} ({self.value})"
    def __repr__(self):
        return f"{self.name}: {self.value}"