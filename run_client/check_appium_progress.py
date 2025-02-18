# FILE: check_appium_progress.py

import paramiko
from ssh_connect import create_ssh_client, kill_process_on_port, ssh_execute_commands, ssh_python_run
from output_callback_manager import OutputCallbackManager  # 导入单例类


def find_appium_parent_process(port=None):
    if port:
        commands = [f"ps -eo pid,ppid,cmd | grep 'appium.*{port}' | grep -v grep"]
    else:
        commands = ["ps -eo pid,ppid,cmd | grep appium | grep -v grep"]
    ssh = create_ssh_client()
    ssh_execute_commands(ssh, commands)
    ssh.close()


def run_commands(commands):
    ssh = create_ssh_client()
    ssh_execute_commands(ssh, [commands])
    ssh.close()


def terminate_appium_processes(port=None):
    if port:
        commands = [f"pkill -f 'appium.*{port}' -9"]
    else:
        commands = ["pkill -f appium -9"]
    ssh = create_ssh_client()
    ssh_execute_commands(ssh, commands)
    ssh.close()


def clear_all():
    commands = ["pkill -f 'run_mobile_ui_automation_tests.*' -9"]
    ssh = create_ssh_client()
    ssh_execute_commands(ssh, commands)
    ssh.close()


def list_appium_processes():
    commands = ["ps aux | grep appium | grep -v grep"]
    ssh = create_ssh_client()
    out, errors = ssh_execute_commands(ssh, commands, read_output=True)
    ssh.close()

    return out


def kill_device_processes(device):
    commands = [f"pkill -f '{device}'"]
    ssh = create_ssh_client()
    ssh_execute_commands(ssh, commands)
    ssh.close()


def list_device_processes():
    commands = ["ps aux | grep run_mobile_ui_automation_tests | grep -v grep"]
    ssh = create_ssh_client()
    ssh_execute_commands(ssh, commands)
    ssh.close()


def update_app_now(device, version, apk_path):
    commands = [f"adb -s {device} install /var/ftp/pub/short_tv_apk/{version}/{apk_path}"]
    ssh = create_ssh_client()
    ssh_execute_commands(ssh, [f"adb connect {device}"])
    ssh_execute_commands(ssh, commands)
    ssh.close()


def git_pull():
    commands = ["cd code/mobile-ui-automation-tests/short_tv", "git reset --hard HEAD && git pull"]
    ssh = create_ssh_client()
    ssh_execute_commands(ssh, commands)
    ssh.close()


def open_report():
    commands = ["ps aux | grep short_tv_report_web_server | grep -v grep"]
    ssh = create_ssh_client()
    stdout_result, stderr_result = ssh_execute_commands(ssh, commands, read_output=True)
    if not stdout_result:
        commands = [
            "cd code/mobile-ui-automation-tests/run_web",
            "source .venv/bin/activate",
            "python short_tv_report_web_server.py"]
        ssh_execute_commands(ssh, commands)
    ssh.close()


def kill_process_by_device(ssh, device):
    # 查找包含 172.16.9.28:9999 的所有 run_mobile_ui_automation_tests.py 进程
    find_command = f"ps aux | grep 'run_mobile_ui_automation_tests.py' | grep '{device}' | grep -v grep"
    stdin, stdout, stderr = ssh.exec_command(find_command)
    process_list = stdout.read().decode().strip().split("\n")
    OutputCallbackManager().get_callback()(process_list)
    # 提取进程 ID 并终止进程
    for process in process_list:
        if process:
            pid = process.split()[1]
            kill_command = f"kill -9 {pid}"
            ssh_execute_commands(ssh, [kill_command])


if __name__ == "__main__":
    # 更新代码
    git_pull()

    # 列出所有 Appium 进程
    # list_appium_processes()

    # 终止所有 Appium 进程
    # terminate_appium_processes(9028)
    find_appium_parent_process(99608)
