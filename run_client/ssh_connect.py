# FILE: ssh_connect.py

import paramiko
import threading
import re
import time
from output_callback_manager import OutputCallbackManager  # 导入单例类
from adb_connect import run_command


def extract_ip_segment(device):
    match = re.search(r"(\d+)\.(\d+)\.(\d+)\.(\d+):(\d+)", device)
    if match:
        return match.group(4)
    return None


def read_stdout(stdout):
    output_callback = OutputCallbackManager().get_callback()
    while True:
        line = stdout.readline()
        if not line:
            break
        output_callback(f"<<{line.strip()}\n")


def read_stderr(stderr):
    output_callback = OutputCallbackManager().get_callback()
    while True:
        line = stderr.readline()
        if not line:
            break
        output_callback(f"{line.strip()}\n")


def ssh_execute_commands(
        ssh, commands, android_home="/home/hexingyuan/Android/Sdk", read_output=False
):
    try:
        output_callback = OutputCallbackManager().get_callback()

        if android_home:
            env_setup = (
                f"export ANDROID_HOME={android_home} && "
                f"export PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$PATH"
            )
            combined_command = f"{env_setup} && " + " && ".join(commands)
        else:
            combined_command = " && ".join(commands)

        output_callback(
            f">> Executing combined command:\n"
            + combined_command.replace(" && ", " &&\n")
        )
        output_callback("\n")

        stdin, stdout, stderr = ssh.exec_command(combined_command)
        if read_output:
            stdout_result = stdout.read().decode()
            stderr_result = stderr.read().decode()
            return stdout_result, stderr_result
        else:
            stdout_thread = threading.Thread(target=read_stdout, args=(stdout,))
            stderr_thread = threading.Thread(target=read_stderr, args=(stderr,))
            stdout_thread.start()
            stderr_thread.start()

            stdout_thread.join()
            stderr_thread.join()

    except paramiko.AuthenticationException:
        output_callback("Authentication failed, please verify your credentials.\n")
    except paramiko.SSHException as sshException:
        output_callback(f"Unable to establish SSH connection: {sshException}\n")
    except paramiko.BadHostKeyException as badHostKeyException:
        output_callback(f"Unable to verify server's host key: {badHostKeyException}\n")
    except TimeoutError as timeoutError:
        output_callback(f"Connection timed out: {timeoutError}\n")
    except Exception as e:
        output_callback(f"An error occurred: {e}\n")
        output_callback(f"Exception type: {type(e).__name__}\n")
        output_callback(f"Exception args: {e.args}\n")
        return None, str(e)


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
            kill_command = f"kill -9 {pid} process={process}"
            ssh_execute_commands(ssh, [kill_command])


def kill_process_on_port(ssh, port):
    output_callback = OutputCallbackManager().get_callback()
    stdin, stdout, stderr = ssh.exec_command(f"lsof -i:{port}")
    output = stdout.read().decode()
    if output:
        output_callback(f"Port {port} is occupied. Killing process...\n")

        stdin, stdout, stderr = ssh.exec_command(f"fuser -k {port}/tcp")
        stdout.channel.recv_exit_status()

        output_callback(f"fuser output: {stdout.read().decode()}\n")
        output_callback(f"fuser error: {stderr.read().decode()}\n")

        while True:
            stdin, stdout, stderr = ssh.exec_command(f"lsof -i:{port}")
            output = stdout.read().decode()
            if not output:
                output_callback(f"Port {port} has been released.\n")
                break
            time.sleep(1)


def ssh_python_run(ssh, params, read_output=False):
    commands = [
        "cd code/mobile-ui-automation-tests/short_tv",
        "source .venv/bin/activate",
        f"python run_mobile_ui_automation_tests.py {params}",
    ]
    return ssh_execute_commands(ssh, commands, read_output=read_output)


def ssh_get_apks(ssh, version, read_output=True):
    commands = [
        f"ls /var/ftp/pub/short_tv_apk/{version}",
    ]
    return ssh_execute_commands(ssh, commands, read_output=read_output)


def ssh_get_apk_version(ssh, read_output=True):
    commands = [
        f"ls /var/ftp/pub/short_tv_apk",
    ]
    return ssh_execute_commands(ssh, commands, read_output=read_output)


def ssh_python_run_test_cases(
        ssh, device, version, module, proxy, feishu, record, apk=" ", apk_path=" ", exif_params=" "
):
    appium_port_str = extract_ip_segment(device)
    appium_port = 9000 + int(appium_port_str)
    kill_process_by_device(ssh, device)

    if apk != " ":
        params = f"{device} -modules {module} -port {appium_port} {proxy} {feishu} {record} {apk} /var/ftp/pub/short_tv_apk/{version}/{apk_path} {exif_params}"
    else:
        params = f"{device} -modules {module} -port {appium_port} {proxy} {feishu} {record} {exif_params}"
    ssh_execute_commands(ssh, [f"adb connect {device}"])
    ssh_python_run(ssh, params)


def create_ssh_client():
    hostname = "192.168.120.54"
    sshport = 22
    username = "root"
    password = "hexingyuan123"
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname, sshport, username, password, timeout=30)
    output_callback = OutputCallbackManager().get_callback()
    output_callback("Creating SSH client...\n")
    return ssh

# if __name__ == "__main__":
#     ssh = create_ssh_client()
#     try:
#         device = "172.16.9.21:6666"
#         version = "v1_9_11"
#         module = "广告模块"
#         run_command(f"adb connect {device}")
#         ssh_python_run_test_cases(ssh, device, version, module, "-proxy", "", "", "")
#
#     finally:
#         ssh.close()
