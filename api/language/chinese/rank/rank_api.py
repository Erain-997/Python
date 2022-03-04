# -*- encoding=utf8 -*-
# Time：2021/08/13
__author__ = "admin"

from airtest.core.api import *
from internal.file import project_directory


def rank_api():
    touch(
        Template(project_directory() + r"\api\rank\tpl1628230466210.png", record_pos=(-0.006, -0.053),
                 resolution=(1290, 864)))
    snapshot(msg="排行榜形象", quality=99)
    touch(
        Template(project_directory() + r"\api\rank\tpl1628230480779.png", record_pos=(0.458, -0.283),
                 resolution=(1290, 864)))


if __name__ == '__main__':
    print(project_directory())
