#!/usr/bin/env python3
# -*-coding:utf8-*-

from typing import (
    Optional,
)
from .arm_msg_type import ArmMsgType as ArmMsgType_V2
from .can_id import CanIDPiper as CanIDPiper_V2

_ARM_MSG_TYPE = ArmMsgType_V2
_CAN_ID = CanIDPiper_V2

class ArmMessageMapping:
    '''
    msg_v2
    
    机械臂消息类型和CAN ID的映射
    '''
    '''
    msg_v2
    
    Mapping of Robotic Arm Message Types and CAN IDs
    '''
    ArmMsgType = _ARM_MSG_TYPE
    CanIDPiper = _CAN_ID

    # 从父版本映射中删除的 CAN ID。
    # 适用场景：新协议版本废弃了某条旧报文，或者某个旧 CAN ID 在新版本中不应再被解析。
    # 示例：
    #   removed_mapping_ids = {0x15A}
    removed_mapping_ids = set()

    # 已有功能的 CAN ID 发生变化时使用。
    # changed_mapping 会先删除父版本中同名消息类型对应的旧 CAN ID，再写入新的 CAN ID。
    # 适用场景：例如 V5 将 PiperMsgJointMitCtrl_1 从 0x15A 改到 0x16A。
    # 示例：
    #   changed_mapping = {
    #       CanIDPiper_V5.ARM_JOINT_MIT_CTRL_1.value: ArmMsgType_V5.PiperMsgJointMitCtrl_1,
    #   }
    changed_mapping = {}

    # 新增的 CAN ID 到消息类型映射。
    # 适用场景：新协议版本增加了父版本没有的新报文。
    # 如果只是新增报文，不会删除父版本中的任何旧映射。
    # 示例：
    #   additional_mapping = {
    #       CanIDPiper_V4.NEW_FRAME.value: ArmMsgType_V4.PiperMsgNewFrame,
    #   }
    additional_mapping = {}

    # 当有一个新类继承 ArmMessageMapping 或它的子类时，Python 自动调用这个函数
    # 定义 ArmMessageMapping 自身时，不会调用自己的 __init_subclass__。
    # 只有“子类创建完成时”才会调用父类的 __init_subclass__。
    def __init_subclass__(cls, **kwargs):
        # 作用：调用父类的 __init_subclass__。
        # 在当前场景中，父类最终是 object，通常没有额外逻辑。
        # 但保留这一行是标准写法，方便未来多继承或父类增加逻辑时不被跳过。
        super().__init_subclass__(**kwargs)

        parent_mapping_cls = next(
            # __mro__ 是 Method Resolution Order，类的方法解析顺序。
            # 如果未来是：
            # class ArmMessageMapping_V4(ArmMessageMapping_V3):
            #     ...
            # 那么大致是：
            # ArmMessageMapping_V4.__mro__ == (
            #     ArmMessageMapping_V4,
            #     ArmMessageMapping_V3,
            #     ArmMessageMapping,
            #     object
            # )
            # cls.__mro__[1:]
            # 表示跳过当前类自己，从父类开始查找。
            # 比如 V4：
            # cls.__mro__[1:] == (
            #     ArmMessageMapping_V3,
            #     ArmMessageMapping,
            #     object
            # )
            base for base in cls.__mro__[1:]
            # 只找有 id_to_type_mapping 的类。
            # 因为：
            # ArmMessageMapping_V3 有映射表。
            # ArmMessageMapping 有映射表。
            # object 没有映射表。
            if hasattr(base, "id_to_type_mapping")
            # next(...)
            # 找到第一个符合条件的父类。
            # 如果当前是 V4，且继承 V3：
            # parent_mapping_cls == ArmMessageMapping_V3
        )
        # 构造当前版本允许使用的 CAN ID 集合
        # 对字典直接 set(...)，得到的是字典的 key 集合
        valid_can_ids = set(parent_mapping_cls.id_to_type_mapping)
        # 把当前版本 CanIDPiper 中声明的 CAN ID 也加入合法集合
        valid_can_ids.update(item.value for item in cls.CanIDPiper)
        # 为当前版本创建一张新的映射表
        cls.id_to_type_mapping = {}
        for can_id, msg_type in parent_mapping_cls.id_to_type_mapping.items():
            # 在当前设计里，valid_can_ids 已经包含父版本所有 ID，所以一般不会触发。
            if can_id not in valid_can_ids:
                continue
            # 判断父版本的消息类型名称是否存在于当前版本的 ArmMsgType 中。
            if msg_type.name in cls.ArmMsgType.__members__:
                # 如果当前版本也有同名消息类型，则把父版本 enum 转换成当前版本 enum。
                # 例如：
                # 0x15A: ArmMsgType_V2.PiperMsgJointMitCtrl_1
                # 转换成：
                # 0x15A: ArmMsgType_V3.PiperMsgJointMitCtrl_1
                # 因为 V2 enum 和 V3 enum 是不同类型，即使名字一样，也不是同一个对象。
                cls.id_to_type_mapping[can_id] = cls.ArmMsgType[msg_type.name]
            else:
                cls.id_to_type_mapping[can_id] = msg_type
        # cls.xxx 会沿继承链查找，如果当前类没写，会拿到父类的配置。
        # 例如：
        # class V3:
        #     additional_mapping = {A}
        # class V4(V3):
        #     additional_mapping = {B}
        # 如果用 cls.additional_mapping，可能会混淆继承来的配置。
        # 用 cls.__dict__.get(...) 表示：
        # 当前类自己写了，就用当前类自己的。
        # 当前类没写，就用空集合或空字典。
        # 不会重复应用父类配置。
        removed_mapping_ids = cls.__dict__.get("removed_mapping_ids", set())
        changed_mapping_config = cls.__dict__.get("changed_mapping", {})
        additional_mapping_config = cls.__dict__.get("additional_mapping", {})

        for can_id in removed_mapping_ids:
            # pop(can_id, None) 的含义：
            # 如果存在这个 key，则删除。
            # 如果不存在，不报错，返回 None。
            cls.id_to_type_mapping.pop(can_id, None)

        changed_mapping = cls._normalize_mapping(changed_mapping_config, valid_can_ids)
        for changed_msg_type in changed_mapping.values():
            # 循环过程中会删除字典项,如果直接遍历字典同时删除,会报错,所以先转成列表，遍历的是快照。
            for can_id, msg_type in list(cls.id_to_type_mapping.items()):
                # 为什么用 name，不是直接比较 enum 对象？
                # 因为旧映射可能是父版本 enum,新映射可能是当前版本 enum,所以用名字判断同一个功能
                if msg_type.name == changed_msg_type.name:
                    cls.id_to_type_mapping.pop(can_id)
        cls.id_to_type_mapping.update(changed_mapping)

        cls.id_to_type_mapping.update(
            cls._normalize_mapping(additional_mapping_config, valid_can_ids)
        )

        cls.type_to_id_mapping = {v: k for k, v in cls.id_to_type_mapping.items()}

    @classmethod
    def _normalize_mapping(cls, mapping, valid_can_ids):
        normalized_mapping = {}
        for can_id, msg_type in mapping.items():
            if can_id not in valid_can_ids:
                raise ValueError(f"CAN ID {can_id} 未在 {cls.CanIDPiper.__name__} 中声明")

            msg_type_name = msg_type if isinstance(msg_type, str) else msg_type.name
            if msg_type_name not in cls.ArmMsgType.__members__:
                raise ValueError(f"消息类型 {msg_type_name} 未在 {cls.ArmMsgType.__name__} 中声明")

            normalized_mapping[can_id] = cls.ArmMsgType[msg_type_name]

        return normalized_mapping
    
    # 初始化映射字典
    id_to_type_mapping = {
        # 反馈,feedback
        CanIDPiper.ARM_STATUS_FEEDBACK.value: ArmMsgType.PiperMsgStatusFeedback,
        CanIDPiper.ARM_END_POSE_FEEDBACK_1.value: ArmMsgType.PiperMsgEndPoseFeedback_1,
        CanIDPiper.ARM_END_POSE_FEEDBACK_2.value: ArmMsgType.PiperMsgEndPoseFeedback_2,
        CanIDPiper.ARM_END_POSE_FEEDBACK_3.value: ArmMsgType.PiperMsgEndPoseFeedback_3,
        CanIDPiper.ARM_JOINT_FEEDBACK_12.value: ArmMsgType.PiperMsgJointFeedBack_12,
        CanIDPiper.ARM_JOINT_FEEDBACK_34.value: ArmMsgType.PiperMsgJointFeedBack_34,
        CanIDPiper.ARM_JOINT_FEEDBACK_56.value: ArmMsgType.PiperMsgJointFeedBack_56,
        CanIDPiper.ARM_GRIPPER_FEEDBACK.value: ArmMsgType.PiperMsgGripperFeedBack,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_1.value: ArmMsgType.PiperMsgHighSpdFeed_1,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_2.value: ArmMsgType.PiperMsgHighSpdFeed_2,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_3.value: ArmMsgType.PiperMsgHighSpdFeed_3,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_4.value: ArmMsgType.PiperMsgHighSpdFeed_4,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_5.value: ArmMsgType.PiperMsgHighSpdFeed_5,
        CanIDPiper.ARM_INFO_HIGH_SPD_FEEDBACK_6.value: ArmMsgType.PiperMsgHighSpdFeed_6,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_1.value: ArmMsgType.PiperMsgLowSpdFeed_1,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_2.value: ArmMsgType.PiperMsgLowSpdFeed_2,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_3.value: ArmMsgType.PiperMsgLowSpdFeed_3,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_4.value: ArmMsgType.PiperMsgLowSpdFeed_4,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_5.value: ArmMsgType.PiperMsgLowSpdFeed_5,
        CanIDPiper.ARM_INFO_LOW_SPD_FEEDBACK_6.value: ArmMsgType.PiperMsgLowSpdFeed_6,
        # 发送,transmit
        CanIDPiper.ARM_MOTION_CTRL_1.value: ArmMsgType.PiperMsgMotionCtrl_1,
        # CanIDPiper.ARM_STOP_CTRL.value: ArmMsgType.PiperMsgStopCtrl,
        # CanIDPiper.ARM_TRACK_CTRL.value: ArmMsgType.PiperMsgTrackCtrl,
        # CanIDPiper.ARM_GRAG_TEACH_CTRL.value: ArmMsgType.PiperMsgGragTeachCtrl,
        CanIDPiper.ARM_MOTION_CTRL_2.value: ArmMsgType.PiperMsgMotionCtrl_2,
        # CanIDPiper.ARM_MODE_CTRL.value: ArmMsgType.PiperMsgModeCtrl,
        # CanIDPiper.ARM_MOVE_MODE_CTRL.value: ArmMsgType.PiperMsgMoveModeCtrl,
        # CanIDPiper.ARM_MOVE_SPD_RATE_CTRL.value: ArmMsgType.PiperMsgMoveSpdRateCtrl,
        CanIDPiper.ARM_MOTION_CTRL_CARTESIAN_1.value: ArmMsgType.PiperMsgMotionCtrlCartesian_1,
        CanIDPiper.ARM_MOTION_CTRL_CARTESIAN_2.value: ArmMsgType.PiperMsgMotionCtrlCartesian_2,
        CanIDPiper.ARM_MOTION_CTRL_CARTESIAN_3.value: ArmMsgType.PiperMsgMotionCtrlCartesian_3,
        CanIDPiper.ARM_JOINT_CTRL_12.value: ArmMsgType.PiperMsgJointCtrl_12,
        CanIDPiper.ARM_JOINT_CTRL_34.value: ArmMsgType.PiperMsgJointCtrl_34,
        CanIDPiper.ARM_JOINT_CTRL_56.value: ArmMsgType.PiperMsgJointCtrl_56,
        CanIDPiper.ARM_CIRCULAR_PATTERN_COORD_NUM_UPDATE_CTRL.value: ArmMsgType.PiperMsgCircularPatternCoordNumUpdateCtrl,
        CanIDPiper.ARM_GRIPPER_CTRL.value: ArmMsgType.PiperMsgGripperCtrl,
        #----------------------------------基于V1.5-2版本后---------------------------------------------#
        CanIDPiper.ARM_JOINT_MIT_CTRL_1.value: ArmMsgType.PiperMsgJointMitCtrl_1,
        CanIDPiper.ARM_JOINT_MIT_CTRL_2.value: ArmMsgType.PiperMsgJointMitCtrl_2,
        CanIDPiper.ARM_JOINT_MIT_CTRL_3.value: ArmMsgType.PiperMsgJointMitCtrl_3,
        CanIDPiper.ARM_JOINT_MIT_CTRL_4.value: ArmMsgType.PiperMsgJointMitCtrl_4,
        CanIDPiper.ARM_JOINT_MIT_CTRL_5.value: ArmMsgType.PiperMsgJointMitCtrl_5,
        CanIDPiper.ARM_JOINT_MIT_CTRL_6.value: ArmMsgType.PiperMsgJointMitCtrl_6,
        #---------------------------------------------------------------------------------------------#
        CanIDPiper.ARM_MASTER_SLAVE_MODE_CONFIG.value: ArmMsgType.PiperMsgMasterSlaveModeConfig,
        # CanIDPiper.ARM_MS_LINKAGE_CONFIG.value: ArmMsgType.PiperMsgMSLinkageConfig,
        # CanIDPiper.ARM_MS_FEEDBACK_INSTRUCTION_OFFSET_CONFIG.value: ArmMsgType.PiperMsgMSFeedbackInstructionOffsetConfig,
        # CanIDPiper.ARM_MS_CTRL_INSTRUCTION_OFFSET_CONFIG.value: ArmMsgType.PiperMsgMSCtrlInstructionOffsetConfig,
        # CanIDPiper.ARM_MS_LINKAGE_CTRL_OFFSET_CONFIG.value: ArmMsgType.PiperMsgMSLinkageCtrlOffsetConfig,
        CanIDPiper.ARM_MOTOR_ENABLE_DISABLE_CONFIG.value: ArmMsgType.PiperMsgMotorEnableDisableConfig,
        # CanIDPiper.ARM_MOTOR_DISABLE_CONFIG.value: ArmMsgType.PiperMsgMotorDisableConfig,
        # CanIDPiper.ARM_SEARCH_MOTOR_ANGLE_CONFIG.value: ArmMsgType.PiperMsgSearchMotorAngleConfig,
        CanIDPiper.ARM_SEARCH_MOTOR_MAX_SPD_ACC_LIMIT.value: ArmMsgType.PiperMsgSearchMotorMaxAngleSpdAccLimit,
        # CanIDPiper.ARM_SEARCH_MOTOR_MAX_ACC_CONFIG.value: ArmMsgType.PiperMsgSearchMotorMaxAccConfig,
        CanIDPiper.ARM_FEEDBACK_CURRENT_MOTOR_ANGLE_LIMIT_MAX_SPD.value: ArmMsgType.PiperMsgFeedbackCurrentMotorAngleLimitMaxSpd,
        CanIDPiper.ARM_MOTOR_ANGLE_LIMIT_MAX_SPD_SET.value: ArmMsgType.PiperMsgMotorAngleLimitMaxSpdSet,
        CanIDPiper.ARM_JOINT_CONFIG.value: ArmMsgType.PiperMsgJointConfig,
        CanIDPiper.ARM_INSTRUCTION_RESPONSE_CONFIG.value: ArmMsgType.PiperMsgInstructionResponseConfig,
        CanIDPiper.ARM_FEEDBACK_RESP_SET_INSTRUCTION.value: ArmMsgType.PiperMsgFeedbackRespSetInstruction,
        CanIDPiper.ARM_PARAM_ENQUIRY_AND_CONFIG.value: ArmMsgType.PiperMsgParamEnquiryAndConfig,
        CanIDPiper.ARM_FEEDBACK_CURRENT_END_VEL_ACC_PARAM.value: ArmMsgType.PiperMsgFeedbackCurrentEndVelAccParam,
        CanIDPiper.ARM_END_VEL_ACC_PARAM_CONFIG.value: ArmMsgType.PiperMsgEndVelAccParamConfig,
        CanIDPiper.ARM_CRASH_PROTECTION_RATING_CONFIG.value: ArmMsgType.PiperMsgCrashProtectionRatingConfig,
        CanIDPiper.ARM_CRASH_PROTECTION_RATING_FEEDBACK.value: ArmMsgType.PiperMsgCrashProtectionRatingFeedback,
        CanIDPiper.ARM_FEEDBACK_CURRENT_MOTOR_MAX_ACC_LIMIT.value: ArmMsgType.PiperMsgFeedbackCurrentMotorMaxAccLimit,
        #----------------------------------基于V1.5-2版本后---------------------------------------------#
        CanIDPiper.ARM_GRIPPER_TEACHING_PENDANT_PARAM_CONFIG.value: ArmMsgType.PiperMsgGripperTeachingPendantParamConfig,
        CanIDPiper.ARM_GRIPPER_TEACHING_PENDANT_PARAM_FEEDBACK.value: ArmMsgType.PiperMsgGripperTeachingPendantParamFeedback,
        #---------------------------------------------------------------------------------------------#
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_1.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_1,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_2.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_2,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_3.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_3,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_4.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_4,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_5.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_5,
        CanIDPiper.ARM_FEEDBACK_JOINT_VEL_ACC_6.value: ArmMsgType.PiperMsgFeedbackJointVelAcc_6,
        CanIDPiper.ARM_LIGHT_CTRL.value: ArmMsgType.PiperMsgLightCtrl,
        CanIDPiper.ARM_CAN_UPDATE_SILENT_MODE_CONFIG.value: ArmMsgType.PiperMsgCanUpdateSilentModeConfig,
        CanIDPiper.ARM_FIRMWARE_READ.value: ArmMsgType.PiperMsgFirmwareRead,
    }

    type_to_id_mapping = {v: k for k, v in id_to_type_mapping.items()}

    @classmethod
    def get_mapping(cls, can_id: Optional[int] = None, msg_type: Optional[ArmMsgType] = None):
        '''
        根据输入的参数返回对应的映射值，输入 id 返回类型，输入类型返回 id
        
        :param can_id: CAN ID
        :param msg_type: 机械臂消息类型
        :return: 对应的类型或 id
        '''
        if can_id is not None and msg_type is not None:
            raise ValueError("只能输入 CAN ID 或消息类型中的一个")

        if can_id is not None:
            if can_id in cls.id_to_type_mapping:
                return cls.id_to_type_mapping[can_id]
            else:
                raise ValueError(f"CAN ID {can_id} 不在映射中")

        if msg_type is not None:
            if msg_type in cls.type_to_id_mapping:
                return cls.type_to_id_mapping[msg_type]
            else:
                raise ValueError(f"消息类型 {msg_type} 不在映射中")

        raise ValueError("必须输入 CAN ID 或消息类型中的一个")

# 测试代码
# if __name__ == "__main__":
#     # 根据 ID 查找类型
#     print(ArmMessageMapping.get_mapping(can_id=0x2A2))  # 输出: PiperMsgEndPoseFeedback_1 (0x2)

#     # 根据类型查找 ID
#     print(ArmMessageMapping.get_mapping(msg_type=ArmMsgType.PiperMsgJointFeedBack_56))  # 输出: 0x2A7
