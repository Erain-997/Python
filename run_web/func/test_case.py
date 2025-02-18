# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/12/30
import datetime
import json
import os
import shutil
import subprocess
from math import ceil

from common.data import CaseInfo, BASE_DIR, APK_DIR
from common.log_tools import Log
from common.mysql import MySQLClient
from common.tools import mysql_execute, json_case_info, get_device_status, get_module
from func.common import func_git_pull
from func.device import func_get_device_info


def func_get_list(field_name, table_name):
    if field_name == "passed":
        field_name = "pass"
        return {
            "data": ["true", "false", "Null"],
            "code": 0,
            "result": "success"
        }
    command = f"SELECT DISTINCT {field_name} FROM {table_name}"
    result = mysql_execute(command, [])
    if result:
        if field_name == "allure_mark":
            unique_values = {"story": [], "feature": []}
            for row in result:
                if "allure_mark" in row and row["allure_mark"] and "story" in json.loads(row["allure_mark"]):
                    name = json.loads(row["allure_mark"])["story"]
                    unique_values["story"].append(name)
                if "allure_mark" in row and row["allure_mark"] and "feature" in json.loads(row["allure_mark"]):
                    name = json.loads(row["allure_mark"])["feature"]
                    unique_values["feature"].append(name)
        elif field_name == "pytest_mark":
            tmp = set()
            for row in result:
                if "pytest_mark" in row and row["pytest_mark"]:
                    name = json.loads(row["pytest_mark"])
                    for i in name:
                        tmp.add(f"{i}")
            unique_values = list(tmp)
        else:
            unique_values = [row[field_name] for row in result if row[field_name]]
        return {
            "data": unique_values,
            "code": 0,
            "result": "success"
        }
    else:
        return {
            "data": "请检查字段",
            "code": -1,
            "result": "error"
        }


def func_create_case(case_info: CaseInfo):
    command = """
        INSERT INTO cases (
            module_name, class_name, title_name, case_id, case_setup, case_steps, data_resource, 
            expect_result, pytest_mark, allure_mark, case_type, user_name, executor, development_status, 
            runtime, actual_result, pass, remarks
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """
    params = [
        case_info.module_name, case_info.class_name, case_info.title_name,
        case_info.case_id, case_info.case_setup, case_info.case_steps, case_info.data_resource,
        case_info.expect_result, case_info.pytest_mark, case_info.allure_mark, case_info.case_type, case_info.user_name,
        case_info.executor, case_info.development_status,
        case_info.runtime, case_info.actual_result, False, case_info.remarks
    ]

    result = mysql_execute(command, params)
    recheck = func_get_case(case_info.title_name)
    if not recheck["data"]:
        response = {
            "data": result,
            "code": 0,
            "result": "用例新增失败"
        }
    else:
        response = {
            "data": recheck["data"][0],
            "code": 0,
            "result": "success"
        }
    return response


def func_delete_case(datas):
    # todo 要是出现了先写代码再写用例的情况, 就在网页上补充用例名, 确保用例名字存在
    # error_list=[]
    for data in datas["title_name"]:
        # set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
        command = f"DELETE FROM cases WHERE title_name=%s"
        params = [data]
        result = mysql_execute(command, params)

    return {
        "code": 0,
        "result": "success"
    }


def func_update_case(title_name, data: dict):
    del data['title_name']
    set_clause = ", ".join([f"{key} = %s" for key in data.keys() if key in CaseInfo.__annotations__.keys()])
    command = f"UPDATE cases SET {set_clause} WHERE title_name = %s"
    command = command.replace("passed", "pass")
    # params = [data[key] if isinstance(data[key], str) else json.dumps(data[key], ensure_ascii=False) for key in data.keys() if key in CaseInfo.__annotations__.keys()] + [title_name]
    params = []
    for key in data.keys():
        if key in CaseInfo.__annotations__.keys():
            value = data[key]
            if isinstance(value, str):
                params.append(value)
            elif isinstance(value, bool):
                params.append(1 if value else 0)
            else:
                params.append(json.dumps(value, ensure_ascii=False))
    params.append(title_name)
    if len(params) > 1:
        result = mysql_execute(command, params)

    recheck = func_get_case(title_name)
    if not recheck["data"]:
        response = {
            "data": {},
            "code": 1,
            "result": "用例更新失败, 找不到该用例名称的用例"
        }
    else:
        response = {
            "data": recheck["data"][0],
            "code": 0,
            "result": "success"
        }
    return response


