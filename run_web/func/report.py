# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/12/30
import json
import os
import shutil
import subprocess
from math import ceil

from common.data import BASE_DIR, ReportInfo
from common.log_tools import Log
from common.mysql import MySQLClient
from common.tools import mysql_execute, get_device_name_zh


def func_delete_report(report_names):
    error_list = {}
    for report_name in report_names:
        try:
            folder_path = os.path.join(BASE_DIR, 'report_output', report_name)

            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                Log.logger.info(f"成功删除文件夹: {folder_path}")

                client = MySQLClient()
                client.connect()
                report_name = f"files/{report_name}/reports/index.html"
                result = client.execute_query("SELECT * FROM  report WHERE new_name=%s", [report_name])
                if result:
                    plan_id = result[0]["plan_id"]
                    result_plan = client.execute_query("SELECT * FROM test_plan WHERE id=%s", [plan_id])
                    if result_plan:
                        if result_plan[0]["last_report"] and result_plan[0]["last_report"] == report_name:
                            client.execute_non_query("UPDATE test_plan SET last_report=%s  WHERE id=%s",
                                                     [None, plan_id])
                        if result_plan[0]["report"] and report_name in json.loads(result_plan[0]["report"]):
                            updated_list = json.loads(result_plan[0]["report"])
                            updated_list.remove(report_name)
                            if not updated_list:
                                updated_list = None
                            else:
                                updated_list = json.dumps(updated_list, ensure_ascii=False)
                            client.execute_non_query("UPDATE test_plan SET report=%s  WHERE id=%s",
                                                     [updated_list, plan_id])

                client.execute_non_query("DELETE FROM report WHERE new_name = %s", [report_name])

            else:
                Log.logger.info(f"文件夹不存在: {folder_path}")

        except Exception as e:
            Log.logger.error(f"删除文件夹时发生错误: {str(e)}")
            error_list[report_name] = {
                "result": str(e)
            }
    if error_list:
        return {
            "data": "",
            "code": 1,
            "result": error_list
        }
    else:
        return {
            "data": {},
            "code": 0,
            "result": "success"
        }


def func_update_report(old_name, new_name):
    old = f"{BASE_DIR}/report_output/{old_name}"
    new = f"{BASE_DIR}/report_output/{new_name}"
    os.rename(old, new)

    report_old = f"files/{old_name}/reports/index.html"
    report_new = f"files/{new_name}/reports/index.html"

    client = MySQLClient()
    client.connect()
    client.execute_non_query("UPDATE report SET new_name=%s  WHERE old_name=%s", [report_new, report_old])

    result = client.execute_query("SELECT * FROM  report WHERE old_name=%s", [report_old])
    if result:
        result_plan = client.execute_query("SELECT * FROM test_plan WHERE id=%s", [result[0]["plan_id"]])
        if result_plan:
            if result_plan[0]["last_report"] and result_plan[0]["last_report"] == report_old:
                client.execute_non_query("UPDATE test_plan SET last_report=%s  WHERE id=%s",
                                         [report_new, result[0]["plan_id"]])
            if result_plan[0]["report"] and report_old in json.loads(result_plan[0]["report"]):
                updated_list = [s.replace(report_old, report_new) for s in json.loads(result_plan[0]["report"])]
                client.execute_non_query("UPDATE test_plan SET report=%s  WHERE id=%s",
                                         [json.dumps(updated_list, ensure_ascii=False), result[0]["plan_id"]])
    client.close()

    response = {
        "data": {
            "report_path": "/reports/index.html",
            "report_log_path": "/log",
            "report_root_path": "/files",
            "report": new
        },
        "code": 0
    }
    return response


