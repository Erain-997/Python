import logging
import os

from common.utils.arg_parse_func import args
from common.utils.path_config import android
class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[37m",    # 白色
        "INFO": "\033[32m",     # 绿色
        "WARNING": "\033[33m",  # 黄色
        "ERROR": "\033[31m",    # 红色
        "CRITICAL": "\033[41m", # 背景红色
    }
    RESET = "\033[0m"

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        record.msg = f"{color}{record.msg}{self.RESET}"
        return super().format(record)

class LogTool:
    def __init__(self):
        self.logs_path = os.path.join(android.report_output_dir, str(args.output_report))
        self.logger = logging.getLogger('pytest')
        self.logger.setLevel(logging.INFO)

        self.formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(filename)s] -> %(message)s")

        # 创建 flow_data 和 mock 文件夹
        # os.makedirs(args.output_report, exist_ok=True)
        folders_to_create = ["flow_data", "mock"]
        for folder in folders_to_create:
            folder_path = os.path.join(android.report_output_dir, args.output_report, folder)
            os.makedirs(folder_path, exist_ok=True)

        # 添加文件处理器
        if not args.get_cases:
            os.makedirs(os.path.join(self.logs_path, "log"), exist_ok=True)
            handler = logging.FileHandler(self.logs_path + "/log/日志_终端.log", encoding="gbk")
            handler.setLevel(logging.INFO)
            handler.setFormatter(self.formatter)
            self.logger.addHandler(handler)

         # 添加终端处理器（带颜色）
        colored_formatter = ColoredFormatter(
            "[%(asctime)s] [%(levelname)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        # 添加终端处理器
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)  # 设置终端日志级别为 INFO
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        self.logger.info("日志初始化完成")

    def write(self, message):
        """重定向标准输出到日志记录器"""
        if message.strip():  # 避免空行
            self.logger.info(message.strip())

    def flush(self):
        """实现 flush 方法以满足标准输出的要求"""
        for handler in self.logger.handlers:
            handler.flush()

    def isatty(self):
        """如果文件描述符连接到一个终端（例如，标准输入、标准输出或标准错误），则返回 True"""
        return True  # 或者根据实际情况返回 True 或 False


Log = LogTool()
