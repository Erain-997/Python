# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/12/30
import json
from math import ceil

from common.data import TestPlan
from common.mysql import MySQLClient
from common.tools import mysql_execute, json_case_plan_info


def func_test_plan_add(test_plan: TestPlan):
    if (
            test_plan.allure_stories or test_plan.allure_features or test_plan.k or test_plan.m) and not test_plan.root_path:
        return {
            "data": test_plan.to_dict(),
            "code": 1,
            "result": "新增用例失败, 请检查root_path路径"
        }
    client = MySQLClient()
    client.connect()
    command = """
            INSERT INTO test_plan (
                name,device,language, root_path,modules, proxy, feishu, record, apk,apk_select_version,apk_select_package, k, m, status, 
                allure_features, allure_stories, version, creat_time, update_time, user,remarks
            ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s
        );
        """
    params = [
        test_plan.name, test_plan.device, test_plan.language, test_plan.root_path,
        json.dumps(test_plan.modules, ensure_ascii=False),
        test_plan.proxy,
        test_plan.feishu, test_plan.record, test_plan.apk, test_plan.apk_select_version, test_plan.apk_select_package,
        test_plan.k,
        test_plan.m, "Not Running", json.dumps(test_plan.allure_features, ensure_ascii=False),
        json.dumps(test_plan.allure_stories, ensure_ascii=False), test_plan.version,
        test_plan.creat_time, test_plan.update_time, test_plan.user, test_plan.remarks
    ]

    client.execute_non_query(command, params)
    result_id = client.execute_query("SELECT LAST_INSERT_ID()", [])
    if not result_id:
        return {
            "data": test_plan.to_dict(),
            "code": 1,
            "result": "新增用例失败, 请检查字段"
        }
    new_id = result_id[0]["LAST_INSERT_ID()"]
    result = client.execute_query(f"SELECT * FROM test_plan WHERE id = %s", [new_id])
    client.close()
    for i in result:
        if i['apk']:
            i['apk'] = True
        else:
            i['apk'] = False
    return {
        "data": json_case_plan_info(result),
        "code": 0
    }


def func_delete_test_plan(plan_id):
    mysql_execute(f"DELETE FROM test_plan WHERE id = '{plan_id}'", [])

    return {
        "data": "该测试计划已删除",
        "code": 0
    }


def func_update_test_plan(plan_id, data: dict):
    client = MySQLClient()
    client.connect()
    del data['plan_id']
    set_clause = ", ".join([f"{key} = %s" for key in data.keys() if key in TestPlan.__annotations__.keys()])
    command = f"UPDATE test_plan SET {set_clause} WHERE id = %s"
    params = []
    for key in data.keys():
        if key in TestPlan.__annotations__.keys():
            value = data[key]
            if isinstance(value, str):
                params.append(value)
            elif isinstance(value, bool):
                params.append(1 if value else 0)
            else:
                params.append(json.dumps(value, ensure_ascii=False))
    params.append(plan_id)
    # params =[data[key] if isinstance(data[key], str) else json.dumps(data[key], ensure_ascii=False) for key in data.keys() if key in TestPlan.__annotations__.keys()] + [plan_id]
    client.execute_non_query(command, params)

    recheck = client.execute_query(f"SELECT * FROM test_plan WHERE id = %s", [plan_id])
    client.close()
    if recheck:
        for i in recheck:
            if i['apk']:
                i['apk'] = True
            else:
                i['apk'] = False
        response = {
            "data": json_case_plan_info(recheck),
            "code": 0,
            "result": "success"
        }
    else:
        response = {
            "data": "plan_id 不存在",
            "code": 1,
            "result": "success"
        }
    return response


def func_get_test_plan(plan_id):
    command = "SELECT * FROM test_plan WHERE id = %s"
    params = [plan_id]

    result = mysql_execute(command, params)
    if not result:
        response = {
            "data": [],
            "code": 0,
            "result": "测试计划不存在"
        }
    else:
        if result[0]["report"]:
            report_num = json.loads(result[0]["report"])
            result[0]["report_num"] = len(report_num)
        else:
            result[0]["report_num"] = 0
        if result[0]['apk']:
            result[0]['apk'] = True
        else:
            result[0]['apk'] = False
        response = {
            "data": json_case_plan_info(result),
            "code": 0,
            "result": "success"
        }
    return response


def func_test_plan_list(data: dict, page=1, size=10):
    client = MySQLClient()
    client.connect()

    # 获取总记录数
    set_clause = " and ".join([f"{key} = %s" for key in data.keys() if key in TestPlan.__annotations__.keys()])
    # params = [data[key] for key in data.keys() if key in TestPlan.__annotations__.keys()]
    params = []
    for key in data.keys():
        if key in TestPlan.__annotations__.keys():
            value = data[key]
            if key == "modules":
                params.append(json.dumps(value, ensure_ascii=False))
            else:
                params.append(value)
    if params:
        total_count_query = f"SELECT COUNT(*) FROM test_plan WHERE {set_clause}"
    else:
        total_count_query = f"SELECT COUNT(*) FROM test_plan"
    total_count_result = client.execute_query(total_count_query, params)
    total_count = total_count_result[0]["COUNT(*)"] if total_count_result else 0
    if total_count == 0:
        return {
            "data": {},
            "code": 0
        }

    # 计算总页数
    max_page = ceil(total_count / int(size))
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
            query = f"SELECT * FROM test_plan WHERE {set_clause} ORDER BY id DESC"
        else:
            query = f"SELECT * FROM test_plan WHERE {set_clause} ORDER BY id DESC LIMIT {size} OFFSET {offset}"
    else:
        if page == 1 and total_count <= size:
            query = f"SELECT * FROM test_plan ORDER BY id DESC"
        else:
            query = f"SELECT * FROM test_plan ORDER BY id DESC LIMIT {size} OFFSET {offset}"

    # 如果只有一页且总记录数小于或等于size，则不使用LIMIT和OFFSET

    result = client.execute_query(query, params)
    client.close()

    # 计算总页数
    # total_pages = ceil(total_count / int(size))

    for i in result:
        if i['apk']:
            i['apk'] = True
        else:
            i['apk'] = False
        if i["report"]:
            report_num = json.loads(i["report"])
            i["report_num"] = len(report_num)
        else:
            i["report_num"] = 0
    response = {
        "data": {
            "test_plan_list": json_case_plan_info(result),
            "total_pages": max_page,
            "current_page": page,
            "total_count": total_count,
        },
        "code": 0
    }
    return response


def func_get_list_test_plan(field_name, table_name):
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
