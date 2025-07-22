from .fps import C_FPSCounter
from .tf import (
    quat_convert_euler,
    euler_convert_quat,
)

from .logger_mag import LogManager, LogLevel
import logging
global_area = "PIPER"
LogManager.init_logger(global_area=global_area, 
                    level=LogLevel.SILENT, 
                    log_to_file=False, 
                    log_file_name=None, 
                    log_file_path=None,
                    file_mode='w')
logger = LogManager.get_logger(global_area=global_area)

__all__ = [
    'C_FPSCounter',
    'quat_convert_euler',
    'euler_convert_quat',
    'logging',
    'LogManager',
    'LogLevel',
    'global_area',
    'logger',
]

