import unittest

import can

from piper_sdk.interface.piper_interface_v3 import C_PiperInterface_V3
from piper_sdk.piper_msgs.msg_v3 import ArmMsgType, PiperMessage
from piper_sdk.piper_msgs.msg_v3.feedback.arm_feedback_status import (
    ArmMsgFeedbackStatusEnum_V3,
)
from piper_sdk.piper_msgs.msg_v3.transmit.arm_joint_mit_ctrl import (
    ArmMsgJointMitCtrl_V3,
)
from piper_sdk.piper_msgs.msg_v3.transmit.arm_motion_ctrl_2 import (
    ArmMsgMotionCtrl_2_V3,
)
from piper_sdk.protocol.protocol_v3 import C_PiperParserV3


def _frame(arbitration_id, data):
    msg = can.Message(arbitration_id=arbitration_id, data=data, is_extended_id=False)
    msg.timestamp = 123.0
    return msg


class _FakeCan:
    class CAN_STATUS:
        SEND_MESSAGE_SUCCESS = object()

    def __init__(self):
        self.sent = None

    def SendCanMessage(self, arbitration_id, data):
        self.sent = (arbitration_id, bytes(data))
        return self.CAN_STATUS.SEND_MESSAGE_SUCCESS


class V3ProtocolRegressionTests(unittest.TestCase):
    def setUp(self):
        self.parser = C_PiperParserV3()

    def test_mit_encoder_packs_all_v3_bitfields(self):
        msg = PiperMessage(
            type_=ArmMsgType.PiperMsgJointMitCtrl_1,
            arm_joint_mit_ctrl=ArmMsgJointMitCtrl_V3(
                pos_ref=0x1234,
                vel_ref=0xABC,
                kp=0xDEF,
                kd=0x345,
                t_ref=0x678,
            ),
        )
        frame = can.Message(arbitration_id=0, data=[], is_extended_id=False)

        self.assertTrue(self.parser.EncodeMessage(msg, frame))
        self.assertEqual(list(frame.data), [0x12, 0x34, 0xAB, 0xCD, 0xEF, 0x34, 0x56, 0x78])

    def test_mit_interface_clamps_velocity_and_gains_before_encoding(self):
        interface = C_PiperInterface_V3("test-v3-mit-limits", can_auto_init=False)
        fake_can = _FakeCan()
        interface._arm_can = fake_can

        interface.JointMitCtrl(1, 0.0, 46.0, 501.0, 6.0, 17.0)

        self.assertEqual(fake_can.sent[0], 0x15A)
        self.assertEqual(list(fake_can.sent[1])[2:], [0xFF] * 6)

    def test_motion_control_v3_move_m_and_installation_position_encoding(self):
        msg = PiperMessage(
            type_=ArmMsgType.PiperMsgMotionCtrl_2,
            arm_motion_ctrl_2=ArmMsgMotionCtrl_2_V3(
                ctrl_mode=0x01,
                move_mode=0x06,
                move_spd_rate_ctrl=100,
                mit_mode=0xAD,
                installation_pos=0x04,
            ),
        )
        frame = can.Message(arbitration_id=0, data=[], is_extended_id=False)

        self.assertTrue(self.parser.EncodeMessage(msg, frame))
        self.assertEqual(frame.arbitration_id, 0x151)
        self.assertEqual(list(frame.data), [0x01, 0x06, 100, 0xAD, 0x00, 0x04, 0x00, 0x00])
        with self.assertRaises(ValueError):
            ArmMsgMotionCtrl_2_V3(installation_pos=0x05)

    def test_v3_status_decodes_move_m_feedback(self):
        msg = PiperMessage()

        self.assertTrue(self.parser.DecodeMessage(_frame(0x2A1, [0, 0, 6, 0, 0, 0, 0, 0]), msg))
        self.assertEqual(msg.arm_status_msgs.mode_feed, ArmMsgFeedbackStatusEnum_V3.ModeFeed.MOVE_M)

    def test_v3_ik_feedback_frames_decode_joint_pairs(self):
        cases = (
            (0x2AA, [1, 2]),
            (0x2AB, [3, 4]),
            (0x2AC, [5, 6]),
        )

        for arbitration_id, expected in cases:
            msg = PiperMessage()
            data = [0, 0, 0, expected[0], 0, 0, 0, expected[1]]

            self.assertTrue(self.parser.DecodeMessage(_frame(arbitration_id, data), msg))
            feedback = msg.arm_ik_joint_feedback
            self.assertIn(expected[0], vars(feedback).values())
            self.assertIn(expected[1], vars(feedback).values())
