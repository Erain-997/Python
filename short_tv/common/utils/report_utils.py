import datetime
import unittest

from XTestRunner import HTMLTestRunner

from common.utils.path_config import android


class ReportUtils:
    def __init__(self, start_dir, pattern, device_name, demand_name):
        self.start_dir = start_dir
        self.pattern = pattern
        self.device_name = device_name
        self.demand_name = demand_name

    def create_report(self):
        # 生成时间戳
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # 构造title字符串
        title = f"{timestamp}-{self.demand_name}-{self.device_name}"
        # 发现测试用例
        suite = unittest.defaultTestLoader.discover(self.start_dir, pattern=self.pattern)
        # 执行测试并生成报告
        with open(f"{android.html_dir}/" + title + ".html", "wb") as f:
            runner = HTMLTestRunner(stream=f, title=title, rerun=1, language="zh-CN")
            return runner.run(suite)
