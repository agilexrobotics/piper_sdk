import os
import numpy as np
import pinocchio as pin
from typing import Optional

class PiperPinocchio:
    def __init__(self, urdf_path=None):
        package_dirs = [os.path.dirname(os.path.dirname(urdf_path))]
        self.robot = pin.RobotWrapper.BuildFromURDF(urdf_path, package_dirs)
        self.model = self.robot.model
        self.data = self.model.createData()
        self.robot.data = self.data
        self._nq = self.model.nq
        self._nv = self.model.nv
        self._q_temp = np.zeros(self._nq)
        self._v_temp = np.zeros(self._nv)
        self._a_temp = np.zeros(self._nv)
        self._gravity_world = np.array([0.0, 0.0, -9.81], dtype=float)

    def _prepare_q_input(self, q: np.ndarray) -> tuple[np.ndarray, int]:
        q_len = len(q)
        if q_len == self._nq:
            return q, q_len

        self._q_temp.fill(0.0)
        self._q_temp[:q_len] = q
        return self._q_temp, q_len
    
    def set_base_orientation(self, base_orientation: Optional[np.ndarray]) -> None:
        if base_orientation is None:
            self.model.gravity.linear = self._gravity_world
            return

        if base_orientation.shape == (4,):
            rotation = pin.Quaternion(
                base_orientation[3],
                base_orientation[0],
                base_orientation[1],
                base_orientation[2],
            ).toRotationMatrix()
        elif base_orientation.shape == (3, 3):
            rotation = base_orientation
        else:
            raise ValueError("基座姿勢の形式が不正です")

        self.model.gravity.linear = rotation.T @ self._gravity_world

    def gravity_compensation(self, q: np.ndarray, base_orientation: Optional[np.ndarray] = None) -> np.ndarray:
        """
        重力補償を計算（ベース姿勢は任意）

        :param q: 関節角度
        :param base_orientation: 基座姿勢（四元数xyzwまたは回転行列）。Noneは水平基座
        :return: 重力補償トルク
        """
        if base_orientation is not None:
            self.set_base_orientation(base_orientation)

        q_input, q_len = self._prepare_q_input(q)

        tau_ff = pin.rnea(self.model, self.data, q_input, self._v_temp, self._a_temp)
        return tau_ff[:q_len]

    def mass_matrix(self, q: np.ndarray, base_orientation: Optional[np.ndarray] = None) -> np.ndarray:
        """
        関節空間慣性行列を計算して返す

        :param q: 関節角度
        :param base_orientation: 基座姿勢（四元数xyzwまたは回転行列）。Noneは現在設定を維持
        :return: 慣性行列 M(q)
        """
        if base_orientation is not None:
            self.set_base_orientation(base_orientation)

        q_input, q_len = self._prepare_q_input(q)
        mass_matrix = np.array(pin.crba(self.model, self.data, q_input), copy=True)
        mass_matrix = 0.5 * (mass_matrix + mass_matrix.T)
        return mass_matrix[:q_len, :q_len]
