import logging
import os
import threading
import datetime
from enum import IntEnum

class LogLevel(IntEnum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
    SILENT = 100  # 自定义等级：屏蔽所有终端输出

class ContextLoggerAdapter(logging.LoggerAdapter):
    def __init__(self, logger, extra):
        super().__init__(logger, extra)

    def process(self, msg, kwargs):
        kwargs["extra"] = self.extra
        return msg, kwargs

class LogManager:
    _instances = {}
    _lock = threading.Lock()

    @classmethod
    def init_logger(cls,
                    global_area='global_area',
                    level=LogLevel.INFO,
                    log_to_file=False,
                    log_file_name=None,
                    log_file_path=None,
                    file_mode='w'):
        with cls._lock:
            if global_area in cls._instances:
                return

            if log_file_name is None:
                log_file_name = global_area

            if not isinstance(level, LogLevel):
                raise ValueError(f"Logger '{global_area}' '{level}' is not 'LogLevel' Type ")
            
            # if log_file_path is None:
            #     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            #     log_dir = os.path.join(base_dir, 'log')
            #     os.makedirs(log_dir, exist_ok=True)
            #     log_file_path = os.path.join(log_dir, f'{log_file_name}.log')
            if log_file_path is None:
                now_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                log_dir = os.path.join(base_dir, 'log', now_str)
                if(log_to_file):
                    os.makedirs(log_dir, exist_ok=True)
                log_file_path = os.path.join(log_dir, f'{log_file_name}.log')
            
            logger = logging.getLogger(global_area)
            logger.setLevel(logging.DEBUG)
            logger.propagate = False

            formatter = logging.Formatter(
                '[%(asctime)s] [%(levelname)s] [%(global_area)s] [%(local_area)s] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

            # 控制台 handler
            # if level < LogLevel.SILENT:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

            # 文件 handler
            file_handler = None
            if log_to_file:
                file_handler = logging.FileHandler(log_file_path, encoding='utf-8', mode=file_mode)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
    
            cls._instances[global_area] = {
                'logger': logger,
                "level":level,
                "stream_handler": stream_handler,  # 记录 stream handler
                "log_file_name": log_file_name,
                "log_file_path": log_file_path,
                "file_handler": file_handler,
                "file_mode":file_mode,
                'global_area': global_area,
                'local_area': 'local_area'
            }

    @classmethod
    def update_logger(cls,
                    global_area:str='global_area',
                    local_area:str=None,
                    level:LogLevel=None,
                    log_to_file=None,
                    log_file_name=None,
                    log_file_path=None,
                    file_mode=None,
                    force_update=False):
        with cls._lock:
            if global_area not in cls._instances:
                raise RuntimeError(f"Logger '{global_area}' not initialized.")

            instance = cls._instances[global_area]
            logger:logging.Logger = instance['logger']
            original_level = instance.get("level")
            stream_handler:logging.StreamHandler = instance.get("stream_handler")
            file_handler:logging.FileHandler = instance.get("file_handler")
            file_mode_instance:str = instance.get("file_mode")
            adapter = ContextLoggerAdapter(logger, {
                "global_area": global_area,
                "local_area": 'LOGGER'
            })
            if local_area is not None:
                instance['local_area'] = local_area
            else: 
                raise ValueError(f"Logger '{local_area}' not be None")

            if level is not None and isinstance(level, LogLevel):
                if original_level != level:
                    adapter.warning(
                        f"Log level update from '{logging.getLevelName(original_level)}' "
                        f"to '{logging.getLevelName(level)}' for logger '{global_area}'."
                    )
                instance["level"] = level

            if stream_handler:
                stream_handler.setLevel(instance.get("level"))

            # 文件 handler 逻辑处理
            skip = False
            if log_to_file:
                os.makedirs(os.path.dirname(instance["log_file_path"]), exist_ok=True)
                if log_file_name is not None:
                    instance["log_file_name"] = log_file_name
                if log_file_path is not None:
                    instance["log_file_path"] = log_file_path
                if file_mode is not None:
                    instance["file_mode"] = file_mode

                # 如果已有文件 handler
                if file_handler:
                    # 若不强制更新，检测不支持动态更新的参数是否被修改
                    if not force_update:
                        # 修改记录的log等级
                        file_handler.setLevel(instance.get("level"))
                        if (instance["file_mode"] != file_mode_instance):
                            adapter.warning(f"Attempt to update FileHandler with non-dynamic fields (file_mode). "
                                            f"Because force_update=False. Will Skipping (file_mode) update...")
                            skip = True
                        if (instance["log_file_path"] != file_handler.baseFilename):
                            adapter.warning(f"Attempt to update FileHandler with non-dynamic fields (log_file_path). "
                                            f"Because force_update=False. Will Skipping (log_file_path) update...")
                            skip = True
                        if skip:
                            return
                    else:
                        if (instance["file_mode"] != file_mode_instance or instance["log_file_path"] != file_handler.baseFilename):
                            adapter.debug(f"You are force-updating file handler")
                            # 强制更新，删除旧 handler，重建
                            if(instance["file_mode"] == 'w'):
                                adapter.warning(f"You are force-updating file handler with mode='w'"
                                                f"This will overwrite the existing log file.")
                            logger.removeHandler(file_handler)
                            file_handler = logging.FileHandler(instance["log_file_path"], encoding='utf-8', mode=instance["file_mode"])
                            file_handler.setLevel(instance.get("level"))
                            formatter = logging.Formatter(
                                '[%(asctime)s] [%(levelname)s] [%(global_area)s] [%(local_area)s] %(message)s',
                                datefmt='%Y-%m-%d %H:%M:%S'
                            )
                            file_handler.setFormatter(formatter)
                            logger.addHandler(file_handler)
                            instance['file_handler'] = file_handler
                else:
                    # 没有旧 handler，直接添加
                    file_handler = logging.FileHandler(instance["log_file_path"], encoding='utf-8', mode=instance["file_mode"])
                    file_handler.setLevel(instance.get("level"))
                    formatter = logging.Formatter(
                        '[%(asctime)s] [%(levelname)s] [%(global_area)s] [%(local_area)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S'
                    )
                    file_handler.setFormatter(formatter)
                    logger.addHandler(file_handler)
                    instance['file_handler'] = file_handler

    # @classmethod
    # def get_logger(cls, global_area='global_area'):
    #     if global_area not in cls._instances:
    #         raise RuntimeError(f"Logger '{global_area}' not initialized.")
    #     instance = cls._instances[global_area]
    #     logger = instance['logger']
    #     return ContextLoggerAdapter(logger, {
    #         'global_area': instance['global_area'],
    #         'local_area': instance['local_area']
    #     })
    @classmethod
    def get_logger(cls, global_area='global_area', local_area=None):
        if global_area not in cls._instances:
            raise RuntimeError(f"Logger '{global_area}' not initialized.")
        instance = cls._instances[global_area]
        return ContextLoggerAdapter(instance['logger'], {
            'global_area': instance['global_area'],
            'local_area': local_area or instance['local_area']
        })


    # @classmethod
    # def clear_log_files(cls):
    #     """清除所有 .log 文件(保留 __init__.py)"""
    #     base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #     log_dir = os.path.join(base_dir, 'log')
    #     if not os.path.exists(log_dir):
    #         return
    #     for f in os.listdir(log_dir):
    #         file_path = os.path.join(log_dir, f)
    #         if f.endswith('.log') and os.path.isfile(file_path):
    #             os.remove(file_path)
    @classmethod
    def clear_log_files(cls):
        """清除所有 .log 文件和空日志文件夹（保留 __init__.py）"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_base_dir = os.path.join(base_dir, 'log')
        if not os.path.exists(log_base_dir):
            return

        for root, dirs, files in os.walk(log_base_dir, topdown=False):
            for f in files:
                if f.endswith('.log'):
                    os.remove(os.path.join(root, f))
            # 如果子目录为空（删除完日志文件），就移除它
            if not os.listdir(root):
                os.rmdir(root)

    
    @classmethod
    def get_log_file_path(cls, global_area:str='global_area',):
        instance = cls._instances[global_area]
        return instance["log_file_path"]
    

# logger_mag_file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print(logger_mag_file_dir)
# log_dir = os.path.join(logger_mag_file_dir, 'log')
# print(os.path.exists(log_dir))

# base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# log_dir = os.path.join(base_dir, 'log')
# print(log_dir)
# LogManager.init_logger(global_area="PIPER", level=LogLevel.WARNING, log_to_file=False, file_mode='a')
# logger = LogManager.get_logger(global_area="PIPER")
# print(LogManager.get_log_file_path("PIPER"))
# logger.error("This is a message from SubModule1.")
# LogManager.update_logger(global_area="PIPER",local_area="SubModule1", level=LogLevel.DEBUG, log_to_file=True,file_mode='w',force_update=True)
# logger = LogManager.get_logger(global_area="PIPER")
# logger.info("This is a message from SubModule111111.")
# LogManager.update_logger(global_area="PIPER",local_area="SubModule2", level=LogLevel.DEBUG, log_to_file=True,file_mode='a',force_update=True)
# logger = LogManager.get_logger(global_area="PIPER")
# a=2
# logger.error(f"'This is a message from SubModule222222.',{a}")
# LogManager.clear_log_files()

