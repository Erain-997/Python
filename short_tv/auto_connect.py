# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/11/29
import json
import logging
import os
import subprocess
import time

import paramiko

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def ssh_exec(ssh, ssh_command):
    # 查询150已连接设备
    env_setup = (
        f"export PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$PATH"
    )
    combined_command = f"{env_setup} && " + ssh_command
    return ssh.exec_command(combined_command)


def get_remote_devices():
    try:
        data = set()
        ssh = create_ssh_client()
        stdin, stdout, stderr = ssh_exec(ssh, "adb devices")
        for line in stdout:
            if line.strip() and "\t" in line:
                serial, status = line.split("\t")
                data.add(serial)
        ssh.close()
        return data

    except subprocess.CalledProcessError:
        logging.error("adb命令执行报错")


def get_local_devices(p):
    try:
        data = set()
        devices_info = {}
        output = subprocess.check_output(["adb", "devices"]).decode("utf-8").strip().split("\n")[1:]
        for line in output:
            if line.strip() and ":" not in line:
                serial, status = line.split("\t")
                data.add(serial)

        device_ips = set()
        for udid in data:
            ip = get_device_ip(udid)
            if ip:
                device_ips.add(f"{ip}:{p}")
                devices_info[f"{ip}:{p}"] = get_device_info(udid, ip)
        return devices_info, device_ips

    except subprocess.CalledProcessError:
        logging.error("adb命令执行报错")


def get_device_ip(udid):
    try:
        result = subprocess.run(['adb', '-s', udid, 'shell', 'ip', '-f', 'inet', 'addr', 'show'],
                                capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if 'inet' in line and '127.0.0.1' not in line:
                ip = line.split()[1].split('/')[0]
                return ip
    except subprocess.CalledProcessError as e:
        logging.error(f"Error: {e}")
        return None


def restart_adb_tcpip(device, port):
    try:
        subprocess.check_output(['adb', "-s", device, 'tcpip', str(port)]).decode("utf-8").strip()
        logging.info(f"ADB重启成功，监听TCP/IP端口 {port}")
    except subprocess.CalledProcessError as e:
        logging.error(f"重启ADB失败: {e}")


def create_ssh_client():
    hostname = "192.168.120.150"
    sshport = 22
    username = "root"
    password = "1"
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname, sshport, username, password, timeout=30)
    return s


def get_device_info(serial, ip):
    try:
        # 获取设备名称
        model = subprocess.check_output(
            ["adb", "-s", serial, "shell", "getprop", "ro.product.model"]
        ).decode("utf-8").strip()
        brand = subprocess.check_output(
            ["adb", "-s", serial, "shell", "getprop", "ro.product.brand"]
        ).decode("utf-8").strip()
        device_name = f"{brand} {model}"

        # 获取安卓版本
        version = subprocess.check_output(
            ["adb", "-s", serial, "shell", "getprop", "ro.build.version.release"]
        ).decode("utf-8").strip()

        # 获取分辨率
        resolution_output = subprocess.check_output(
            ["adb", "-s", serial, "shell", "wm", "size"]
        ).decode("utf-8").strip()
        resolution = resolution_output.split(":")[1].strip() if resolution_output else None

        # 返回设备信息字典
        return {
            "name": device_name,
            "udid": serial,
            "ip": ip,
            "version": version,
            "resolution": resolution,
            "connect": False,
        }

    except subprocess.CalledProcessError as e:
        logging.error(f"获取设备信息时出错: {e}")
        return {}


def check_connection(serial):
    ssh = create_ssh_client()
    command = f"adb -s {serial} get-state"
    stdin, stdout, stderr = ssh_exec(ssh, command)
    stderr_res = stderr.read().decode()
    if stderr_res != "":
        logging.error(f"该设备已断开远程连接: {serial}, {stderr_res}")
        return False
    logging.info(f"检查设备: {serial}, 已连接")
    ssh.close()
    return True


def read_device_file(file_path):
    """读取设备文件，返回设备列表"""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r') as file:
        return json.load(file)


def get_new_devices(both, current):
    """比较现有设备列表和当前设备列表，返回新增的设备"""
    new = [device for device in current if device not in both]
    history = [device for device in both if device not in current]
    return new, history


if __name__ == "__main__":
    port = 9999
    file_path = 'devices.json'
    # 方法1
    while True:
        # 读取已连接过的设备列表
        all_devices_map = read_device_file(file_path)
        remote_devices = get_remote_devices()
        local_device, local_device_ips = get_local_devices(port)
        offline_device = local_device_ips - remote_devices
        # 找出新增的设备
        new_devices, history_devices = get_new_devices(all_devices_map, local_device)
        # 将新增的设备写入文件
        if new_devices:
            with open(file_path, 'w', encoding='utf-8') as file:
                logging.info(f"更新设备: {local_device}")
                for k, v in local_device.items():
                    all_devices_map[k] = v
                    all_devices_map[k]['connect'] = True
                json.dump(all_devices_map, file)

        if offline_device:
            for i in offline_device:
                logging.info("************************************")
                logging.info("正在重新连接...%s", local_device[i])
                logging.info(f"掉线设备: {get_device_info(local_device[i]['udid'], i)}")
                ssh_main = create_ssh_client()
                restart_adb_tcpip(local_device[i]['udid'], port)
                ssh_exec(ssh_main, f"nohup adb connect {i} &")
                ssh_main.close()
                if check_connection(i):
                    logging.info("重新连接成功")
                    all_devices_map[i]['connect'] = True
                else:
                    logging.error("重新连接失败")
                logging.info("************************************")
        else:
            logging.info("无设备掉线")

        for j in history_devices:
            if not check_connection(j):
                all_devices_map[j]['connect'] = False
                logging.info(f"历史连接设备 {j} 已断开远程连接, 正在尝试直接远程连接")
                ssh_main = create_ssh_client()
                ssh_exec(ssh_main, f"nohup adb connect {j} &")
                ssh_main.close()
                if check_connection(j):
                    logging.info("重新连接成功")
                    all_devices_map[j]['connect'] = True
                else:
                    logging.error("重新连接失败, 请使用usb连接设备")

        time.sleep(15)
