# -*- encoding=utf8 -*-
__author__ = "admin"

from airtest.core.api import *
from internal.file import img_path


def role_api():
    touch(
        Template(r"E:\code\tools\airtestProject\wsy_ui\api\role_info\tpl1628222406947.png", record_pos=(-0.451, -0.26),
                 resolution=(1290, 864)))
    snapshot(filename=img_path() + r"/君主形象.png", msg="君主形象", quality=99)
    touch(
        Template(r"E:\code\tools\airtestProject\wsy_ui\api\role_info\tpl1628213030293.png", record_pos=(0.457, -0.284),
                 resolution=(1290, 864)))
