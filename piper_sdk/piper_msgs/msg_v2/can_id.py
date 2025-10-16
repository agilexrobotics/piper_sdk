#!/usr/bin/env python3
# -*-coding:utf8-*-

from enum import Enum, auto

class CanIDPiper(Enum):
    '''
    msg_v2
    
    机械臂can id
    '''
    '''
    msg_v2
    
    piper's can_ids
    '''
    # 主动反馈指令，可设置整体偏移为 0x2B1~0x2B8或 0x2C1~0x2C8，详见指令0x470
    ARM_STATUS_FEEDBACK = 0x2A1         #机械臂状态反馈ID
    ARM_END_POSE_FEEDBACK_1 = 0x2A2     #机械臂末端姿态反馈
    ARM_END_POSE_FEEDBACK_2 = 0x2A3
    ARM_END_POSE_FEEDBACK_3 = 0x2A4
    ARM_JOINT_FEEDBACK_12 = 0x2A5       #机械臂关节反馈
    ARM_JOINT_FEEDBACK_34 = 0x2A6
    ARM_JOINT_FEEDBACK_56 = 0x2A7
    ARM_GRIPPER_FEEDBACK = 0x2A8        #机械臂夹爪反馈
    # 运动控制指令，可设置整体偏移为 0x160~0x169或 0x170~0x179，详见指令0x470
    ARM_MOTION_CTRL_1 = 0x150
    # ARM_STOP_CTRL = 0x150               #机械臂快速急停
    # ARM_TRACK_CTRL = 0x150              #机械臂轨迹指令
    # ARM_GRAG_TEACH_CTRL = 0x150         #机械臂拖动示教指令
    ARM_MOTION_CTRL_2 = 0x151
    # ARM_MODE_CTRL = 0x151               #机械臂控制模式
    # ARM_MOVE_MODE_CTRL = 0x151          #机械臂Mode模式
    # ARM_MOVE_SPD_RATE_CTRL = 0x151      #机械臂运动速度百分比
    ARM_MOTION_CTRL_CARTESIAN_1=0x152#机械臂运动控制直角坐标系指令1,X&Y
    ARM_MOTION_CTRL_CARTESIAN_2=0x153#机械臂运动控制直角坐标系指令1,Z&RX
    ARM_MOTION_CTRL_CARTESIAN_3=0x154#机械臂运动控制直角坐标系指令1,RY&RZ
    ARM_JOINT_CTRL_12=0x155             #机械臂臂部关节控制指令12,J1&J2
    ARM_JOINT_CTRL_34=0x156             #机械臂臂部关节控制指令12,J3&J4
    ARM_JOINT_CTRL_56=0x157             #机械臂臂部关节控制指令12,J5&J6
    ARM_CIRCULAR_PATTERN_COORD_NUM_UPDATE_CTRL=0x158#圆弧模式坐标序号更新指令数据
    ARM_GRIPPER_CTRL = 0x159            #夹爪控制指令
    #----------------------------------基于V1.5-2版本后---------------------------------------------#
    ARM_JOINT_MIT_CTRL_1 = 0x15A
    ARM_JOINT_MIT_CTRL_2 = 0x15B
    ARM_JOINT_MIT_CTRL_3 = 0x15C
    ARM_JOINT_MIT_CTRL_4 = 0x15D
    ARM_JOINT_MIT_CTRL_5 = 0x15E
    ARM_JOINT_MIT_CTRL_6 = 0x15F
    #---------------------------------------------------------------------------------------------#
    # 机械臂参数配置与设定指令
    # 若指令名称带有反馈、应答; 决策控制单元->机械臂主控
    # 若指令名称带有查询、设置; 机械臂主控->决策控制单元
    ARM_MASTER_SLAVE_MODE_CONFIG = 0x470
    # ARM_MS_LINKAGE_CONFIG = 0x470          #随动主从模式设置指令-联动设置指令
    # ARM_MS_FEEDBACK_INSTRUCTION_OFFSET_CONFIG = 0x470#随动主从模式设置指令-反馈指令偏移值
    # ARM_MS_CTRL_INSTRUCTION_OFFSET_CONFIG = 0x470#随动主从模式设置指令-控制指令偏移
    # ARM_MS_LINKAGE_CTRL_OFFSET_CONFIG = 0x470#随动主从模式设置指令-联动模式控制目标地址偏移值
    # 设置为示教输入臂后，主动周期反馈报文 ID 增加偏移（偏移量可设置），模式切换为联动示教输入模式，不响应控制指令，且会主动发送关节模式控制指令；
    # 设置为运动输出臂后恢复为常规状态（退出联动示教输入模式，进入待机模式）；未收到此条指令的机械臂默认为此状态
    ARM_MOTOR_ENABLE_DISABLE_CONFIG = 0x471     #电机使能指令
    # ARM_MOTOR_DISABLE_CONFIG = 0x471    #电机失能指令
    # ARM_SEARCH_MOTOR_ANGLE_CONFIG = 0x472 #查询电机角度
    ARM_SEARCH_MOTOR_MAX_SPD_ACC_LIMIT = 0x472 #查询电机角度/最大速度/加速度限制
    # ARM_SEARCH_MOTOR_MAX_ACC_CONFIG = 0x472 #查询电机最大加速度限制
    ARM_FEEDBACK_CURRENT_MOTOR_ANGLE_LIMIT_MAX_SPD = 0x473 #反馈当前电机最大角度限制,最小角度限制,最大关节速度
    ARM_MOTOR_ANGLE_LIMIT_MAX_SPD_SET = 0x474      #电机角度限制/最大速度设置指令
    ARM_JOINT_CONFIG = 0x475            #关节设置指令
    ARM_INSTRUCTION_RESPONSE_CONFIG=0x476#设置指令应答
    ARM_FEEDBACK_RESP_SET_INSTRUCTION = 0x476 #设置指令应答反馈
    ARM_PARAM_ENQUIRY_AND_CONFIG = 0x477#机械臂参数查询与设置指令
    ARM_FEEDBACK_CURRENT_END_VEL_ACC_PARAM = 0x478    #反馈当前末端速度/加速度参数
    ARM_END_VEL_ACC_PARAM_CONFIG = 0x479      #末端速度/加速度参数设置指令
    ARM_CRASH_PROTECTION_RATING_CONFIG=0x47A#碰撞防护等级设置指令
    ARM_CRASH_PROTECTION_RATING_FEEDBACK=0x47B#碰撞防护等级反馈指令
    ARM_FEEDBACK_CURRENT_MOTOR_MAX_ACC_LIMIT=0x47C#反馈当前电机最大加速度限制
    #----------------------------------基于V1.5-2版本后---------------------------------------------#
    ARM_GRIPPER_TEACHING_PENDANT_PARAM_CONFIG = 0x47D
    ARM_GRIPPER_TEACHING_PENDANT_PARAM_FEEDBACK = 0x47E
    #---------------------------------------------------------------------------------------------#
    ARM_FEEDBACK_JOINT_VEL_ACC_1 = 0x481         #反馈当前关节的末端速度/加速度
    ARM_FEEDBACK_JOINT_VEL_ACC_2 = 0x482
    ARM_FEEDBACK_JOINT_VEL_ACC_3 = 0x483
    ARM_FEEDBACK_JOINT_VEL_ACC_4 = 0x484
    ARM_FEEDBACK_JOINT_VEL_ACC_5 = 0x485
    ARM_FEEDBACK_JOINT_VEL_ACC_6 = 0x486
    #灯光控制0x1节点ID，帧ID 0x121
    ARM_LIGHT_CTRL = 0x121              #灯光控制指令
    #驱动器信息高速反馈，节点ID 0x1~0x6
    ARM_INFO_HIGH_SPD_FEEDBACK_1 = 0x251
    ARM_INFO_HIGH_SPD_FEEDBACK_2 = 0x252
    ARM_INFO_HIGH_SPD_FEEDBACK_3 = 0x253
    ARM_INFO_HIGH_SPD_FEEDBACK_4 = 0x254
    ARM_INFO_HIGH_SPD_FEEDBACK_5 = 0x255
    ARM_INFO_HIGH_SPD_FEEDBACK_6 = 0x256
    #驱动器信息低速反馈，节点ID 0x1~0x6
    ARM_INFO_LOW_SPD_FEEDBACK_1 = 0x261
    ARM_INFO_LOW_SPD_FEEDBACK_2 = 0x262
    ARM_INFO_LOW_SPD_FEEDBACK_3 = 0x263
    ARM_INFO_LOW_SPD_FEEDBACK_4 = 0x264
    ARM_INFO_LOW_SPD_FEEDBACK_5 = 0x265
    ARM_INFO_LOW_SPD_FEEDBACK_6 = 0x266
    #CAN 升级总线静默模式设定指令
    ARM_CAN_UPDATE_SILENT_MODE_CONFIG=0x422
    # 固件读取指令
    ARM_FIRMWARE_READ = 0x4AF
    def __str__(self):
        return f"{self.name} (0x{self.value:X})"
    def __repr__(self):
        return f"{self.name}: 0x{self.value:X}"