#!/usr/bin/env python3
# -*-coding:utf8-*-

from enum import Enum, auto

class InterfaceVersion(Enum):
    '''
    Interface版本枚举
    '''
    '''
    Interface Version Enumeration.
    '''
    INTERFACE_V1 = auto()
    INTERFACE_V2 = auto()
    INTERFACE_UNKNOWN = auto()
    def __str__(self):
        return f"{self.name} (0x{self.value:X})"
    def __repr__(self):
        return f"{self.name}: 0x{self.value:X}"