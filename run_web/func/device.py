# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/12/30
import json
import re
import subprocess
import threading
import time

import pymysql

from common.data import DeviceInfo
from common.log_tools import Log
from common.mysql import MySQLClient
from common.tools import get_device_status, get_device_udid, get_device_info, mysql_execute


def func_create_device(device_info: DeviceInfo):
    command = """
        INSERT INTO devices (
            udid, device_system, system_version, name,name_zh, model, ip, tcpip_port, resolution, 
            testing_status, connect_status, owner, remarks
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """
    params = [
        device_info.udid, device_info.device_system, device_info.system_version,
        device_info.name, device_info.name_zh, device_info.model, device_info.ip, device_info.tcpip_port,
        device_info.resolution, device_info.testing_status, device_info.connect_status,
        device_info.owner, device_info.remarks
    ]

    # result = mysql_execute(command, params)
    # command, params = func_get_device_info(device_info.udid)
    # recheck = mysql_execute(command, params)

    return command, params


def func_add_device(device):
    output = subprocess.check_output(["adb", "connect", device]).decode("utf-8").strip()
    time.sleep(0.5)
    if "connected" in output:
        status = get_device_status(device)
        if status == "device":
            try:
                udid = get_device_udid(device)
                device_info = get_device_info(device)
                # device_info.connect_status = status
                device_info.tcpip_port = device.split(":")[1]
                client = MySQLClient()
                client.connect()
                command, params = func_create_device(device_info)
                client.execute_non_query(command, params)
                client.close()
                return {
                    "devices": device_info.to_dict(),
                    "result": "",
                    "code": 0
                }
            except pymysql.err.IntegrityError as e:
                return {
                    "devices": "",
                    "result": "设备已存在, 请检查ip是否冲突",
                    "code": 1
                }
        if status == "unauthorized":
            return {
                "devices": "",
                "result": "请点击设备允许USB调试",
                "code": 1
            }
    elif "10061" in output:
        return {
            "devices": "",
            "result": "设备不存在, 请检查tcpip端口和ip",
            "code": 1
        }
    elif "authenticate" in output:
        return {
            "devices": "",
            "result": "请点击设备允许USB调试",
            "code": 1
        }
    else:
        return {
            "devices": "",
            "result": output,
            "code": 1
        }


def func_delete_device(udid=None, device=None):
    command = ""

    if udid:
        command = f"DELETE FROM devices WHERE udid = '{udid}'"
    if device and ":" in device:
        try:
            subprocess.check_output(["adb", "disconnect", device]).decode("utf-8").strip()
        except Exception as e:
            Log.logger.info("设备本身未连接: %s", str(e))
        ip = device.split(":")[0]
        command = f"DELETE FROM devices WHERE ip = '{ip}'"

    params = []
    mysql_execute(command, params)

    return {
        "devices": "",
        "result": "设备已删除",
        "code": 0
    }


def func_update_device(udid, data):
    set_clause = ", ".join([f"{key} = %s" for key in data.keys() if key in DeviceInfo.__annotations__.keys()])
    command = f"UPDATE devices SET {set_clause} WHERE udid = %s"
    # params = [data[key] if isinstance(data[key], str) else json.dumps(data[key], ensure_ascii=False) for key in data.keys() if key in DeviceInfo.__annotations__.keys()] + [udid]
    params = []
    for key in data.keys():
        if key in DeviceInfo.__annotations__.keys():
            value = data[key]
            if isinstance(value, str):
                params.append(value)
            elif isinstance(value, bool):
                params.append(1 if value else 0)
            else:
                params.append(json.dumps(value, ensure_ascii=False))
    params.append(udid)
    # result = mysql_execute(command, params)
    return command, params


def func_set_device(udid, name_zh, owner, remarks, connect, device=None):
    if connect and not device:
        return {
            "result": "device 参数缺失",
            "code": 1
        }
    if not connect and device:
        if get_device_status(device):
            subprocess.check_output(["adb", "disconnect", device]).decode("utf-8").strip()
            return {
                "result": "设备已断开",
                "code": 1
            }
    command, params = func_update_device(udid, {
        "name_zh": name_zh,
        "owner": owner,
        "remarks": remarks,
        # "connect_status": "device" if connect else "unknown"
    })
    client = MySQLClient()
    client.connect()

    client.execute_non_query(command, params)

    command, params = func_get_device_info(udid)
    result = client.execute_query(command, params)
    res_data = None
    if result:
        if connect:
            output = subprocess.check_output(["adb", "connect", device]).decode("utf-8").strip()
            time.sleep(0.5)
            if "connected" in output:
                result[0]["connect_status"] = "device"
                udid_recheck = get_device_udid(device)
                if udid_recheck != udid:
                    res_data = f"udid与ip不匹配, 请检查设备信息, 该IP对应udid为: {udid_recheck}"
            elif "timed out" in output:
                res_data = "设备无法连接, 请确认ip"
            else:
                result[0]["connect_status"] = "offline"
        else:
            subprocess.check_output(["adb", "disconnect", device]).decode("utf-8").strip()
            result[0]["connect_status"] = "offline"

        if not res_data:
            res_data = result[0]

    client.connection.commit()
    client.close()
    if res_data:
        return {
            "data": res_data,
            "code": 0,
            "result": "Success"
        }
    else:
        return {
            "data": "",
            "code": 1,
            "result": "设备异常"
        }