def func_get_case(title_name):
    command = "SELECT * FROM cases WHERE title_name = %s"
    params = [title_name]
    result = mysql_execute(command, params)
    if not result:
        response = {
            "data": [],
            "code": 0,
            "result": "用例不存在"
        }
    else:
        response = {
            "data": json_case_info(result),
            "code": 0,
            "result": "success"
        }
    return response


def func_get_case_list(data: dict, page=1, size=10):
    client = MySQLClient()
    client.connect()
    if "passed" in data:
        if data["passed"] == "true":
            data["passed"] = True
        elif data["passed"] == "false":
            data["passed"] = False
        else:
            data["passed"] = 'null'

    # 获取总记录数
    set_clause = " and ".join([f"{key} = %s" for key in data.keys() if key in CaseInfo.__annotations__.keys()])
    if "passed" in set_clause:
        set_clause = set_clause.replace("passed", "pass")
    params = [data[key] for key in data.keys() if key in CaseInfo.__annotations__.keys()]
    if "pass = " in set_clause and data["passed"] == 'null':
        set_clause = set_clause.replace("pass = %s", "pass is null")
        params.remove('null')
    if params or "passed" in data:
        total_count_query = f"SELECT COUNT(*) FROM cases WHERE {set_clause}"
    else:
        total_count_query = f"SELECT COUNT(*) FROM cases"
    total_count_result = client.execute_query(total_count_query, params)
    total_count = total_count_result[0]["COUNT(*)"] if total_count_result else 0
    if total_count == 0:
        return {
            "data": {
                "report_path": "/reports/index.html",
                "report_log_path": "/log",
                "report_root_path": "/files",
                "report_list": [],
                "total_pages": 1,
                "current_page": 1,
                "total_count": 0,
            },
            "code": 0
        }

    max_page = (total_count + size - 1) // size  # 向上取整

    # 确定当前页是否在有效范围内
    if page > max_page:
        page = max_page
        if max_page == 0:  # 当total_count为0时
            page = 1
            size = total_count  # 或者使用默认值

    # 计算偏移量
    offset = (page - 1) * size
    if (params or "passed" in data) and set_clause:
        if page == 1 and total_count <= size:
            query = f"SELECT * FROM cases WHERE {set_clause} ORDER BY id DESC"
        else:
            query = f"SELECT * FROM cases WHERE {set_clause} ORDER BY id DESC LIMIT {str(size)} OFFSET {str(offset)}"
    else:
        if page == 1 and total_count <= size:
            query = f"SELECT * FROM cases ORDER BY id DESC"
        else:
            query = f"SELECT * FROM cases ORDER BY id DESC LIMIT {str(size)} OFFSET {str(offset)}"

    result = client.execute_query(query, params)
    client.close()

    # 计算总页数
    total_pages = ceil(total_count / int(size))

    response = {
        "data": {
            "cases_list": json_case_info(result),
            "total_pages": total_pages,
            "current_page": page,
            "total_count": total_count,
            "path": "sys_android/test_cases/new"
        },
        "code": 0
    }

    return response


