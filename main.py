# -*- encoding=utf8 -*-
# Time：2021/08/13
__author__ = "2018248"

import os
import pytest
from devices_init.devices_init import args
from internal.tools.project_path import root_directory, report_path, allure_path, push_path
from internal.tools.db import allure_report_add

if __name__ == '__main__':
    pytest.main(
        ["-v", "-s", "--showprogress", root_directory(split_path_list=["internal"]) + "/test_cases", "--alluredir",
         report_path(args.task_id, args.devices), "--clean-alluredir"])

    os.system(
        "allure generate " + report_path(args.task_id, args.devices) + " -o " + allure_path(args.task_id,
                                                                                            args.devices) + " --clean")
    allure_report_add(args.task_id, push_path(args.task_id), args.devices)



