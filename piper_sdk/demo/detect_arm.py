# terminal_monitor.py
# python3 piper_sdk/demo/detect_arm.py --can_port can0 --hz 10 --req_flag 0
# python3 piper_sdk/demo/detect_arm.py --can_port can0 --hz 10 --req_flag 1
import time
import argparse
from enum import Enum, auto
import os
import sys
import threading
from piper_sdk import *
# Windows 和 Unix 不同的键盘输入方式
try:
    import termios
    import tty
except ImportError:
    import msvcrt

parser = argparse.ArgumentParser(description="Piper Terminal Table Monitor")
parser.add_argument("--can_port", type=str, default="can0", help="CAN port name")
parser.add_argument("--hz", type=float, default=10, help="Refresh rate (Hz), range: 0.5 ~ 200")
parser.add_argument("--req_flag", type=int, default=1, help=", 0 or 1")
args = parser.parse_args()

exit_flag = False

piper = C_PiperInterface_V2(args.can_port)
piper.ConnectPort()

def clamp_refresh_rate(rate_hz):
    return max(0.5, min(rate_hz, 200.0))

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def key_listener():
    global exit_flag
    if os.name == 'nt':
        while True:
            if msvcrt.kbhit():
                if msvcrt.getch().lower() == b'q':
                    exit_flag = True
                    print("exit...")
                    break
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                if sys.stdin.read(1).lower() == 'q':
                    exit_flag = True
                    print("exit...")
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

class ArmStatusTool():
    class CtrlMode(Enum):
        Standby = 0x00
        Can_ctrl = 0x01
        Teaching_mode = 0x02
        Ethernet_control_mode = 0x03
        WiFi_control_mode = 0x04
        Remote_control_mode = 0x05
        Linkage_teaching_input_mode = 0x06
        Offline_trajectory_mode = 0x07
        def __str__(self):
            return f"{self.name} (0x{self.value:X})"
        def __repr__(self):
            return f"{self.name}: 0x{self.value:X}"
        @classmethod
        def from_value(cls, val):
            if isinstance(val, str):
                val = int(val, 0)  # 自动识别 '0x02'、'02'、'2' 等形式
            return cls(val)
    class ArmStatus(Enum):
        Normal = 0x00
        Emergency_stop = 0x01
        No_solution = 0x02
        Singularity_point = 0x03
        Target_angle_exceeds_limit = 0x04
        Joint_communication_err = 0x05
        Joint_brake_not_released = 0x06
        Collision_occurred = 0x07
        Overspeed_during_teaching_drag = 0x08
        Joint_status_err = 0x09
        Other_err = 0x0A
        Teaching_record = 0x0B
        Teaching_execution = 0x0C
        Teaching_pause = 0x0D
        Main_controller_NTC_over_temperature = 0x0E
        Release_resistor_NTC_over_temperature = 0x0F
        def __str__(self):
            return f"{self.name} (0x{self.value:X})"
        def __repr__(self):
            return f"{self.name}: 0x{self.value:X}"
        @classmethod
        def from_value(cls, val):
            if isinstance(val, str):
                val = int(val, 0)  # 自动识别 '0x02'、'02'、'2' 等形式
            return cls(val)
    class ModeFeed(Enum):
        MOVE_P = 0x00
        MOVE_J = 0x01
        MOVE_L = 0x02
        MOVE_C = 0x03
        MOVE_M = 0x04
        MOVE_CPV = 0x05
        def __str__(self):
            return f"{self.name} (0x{self.value:X})"
        def __repr__(self):
            return f"{self.name}: 0x{self.value:X}"
        @classmethod
        def from_value(cls, val):
            if isinstance(val, str):
                val = int(val, 0)  # 自动识别 '0x02'、'02'、'2' 等形式
            return cls(val)
    class MotionStatus(Enum):
        Reached_the_target_position = 0x00
        Not_yet_reached_the_target_position = 0x01
        def __str__(self):
            return f"{self.name} (0x{self.value:X})"
        def __repr__(self):
            return f"{self.name}: 0x{self.value:X}"
        @classmethod
        def from_value(cls, val):
            if isinstance(val, str):
                val = int(val, 0)  # 自动识别 '0x02'、'02'、'2' 等形式
            return cls(val)
    # def __str__(self):
    #     return f"{self.name} (0x{self.value:X})"
    # def __repr__(self):
    #     return f"{self.name}: 0x{self.value:X}"