async def func_run_cases(plan_id):
    if plan_id == -1:
        func_git_pull()
        command = ["python", f"{BASE_DIR}/run_mobile_ui_automation_tests.py", "1", "1", "-get_cases"]
        subprocess.Popen(command, cwd=BASE_DIR)
        return {
            "data": "更新代码用例入库",
            "code": 0,
            "result": "success"
        }

    client = MySQLClient()
    client.connect()
    result = client.execute_query("SELECT * FROM test_plan WHERE id = %s", [plan_id])
    if not result:
        return {
            "data": "plan_id 有误",
            "code": 1,
            "result": "error"
        }
    udid = result[0]["device"]

    command, params = func_get_device_info(udid)
    result_device = client.execute_query(command, params)
    if not result_device:
        return {
            "data": "设备信息异常",
            "code": 0
        }
    else:
        if result_device[0]["testing_status"] is not None:
            return {
                "data": "",
                "code": 1,
                "result": "该设备正在测试中"
            }

    device_ip = result_device[0]["ip"] + ":" + result_device[0]["tcpip_port"]
    status = get_device_status(device_ip)
    if status == "device":
        udid_check = subprocess.check_output(["adb", "-s", device_ip, "shell", "getprop", "ro.serialno"]).decode(
            "utf-8").strip()
        if udid_check != udid:
            return {
                "data": "ip与udid不匹配, 该ip设备udid为: " + udid_check,
                "code": 0,
                "result": "请检查设备ip与udid信息"
            }
    else:
        subprocess.check_output(["adb", "connect", device_ip])
        output = subprocess.check_output(["adb", "devices"]).decode("utf-8").strip().split("\n")[1:]
        Log.logger.info(f"查看当前已连接设备: {output}")
        Log.logger.info(f"尝试重新连接设备: {device_ip}")
        status = get_device_status(device_ip)
        if status != "device":
            return {
                "data": result_device,
                "code": 1,
                "result": "设备已掉线"
            }

    task_id = result[0]["id"]
    root_path = result[0]["root_path"]
    if not root_path:
        root_path = "sys_android/test_cases/new/"
    apk = result[0]["apk"]
    apk_select_version = result[0]["apk_select_version"]
    apk_select_package = result[0]["apk_select_package"]
    k = result[0]["k"]
    m = result[0]["m"]
    proxy = result[0]["proxy"]
    feishu = result[0]["feishu"]
    record = result[0]["record"]
    language = result[0]["language"]
    allure_features = json.loads(result[0]["allure_features"])
    allure_stories = json.loads(result[0]["allure_stories"])
    modules = json.loads(result[0]["modules"])
    test_now = datetime.datetime.now()
    report = f"{device_ip.replace('.', '_').replace(':', '_')}_{test_now.strftime('%Y_%m_%d_%H_%M_%S')}"
    command = ["python", f"{BASE_DIR}/run_mobile_ui_automation_tests.py", device_ip, report, "-root_path", root_path,
               "-task_id", str(task_id), "-compress"]

    # 处理模块
    cases = []
    for i in modules:
        module_name = get_module(i)
        if module_name:
            cases.append(os.path.join(root_path, module_name))
        else:
            cases.append(os.path.join(root_path, i))
    for i in cases:
        if "::" in i:
            file = i.split("::")[0]
        else:
            file = i
        if not os.path.exists(os.path.join(BASE_DIR, file)):
            return {
                "data": f"{i} 用例不存在, 请确认用例",
                "code": 1,
                "result": "error"
            }
    try:
        if cases:
            command.extend(["-modules", *cases])
        else:
            command.extend(["-modules", root_path])
        if k or m or allure_features or allure_stories:
            # command.extend([])
            if k:
                command.extend(["-k", k])
            elif m:
                command.extend(["-m", m])
            elif allure_features:
                command.extend(["--allure_features", *allure_features])
            elif allure_stories:
                command.extend(["--allure_stories", *allure_stories])

        if proxy:
            command.append("-proxy")
        if feishu:
            command.append("-feishu")
        if record:
            command.append("-record")
        if apk:
            apk_path = os.path.join(APK_DIR, "short_tv_apk", apk_select_version, apk_select_package)
            command.extend(["-apk", apk_path])
        if language:
            command.extend(["-language", language])

        mysql_execute(f"UPDATE test_plan SET status='Running',last_run_time= %s,last_report=%s WHERE id = %s",
                      [test_now.strftime("%Y-%m-%d %H:%M:%S"), f"files/{report}", plan_id])

        Log.logger.info("pytest命令:%s", command)
        subprocess.Popen(command, cwd=BASE_DIR)
        return {
            "data": {
                "log": f"files/{report}/log",
                "report": f"files/{report}/reports/index.html"
            },
            "code": 0,
            "result": "success"
        }

        # # 等待子进程结束（可选）
        # await task
        # process.wait()
    except subprocess.CalledProcessError as e:
        return {
            "data": str(e),
            "code": 1,
            "result": "error"
        }


