import logging
import os
from datetime import datetime
from typing import Optional


class LoggerManager:
    _instance = None
    _loggers = {}
    _log_path = None
    _file_handler = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(LoggerManager, cls).__new__(cls)
        return cls._instance

    def init(self, filename: Optional[str] = None, log_dir: Optional[str] = None, level=logging.INFO):
        """主入口调用：设置日志路径 + 替换已有 logger 的 FileHandler"""
        if self._initialized:
            return

        if log_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            log_dir = os.path.join(base_dir, "log")

        os.makedirs(log_dir, exist_ok=True)

        if filename:
            log_filename = filename + datetime.now().strftime("-%Y-%m-%d_%H-%M-%S") + ".log"
        else:
            log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"

        self._log_path = os.path.join(log_dir, log_filename)

        # 创建共享的 FileHandler
        self._file_handler = logging.FileHandler(self._log_path, encoding="utf-8")
        self._file_handler.setLevel(level)
        file_fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self._file_handler.setFormatter(file_fmt)

        # ✅ 替换之前已创建的 logger 的 FileHandler
        for logger in self._loggers.values():
            # 删除旧的 FileHandler
            logger.handlers = [h for h in logger.handlers if not isinstance(h, logging.FileHandler)]
            logger.addHandler(self._file_handler)

        self._initialized = True

    def get_logger(self, name: Optional[str] = None, level=logging.INFO):
        if name is None:
            name = "default"

        if name in self._loggers:
            return self._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.propagate = False

        # 避免重复添加 handler
        if not logger.handlers:
            # Console
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_fmt = logging.Formatter(
                "[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            console_handler.setFormatter(console_fmt)
            logger.addHandler(console_handler)

            # File (如果已初始化则添加)
            if self._file_handler:
                logger.addHandler(self._file_handler)

        self._loggers[name] = logger
        return logger

    def get_log_path(self):
        return self._log_path
