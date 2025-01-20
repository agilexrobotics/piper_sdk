import math
from typing_extensions import (
    Literal,
)

class C_PiperForwardKinematics():
    def __init__(self):
        self.RADIAN = 57.295777
        self.PI_2 = math.pi / 2
        # DH参数矩阵（Denavit-Hartenberg）
        self.DH_matrix = [
            [0.0, 0.123, 0.0, -self.PI_2],
            [-self.PI_2, 0.0, 0.28503, 0.0],
            [self.PI_2, 0.02198, 0.0, self.PI_2],
            [0.0, 0.25075, 0.0, -self.PI_2],
            [0.0, 0.0, 0.0, self.PI_2],
            [0.0, 0.091, 0.0, 0.0]
        ]
    
    def __arm_rotmat_to_eulerangle(self, rotationM, eulerAngles):
        # 旋转矩阵转换为欧拉角
        if abs(rotationM[6]) >= 1.0 - 0.0001:
            if rotationM[6] < 0:
                A = 0.0
                B = self.PI_2
                C = math.atan2(rotationM[1], rotationM[4])
            else:
                A = 0.0
                B = -self.PI_2
                C = -math.atan2(rotationM[1], rotationM[4])
        else:
            B = math.atan2(-rotationM[6], math.sqrt(rotationM[0] ** 2 + rotationM[3] ** 2))
            cb = math.cos(B)
            A = math.atan2(rotationM[3] / cb, rotationM[0] / cb)
            C = math.atan2(rotationM[7] / cb, rotationM[8] / cb)

        eulerAngles[0] = C
        eulerAngles[1] = B
        eulerAngles[2] = A

    # 矩阵相乘函数
    def __matrix_multiply(self, A, B, m, p, n, C):
        for i in range(m):
            for j in range(n):
                C[i * n + j] = 0
                for k in range(p):
                    C[i * n + j] += A[i * p + k] * B[k * n + j]
    
    # 正向运动学函数
    def arm_forward(self, joint_states:list, joint_index:Literal[1, 2, 3, 4, 5, 6]=6):
        q_in = [0.0] * 6
        q = [0.0] * 6
        cosq = sinq = cosa = sina = 0.0
        P06 = [0.0] * 6
        R06 = [0.0] * 9
        R = [[0.0] * 9 for _ in range(6)]
        R02 = [0.0] * 9
        R03 = [0.0] * 9
        R04 = [0.0] * 9
        R05 = [0.0] * 9
        L0_bs = [0.0] * 3
        L0_se = [0.0] * 3
        L0_ew = [0.0] * 3
        L0_wt = [0.0] * 3

        L1_base = [0.0, -0.123, 0.0]
        L2_arm = [0.28503, 0.0, 0.0]
        L3_elbow = [-0.02198, 0.0, 0.25075]
        L6_wrist = [0.0, 0.0, 0.091]
        migration_val = [0, 84.22, -169.22, 0, 0, 0]

        # 将输入关节角度转换为弧度
        for i in range(6):
            q_in[i] = (joint_states[i] - migration_val[i]) / self.RADIAN

        # 计算每个关节的旋转矩阵
        for i in range(joint_index):
            q[i] = q_in[i] + self.DH_matrix[i][0]
            cosq = math.cos(q[i])
            sinq = math.sin(q[i])
            cosa = math.cos(self.DH_matrix[i][3])
            sina = math.sin(self.DH_matrix[i][3])

            R[i][0] = cosq
            R[i][1] = -cosa * sinq
            R[i][2] = sina * sinq
            R[i][3] = sinq
            R[i][4] = cosa * cosq
            R[i][5] = -sina * cosq
            R[i][6] = 0.0
            R[i][7] = sina
            R[i][8] = cosa

        # 矩阵相乘
        self.__matrix_multiply(R[0], R[1], 3, 3, 3, R02)
        self.__matrix_multiply(R02, R[2], 3, 3, 3, R03)
        self.__matrix_multiply(R03, R[3], 3, 3, 3, R04)
        self.__matrix_multiply(R04, R[4], 3, 3, 3, R05)
        self.__matrix_multiply(R05, R[5], 3, 3, 3, R06)

        self.__matrix_multiply(R[0], L1_base, 3, 3, 1, L0_bs)
        self.__matrix_multiply(R02, L2_arm, 3, 3, 1, L0_se)
        self.__matrix_multiply(R03, L3_elbow, 3, 3, 1, L0_ew)
        self.__matrix_multiply(R06, L6_wrist, 3, 3, 1, L0_wt)

        for i in range(3):
            P06[i] = L0_bs[i] + L0_se[i] + L0_ew[i] + L0_wt[i]

        # 计算旋转矩阵对应的欧拉角
        euler = [0.0] * 3
        self.__arm_rotmat_to_eulerangle(R06, euler)
        P06[3:] = euler

        # 更新输出
        pos_rot = [ P06[0] * 1000, P06[1] * 1000, P06[2] * 1000,
                    P06[3] * self.RADIAN, P06[4] * self.RADIAN, P06[5] * self.RADIAN]
        return pos_rot