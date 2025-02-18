# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/11/20
import json
import re
import subprocess

from common.data import DeviceInfo
from common.log_tools import Log
from common.mysql import MySQLClient


def get_device_info(serial):
    try:
        # 获取udid
        udid = subprocess.check_output(["adb", "-s", serial, "shell", "getprop", "ro.serialno"]).decode(
            "utf-8").strip()
        # 获取设备名称
        name_output_model = subprocess.check_output(
            ["adb", "-s", serial, "shell", "getprop", "ro.product.model"]).decode("utf-8").strip()
        # 获取设备型号
        name_brand_output = subprocess.check_output(
            ["adb", "-s", serial, "shell", "getprop", "ro.product.brand"]).decode("utf-8").strip()
        # 获取设备 IP 地址
        ip_output = subprocess.check_output(
            ["adb", "-s", serial, "shell", "ip", "-f", "inet", "addr", "show", "wlan0"]).decode("utf-8").strip()
        ip_pattern = r'inet (\d+\.\d+\.\d+\.\d+/\d+)'
        match = re.search(ip_pattern, ip_output)
        ip = match.group(1).split("/")[0] if match else "N/A"
        # 获取安卓版本
        version_output = subprocess.check_output(
            ["adb", "-s", serial, "shell", "getprop", "ro.build.version.release"]).decode("utf-8").strip()
        resolution = subprocess.check_output(
            ["adb", "-s", serial, "shell", "wm", "size"]).decode("utf-8").strip()
        if resolution:
            resolution = resolution.split(":")[1].strip()

        # 创建 DeviceInfo 对象
        device_info = DeviceInfo(
            udid=udid,
            device_system="Android",
            system_version=version_output,
            name=name_output_model,
            model=name_brand_output,
            ip=ip,
            resolution=resolution
        )

        return device_info
    except subprocess.CalledProcessError as e:
        Log.logger.info("获取设备基础信息失败: %s", e)
        return None


def mysql_execute(query, params):
    if not query:
        return
    client = MySQLClient()
    client.connect()
    Log.logger.info("数据库执行: %s,%s", query, params)
    result = client.execute_query(query, params)
    client.connection.commit()
    client.close()

    return result

def get_device_name_zh(udid):
    command = "SELECT name_zh FROM devices WHERE udid = %s"
    params = [udid]

    result = mysql_execute(command, params)
    if result:
        name=f"{result[0]['name_zh']}\n{udid}"
    else:
        name=udid
    return name

def get_device_udid(serial):
    udid = subprocess.check_output(["adb", "-s", serial, "shell", "getprop", "ro.serialno"]).decode(
        "utf-8").strip()
    return udid


def get_device_status(serial):
    output = subprocess.check_output(["adb", "devices"]).decode("utf-8").strip().split("\n")[1:]
    for line in output:
        if line.strip():
            name, status = line.split("\t")
            if name.strip() == serial:
                return status.replace("\r", "")

    return None


def json_case_plan_info(res):
    try:
        for i in res:
            i["allure_features"] = json.loads(i["allure_features"]) if i["allure_features"] else None
            i["allure_stories"] = json.loads(i["allure_stories"]) if i["allure_stories"] else None
            i["report"] = json.loads(i["report"]) if i["report"] else None
            i["modules"] = json.loads(i["modules"]) if i["modules"] else None
    except Exception as e:
        Log.logger.error("序列化失败:%s", str(e))
    return res


# todo 有问题, 返回的布尔值, 类型不是布尔而是str, 把字段改为pass恢复
def json_case_info(res):
    try:
        for i in res:
            i["allure_mark"] = json.loads(i["allure_mark"]) if i["allure_mark"] else None
            i["pytest_mark"] = json.loads(i["pytest_mark"]) if i["pytest_mark"] else None
    except Exception as e:
        Log.logger.error("序列化失败:%s", str(e))
    return res


def get_module(module_name_zh):
    result = mysql_execute(f"SELECT class_name FROM cases WHERE module_name_zh = %s", [module_name_zh])
    if result:
        return result[0]["class_name"]
    else:
        return None


if __name__ == '__main__':
    result1 = mysql_execute("SHOW COLUMNS FROM test_plan", [])
    for i in result1:
        if i["Type"] == "tinyint(1)":
            print(i["Field"])  # proxy
    result11 = mysql_execute("SELECT * FROM test_plan WHERE id = %s", [21])

    print(result11[0]["proxy"], isinstance(result11[0]["proxy"], bool))
    print(result11[0]["apk"], isinstance(result11[0]["apk"], bool))
