import os
import platform
import shutil
import subprocess
import time

import allure
import chardet
import pytest
import requests
import yaml

from common.utils.arg_parse_func import args
from common.utils.log_utils import Log
from common.utils.path_config import android
from common.utils.tools import get_local_ip, get_available_port
from common.utils.tools import timestamp
from common.mysql.mysql_tools import mysql_execute

def adb_logcat(file_path):
    # 启动日志记录
    logcat_process = subprocess.Popen(
        ["adb", "-s", args.device, "logcat", "-v", "threadtime"],
        stdout=open(file_path, "w"),
    )
    return logcat_process


@allure.step("logcat日志")
def stop_logcat(logcat_process, file_path):
    # 结束logcat
    logcat_process.terminate()
    logcat_process.wait()
    # 读取日志文件内容
    with open(file_path, "rb") as log_file:
        logcat_data = log_file.read()
    # 将日志数据附加到 Allure 报告中
    allure.attach(logcat_data, name="logcat日志", attachment_type=allure.attachment_type.TEXT)
    # os.remove(file_path)


def start_proxy():
    if not args.proxy and not args.proxy_port:
        return
    if args.proxy_port:
        proxy_port = args.proxy_port
    else:
        proxy_port = str(get_available_port())
    # Log.logger.info(f"-----启动mitmdump代理, 端口{proxy_port}-----")
    # 记录mitmdump端口
    mysql_execute(f"UPDATE test_plan SET mitmdump_port=%s WHERE id = %s",[proxy_port, args.task_id])
    log_file_path = f"{android.report_output_dir}/{args.output_report}/log/日志_proxy.log"
    with open(log_file_path, "w", encoding="gbk") as log_file:
        proxy_process = subprocess.Popen(
            ["mitmdump", "-v", "--mode", "regular", "-p", proxy_port, "-s", "tv_proxy.py",
             # "-w", f"{android.temp_dir}/proxy_data.pcap",
             "--allow-hosts", "test-api.shorttv.live"],
            stdout=log_file,
        )
        # TODO 设置手机代理
        subprocess.check_output(
            ["adb", "-s", args.device, "shell", "settings", "put", "global", "http_proxy",
             f"{get_local_ip()}:{proxy_port}"])
        # Log.logger.info(f"-----设置手机代理, 端口{get_local_ip()}:{proxy_port}-----")
        return proxy_process


def stop_proxy(proxy_process):
    if not args.proxy and not args.proxy_port:
        return
    subprocess.check_output(["adb", "-s", args.device, "shell", "settings", "put", "global", "http_proxy", ":0"])
    # # Log.logger.info(f"-----关闭mitmdump代理-----")
    proxy_process.kill()
    time.sleep(2)

    # 移动文件
    for item in os.listdir(android.flow_data_dir):
        if item.startswith("flow_data_"):
            ip = item.replace("flow_data_", "").replace(".json", "")
            if ip == args.device.split(':')[0]:
                src_path = os.path.join(android.flow_data_dir, item)
                dst_path = os.path.join(android.report_output_dir, str(args.output_report), "flow_data", item)

                # 检查目标文件是否存在
                if os.path.exists(dst_path):
                    base_name, ext = os.path.splitext(item)
                    new_name = f"{base_name}_{timestamp()}.json"
                    dst_path = os.path.join(android.report_output_dir, str(args.output_report), "flow_data", new_name)

                shutil.move(src_path, dst_path)

    for item in os.listdir(android.mock_dir):
        if item.startswith("mock_"):
            ip = item.replace("mock_", "").replace(".yaml", "")
            if ip == args.device.split(':')[0]:
                src_path = os.path.join(android.mock_dir, item)
                dst_path = os.path.join(android.report_output_dir, str(args.output_report), "mock", item)

                # 检查目标文件是否存在
                if os.path.exists(dst_path):
                    # 文件存在，增加后缀 _1
                    base_name, ext = os.path.splitext(item)
                    new_name = f"{base_name}_{timestamp()}.yaml"
                    dst_path = os.path.join(android.report_output_dir, str(args.output_report), "mock", new_name)

                shutil.move(src_path, dst_path)


def adb_shell(command):
    # 获取所有连接的设备
    devices_output = subprocess.check_output(["adb", "devices"]).decode('utf-8')

    # 解析设备列表
    devices = []
    for line in devices_output.splitlines():
        if "List of devices" in line:
            continue
        if line.strip() and not line.startswith("* daemon"):
            device_info = line.split()
            if device_info:
                devices.append(device_info[0])

    # 检查指定设备是否在连接的设备列表中
    if args.device in devices:
        # 使用 subprocess.run 捕获命令输出
        result = subprocess.run(["adb", "-s", args.device, "shell", command], capture_output=True, text=True)
        return result.stdout
    else:
        print(f"Device {args.device} not found in connected devices.")
        return None


# TODO 需返回当前adb命令的执行结果


