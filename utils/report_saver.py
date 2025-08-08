import requests
from locust import events
import os
import time
import signal
from utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(name=__name__)
_report_saved = False
_report_path = None


def save_html_report(filename: str = None):
    global _report_saved, _report_path
    if _report_saved:
        return
    _report_saved = True

    report_url = "http://localhost:8089/stats/report?download=1&theme=light"
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_dir = "reports"
    os.makedirs(output_dir, exist_ok=True)
    locust_output_dir = os.path.join(output_dir, "locust")
    os.makedirs(locust_output_dir, exist_ok=True)

    if filename:
        filename = filename if filename.endswith(".html") else f"{filename}_{timestamp}.html"
        report_path = os.path.join(locust_output_dir, filename)
    else:
        report_path = os.path.join(locust_output_dir, f"locust_report_{timestamp}.html")

    _report_path = report_path  # 存储最终路径（可供外部使用）

    try:
        logger.info(f"📥 正在下载 HTML 报告: {report_url}")
        resp = requests.get(report_url)
        resp.raise_for_status()
        with open(report_path, "wb") as f:
            f.write(resp.content)
        logger.info(f"✅ 已保存 HTML 报告: {report_path}")
    except Exception as e:
        logger.error(f"❌ 下载 HTML 报告失败: {e}")


def start_report_monitoring(filename: str = None):
    """显式启动监听器注册和信号处理，可传入自定义报告文件名"""
    if getattr(start_report_monitoring, "_started", False):
        return
    start_report_monitoring._started = True

    def wrapped_save(*args, **kwargs):
        save_html_report(filename)

    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        wrapped_save()

    @events.quitting.add_listener
    def on_quitting(environment, **kwargs):
        wrapped_save()

    def handle_sighup(signum, frame):
        print("🔔 收到 SIGHUP 信号，保存 HTML 报告")
        wrapped_save()

    signal.signal(signal.SIGHUP, handle_sighup)

    logger.info("📊 已启动报告保存监听器和信号处理")


def get_report_path():
    """返回最终保存的报告路径（如果有）"""
    return _report_path
