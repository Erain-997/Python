# -*- encoding=utf8 -*-
# Time：2021/08/13
# __author__ = "2018248"
import requests
from airtest.core.api import *
from internal.file import *
from airtest.aircv import *

global resolution
global role_path


def return_kay():
    """
    返回键
    """
    a = exists_imperial(parent_path(__file__) + f"\\screen_shots\\common" + r"\返回.png", (0.453, -0.267))
    if a:
        touch((a[0], a[1]))
        return True
    return False


def off_kay():
    """
    关闭弹窗
    """
    if exists(Template(parent_path(__file__) + f"\\screen_shots\\common" + r"\关闭.png",
                       record_pos=(0.404, -0.646), resolution=resolution)):
        touch(Template(parent_path(__file__) + f"\\screen_shots\\common" + r"\关闭.png"), resolution=resolution)



def main_scene_right():
    swipe((181, 90), (20, 90), duration=0.1, steps=2)


def main_scene_left():
    swipe((181, 90), (500, 90), duration=0.1, steps=2)


def get_resolutiond():
    # 获取当前设备分辨率
    # 给作弊器图片存放的rolePath赋值
    # 给分辨率resolution赋值
    w, h = device().get_current_resolution()
    global resolution
    resolution = (w, h)
    global role_path
    role_path = grandparent_path(__file__) + "\\role\\"
    return w, h


def exists_imperial(path, record_pos=None, threshold=0.8):
    # 简化写法
    return exists(Template(path, record_pos=record_pos, resolution=resolution, threshold=threshold))


def touch_up100(x_and_y):
    if len(x_and_y) > 0:
        touch((x_and_y[0], x_and_y[1] - 100))
    else:
        print("坐标点击up100有问题,速看")


def touch_down150(x_and_y):
    if len(x_and_y) > 0:
        touch((x_and_y[0], x_and_y[1] + 150))
    else:
        print("坐标点击down150有问题,速看")


def touch_left150(x_and_y):
    if len(x_and_y) > 0:
        touch((x_and_y[0] - 150, x_and_y[1]))
    else:
        print("坐标点击左150有问题,速看")


def find_enter_path(target_img_path):
    c = 0
    while not exists_imperial(target_img_path, record_pos=(-0.107, -0.275)):
        if c < 6:
            main_scene_right()
        else:
            main_scene_left()
        c += 1
        if c > 20:
            break


def back_to_main():
    for i in range(5):
        success = return_kay()
        if not success:
            break
        sleep(1.5)


def find_in_area(img_list, area):
    # 在传参区域中寻找目标图片,返回该图片在整个屏幕中的坐标
    # area为左上的xy和右下的xy,比如[81, 890, 733, 1050]
    found_pos = None
    local_screen = aircv.crop_image(G.DEVICE.snapshot(), area)  # 把目标区域截下来,在其中找图
    for i in img_list:
        pos = Template(i).match_in(local_screen)
        if pos:
            # print("在区域中找到了", pos[0] + area[0], pos[1] + area[1])
            found_pos = (pos[0] + area[0], pos[1] + area[1])
            break
    return found_pos


def find_in_area_and_swipe(img_list, area, swipe_pos):
    # swipe_pos参数为滑动起点和终点坐标
    pos = find_in_area(img_list, area)
    c = 0
    while not pos:
        if len(swipe_pos) == 2:
            swipe(swipe_pos[0], swipe_pos[1], duration=0.01, steps=2)
        else:
            touch(swipe_pos[0])
        sleep(0.2)
        pos = find_in_area(img_list, area)
        if c > 45:
            if len(swipe_pos) == 2:
                swipe(swipe_pos[0], swipe_pos[1], duration=0.01, steps=2)
            else:
                touch((swipe_pos[0][0] - 500, swipe_pos[0][1]))
            swipe(swipe_pos[1], swipe_pos[0], duration=0.01, steps=2)
            pos = find_in_area(img_list, area)
        if c > 90:
            break
        c += 1
    return pos


def head():
    width, height = get_resolutiond()
    """
    头部区域
    """
    return [1, 1, width, height * 0.3]


def central_section():
    """
    中部区域
    """
    width, height = get_resolutiond()
    return [1, height * 0.3, width, height * 0.6]


def tail():
    """
    尾部部区域
    """
    width, height = get_resolutiond()
    return [1, height * 0.6, width, height]


def big_central_section():
    """
    大中部区域
    """
    width, height = get_resolutiond()
    return [1, height * 0.2, width, height * 0.8]


def big_tail():
    """
    大中下部区域
    """
    width, height = get_resolutiond()
    return [1, height * 0.4, width, height]