def find_log_value_by_key(file_path, key):
    """从指定的日志文件中查找给定键对应的值"""
    # 检测文件编码
    detected_encoding = _detect_encoding(file_path)
    try:
        with open(file_path, "r", encoding=detected_encoding) as file:
            for line in file:
                if key in line:
                    # 提取键后面的值
                    value = _extract_value_from_line(line, key)
                    if value is not None:
                        return value
    except UnicodeDecodeError:
        # 尝试其他编码方式
        encodings = ["utf-8", "gbk", "iso-8859-1", "cp1252"]
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as file:
                    for line in file:
                        if key in line:
                            # 提取键后面的值
                            value = _extract_value_from_line(line, key)
                            if value is not None:
                                return value
            except UnicodeDecodeError:
                continue
    return None


def _detect_encoding(file_path):
    """检测文件的编码格式"""
    with open(file_path, "rb") as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result["encoding"]


def _extract_value_from_line(line, key):
    """从日志行中提取key的值"""
    parts = line.split(key)
    if len(parts) > 1:
        # 提取键后面的值
        value_part = parts[1].split(":")[1].strip()
        return value_part
    return None


def is_appium_running_and_kill(port):
    try:
        # 查找 Appium 进程
        result = subprocess.run(f"netstat -ano | findstr :{port}",shell=True,  check=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        lines = result.stdout.decode('utf-8', errors='replace').splitlines()

        for line in lines:
            parts = line.split()
            if len(parts) > 4:
                pid = parts[-1]
                # 杀死 Appium 进程
                kill_result = subprocess.run(f"taskkill /F /PID {pid}",shell=True,  check=True, stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                Log.logger.info(f"Killed Appium process with PID {pid}")
                return 0, kill_result.stdout.decode('utf-8', errors='replace'), kill_result.stderr.decode('utf-8',
                                                                                                          errors='replace')

        Log.logger.info(f"No Appium process found on port {port}")
        return 0, "", ""

    except subprocess.CalledProcessError as e:
        return e.returncode, e.stdout.decode('utf-8', errors='replace'), e.stderr.decode('utf-8', errors='replace')


def wait_for_appium_to_start(port, timeout=500):
    is_appium_running_and_kill(port)
    # 记录appium端口
    mysql_execute(f"UPDATE test_plan SET appium_port=%s WHERE id = %s",[str(port), args.task_id])
    log_file_path = f"{android.report_output_dir}/{args.output_report}/log/日志_appium.log"
    with open(log_file_path, "w", encoding="gbk") as log_file:
        try:
            if "Windows" in platform.platform():
                appium_process = subprocess.Popen(["appium", "-p", str(port)], shell=True, stdout=log_file)
            elif "Linux" in platform.platform() or "macOS" in platform.platform():
                appium_process = subprocess.Popen(["appium", "-p", str(port)], stdout=log_file)
            else:
                appium_process = subprocess.Popen(["appium", "-p", str(port)], stdout=log_file)
            Log.logger.info(f"Starting Appium in port {str(port)}...")

            # 等待Appium启动
            start_time = time.time()
            while True:
                if time.time() - start_time > timeout:
                    Log.logger.info(f"Appium启动超时..................")
                    raise TimeoutError("Appium failed to start within the specified timeout.")
                try:
                    response = requests.get(f"http://localhost:{port}/status")
                    if response.status_code == 200:
                        Log.logger.info(f"Appium started on port {str(port)}")
                        break
                    else:
                        time.sleep(1)
                except requests.RequestException as e:
                    Log.logger.info(f"appium还在启动中: {time.time() - start_time}s")
                    time.sleep(1)

        except Exception as e:
            Log.logger.info(f"Failed to start Appium: {e}")
            raise


# 读取yaml文件数据
def read_yaml(file_path):
    return yaml.safe_load(open(file_path, encoding="utf-8"))


def update_short_max():
    pytest.main(
        [
            "-vs",
            f"{android.api_dir}/test_shortmax.py",
        ]
    )


def install_apk(path):
    """
    安装指定apk
    """
    try:
        output = subprocess.check_output(["adb", "-s", args.device, "install", path]).decode("utf-8").strip()
        if "Success" in output:
            Log.logger.info(f"APK 安装成功: {path}")
    except Exception as e:
        return f"apk安装失败, 请检查路径和apk包 {args.device}: {e}"


def get_locale_language():
    try:
        output = (
            subprocess.check_output(["adb", "-s", args.device, "shell", "getprop", "persist.sys.locale"])
            .decode("utf-8")
            .strip()
        )
        if output:
            language = output.split("-")
            if len(language) == 3:
                return language[0] + "-" + language[1], language[2]
            else:
                return language[0], language[1]
        else:
            Log.logger.info(f"设备区域特殊, 需要兼容: %s", str(output))
            return None, None

    except Exception as e:
        Log.logger.info(f"设备区域特殊, 需要兼容. %s", str(e))
        return None, None


def precise_sleep(duration):
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < duration:
        pass
