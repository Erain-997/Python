# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08
import os
import shutil
import time
from test_components.toolkit.mysql_db_method import MysqlDB
from internal.tools.project_path import project_directory, log_path

filePath = os.path.join(project_directory(os.path.dirname(__file__)), "config", "db_config.ini")


def get_db():
    return "vikingard_ui"


db = MysqlDB(filePath, db_name=get_db())


def login_element():
    sql = "SELECT *  FROM vk_login"
    data_object = db.db_execute(sql)

    return data_object


def guide_element():
    sql = "SELECT *  FROM vk_guide"
    data_object = db.db_execute(sql)

    return data_object


def app_init(name):
    sql = "SELECT *  FROM vk_image where name =%s"
    data_object = db.db_execute(sql, args=name)
    return data_object


def show_tables():
    sql = f"select table_name from information_schema.tables where table_schema='{get_db()}'"
    data_object = db.db_execute(sql)
    tables = []
    for data in data_object:
        tables.append(data["TABLE_NAME"])
    return tables


def module_element(table):
    sql = f"SELECT *  FROM {table} order by id"
    data_object = db.db_execute(sql)
    return data_object


def module_order():
    sql = "SELECT *  FROM vk_module_order order by id"
    data_object = db.db_execute(sql)
    sort = {}
    for data in data_object:
        sort[data["id"]] = data["tb_name"]
    return sort


def login_role_write(user_id):
    sql = "update vk_login set input_text=%s where id=1"
    data_object = db.db_execute(sql, args=user_id)
    return data_object


def db_close():
    db.db_close()


def module_object(module):
    tables_list = []
    for key, value in module_order().items():
        tables_list.append(value)
    # 过滤基础表格 引导,模块顺序,登录,图片
    for i in ["vk_guide", "vk_module_order", "vk_login", "vk_image"]:
        if i in tables_list:
            tables_list.remove(i)
    if module != "all":
        if "+" in module:
            tables_list = module.split("+")
            while '' in tables_list:
                tables_list.remove('')
        else:
            tables_list = [module]
        # 执行模块是否被总模块包含
        if not set(tables_list).issubset(set(show_tables())):
            print("无效模块名称")

    for key, value in module_order().items():
        if value in tables_list:
            tables_list.remove(value)
            tables_list.insert(key, value)
    return tables_list


def allure_report_add(task_id, report_path, devices_id):
    add_db = MysqlDB(filePath, db_name="api_report")
    shutil.make_archive('test', 'zip', report_path)
    report_info_file = report_path + r"/" + devices_id + r"/allure-reports/widgets/summary.json"
    with open(report_info_file, "r") as report_f:
        report_info = report_f.read()
        report_f.close()
    report_log_file = log_path() + devices_id + ".log"
    with open(report_log_file, "r", encoding="utf-8") as report_f:
        report_log = report_f.read()
        report_f.close()
    with open("test.zip", 'rb') as f:
        sql = f"INSERT INTO vk_ui_report SET report_name=%s,report_data=%s,create_time=%s ,report_info=%s,log_data=%s"
        add_db.db_execute(sql, args=(task_id, f.read(), str(int(time.time())), report_info, report_log))
        f.close()
    os.remove("test.zip")
    with open(report_log_file, "w", encoding="utf-8") as report_f:
        report_f.write("")
        report_f.close()
    # os.remove(report_log_file)
    add_db.db_close()


