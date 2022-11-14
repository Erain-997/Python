# _*_coding:utf-8_*_
# Author：zxp
# Time：2021/01/13

import os
import configparser


def root_directory(path):
    """
    项目路径
    :param path:
    :return:
    """
    cur_path = os.path.abspath(path)
    return os.path.split(cur_path)[0] + '/' + os.path.split(cur_path)[1]


def project_directory(path):
    """
    项目路径
    :param path:
    :return:
    """
    cur_path = os.path.abspath(path)
    return os.path.split(cur_path)[0]


def report_path(path):
    """
    报告路径
    :param path:
    :return:
    """
    return root_directory(path) + "/result"


def img_path(path=os.path.dirname(__file__)):
    """
    img 路径
    :param path:
    :return:
    """
    return root_directory(path) + "/img/"


def config_path(path=os.path.dirname(__file__)):
    """
    img 路径
    :param path:
    :return:
    """
    return root_directory(path) + "/config/config.ini"