def func_stop_testing(plan_id):
    command = "SELECT * FROM test_plan WHERE id = %s"
    params = [plan_id]

    result = mysql_execute(command, params)
    if not result:
        return {
            "data": "请确认 plan_id",
            "code": 1,
            "result": "error"
        }
    # 清理环境
    # 删除文件夹
    udid = result[0]["device"]
    if "/" in result[0]["last_report"]:
        folder_path = os.path.join(BASE_DIR, 'report_output', result[0]["last_report"].split("/")[1])

        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            Log.logger.info(f"成功删除文件夹: {folder_path}")
        else:
            Log.logger.info(f"文件夹不存在: {folder_path}")
    try:
        command, params = func_get_device_info(udid)
        result_device = mysql_execute(command, params)
        if not result_device:
            return {
                "data": "设备信息异常",
                "code": 0
            }

        device = result_device[0]["ip"] + ":" + result_device[0]["tcpip_port"]
        output = ""
        try:
            output = subprocess.check_output(
                f"ps aux | grep {device} | grep -v grep",
                shell=True,
                stderr=subprocess.STDOUT
            ).decode("utf-8")
        except subprocess.CalledProcessError as e:
            mysql_execute(f"UPDATE test_plan SET status='Not Running' WHERE id = %s", [plan_id])
            return {
                "data": "当前设备无进程",
                "code": 0,
                "result": "success"
            }
        if output != "":
            Log.logger.info("\n当前设备%s, 存在的进程:%s\n", device, output)
            # 清理主进程
            output = subprocess.check_output(
                f"sudo pkill -f '{device}'",
                shell=True,
                stderr=subprocess.STDOUT
            ).decode("utf-8")
            # 清理appium
            if result_device[0]["appium_port"]:
                output = subprocess.check_output(
                    f"sudo pkill -f '{"appium -p " + result_device[0]["appium_port"]}'",
                    shell=True,
                    stderr=subprocess.STDOUT
                ).decode("utf-8")
            # 清理mitmdump
            if result_device[0]["mitmdump_port"]:
                output = subprocess.check_output(
                    f"sudo pkill -f '{"mitmdump -v --mode regular -p " + result_device[0]["mitmdump_port"]}'",
                    shell=True,
                    stderr=subprocess.STDOUT
                ).decode("utf-8")

            mysql_execute(f"UPDATE test_plan SET status='Stop',appium_port=null,mitmdump_port=null WHERE id = %s",
                          [plan_id])
            mysql_execute(f"UPDATE devices SET testing_status=null WHERE udid = %s", [udid])
            subprocess.check_output(["adb", "-s", device, "shell", "settings", "put", "global", "http_proxy", ":0"])
            return {
                "data": {},
                "code": 0,
                "result": "success"
            }

    except subprocess.CalledProcessError as e:
        mysql_execute(f"UPDATE test_plan SET status='Stop' WHERE id = %s", [plan_id])
        mysql_execute(f"UPDATE devices SET testing_status=null WHERE udid = %s", [udid])
        if "Signals.SIGTERM: 15" in str(e):
            return {
                "data": {},
                "code": 0,
                "result": "success"
            }
        else:
            return {
                "data": str(e),
                "code": 1,
                "result": "error"
            }
