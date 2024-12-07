#!/usr/bin/env python3
# -*-coding:utf8-*-

# 机械臂控制base


from ..interface.piper_interface import C_PiperInterface


class C_PiperBase(C_PiperInterface):
    def __init__(self, can_name: str = "can0") -> None:
        super().__init__(can_name)

    def Connect(self, can_name: str):
        return self.ConnectPort(can_name)
