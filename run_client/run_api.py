import sys
from adb_connect import ADBManager, run_command
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import subprocess
import re
from ssh_connect import create_ssh_client, read_stderr, ssh_python_run, ssh_get_apks, ssh_get_apk_version
import paramiko
from output_callback_manager import OutputCallbackManager  # 导入单例类
from check_appium_progress import (
    git_pull,
    list_appium_processes,
    kill_device_processes,
    list_device_processes,
    run_commands,
    clear_all,
    terminate_appium_processes, update_app_now, open_report,
)
from ssh_connect import (
    create_ssh_client,
    ssh_python_run,
    ssh_python_run_test_cases,
    ssh_execute_commands,
)


class Api:
    def __init__(self):

        self.apk_list = ["无"]
        self.cases_list = ["无模块"]
        self.apk_version_list = ["无版本"]

        ssh = create_ssh_client()
        stdout_result, stderr_result = ssh_get_apk_version(ssh, read_output=True)
        self.apk_version_list.extend([i for i in stdout_result.split("\n") if i])
        if len(self.apk_version_list) > 0:
            stdout_result, stderr_result = ssh_get_apks(ssh, self.apk_version_list[-1], read_output=True)
            self.apk_list.extend([i for i in stdout_result.split("\n") if i])

        stdout_result, stderr_result = ssh_python_run(ssh, "-h", read_output=True)
        # 使用正则表达式提取模块名称
        pattern = r"目前支持:\s*\[(.*?)\]"
        match = re.search(pattern, stdout_result, re.DOTALL)
        if match:
            modules_str = match.group(1)
            self.cases_list.extend([
                module.strip().strip("'") for module in modules_str.split(",")
            ])
        ssh.close()

    def start_app(self):
        apk_list = ["无"]
        cases_list = ["无模块"]
        ssh = create_ssh_client()
        stdout_result, stderr_result = ssh_get_apk_version(ssh, read_output=True)
        apk_version_list = [i for i in stdout_result.split("\n") if i]
        if len(apk_version_list) > 0:
            stdout_result, stderr_result = ssh_get_apks(ssh, apk_version_list[-1], read_output=True)
            apk_list = [i for i in stdout_result.split("\n") if i]

        stdout_result, stderr_result = ssh_python_run(ssh, "-h", read_output=True)
        # 使用正则表达式提取模块名称
        pattern = r"目前支持:\s*\[(.*?)\]"
        match = re.search(pattern, stdout_result, re.DOTALL)
        if match:
            modules_str = match.group(1)
            cases_list = [
                module.strip().strip("'") for module in modules_str.split(",")
            ]
        ssh.close()

        return apk_version_list, apk_list, cases_list

    def get_supported_modules(self):
        ssh = create_ssh_client()
        stdout_result, stderr_result = ssh_python_run(ssh, "-h", read_output=True)
        ssh.close()

        # 使用正则表达式提取模块名称
        pattern = r"目前支持:\s*\[(.*?)\]"
        match = re.search(pattern, stdout_result, re.DOTALL)
        if match:
            modules_str = match.group(1)
            for module in modules_str.split(","):
                m = module.strip().strip("'")
                if m not in self.cases_list:
                    self.cases_list.append(m)

    def get_apks(self, version):
        ssh = create_ssh_client()
        stdout_result, stderr_result = ssh_get_apks(ssh, version, read_output=True)
        ssh.close()
        modules_list = [i for i in stdout_result.split("\n") if i]
        return modules_list

    def get_apk_versions(self):
        ssh = create_ssh_client()
        stdout_result, stderr_result = ssh_get_apk_version(ssh, read_output=True)
        ssh.close()
        modules_list = [i for i in stdout_result.split("\n") if i]
        return modules_list

    def get_device_list(self):
        return ADBManager.get_connected_devices()

    def set_device_ip(self, device_list):
        result = {}
        tcp_port = 9999

        for device in device_list:
            # 只处理直连设备
            if "." not in device and ":" not in device:
                adb_manager = ADBManager(device_name=device, port=tcp_port)
                device_ip = adb_manager.get_device_ip()
                name1 = adb_manager.run_adb_command("shell getprop ro.product.brand")
                name2 = adb_manager.run_adb_command("shell getprop ro.product.model")

                result[device_ip] = {
                    "uid": device,
                    "name": name1 + name2,
                    "ip": device_ip + f":{tcp_port}",
                    "adb": adb_manager
                }
            else:
                if device.split(":")[0] not in result:
                    device_port = device.split(":")[-1]
                    adb_manager = ADBManager(device_name=device, port=device_port)
                    name1 = adb_manager.run_adb_command("shell getprop ro.product.brand")
                    name2 = adb_manager.run_adb_command("shell getprop ro.product.model")
                    result[device.split(":")[0]] = {
                        "uid": "远程连接设备",
                        "name": name1 + name2,
                        "ip": device,
                        "adb": adb_manager
                    }
        return result

    def run_single_script(self, commands):
        # run_commands(commands)
        threading.Thread(target=run_commands, args=(commands,)).start()

    def update_app(self, device, version, apk_path):
        if not device:
            messagebox.showerror("错误", f"未检测到设备, 请选择设备")
            return
        threading.Thread(target=update_app_now, args=(device, version, apk_path,)).start()

    def run_adb_operations(self, operation, device=""):
        output_callback = OutputCallbackManager().get_callback()

        def adb_operations():
            if operation == "clear_proxy":
                adb_manager = ADBManager(device_name=device, port=9999)
                output_callback(
                    f"Using device: {device} on port {adb_manager.port}\n"
                )
                adb_manager.clear_proxy()
                current_proxy = adb_manager.get_proxy()
                output_callback(
                    f"Proxy cleared, current proxy: {current_proxy}\n"
                )
                messagebox.showinfo("Success", "Proxy cleared successfully.")
            elif operation == "list_appium_processes":
                out = list_appium_processes()
                if out == "":
                    output_callback("\n 当前无设备在执行测试 \n")
            elif operation == "kill_appium_processes":
                terminate_appium_processes()
            elif operation == "git_pull":
                git_pull()
                output_callback("\n 脚本已更新完成.\n")
            elif operation == "open_report":
                open_report()
            elif operation == "kill_device_processes":
                if not device:
                    output_callback("\n 脚本终止失败, 请选择设备.\n")
                    return
                kill_device_processes(device)
                output_callback("\n 脚本已终止, 将不会产生报告.\n")
            elif operation == "clear_all":
                clear_all()
                output_callback("\n 脚本已终止, 将不会产生报告.\n")
            elif operation == "list_device_processes":
                list_device_processes()
            else:
                output_callback(f"Unknown operation: {operation}\n")

        threading.Thread(target=adb_operations).start()

    def run_adb_connect(self, device):
        run_command(f"adb connect {device}")

    def run_python_script(self, version, module, device, proxy, feishu, record, apk, apk_path, exif_params):
        def script_operations():
            ssh = create_ssh_client()
            try:

                ssh_python_run_test_cases(
                    ssh=ssh,
                    device=device,
                    version=version,
                    module=module,
                    proxy=proxy,
                    feishu=feishu,
                    record=record,
                    apk=apk,
                    apk_path=apk_path,
                    exif_params=exif_params
                )
            except Exception as e:
                output_callback = OutputCallbackManager().get_callback()
                output_callback(f"An error occurred: {e}\n")
            finally:
                ssh.close()

        threading.Thread(target=script_operations).start()

    def add_to_history(self, value, lists):
        if value and value not in lists:
            lists.append(value)


# 示例调用
if __name__ == "__main__":
    api = Api()
    modules = api.get_supported_modules()
    print(modules)