def func_get_device_list():
    devices = {}
    output = subprocess.check_output(["adb", "devices"]).decode("utf-8").strip().split("\n")[1:]
    client = MySQLClient()
    client.connect()

    result = client.execute_query("SELECT * FROM devices", [])
    for i in result:
        devices[i["udid"]] = i

    for line in output:
        if line.strip():
            serial, status = line.split("\t")
            try:
                if ":" in serial:
                    udid = subprocess.check_output(["adb", "-s", serial, "shell", "getprop", "ro.serialno"]).decode(
                        "utf-8").strip()
                else:
                    udid = serial

                device_info = devices.get(udid)
                if device_info:
                    # 返回值更新
                    if ":" in serial:
                        device_info["ip"] = serial.split(":")[0]
                        device_info["tcpip_port"] = serial.split(":")[1]
                        device_info["connect_status"] = status.replace("\r", "")
                        # 数据库更新
                        command, params = func_update_device(udid, {
                            "ip": serial.split(":")[0],
                            "tcpip_port": serial.split(":")[1],
                            # "connect_status": status.replace("\r", "")
                        })
                        client.execute_non_query(command, params)
                else:
                    device_info = get_device_info(serial)
                    device_info.connect_status = status.replace("\r", "")
                    if ":" in serial:
                        device_info.tcpip_port = serial.split(":")[1].strip()
                    else:
                        device_info.tcpip_port = "未设置"
                    command, params = func_create_device(device_info)
                    client.execute_non_query(command, params)
                    devices[udid] = device_info.to_dict()
                    result = client.execute_query("SELECT id FROM devices WHERE udid= %s ", [device_info.udid])
                    if result:
                        devices[udid]["id"] = result[0]["id"]

            except Exception as e:
                Log.logger.info("获取设备信息失败: %s", str(e))

    client.close()

    return {
        # "devices": {udid: device.__dict__ for udid, device in devices.items()},
        "devices": devices,
        "code": 0,
        "result": "Success"
    }


def func_get_device_info(device):
    if ":" in device:
        device = device.split(":")[0]
        command = "SELECT * FROM devices WHERE ip = %s"
    else:
        command = "SELECT * FROM devices WHERE udid = %s"
    params = [device]

    # result = mysql_execute(command, params)
    return command, params


def func_get_device_status(device, udid):
    client = MySQLClient()
    client.connect()
    command, params = func_get_device_info(udid)
    result = client.execute_query(command, params)

    if not result:
        return {
            "data": "",
            "result": "设备信息异常",
            "code": 1
        }

    devices = result[0]
    devices["connect_status"] = get_device_status(device)
    if devices["connect_status"] == "device":
        udid_check = subprocess.check_output(["adb", "-s", device, "shell", "getprop", "ro.serialno"]).decode(
            "utf-8").strip()
        if udid_check != udid:
            return {
                "data": "ip与udid不匹配, 该ip设备udid为: " + udid_check,
                "code": 0,
                "result": "请检查设备ip与udid信息"
            }
    else:
        return {
            "data": devices,
            "code": 1,
            "result": "请检查设备ip"
        }

    try:
        # 查进程是最准的, 怕捞数据库的数据不对, 有优化空间
        output = subprocess.check_output(
            f"ps aux | grep {device} | grep -v grep",
            shell=True,
            stderr=subprocess.STDOUT
        )
        pattern = r'-modules\s+(\S+)'
        match = re.search(pattern, output.decode('utf-8', errors='replace'))
        if match:
            modules = match.group(1).split()
            devices["testing_status"] = modules

        return {
            "data": devices,
            "code": 0,
            "result": "Success"
        }

    except subprocess.CalledProcessError as e:
        # 进程不存在说明该设备没在跑
        # if e.returncode == 1:
        return {
            "data": devices,
            "code": 0,
            "result": "Success"
        }


def func_set_device_proxy(device_list, value):
    def set_device_proxy(device, value, response_dict):
        try:
            output_device = subprocess.check_output(
                ["adb", "-s", device, "shell", "settings", "put", "global", "http_proxy", value]).decode(
                "utf-8").strip()
            if "" == output_device:
                response_dict["data"].append({device: "Success"})
            else:
                response_dict["data"].append({device: output_device})
        except subprocess.CalledProcessError as e:
            response_dict[device] = {"result": str(e), "code": 1}

    response_dict = {
        "data": [],
        "code": 0,
        "result": "Success"
    }
    threads = []

    for device in device_list:
        thread = threading.Thread(target=set_device_proxy, args=(device, value, response_dict))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return response_dict
