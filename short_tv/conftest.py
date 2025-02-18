import json

from common.mysql.mysql import MySQLClient
from common.mysql.mysql_tools import update_case_by_name, create_case, get_title_name, get_case_id, update_case_by_id
from common.utils.arg_parse_func import args
from common.utils.log_utils import Log

DevelopmentStatus = ["待编写", "功能用例编写中", "功能用例已完成", "自动化用例开发中", "自动化用例调试中",
                     "已开发完成"]


def pytest_collection_modifyitems(items):
    if not args.get_cases:
        return
    client = MySQLClient()
    client.connect()
    for item in items:
        case_description = item.function.__doc__ if item.function.__doc__ else "No description provided"
        title_name = getattr(item.function, '__allure_display_name__', None) or item.name

        pytest_mark = []
        development_status = "待编写"
        allure_mark = {"story": [], "feature": []}
        for mark in item.own_markers:
            if mark.name == "allure_label":
                allure_mark[mark.kwargs["label_type"]].append(mark.args[0])
            elif mark.name == "allure_description":
                case_description = mark.args[0]
            elif not mark.name.startswith("allure"):
                pytest_mark.append(mark.name)
                if mark.name in DevelopmentStatus:
                    development_status = mark.name

        # 收集用例信息

        module_name = item.parent.parent.name
        class_name = f"{module_name}::{item.parent.name}"
        case_id = f"{class_name}::{item.name}"
        module_name_zh = ""
        for mark in item.parent.own_markers:
            if mark.name == "allure_label":
                module_name_zh = mark.args[0]
        query, params = get_title_name(title_name)
        Log.logger.info("数据库执行: %s,%s", query, params)
        res_title_name = client.execute_query(query, params)
        query, params = get_case_id(case_id)
        Log.logger.info("数据库执行: %s,%s", query, params)
        res_case_id = client.execute_query(query, params)
        if not res_title_name and not res_case_id:
            query, params = create_case(
                module_name=module_name,
                module_name_zh=module_name_zh,
                class_name=class_name,
                title_name=title_name,
                description=case_description,
                case_id=case_id,
                pytest_mark=json.dumps(pytest_mark, ensure_ascii=False),
                allure_mark=json.dumps(allure_mark, ensure_ascii=False),
                development_status=development_status,
            )
        elif res_case_id:
            query, params = update_case_by_id(case_id, {
                "module_name": module_name,
                "module_name_zh": module_name_zh,
                "class_name": class_name,
                "description": case_description,
                "title_name": title_name,
                "pytest_mark": json.dumps(pytest_mark, ensure_ascii=False),
                "allure_mark": json.dumps(allure_mark, ensure_ascii=False),
                "development_status": development_status,

            })
        else:
            query, params = update_case_by_name(title_name, {
                "module_name": module_name,
                "module_name_zh": module_name_zh,
                "class_name": class_name,
                "description": case_description,
                "case_id": case_id,
                "pytest_mark": json.dumps(pytest_mark, ensure_ascii=False),
                "allure_mark": json.dumps(allure_mark, ensure_ascii=False),
                "development_status": development_status,
            })
        Log.logger.info("数据库执行: %s,%s", query, params)
        client.execute_non_query(query, params)
    client.close()
