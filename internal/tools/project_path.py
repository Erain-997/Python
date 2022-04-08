# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08

import os


def root_directory(path_file=__file__, split_path_list=None):
    """
    项目路径
    :param split_path_list: type list
    :param path_file:
    :return:
    """
    cur_path = os.path.abspath(os.path.dirname(path_file))
    if split_path_list is not None and type(split_path_list) is list:
        for i in split_path_list:
            path = cur_path.split(i)[0]
        return path
    return cur_path


def project_directory(path=os.path.dirname(__file__)):
    """
    项目路径
    :param path:
    :return:
    """
    cur_path = os.path.abspath(path)
    return os.path.split(cur_path)[0]


def report_path(task_id, device_id):
    """
    报告路径
    :param path:
    :param task_id:
    :param device_id:
    :return:
    """
    return root_directory(split_path_list=["internal"]) + "report" + "/" + task_id + "/" + device_id


def push_path(task_id):
    """
    报告路径
    :param path:
    :param task_id:

    :return:
    """
    return root_directory(split_path_list=["internal"]) + "report" + "/" + task_id


def allure_path(task_id, device_id):
    """
    html报告路径
    :param path:
    :param task_id:
    :param device_id:
    :return:
    """
    return root_directory(split_path_list=["internal"]) + "report" + "/" + task_id + "/" + device_id + "/allure-reports"


def img_path():
    """
    img 路径
    :param path:
    :return:
    """
    return root_directory(split_path_list=["internal"]) + "img/"


def log_path():
    """
    img 路径
    :param path:
    :return:
    """
    return root_directory(split_path_list=["internal"]) + "report/log/"


def report_img():
    return root_directory(split_path_list=["internal"]) + "report/report_img/"


def config_path(path):
    """
     路径
    :param path:
    :return:
    """
    return project_directory(path) + "/src/config"


def report_mp4():
    return root_directory(split_path_list=["airtest_client_engine"]) + r"vikingar_client_server\apk/"


if __name__ == '__main__':
    print(report_mp4())
