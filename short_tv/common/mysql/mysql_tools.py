# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/12/3
import re
from datetime import datetime

from common.mysql.mysql import MySQLClient, MySQLClient2
from common.utils.log_utils import Log


def get_case_list():
    return 'SELECT * FROM cases '


def get_title_name(title_name):
    return "SELECT * FROM cases WHERE title_name = %s", [title_name]


def get_case_id(case_id):
    return "SELECT * FROM cases WHERE case_id = %s", [case_id]


def update_case_by_id(case_id, data: dict):
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    return f"UPDATE cases SET {set_clause} WHERE case_id = %s", list(data.values()) + [case_id]


def update_case_by_name(title_name, data: dict):
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    return f"UPDATE cases SET {set_clause} WHERE title_name = %s", list(data.values()) + [title_name]


def create_case(
        module_name=None, class_name=None, title_name=None, case_id=None, module_name_zh=None,
        case_setup=None, case_steps=None, data_resource=None, description=None,
        expect_result=None, pytest_mark=None, allure_mark=None, case_type="功能",
        user_name=None, executor=None, development_status="待编写",
        runtime=None, actual_result=None, passed=None, remarks=None
):
    return """
        INSERT INTO cases (
            module_name, module_name_zh,class_name, title_name,description, case_id, case_setup, case_steps, data_resource, 
            expect_result, pytest_mark, allure_mark, case_type, user_name, executor, development_status, 
            runtime, actual_result, pass, remarks
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """, [
        module_name, module_name_zh, class_name, title_name, description,
        case_id, case_setup, case_steps, data_resource,
        expect_result, pytest_mark, allure_mark, case_type, user_name, executor, development_status,
        runtime, actual_result, passed, remarks
    ]


def delete_case(data: dict):
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])

    return f"DELETE FROM cases WHERE {set_clause}", list(data.values())


def update_device(device, data: dict):
    ip = device.split(":")[0]
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])
    return f"UPDATE devices SET {set_clause} WHERE ip = %s", list(data.values()) + [ip]


def mysql_execute(query, params):
    result = None
    try:
        if not query:
            return
        client = MySQLClient()
        client.connect()
        Log.logger.info("数据库执行: %s,%s", query, params)
        result = client.execute_query(query, params)
        client.connection.commit()
        client.close()
    except Exception as e:
        Log.logger.error(f"数据库执行失败: {e}")

    return result


def mysql_execute_2(query, params):
    if not query:
        return
    client = MySQLClient2()
    client.connect()
    Log.logger.info("数据库执行: %s,%s", query, params)
    result = client.execute_query(query, params)
    client.connection.commit()
    client.close()

    return result


def update_test_case_info(request, test_status, setup, steps, teardown, check):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        case_id = str(request.node.nodeid.split('/')[-1])
        setup_str = ", \n".join([f"{i + 1}. {item}" for i, item in enumerate(setup)])
        steps_str = ", \n".join([f"{i + 1}. {item}" for i, item in enumerate(steps + teardown)])
        # teardown_str = ", ".join([f"{i + 1}. {item}" for i, item in enumerate(teardown)])
        check_str = ", \n".join([f"{i + 1}. {item}" for i, item in enumerate(check)])

        client = MySQLClient()
        result = client.execute_query("SELECT * FROM cases WHERE case_id = %s", [case_id])

        if result:

            if test_status:
                if result[0]["case_setup"] and "脚本逻辑" in result[0]["case_setup"]:
                    new_setup = re.sub(r'脚本逻辑:\s*([\s\S]*)', f'脚本逻辑:\n{setup_str}', result[0]["case_setup"])
                else:
                    new_setup = f"{result[0]['case_setup']}\n脚本逻辑:\n{setup_str}"
                if result[0]["case_steps"] and "脚本逻辑" in result[0]["case_steps"]:
                    new_steps = re.sub(r'脚本逻辑:\s*([\s\S]*)', f'脚本逻辑:\n{steps_str}', result[0]["case_steps"])
                else:
                    new_steps = f"{result[0]['case_steps']}\n脚本逻辑:\n{steps_str}"
                if result[0]["expect_result"] and "脚本逻辑" in result[0]["expect_result"]:
                    new_check = re.sub(r'脚本逻辑:\s*([\s\S]*)', f'脚本逻辑:\n{check_str}', result[0]["expect_result"])
                else:
                    new_check = f"{result[0]['expect_result']}\n脚本逻辑:\n{check_str}"
                # TODO 首波数据处理下, 后续优化
                new_setup = new_setup.replace("None", "<未手动编写功能用例>")
                new_steps = new_steps.replace("None", "<未手动编写功能用例>")
                new_check = new_check.replace("None", "<未手动编写功能用例>")
                client.execute_non_query(
                    "UPDATE cases SET pass= %s,case_setup= %s,case_steps= %s,expect_result = %s, runtime = %s WHERE case_id = %s",
                    [test_status, new_setup, new_steps, new_check, timestamp, case_id])
            else:
                client.execute_non_query(
                    "UPDATE cases SET pass= %s, runtime = %s WHERE case_id = %s",
                    [test_status, timestamp, case_id])

        client.close()

    except Exception as e:
        Log.logger.error(f"用例更新失败: {e}")
    finally:
        Log.logger.info(f"-----{request.node.name}执行结束-----")


if __name__ == '__main__':
    client = MySQLClient()
    client.connect()
    # command, params = create_case(title_name="demo啊哈哈哈哈")
    # client.execute_query(command, params)
    # command, params = create_case(title_name="demo嘻嘻嘻嘻")
    # client.execute_query(command, params)
    # command = get_case_list()
    # 查询

    result = client.execute_query(f"SELECT *  FROM test_plan", [])

    print("************************************\n", result, "\n************************************\n")
    # client.connection.commit()
    client.close()

    # create_case(title_name="demo啊哈哈哈哈")
    # update_case("demo啊哈哈哈哈", {"class_name": "oh"})
    # delete_case({"title_name": "demo啊哈哈哈哈"})
