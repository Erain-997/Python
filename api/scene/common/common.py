# -*- encoding=utf8 -*-
# Time：2021/08/13
# __author__ = "2018248"

from airtest.core.api import *
from internal.file import grandparent_path


def max_return_kay(language):
    """
    大圆返回键
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\大返回.png",
                   record_pos=(0.453, -0.267), resolution=resolution))


def square_off(language):
    """
    方形灯笼叉叉
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\方形灯笼关闭.png",
                   record_pos=(0.409, -0.235), resolution=resolution))


def min_return_kay(language):
    """
    小方返回键
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\小返回.png",
                   record_pos=(0.453, -0.267), resolution=resolution))


def out_palace(language):
    """
    出宫
    :return:
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\出宫.png",
                   record_pos=(0.436, 0.205), resolution=resolution))


def return_palace(language):
    """
    回宫
    :return:
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\回宫.png",
                   record_pos=(0.433, 0.202), resolution=resolution))


def use_button(language):
    """
    使用按钮
    :return:
    """
    resolution = get_resolution()
    touch(
        Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\使用按钮.png",
                 record_pos=(0.271, 0.167),
                 resolution=resolution))


def open_rush_activity(language):
    """
    打开冲榜活动列表
    :return:
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\开冲榜活动.png",
                   record_pos=(0.177, -0.228), resolution=resolution))


def open_cross_activity(language):
    """
    打开跨服活动列表
    :return:
    """
    resolution = get_resolution()
    touch(
        Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\跨服活动.png",
                 record_pos=(0.09, -0.226),
                 resolution=resolution))


def close_hero(language):
    """
    红灯笼黑叉叉关闭，关闭英雄列表
    :return:
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\红灯笼关闭.png",
                   record_pos=(0.426, -0.174), resolution=resolution))


def open_activity(language):
    """
    打开活动列表
    :return:
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\开活动集合.png",
                   record_pos=(0.445, -0.138), resolution=resolution))


def close_activity(language):
    """
    关闭活动集合
    :return:
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\关活动集合.png",
                   record_pos=(0.445, -0.143), resolution=resolution))


def left_cross_activity(language):
    """
    跨服活动列表右滑
    :return:
    """
    resolution = get_resolution()
    swipe(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\跨服活动右滑.png",
                   record_pos=(0.354, 0.098), resolution=resolution),
          vector=[-0.662, 0.0023])


def close_rush_activity(language):
    """
    关闭冲榜活动列表
    :return:
    """
    resolution = get_resolution()
    touch(Template(grandparent_path(__file__) + f"\\language\\{language}\\common" + r"\关冲榜活动.png",
                   record_pos=(0.459, -0.232), resolution=resolution))


def get_resolution():
    # 获取当前设备分辨率
    w, h = device().get_current_resolution()
    return [w, h]


def exists_imperial(path, common_name, resolution, record):
    return exists(Template(path + common_name, record_pos=record,
                           resolution=resolution))


def swipe_func(path, img_name, record_pos, vector, target_name, record):
    resolution = get_resolution()
    c = 1

    while not exists_imperial(path, fr"{target_name}.png", resolution, record):
        swipe(Template(path + fr"{img_name}.png", record_pos=record_pos, resolution=resolution),
              vector=vector)
        c += 1
        if c == 15:
            # 找不着，返回主界面
            return
    if exists_imperial(path, fr"{target_name}.png", resolution, record):
        touch(Template(path + fr"{target_name}.png", record_pos=record, resolution=resolution))
