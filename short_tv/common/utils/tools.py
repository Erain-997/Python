# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/11/4

import datetime
import os
import random
import shutil
import socket
import sys


def language_name():
    language_names = {
        "en": "英文",
        "zh_cn": "简体中文",
        "zh": "繁体中文",
        "fil": "菲律宾语",
        "ar": "阿拉伯语",
        "hi": "印地语",
        "in": "印尼语",
        "vi": "越南语",
        "pt": "葡萄牙语",
        "es": "西班牙语",
        "ja": "日语",
        "de": "德语",
        "ko": "韩语",
        "th": "泰语",
        "ms": "马来西亚",
        "it": "意大利",
        "ru": "俄语",
        "fr": "法语"
    }
    return language_names


def timestamp():
    return datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


def get_local_ip():
    """
    获取本机 IP 地址
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # 连接到百度服务器以获取外网 IP
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
    except Exception:
        ip_address = "127.0.0.1"
    finally:
        s.close()
    return ip_address


def get_available_port():
    # 定义一个端口范围（这里选择1024到65535之间的端口，但可以根据需要调整）
    min_port = 1024
    max_port = 65535
    while True:
        # 随机选择一个端口
        port = random.randint(min_port, max_port)
        # 创建一个socket对象
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # 尝试绑定端口
                sock.bind(("localhost", port))
                # 如果绑定成功，返回端口号
                return port
            except socket.error as e:
                # 如果绑定失败（端口被占用），继续尝试下一个端口
                Log.logger.info(f"Port {port} is not available: {e}", file=sys.stderr)
                continue


def clear():
    # 获取当前目录
    current_dir = os.getcwd()
    # 遍历当前目录下的所有文件和文件夹
    for item in os.listdir(current_dir):
        # 构建完整路径
        item_path = os.path.join(current_dir, item)

        # 检查是否为文件夹且名称以 'report_output_' 开头
        if os.path.isdir(item_path) and item.startswith("report_output_"):
            try:
                # 删除文件夹及其内容
                shutil.rmtree(item_path)
                print(f"已删除文件夹: {item_path}")
            except Exception as e:
                # 打印异常信息
                print(f"删除文件夹 {item_path} 时发生错误: {e}")