def func_get_report_list(data: dict, page=1, size=10):
    output = subprocess.check_output(["ls", f"{BASE_DIR}/report_output"])
    report_list = output.decode('utf-8', errors='replace').splitlines()

    report_list.remove("flow_data")
    report_list.remove("mock")

    client = MySQLClient()
    client.connect()
    res_data = []
    # 获取总记录数
    set_clause = " and ".join([f"{key} = %s" for key in data.keys() if key in ReportInfo.__annotations__.keys()])
    params = []
    for key in data.keys():
        if key in ReportInfo.__annotations__.keys():
            value = data[key]
            params.append(value)
    if params:
        total_count_query = f"SELECT COUNT(*) FROM test_plan RIGHT JOIN report ON test_plan.id = report.plan_id WHERE {set_clause}"
    else:
        total_count_query = f"SELECT COUNT(*) FROM test_plan RIGHT JOIN report ON test_plan.id = report.plan_id"
    total_count_result = client.execute_query(total_count_query, params)
    total_count = total_count_result[0]["COUNT(*)"] if total_count_result else 0
    if total_count == 0:
        return {
            "data": {},
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

    # 构建查询语句
    if params and set_clause:
        if page == 1 and total_count <= size:
            query = f"SELECT plan_id, device,report.new_name, name,report.test_cases,case_num,report.pass_rate,apk_version,run_time FROM test_plan RIGHT JOIN report ON test_plan.id = report.plan_id WHERE {set_clause} ORDER BY report.id DESC"
        else:
            query = f"SELECT plan_id, device,report.new_name, name,report.test_cases,case_num,report.pass_rate,apk_version,run_time FROM test_plan RIGHT JOIN report ON test_plan.id = report.plan_id WHERE {set_clause} ORDER BY report.id DESC LIMIT {str(size)} OFFSET {str(offset)}"
    else:
        if page == 1 and total_count <= size:
            query = f"SELECT plan_id, device,report.new_name, name,report.test_cases,case_num,report.pass_rate,apk_version,run_time FROM test_plan RIGHT JOIN report ON test_plan.id = report.plan_id ORDER BY report.id DESC"
        else:
            query = f"SELECT plan_id, device,report.new_name, name,report.test_cases,case_num,report.pass_rate,apk_version,run_time FROM test_plan RIGHT JOIN report ON test_plan.id = report.plan_id ORDER BY report.id DESC LIMIT {str(size)} OFFSET {str(offset)}"

    # 如果只有一页且总记录数小于或等于size，则不使用LIMIT和OFFSET

    result = client.execute_query(query, params)
    client.close()

    # 计算总页数
    total_pages = ceil(total_count / int(size))

    for i in result:
        try:
            # todo 优化, 放到最后或最前
            if "name" in i and i["name"] == '接口后端日志':
                res_data.append({
                    "report_name": i["name"],
                    "name": i["name"],
                    "plan_id": 999,
                })
            elif "new_name" in i and i["new_name"].replace("files/", "").replace("/reports/index.html",
                                                                                 "") in report_list:
                res_data.append({
                    "report_name": i["new_name"].replace("files/", "").replace("/reports/index.html", ""),
                    "device": get_device_name_zh(i["device"]),
                    "name": i["name"],
                    "plan_id": i["plan_id"],
                    "test_cases": i["test_cases"],
                    "case_num": i["case_num"],
                    "pass_rate": i["pass_rate"],
                    "apk_version": i["apk_version"],
                    "run_time": i["run_time"],

                })
            elif "new_name" in i and i["new_name"].replace("files/", "").replace("/reports/index.html",
                                                                                 "") not in report_list:
                res_data.append({
                    "report_name": i["new_name"].replace("files/", "").replace("/reports/index.html", ""),
                    "device": get_device_name_zh(i["device"]),
                    "name": i["name"],
                    "plan_id": 0,
                    "test_cases": i["test_cases"],
                    "case_num": i["case_num"],
                    "pass_rate": i["pass_rate"],
                    "apk_version": i["apk_version"],
                    "run_time": i["run_time"],
                })
            else:
                res_data.append({
                    "report_name": "未匹配到测试计划",
                    "device": get_device_name_zh(i["device"]),
                    "name": i["name"],
                    "plan_id": 0,
                    "test_cases": i["test_cases"],
                    "case_num": i["case_num"],
                    "pass_rate": i["pass_rate"],
                    "apk_version": i["apk_version"],
                    "run_time": i["run_time"],
                })
        except Exception as e:
            Log.logger.info(f"字段解析失败: {str(e)}, {i}")
    response = {
        "data": {
            "report_path": "/reports/index.html",
            "report_log_path": "/log",
            "report_root_path": "/files",
            "report_list": res_data,
            "total_pages": total_pages,
            "current_page": page,
            "total_count": total_count,
        },
        "code": 0
    }
    return response


def func_get_list_report(field_name):
    table_name = "report"
    if field_name == "name" or field_name == "device":
        table_name = "test_plan"

    command = f"SELECT DISTINCT {field_name} FROM {table_name}"
    result = mysql_execute(command, [])
    if result:
        if field_name == "modules":
            unique_values = []
            for row in result:
                if "modules" in row and row["modules"]:
                    name = json.loads(row["modules"])
                    unique_values.append(name)
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
