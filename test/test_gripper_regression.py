import threading
import unittest

import can

from piper_sdk.interface.piper_interface_v2 import C_PiperInterface_V2
from piper_sdk.interface.piper_interface_v3 import C_PiperInterface_V3
from piper_sdk.piper_msgs.msg_v2.feedback.arm_feedback_gripper import ArmMsgFeedBackGripper
from piper_sdk.piper_msgs.msg_v3 import PiperMessage
from piper_sdk.piper_msgs.msg_v3.feedback.arm_feedback_gripper import (
    ArmMsgFeedBackGripper_V3,
    ArmMsgFeedbackGripperEnums_V3,
)
from piper_sdk.piper_param.piper_param_manager import C_PiperParamManager
from piper_sdk.protocol.protocol_v3 import C_PiperParserV3


def _frame(arbitration_id, data):
    msg = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    msg.timestamp = 123.0
    return msg


class MessageExportTests(unittest.TestCase):
    def test_top_level_messages_keep_v2_default_and_expose_versioned_aliases(self):
        import piper_sdk
        from piper_sdk.piper_msgs.msg_v2 import ArmMessageMapping as ArmMessageMapping_V2
        from piper_sdk.piper_msgs.msg_v2 import ArmMsgFeedbackStatusEnum as ArmMsgFeedbackStatusEnum_V2
        from piper_sdk.piper_msgs.msg_v2 import ArmMsgType as ArmMsgType_V2
        from piper_sdk.piper_msgs.msg_v2 import CanIDPiper as CanIDPiper_V2
        from piper_sdk.piper_msgs.msg_v2 import PiperMessage as PiperMessage_V2
        from piper_sdk.piper_msgs.msg_v3 import ArmMessageMapping as ArmMessageMapping_V3
        from piper_sdk.piper_msgs.msg_v3 import ArmMsgFeedbackStatusEnum as ArmMsgFeedbackStatusEnum_V3
        from piper_sdk.piper_msgs.msg_v3 import ArmMsgType as ArmMsgType_V3
        from piper_sdk.piper_msgs.msg_v3 import CanIDPiper as CanIDPiper_V3
        from piper_sdk.piper_msgs.msg_v3 import PiperMessage as PiperMessage_V3

        self.assertIs(piper_sdk.PiperMessage, PiperMessage_V2)
        self.assertIsNot(piper_sdk.PiperMessage, PiperMessage_V3)
        self.assertIs(piper_sdk.PiperMessage_V2, PiperMessage_V2)
        self.assertIs(piper_sdk.PiperMessage_V3, PiperMessage_V3)
        self.assertIs(piper_sdk.CanIDPiper, CanIDPiper_V2)
        self.assertIs(piper_sdk.CanIDPiper_V2, CanIDPiper_V2)
        self.assertIs(piper_sdk.CanIDPiper_V3, CanIDPiper_V3)
        self.assertIs(piper_sdk.ArmMsgType, ArmMsgType_V2)
        self.assertIs(piper_sdk.ArmMsgType_V2, ArmMsgType_V2)
        self.assertIs(piper_sdk.ArmMsgType_V3, ArmMsgType_V3)
        self.assertFalse(hasattr(piper_sdk, "ArmMessageMapping"))
        self.assertIs(piper_sdk.ArmMessageMapping_V2, ArmMessageMapping_V2)
        self.assertIs(piper_sdk.ArmMessageMapping_V3, ArmMessageMapping_V3)
        self.assertIs(piper_sdk.ArmMsgFeedbackStatusEnum, ArmMsgFeedbackStatusEnum_V2)
        self.assertIs(piper_sdk.ArmMsgFeedbackStatusEnum_V2, ArmMsgFeedbackStatusEnum_V2)
        self.assertIs(piper_sdk.ArmMsgFeedbackStatusEnum_V3, ArmMsgFeedbackStatusEnum_V3)
        self.assertEqual(piper_sdk.ArmMsgFeedbackStatusEnum.ModeFeed.MOVE_M, 0x04)
        self.assertEqual(piper_sdk.ArmMsgFeedbackStatusEnum_V3.ModeFeed.MOVE_M, 0x06)