def display_table(can_port, refresh_interval):
    global exit_flag
    global args
    listener_thread = threading.Thread(target=key_listener, daemon=True)
    listener_thread.start()
    last_time = 0
    hz = 1
    limit_interval = 1.0 / hz  # 最快 10Hz，即最小间隔 0.1s
    while not exit_flag:
        clear_terminal()
        start_time = time.time()

    # 如果距离上一次执行已超过限制间隔，就执行操作
        if start_time - last_time >= limit_interval:
            if(args.req_flag == 1):
                piper.SearchAllMotorMaxAngleSpd()
                piper.SearchAllMotorMaxAccLimit()
                piper.ArmParamEnquiryAndConfig(param_enquiry=0x02,
                                            param_setting=0x00,
                                            data_feedback_0x48x=0x00,
                                            end_load_param_setting_effective=0x00,
                                            set_end_load=0x03)
                piper.ArmParamEnquiryAndConfig(param_enquiry=0x04,
                                            param_setting=0x00,
                                            data_feedback_0x48x=0x00,
                                            end_load_param_setting_effective=0x00,
                                            set_end_load=0x03)
                piper.ArmParamEnquiryAndConfig(param_enquiry=0x01,
                                            param_setting=0x00,
                                            data_feedback_0x48x=0x00,
                                            end_load_param_setting_effective=0x00,
                                            set_end_load=0x03)
                if(piper.GetPiperFirmwareVersion() == -0x4AF):
                    piper.SearchPiperFirmwareVersion()
            last_time = start_time
        print(time.strftime("%a %b %d %H:%M:%S %Y"))
        # print(f"+{'-'*87}+")
        print(f"+{'='*107}+")
        print(f"Firmware Ver : {piper.GetPiperFirmwareVersion():<10}"
              f"\n"
              f"CAN PORT     : {can_port:<15}  SDK Ver: {piper.GetCurrentSDKVersion().value:<11}"
              f"\n"
              f"Interface Ver: {piper.GetCurrentInterfaceVersion().value:<15}  Protocol Ver: {piper.GetCurrentProtocolVersion().value:<15}"
              )
        print(f"+{'-'*107}+\n"
              f"{'ArmStatus'} :\n"
              f"{'ctrl_mode':<15}{ArmStatusTool.CtrlMode.from_value(piper.GetArmStatus().arm_status.ctrl_mode)}\n"
              f"{'arm_status':<15}{ArmStatusTool.ArmStatus.from_value(piper.GetArmStatus().arm_status.arm_status)}\n"
              f"{'mode_feed':<15}{ArmStatusTool.ModeFeed.from_value(piper.GetArmStatus().arm_status.mode_feed)}\n"
              f"{'motion_status':<15}{ArmStatusTool.MotionStatus.from_value(piper.GetArmStatus().arm_status.motion_status)}"
              )
        ##joint info
        # print(f"{'-'*50}")
        # print(f"         degree    angle_limit   max_spd max_acc")
        # print(f"Joint 1: {round(piper.GetArmJointMsgs().joint_state.joint_1*1e-3, 3):<7} [{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[1].min_angle_limit*1e-1,1):<6},{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[1].max_angle_limit*1e-1, 1):<6}]   {round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[1].max_joint_spd*1e-3, 3):<6}  {round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[1].max_joint_acc*1e-3, 3):<6}")
        # print(f"Joint 2: {round(piper.GetArmJointMsgs().joint_state.joint_2*1e-3, 3):<7} [{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[2].min_angle_limit*1e-1,1):<6},{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[2].max_angle_limit*1e-1, 1):<6}]   {round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[2].max_joint_spd*1e-3, 3):<6}  {round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[2].max_joint_acc*1e-3, 3):<6}")
        # print(f"Joint 3: {round(piper.GetArmJointMsgs().joint_state.joint_3*1e-3, 3):<7} [{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[3].min_angle_limit*1e-1,1):<6},{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[3].max_angle_limit*1e-1, 1):<6}]   {round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[3].max_joint_spd*1e-3, 3):<6}  {round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[3].max_joint_acc*1e-3, 3):<6}")
        # print(f"Joint 4: {round(piper.GetArmJointMsgs().joint_state.joint_4*1e-3, 3):<7} [{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[4].min_angle_limit*1e-1,1):<6},{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[4].max_angle_limit*1e-1, 1):<6}]   {round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[4].max_joint_spd*1e-3, 3):<6}  {round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[4].max_joint_acc*1e-3, 3):<6}")
        # print(f"Joint 5: {round(piper.GetArmJointMsgs().joint_state.joint_5*1e-3, 3):<7} [{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[5].min_angle_limit*1e-1,1):<6},{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[5].max_angle_limit*1e-1, 1):<6}]   {round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[5].max_joint_spd*1e-3, 3):<6}  {round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[5].max_joint_acc*1e-3, 3):<6}")
        # print(f"Joint 6: {round(piper.GetArmJointMsgs().joint_state.joint_6*1e-3, 3):<7} [{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[6].min_angle_limit*1e-1,1):<6},{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[6].max_angle_limit*1e-1, 1):<6}]   {round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[6].max_joint_spd*1e-3, 3):<6}  {round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[6].max_joint_acc*1e-3, 3):<6}")
        print(f"+{'-'*107}+\n"
              f"|{'JointState':<16}|{'J1':^15}{'J2':^15}{'J3':^15}{'J4':^15}{'J5':^15}{'J6':^15}|\n"
              f"+{'-'*16:^16}+{'-'*90:^}+\n"
              f"|{'position(°)':<16}|"
              f"{round(piper.GetArmJointMsgs().joint_state.joint_1*1e-3, 3):^15}"
              f"{round(piper.GetArmJointMsgs().joint_state.joint_2*1e-3, 3):^15}"
              f"{round(piper.GetArmJointMsgs().joint_state.joint_3*1e-3, 3):^15}"
              f"{round(piper.GetArmJointMsgs().joint_state.joint_4*1e-3, 3):^15}"
              f"{round(piper.GetArmJointMsgs().joint_state.joint_5*1e-3, 3):^15}"
              f"{round(piper.GetArmJointMsgs().joint_state.joint_6*1e-3, 3):^15}|\n"
              f"|{'position(rad)':<16}|"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_1.pos*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_2.pos*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_3.pos*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_4.pos*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_5.pos*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_6.pos*1e-3, 3):^15}|\n"
              f"|{'cur_spd(rad/s)':<16}|"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_1.motor_speed*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_2.motor_speed*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_3.motor_speed*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_4.motor_speed*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_5.motor_speed*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_6.motor_speed*1e-3, 3):^15}|\n"
              f"|{'current(A)':<16}|"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_1.current*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_2.current*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_3.current*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_4.current*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_5.current*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_6.current*1e-3, 3):^15}|\n"
              f"|{'effort(N.m)':<16}|"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_1.effort*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_2.effort*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_3.effort*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_4.effort*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_5.effort*1e-3, 3):^15}"
              f"{round(piper.GetArmHighSpdInfoMsgs().motor_6.effort*1e-3, 3):^15}|\n"
              f"|{'voltage(V)':<16}|"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_1.vol*1e-1, 1):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_2.vol*1e-1, 1):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_3.vol*1e-1, 1):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_4.vol*1e-1, 1):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_5.vol*1e-1, 1):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_6.vol*1e-1, 1):^15}|\n"
              f"|{'foc_temp(°C)':<16}|"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_1.foc_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_2.foc_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_3.foc_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_4.foc_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_5.foc_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_6.foc_temp):^15}|\n"
              f"|{'motor_temp(°C)':<16}|"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_1.motor_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_2.motor_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_3.motor_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_4.motor_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_5.motor_temp):^15}"
              f"{round(piper.GetArmLowSpdInfoMsgs().motor_6.motor_temp):^15}|\n"
              f"|{'max_spd(rad/s)':<16}|"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[1].max_joint_spd*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[2].max_joint_spd*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[3].max_joint_spd*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[4].max_joint_spd*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[5].max_joint_spd*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[6].max_joint_spd*1e-3, 3):^15}|\n"
              f"|{'max_acc(rad/s^2)':<16}|"
              f"{round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[1].max_joint_acc*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[2].max_joint_acc*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[3].max_joint_acc*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[4].max_joint_acc*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[5].max_joint_acc*1e-3, 3):^15}"
              f"{round(piper.GetAllMotorMaxAccLimit().all_motor_max_acc_limit.motor[6].max_joint_acc*1e-3, 3):^15}|\n"
              f"|{'collision_level':<16}|"
              f"{round(piper.GetCrashProtectionLevelFeedback().crash_protection_level_feedback.joint_1_protection_level):^15}"
              f"{round(piper.GetCrashProtectionLevelFeedback().crash_protection_level_feedback.joint_2_protection_level):^15}"
              f"{round(piper.GetCrashProtectionLevelFeedback().crash_protection_level_feedback.joint_3_protection_level):^15}"
              f"{round(piper.GetCrashProtectionLevelFeedback().crash_protection_level_feedback.joint_4_protection_level):^15}"
              f"{round(piper.GetCrashProtectionLevelFeedback().crash_protection_level_feedback.joint_5_protection_level):^15}"
              f"{round(piper.GetCrashProtectionLevelFeedback().crash_protection_level_feedback.joint_6_protection_level):^15}|\n"
              f"|{'angle_limit(°)':<16}|"
              f"[{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[1].min_angle_limit*1e-1,1):<6},"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[1].max_angle_limit*1e-1, 1):<6}]"
              f"[{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[2].min_angle_limit*1e-1,1):<6},"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[2].max_angle_limit*1e-1, 1):<6}]"
              f"[{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[3].min_angle_limit*1e-1,1):<6},"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[3].max_angle_limit*1e-1, 1):<6}]"
              f"[{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[4].min_angle_limit*1e-1,1):<6},"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[4].max_angle_limit*1e-1, 1):<6}]"
              f"[{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[5].min_angle_limit*1e-1,1):<6},"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[5].max_angle_limit*1e-1, 1):<6}]"
              f"[{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[6].min_angle_limit*1e-1,1):<6},"
              f"{round(piper.GetAllMotorAngleLimitMaxSpd().all_motor_angle_limit_max_spd.motor[6].max_angle_limit*1e-1, 1):<6}]|\n"
              f"|{'status----------':<16}|{'-'*90:^}|\n"
              f"|{'low_vol_err':<16}|"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.voltage_too_low):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.voltage_too_low):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.voltage_too_low):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.voltage_too_low):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.voltage_too_low):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.voltage_too_low):^15}|\n"
              f"|{'motor_overheat':<16}|"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.motor_overheating):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.motor_overheating):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.motor_overheating):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.motor_overheating):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.motor_overheating):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.motor_overheating):^15}|\n"
              f"|{'foc_overcurrent':<16}|"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_overcurrent):^15}|\n"
              f"|{'foc_overheat':<16}|"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_overcurrent):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_overcurrent):^15}|\n"
              f"|{'collision_status':<16}|"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.collision_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.collision_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.collision_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.collision_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.collision_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.collision_status):^15}|\n"
              f"|{'foc_err':<16}|"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_error_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_error_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_error_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_error_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_error_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_error_status):^15}|\n"
              f"|{'enable_status':<16}|"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.driver_enable_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.driver_enable_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.driver_enable_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.driver_enable_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.driver_enable_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.driver_enable_status):^15}|\n"
              f"|{'stall_protection':<16}|"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_1.foc_status.stall_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_2.foc_status.stall_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_3.foc_status.stall_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_4.foc_status.stall_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_5.foc_status.stall_status):^15}"
              f"{str(piper.GetArmLowSpdInfoMsgs().motor_6.foc_status.stall_status):^15}|\n"
              f"|{'commuciation_err':<16}|"
              f"{str(piper.GetArmStatus().arm_status.err_status.communication_status_joint_1):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.communication_status_joint_2):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.communication_status_joint_3):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.communication_status_joint_4):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.communication_status_joint_5):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.communication_status_joint_6):^15}|\n"
              f"|{'over_angle':<16}|"
              f"{str(piper.GetArmStatus().arm_status.err_status.joint_1_angle_limit):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.joint_2_angle_limit):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.joint_3_angle_limit):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.joint_4_angle_limit):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.joint_5_angle_limit):^15}"
              f"{str(piper.GetArmStatus().arm_status.err_status.joint_6_angle_limit):^15}|\n"
              f"+{'-'*107}+"
              )
        print(
              f"{'End Pose(Euler):':<108}|"
              f"\n"
              f"{'xyz(mm)':<12}"
              f"{round(piper.GetArmEndPoseMsgs().end_pose.X_axis*1e-3, 3):<9}"
              f"{round(piper.GetArmEndPoseMsgs().end_pose.Y_axis*1e-3, 3):<9}"
              f"{round(piper.GetArmEndPoseMsgs().end_pose.Z_axis*1e-3, 3):<9}|"
              f"{'max_linear_vel':^20}"
              f"{round(piper.GetCurrentEndVelAndAccParam().current_end_vel_acc_param.end_max_linear_vel*1e-3, 3):^7}"
              f"{'m/s':<5}|"
              f"{'max_angular_vel':^20}"
              f"{round(piper.GetCurrentEndVelAndAccParam().current_end_vel_acc_param.end_max_angular_vel*1e-3, 3):^7}"
              f"{'rad/s':<8}|"
              f"\n"
              f"{'rpy(degree)':<12}"
              f"{round(piper.GetArmEndPoseMsgs().end_pose.RX_axis*1e-3, 3):<9}"
              f"{round(piper.GetArmEndPoseMsgs().end_pose.RY_axis*1e-3, 3):<9}"
              f"{round(piper.GetArmEndPoseMsgs().end_pose.RZ_axis*1e-3, 3):<9}|"
              f"{'max_linear_acc':^20}"
              f"{round(piper.GetCurrentEndVelAndAccParam().current_end_vel_acc_param.end_max_linear_acc*1e-3, 3):^7}"
              f"{'m/s^2':<5}|"
              f"{'max_angular_acc':^20}"
              f"{round(piper.GetCurrentEndVelAndAccParam().current_end_vel_acc_param.end_max_angular_acc*1e-3, 3):^7}"
              f"{'rad/s^2':<8}|"
              )
        print(f"+{'-'*107}+\n"
              f"{'Gripper&Teaching':<108}|"
              
              f"\n"
              f"{'gripper_pos(mm)':<21}{round(piper.GetArmGripperMsgs().gripper_state.grippers_angle*1e-3, 3):<6}|"
              f"{'Status code :':<59}"
              f"{'|':>22}"
              f"\n"
              f"{'gripper_effort(N.m)':<21}{round(piper.GetArmGripperMsgs().gripper_state.grippers_effort*1e-3, 3):<6}|"
              f"{'voltage_too_low':<23}{str(piper.GetArmGripperMsgs().gripper_state.foc_status.voltage_too_low):<6}|"
              f"{'motor_overheating':<23}{str(piper.GetArmGripperMsgs().gripper_state.foc_status.motor_overheating):<6}"
              f"{'|':>22}"
              f"\n"
              f"{'teaching_per':<21}{piper.GetGripperTeachingPendantParamFeedback().arm_gripper_teaching_param_feedback.teaching_range_per:<6}|"
              f"{'driver_overcurrent':<23}{str(piper.GetArmGripperMsgs().gripper_state.foc_status.driver_overcurrent):<6}|"
              f"{'driver_overheating':<23}{str(piper.GetArmGripperMsgs().gripper_state.foc_status.driver_overheating):<6}"
              f"{'|':>22}"
              f"\n"
              f"{'max_range_config(mm)':<21}{piper.GetGripperTeachingPendantParamFeedback().arm_gripper_teaching_param_feedback.max_range_config:<6}|"
              f"{'sensor_status':<23}{str(piper.GetArmGripperMsgs().gripper_state.foc_status.sensor_status):<6}|"
              f"{'driver_error_status':<23}{str(piper.GetArmGripperMsgs().gripper_state.foc_status.driver_error_status):<6}"
                f"{'|':>22}"              
              f"\n"
              f"{'teaching_friction':<21}{piper.GetGripperTeachingPendantParamFeedback().arm_gripper_teaching_param_feedback.teaching_friction:<6}|"
              f"{'driver_enable_status':<23}{str(piper.GetArmGripperMsgs().gripper_state.foc_status.driver_enable_status):<6}|"
              f"{'homing_status':<23}{str(piper.GetArmGripperMsgs().gripper_state.foc_status.homing_status):<6}"
              f"{'|':>22}"
              )
        # 单独打印 FPS 类
        print(f"+{'='*52}FPS{'='*52}+\n"
              f"{'All FPS':<15}: {round(piper.GetCanFps())}\n"
              f"{'Arm Status':<15}: {round(piper.GetArmStatus().Hz):<5}  {'End Pose':<15}: {round(piper.GetArmEndPoseMsgs().Hz):<5}\n"
              f"{'Gripper Msg':<15}: {round(piper.GetArmGripperMsgs().Hz):<5}  {'High Spd Info':<15}: {round(piper.GetArmHighSpdInfoMsgs().Hz):<5}\n"
              f"{'Low Spd Info':<15}: {round(piper.GetArmLowSpdInfoMsgs().Hz):<5}\n"
              f"{'Joint Ctrl':<15}: {round(piper.GetArmJointCtrl().Hz):<5}  {'Gripper Ctrl':<15}: {round(piper.GetArmGripperCtrl().Hz):<5}\n"
              f"{'Mode Ctrl':<15}: {round(piper.GetArmModeCtrl().Hz):<5}")
        print("=" * 109)
        print("Press 'q' to quit")
        time.sleep(refresh_interval)

def main():
    hz = clamp_refresh_rate(args.hz)
    refresh_interval = 1.0 / hz
    display_table(args.can_port, refresh_interval)

if __name__ == "__main__":
    main()
