#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import atexit
import signal
import threading
from typing import Callable, List, Optional, Sequence


class EmergencyHoldGuard:
    """Engage hold-at-current-position on normal exit and emergency signals."""

    def __init__(
        self,
        piper,
        *,
        joint_ids: Sequence[int] = (1, 2, 3, 4, 5, 6),
        kp: float = 30.0,
        kd: float = 0.8,
        t_ref: float = 0.0,
        mit_speed_percent: int = 100,
        angle_reader: Optional[Callable[[], Sequence[float]]] = None,
        logger: Optional[Callable[[str], None]] = print,
    ):
        self._piper = piper
        self._joint_ids = tuple(joint_ids)
        self._kp = float(kp)
        self._kd = float(kd)
        self._t_ref = float(t_ref)
        self._mit_speed_percent = int(mit_speed_percent)
        self._angle_reader = angle_reader if angle_reader is not None else self._default_read_joint_angles
        self._logger = logger

        self._lock = threading.Lock()
        self._engaged = False
        self._prev_handlers = {}
        self._atexit_registered = False

    def __enter__(self):
        self._register_hooks()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.engage(reason="context_exit")
        self._restore_hooks()
        return False

    def engage(self, *, reason: str = "manual") -> bool:
        """Read current angles and hold the current pose once."""
        with self._lock:
            if self._engaged:
                return False
            self._engaged = True

        self._log(f"[EmergencyHoldGuard] engage: {reason}")
        try:
            current_angles = list(self._angle_reader())
            if len(current_angles) < len(self._joint_ids):
                raise RuntimeError("joint angle reader returned too few values")

            self._piper.MotionCtrl_2(0x01, 0x04, self._mit_speed_percent, 0xAD)
            for joint_id in self._joint_ids:
                angle = float(current_angles[joint_id - 1])
                self._piper.JointMitCtrl(joint_id, angle, 0.0, self._kp, self._kd, self._t_ref)
            self._log("[EmergencyHoldGuard] hold command sent.")
            return True
        except Exception as exc:
            self._log(f"[EmergencyHoldGuard] hold failed: {exc}")
            return False

    def _default_read_joint_angles(self) -> List[float]:
        high_spd_msg = self._piper.GetArmHighSpdInfoMsgs()
        motors = (
            high_spd_msg.motor_1,
            high_spd_msg.motor_2,
            high_spd_msg.motor_3,
            high_spd_msg.motor_4,
            high_spd_msg.motor_5,
            high_spd_msg.motor_6,
        )
        return [float(motor.pos) * 1e-3 for motor in motors]

    def _register_hooks(self):
        for sig in (signal.SIGINT, signal.SIGTERM):
            self._prev_handlers[sig] = signal.getsignal(sig)
            signal.signal(sig, self._signal_handler)
        atexit.register(self._atexit_handler)
        self._atexit_registered = True

    def _restore_hooks(self):
        for sig, prev in self._prev_handlers.items():
            try:
                signal.signal(sig, prev)
            except Exception:
                pass
        self._prev_handlers.clear()

        if self._atexit_registered:
            try:
                atexit.unregister(self._atexit_handler)
            except Exception:
                pass
            self._atexit_registered = False

    def _signal_handler(self, signum, frame):
        try:
            sig_name = signal.Signals(signum).name
        except Exception:
            sig_name = str(signum)
        self.engage(reason=f"signal:{sig_name}")
        raise KeyboardInterrupt(f"{sig_name} received")

    def _atexit_handler(self):
        self.engage(reason="atexit")

    def _log(self, message: str):
        if self._logger is None:
            return
        try:
            self._logger(message)
        except Exception:
            pass