class GripperFeedbackStatusTests(unittest.TestCase):
    def test_v2_feedback_constructor_updates_foc_status(self):
        feedback = ArmMsgFeedBackGripper(status_code=0x40)

        self.assertEqual(feedback.status_code, 0x40)
        self.assertTrue(feedback.foc_status.driver_enable_status)
        self.assertFalse(feedback.foc_status.homing_status)

    def test_v3_feedback_constructor_updates_foc_status(self):
        feedback = ArmMsgFeedBackGripper_V3(status_code=0xC0)

        self.assertEqual(feedback.status_code, 0xC0)
        self.assertTrue(feedback.foc_status.driver_enable_status)
        self.assertTrue(feedback.foc_status.homing_status)


class GripperV3ProtocolTests(unittest.TestCase):
    def test_decode_feedback_width_and_angle_modes(self):
        parser = C_PiperParserV3()

        width_msg = PiperMessage()
        width_ok = parser.DecodeMessage(
            _frame(0x2A8, [0x00, 0x00, 0x00, 0x0A, 0x00, 0x05, 0x40, 0x00]),
            width_msg,
        )
        self.assertTrue(width_ok)
        self.assertEqual(width_msg.gripper_feedback_v3.grippers_val, 10)
        self.assertEqual(width_msg.gripper_feedback_v3.grippers_effort, 5)
        self.assertEqual(width_msg.gripper_feedback_v3.status_code, 0x40)
        self.assertEqual(
            width_msg.gripper_feedback_v3.mode,
            ArmMsgFeedbackGripperEnums_V3.CtrlMode.WIDTH,
        )
        self.assertTrue(width_msg.gripper_feedback_v3.foc_status.driver_enable_status)

        angle_msg = PiperMessage()
        angle_ok = parser.DecodeMessage(
            _frame(0x2A8, [0x00, 0x00, 0x00, 0x14, 0x00, 0x06, 0x80, 0x01]),
            angle_msg,
        )
        self.assertTrue(angle_ok)
        self.assertEqual(angle_msg.gripper_feedback_v3.grippers_val, 20)
        self.assertEqual(angle_msg.gripper_feedback_v3.grippers_effort, 6)
        self.assertEqual(angle_msg.gripper_feedback_v3.status_code, 0x80)
        self.assertEqual(
            angle_msg.gripper_feedback_v3.mode,
            ArmMsgFeedbackGripperEnums_V3.CtrlMode.ANGLE,
        )
        self.assertTrue(angle_msg.gripper_feedback_v3.foc_status.homing_status)

    def test_interface_updates_feedback_and_all_control_codes(self):
        interface = C_PiperInterface_V3("test-v3-gripper-frames", can_auto_init=False)

        interface.ParseCANFrame(
            _frame(0x2A8, [0x00, 0x00, 0x00, 0x0A, 0x00, 0x05, 0x40, 0x00])
        )
        feedback = interface.GetArmGripperMsgs_V3().gripper_state
        self.assertEqual(feedback.grippers_val, 10)
        self.assertEqual(feedback.mode, ArmMsgFeedbackGripperEnums_V3.CtrlMode.WIDTH)
        self.assertTrue(feedback.foc_status.driver_enable_status)

        for code in range(0x08):
            value = code + 1
            interface.ParseCANFrame(
                _frame(0x159, [0x00, 0x00, 0x00, value, 0x00, 0x01, code, 0x00])
            )
            control = interface.GetArmGripperCtrl_V3().gripper_ctrl
            self.assertEqual(control.grippers_val, value)
            self.assertEqual(control.grippers_effort, 1)
            self.assertEqual(control.status_code, code)


