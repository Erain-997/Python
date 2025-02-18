import subprocess
import time
from output_callback_manager import OutputCallbackManager  # 导入单例类


def log_error(message):
    output_callback = OutputCallbackManager().get_callback()
    if output_callback:
        output_callback(f"\033[91m{message}\033[0m\n")  # Red text
    else:
        print(f"\033[91m{message}\033[0m")  # Red text


def log_info(message):
    output_callback = OutputCallbackManager().get_callback()
    if output_callback:
        output_callback(f"{message}\n")
    else:
        print(message)


def run_command(command):
    log_info(f">>{command}")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        log_error(result.stderr)
        return None
    else:
        log_info(f"<<{result.stdout.strip()}")
    return result.stdout


class ADBManager:
    def __init__(self, device_name, port=9999):
        self.device_name = device_name
        self.port = port

    def run_adb_command(self, command):
        command = f"adb -s {self.device_name} {command}"
        return run_command(command)

    def restart_tcpip(self):
        self.run_adb_command(f"tcpip {self.port}")

    def get_device_ip(self):
        # Ensure the device is connected
        devices_output = self.run_adb_command("devices")
        if not devices_output or "device" not in devices_output:
            log_error("No devices connected.")
            return

        # Restart ADB in TCP/IP mode
        self.restart_tcpip()

        # Wait for a few seconds to ensure the device is ready
        time.sleep(3)

        # Get the IP address using ifconfig
        for _ in range(2):
            ip_output = self.run_adb_command("shell ifconfig wlan0")
            if ip_output:
                # Parse the IP address from the output
                for line in ip_output.splitlines():
                    if "inet addr:" in line:
                        ip_address = line.strip().split("inet addr:")[1].split(" ")[0]
                        return ip_address
            time.sleep(0.5)  # Wait for 500 milliseconds

        log_error("Failed to get IP address after 50 attempts.")
        return None

    def set_proxy(self, ip, port):
        # Set the proxy server IP and port
        self.run_adb_command(f"shell settings put global http_proxy {ip}:{port}")
        log_info(f"Proxy set to {ip}:{port} for device {self.device_name}")

    def clear_proxy(self):
        # Clear the proxy server settings
        self.run_adb_command("shell settings put global http_proxy :0")
        log_info(f"Proxy cleared for device {self.device_name}")

    def get_proxy(self):
        # Get the current proxy server IP and port
        proxy = self.run_adb_command("shell settings get global http_proxy")
        log_info(f"Current proxy for device {self.device_name}: {proxy}")
        return proxy

    def connect_device(self, ip):
        self.run_adb_command(f"connect {ip}:{self.port}")

    @staticmethod
    def get_connected_devices():
        result = run_command("adb devices")
        if not result:
            return []

        devices = [
            line.split()[0]
            for line in result.splitlines()
            if "device" in line and not line.startswith("List")
        ]
        return devices


if __name__ == "__main__":
    # 获取所有连接的设备
    devices = ADBManager.get_connected_devices()
    if not devices:
        log_error("No devices connected.")
    else:
        # 为每个设备分配一个 ADBManager 实例，并执行操作
        for i, device in enumerate(devices):
            adb_manager = ADBManager(device_name=device, port=9999)
            log_info(f"Using device: {device} on port {adb_manager.port}")

            adb_manager.run_adb_command("disconnect")
            device_ip = adb_manager.get_device_ip()
            if device_ip:
                adb_manager.connect_device(device_ip)
                adb_manager.set_proxy("192.168.120.54", "8888")
                adb_manager.get_proxy()
                adb_manager.clear_proxy()
                adb_manager.get_proxy()
            adb_manager.run_adb_command("disconnect")
