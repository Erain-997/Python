import logging
import os
import threading
from datetime import datetime, timedelta

from common.data import BASE_DIR


class LogTool:
    def __init__(self, logs_path=os.path.join(BASE_DIR, "report_output", "接口后端日志", "log")):
        self.logs_path = logs_path
        self.logger = logging.getLogger('werkzeug')
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(filename)s] -> %(message)s")

        # 确保日志目录存在
        os.makedirs(self.logs_path, exist_ok=True)

        # 初始化日志文件处理器
        self._setup_file_handler()

        # 添加终端处理器
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        self.logger.info("日志初始化完成,路径:%s", os.path.abspath(__file__))

    def _setup_file_handler(self):
        # 获取当前日期
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_path, f"日志_{current_date}.log")

        # 移除旧的文件处理器
        for handler in self.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                self.logger.removeHandler(handler)

        # 添加新的文件处理器
        handler = logging.FileHandler(log_file, encoding="utf-8")
        handler.setLevel(logging.INFO)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def write(self, message):
        """重定向标准输出到日志记录器"""
        if message.strip():
            self.logger.info(message.strip())

    def flush(self):
        """实现 flush 方法以满足标准输出的要求"""
        for handler in self.logger.handlers:
            handler.flush()

    def isatty(self):
        """如果文件描述符连接到一个终端（例如，标准输入、标准输出或标准错误），则返回 True"""
        return True  # 或者根据实际情况返回 True 或 False

    def check_and_rotate_log(self):
        """检查是否需要滚动日志文件"""
        now = datetime.now()
        next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        time_to_next_midnight = (next_midnight - now).total_seconds()

        # 使用定时任务来检查并滚动日志
        timer = threading.Timer(time_to_next_midnight, self._rotate_log)
        timer.start()

    def _rotate_log(self):
        self._setup_file_handler()
        self.check_and_rotate_log()  # 递归调用以继续检查


# 创建日志工具实例
Log = LogTool()

# 启动日志滚动检查
Log.check_and_rotate_log()