class GripperLimitParameterTests(unittest.TestCase):
    def test_parameter_manager_instances_are_isolated(self):
        first = C_PiperParamManager()
        second = C_PiperParamManager()

        first.SetGripperRangeParam(0.0, 0.05)

        self.assertIsNot(first, second)
        self.assertEqual(first.GetGripperRangeParam(), (0.0, 0.05))
        self.assertEqual(second.GetGripperRangeParam(), (0.0, 0.07))

    def test_parameter_validation_rejects_invalid_values(self):
        manager = C_PiperParamManager()

        with self.assertRaises(ValueError):
            manager.SetJointLimitParam("j1", float("nan"), 1.0)
        with self.assertRaises(ValueError):
            manager.SetGripperRangeParam(0.0, float("inf"))
        with self.assertRaises(ValueError):
            manager.SetGripperRangeParam(-1.0, 1.0)
        with self.assertRaises(ValueError):
            manager.SetGripperRangeParam(2.0, 1.0)
        with self.assertRaises(TypeError):
            manager.SetGripperAngleLimitParam(True, 1.0)
        with self.assertRaises(TypeError):
            manager.SetGripperAngleLimitParam("0", 1.0)

        manager.SetGripperAngleLimitParam(-180.0, 180.0)
        self.assertEqual(manager.GetGripperAngleLimitParam(), (-180.0, 180.0))

    def test_gripper_limit_default_off_and_enabled_modes(self):
        default_off = C_PiperInterface_V2("test-limit-default-off", can_auto_init=False)
        default_off.SetSDKGripperRangeParam(0.0, 0.07)
        self.assertEqual(default_off._CalGripperSDKLimit(200000), 200000)

        width_limited = C_PiperInterface_V2(
            "test-limit-width-on", can_auto_init=False, start_sdk_gripper_limit=True
        )
        width_limited.SetSDKGripperRangeParam(0.0, 0.07)
        self.assertEqual(width_limited._CalGripperSDKLimit(200000), 70000)
        self.assertEqual(width_limited._CalGripperSDKLimit(-1), 0)

        v3_limited = C_PiperInterface_V3(
            "test-limit-v3-on", can_auto_init=False, start_sdk_gripper_limit=True
        )
        v3_limited.SetSDKGripperRangeParam(0.0, 0.07)
        v3_limited.SetSDKGripperAngleLimitParam(-90.0, 90.0)
        self.assertEqual(v3_limited._CalGripperSDKLimit(200000, 0), 70000)
        self.assertEqual(v3_limited._CalGripperSDKLimit(100000, 1), 90000)
        self.assertEqual(v3_limited._CalGripperSDKLimit(-100000, 1), -90000)


class GripperTxMessageThreadingTests(unittest.TestCase):
    def test_tx_msg_is_reused_per_thread_and_isolated_between_threads_v2(self):
        interface = C_PiperInterface_V2("test-tx-thread-v2", can_auto_init=False)
        main_msg = interface.tx_msg

        thread_messages = []

        def collect_messages():
            thread_messages.append(interface.tx_msg)
            thread_messages.append(interface.tx_msg)

        worker = threading.Thread(target=collect_messages)
        worker.start()
        worker.join()

        self.assertIs(main_msg, interface.tx_msg)
        self.assertIs(thread_messages[0], thread_messages[1])
        self.assertIsNot(main_msg, thread_messages[0])

    def test_tx_msg_is_reused_per_thread_and_isolated_between_threads_v3(self):
        interface = C_PiperInterface_V3("test-tx-thread-v3", can_auto_init=False)
        main_msg = interface.tx_msg

        thread_messages = []

        def collect_messages():
            thread_messages.append(interface.tx_msg)
            thread_messages.append(interface.tx_msg)

        worker = threading.Thread(target=collect_messages)
        worker.start()
        worker.join()

        self.assertIs(main_msg, interface.tx_msg)
        self.assertIs(thread_messages[0], thread_messages[1])
        self.assertIsNot(main_msg, thread_messages[0])


if __name__ == "__main__":
    unittest.main()
