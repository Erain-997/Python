# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08

from internal.tools.db import app_init
from internal.tools.project_path import img_path
from airtest.core.api import *

first_time_img = []


def wait_func(case_name):
    data = app_init(case_name)[0]
    if data.get('name') == case_name:
        with open(img_path() + data.get('name') + '.png', 'wb') as f:
            f.write(data.get('data'))
            f.close()
        wait(Template(img_path() + data.get('name') + '.png',
                      record_pos=(data.get('pos_x'), data.get('pos_y')),
                      resolution=(data.get('resolution_x'), data.get('resolution_y'))), timeout=50)


def exists_func(case_name):
    data = app_init(case_name)[0]
    if data.get('name') == case_name:
        if not os.path.exists(img_path() + data.get('name') + '.png') or data.get('name') not in first_time_img:
            first_time_img.append(data.get('name'))
            with open(img_path() + data.get('name') + '.png', 'wb') as f:
                f.write(data.get('data'))
                f.close()
        result = exists(Template(img_path() + data.get('name') + '.png',
                                 record_pos=(data.get('pos_x'), data.get('pos_y')),
                                 resolution=(data.get('resolution_x'), data.get('resolution_y'))))
        if result is False:
            return False
        else:
            return True


def touch_func(case_name):
    data = app_init(case_name)[0]
    if data.get('name') == case_name:
        with open(img_path() + data.get('name') + '.png', 'wb') as f:
            f.write(data.get('data'))
            f.close()
        touch(Template(img_path() + data.get('name') + '.png',
                       record_pos=(data.get('pos_x'), data.get('pos_y')),
                       resolution=(data.get('resolution_x'), data.get('resolution_y'))))


