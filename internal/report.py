# -*- encoding=utf8 -*-
# Time：2021/08/13
__author__ = "2018248"

import time
from airtest.report.report import LogToHtml
from internal.file import replace_dir_name, html_path, project_directory, make_zip, img_path, log_path, del_all_file
from internal.ding import ding_api


def report_output():
    LogToHtml(script_root=project_directory() + r'\main.py',
              static_root=r"http://192.168.5.203:30105/static/",
              log_root=project_directory() + r"\log",
              export_dir=project_directory() + r"\reports",
              logfile=project_directory() + r'\log\log.txt',
              lang='zh',
              plugins=None).report()

    new_report_name = "wsy" + time.strftime("%m%d%H%M",
                                            time.localtime())
    replace_dir_name(html_path(), new_report_name)
    make_zip(img_path(), project_directory() + f"/reports/{new_report_name}/" + new_report_name + ".zip")
    ding_api("万岁爷", new_report_name)
    time.sleep(2)
    del_all_file(img_path())
    del_all_file(log_path())
