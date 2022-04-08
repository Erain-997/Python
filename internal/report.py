# -*- encoding=utf8 -*-
# Time：2021/08/13
__author__ = "2018248"

import time
import os
from airtest.report.report import LogToHtml
from internal.file import replace_dir_name, html_path, project_directory, make_zip, img_path, auto_path, del_all_file
from internal.ding import ding_api
from internal.search_name import get_search_nam


def report_output(minister_id=None, minister_skin_id=None, wive_id=None, wive_skin_id=None, fashion_id=None,version=None):
    LogToHtml(script_root=project_directory() + r'\main.py',
              static_root=r"http://192.168.5.203:30105/static/",
              # log_root=project_directory() + r"\log",
              export_dir=project_directory() + r"\reports",
              # logfile=project_directory() + r'\log\log.txt',
              lang='zh',
              plugins=None).report()

    new_report_name = "sultan" + time.strftime("%m%d%H%M",
                                               time.localtime())
    replace_dir_name(html_path(), new_report_name)
    make_zip(img_path(), project_directory() + f"/reports/{new_report_name}/" + new_report_name + ".zip")
    name, skin = get_search_nam(minister_id, minister_skin_id, wive_id, wive_skin_id,fashion_id)
    ding_api("苏丹", new_report_name, name, skin, version)
    os.popen(auto_path() + r"//rm_reports.sh  " + new_report_name)


if __name__ == '__main__':
    os.popen(auto_path() + r"//rm_reports.sh sultan12131640")
    # name, skin = get_search_nam(None, None, wive_id=6, wive_skin_id=1708)
    ding_api("苏丹", "sultan", "name", "skin","df")
