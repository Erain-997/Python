# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/12/30
import subprocess
import threading


def func_update_app(device_list, app_path):
    def install_app(device, app_path, response_dict):
        try:
            output_device = subprocess.check_output(["adb", "-s", device, "install", app_path]).decode("utf-8").strip()
            if "Success" in output_device:
                response_dict["data"].append({device: "Success"})
            else:
                response_dict["data"].append({device: "failed"})
        except subprocess.CalledProcessError as e:
            response_dict[device] = {"result": str(e), "code": 1}

    response_dict = {
        "data": [],
        "code": 0,
        "result": "Success"
    }
    threads = []

    for device in device_list:
        thread = threading.Thread(target=install_app, args=(device, app_path, response_dict))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return response_dict


def func_get_version_list():
    path = "/var/ftp/pub/short_tv_apk/"
    output = subprocess.check_output(["ls", path])
    version_list = output.decode('utf-8', errors='replace').splitlines()

    response = {
        "data": {
            "version_list": version_list,
            "version_path": path,
            "ftp_server": "ftp://192.168.120.150/pub/short_tv_apk"

        },
        "code": 0
    }
    return response


def func_get_apk_list(version):
    path = f"/var/ftp/pub/short_tv_apk/{version}"
    output = subprocess.check_output(["ls", path])
    apk_list = output.decode('utf-8', errors='replace').split("\n")
    if "" in apk_list:
        apk_list.remove("")

    response = {
        "data": {
            "apk_list": apk_list,
            "apk_path": path,
            "apk_version": version
        },
        "code": 0
    }
    return response
