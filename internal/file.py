#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/04/28
# @Author  : zxp
import os
import shutil
import zipfile


def project_directory(path=os.path.dirname(__file__)):
    """
    项目路径
    :param path:
    :return:
    """
    cur_path = os.path.abspath(path)
    return os.path.split(cur_path)[0]


def current_path(path=__file__):
    """
    当前文件路径
    :param path:
    :return:
    """
    return os.path.abspath(os.path.dirname(path))


def parent_path(path=__file__):
    """
    当前文件的父级路径
    :param path:
    :return:
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(path)))


def grandparent_path(path=__file__):
    """
    当前文件的上上级路径
    :param path:
    :return:
    """
    return os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(path))))


def img_path(path=os.path.dirname(__file__)):
    return project_directory(path) + r"\img"


def to_be_find(img, str_list, path=os.path.dirname(__file__)):
    path_list = [project_directory(path) + rf"\api\to_be_test_img\{str(img)}.png"]
    for i in str_list:
        str_last = "_" + str(i)
        path_list.append(project_directory(path) + rf"\api\to_be_test_img\{str(img) + str_last}.png")
    return path_list


def html_path(path=os.path.dirname(__file__)):
    """
    html 路径
    :param path:
    :return:
    """
    return project_directory(path) + r"/reports/"


def auto_path(path=os.path.dirname(__file__)):
    """
    html 路径
    :param path:
    :return:
    """
    return project_directory(path) + r"/auto/"


def log_path(path=os.path.dirname(__file__)):
    """
    html 路径
    :param path:
    :return:
    """
    return project_directory(path) + "/log"


def del_all_file(file_path):
    path_data = [file_path + "/"]
    for path in path_data:
        for i in os.listdir(path):
            if i != "log.txt":
                os.remove(path + i)
            # shutil.rmtree(r'E:\code\tools\airtestProject\wsy_ui\reports\main.log')


def replace_dir_name(root_dir, report_name):
    dirs = os.listdir(root_dir)
    for dir in dirs:
        if dir == "main.log":
            old_name = os.path.join(root_dir, dir)
            new_name = os.path.join(root_dir, report_name)
            os.rename(old_name, new_name)


def make_zip(localPath, zip_name):
    zip_file = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    pre_len = len(os.path.dirname(localPath))
    for parent, dir_names, filenames in os.walk(localPath):
        for filename in filenames:
            path_file = os.path.join(parent, filename)
            arc_name = path_file[pre_len:].strip(os.path.sep)
            zip_file.write(path_file, arc_name)
    zip_file.close()
