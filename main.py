# -*- encoding=utf8 -*-
# Time：2021/08/13
__author__ = "2018248"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from internal.server_api import process
from api.suitcase.minister_case import minister_case
from internal.file import html_path
from internal.report import report_output

# 所有非蓝英雄列表, 方便复制, 防止每次敲名字
minister_list = ["殷无双", "上官璃", "独孤梦", "芈鸢",
                 "皇甫缨", "司空影", "顾丹阳", "努尔哈赤",
                 "康熙", "道光", "皇太极", "乾隆",
                 "秦帝", "武皇", "嘉庆", "雍正",
                 "顺治", "咸丰", "多尔衮", "岳钟琪",
                 "包龙星", "林则徐", "兰平王", "霍居胥",
                 "太白", "秦祁", "穆兰", "慕容英",
                 "南宫玉", "司徒羽", "沈义", "恭亲王",
                 "安亲王", "康亲王", "礼亲王", "皇太子",
                 "郑燮", "阿桂"]
language_list = ["chinese", "English"]

if __name__ == '__main__':
    process()
    auto_setup(__file__, logdir=True, devices=["Windows:///3610124", ],
    # auto_setup(__file__, logdir=True, devices=["Windows:///?title_re=wsy_client.*", ],
               project_root=html_path())
    # for minister in minister_list:
    #     minister_case(minister)
    minister_case("chinese", "独孤梦")
    report_output()



