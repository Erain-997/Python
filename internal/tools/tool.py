# _*_coding:utf-8_*_
# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08
# import grpc
import allure
import pytest
from internal.tools.db import login_element
import time
from airtest.core.api import snapshot,exists,Template
from internal.tools.project_path import project_directory, root_directory, report_img
from internal.tools.project_path import img_path
from internal.tools.arg_parse_func import get_arg_parse
from internal.tools.db import app_init
args = get_arg_parse()


def except_output(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 异常消息通知
            allure_snapshot(report_img())
            assert False, e

    return wrapper


def allure_snapshot(root_path, file_name="异常截图"):
    snapshot_name = "demo.jpg"
    snapshot(filename=root_path + snapshot_name, quality=99)
    # 报告放入截图
    allure.attach.file(root_path + snapshot_name, file_name, attachment_type=allure.attachment_type.JPG)


def except_go_main(client, e):
    allure_snapshot(report_img())
    # client("ForAutomatedTest_UIText_DotnotMindMe").set_text(
    #     "PytestCommunicateWithAppViaPoco_return_main_scene")
    # time.sleep(5)


def case_snapshot(snapshot_name):
    img_name = "/" + snapshot_name + ".jpg"
    snapshot(filename=report_img() + img_name, quality=99)
    # 报告放入截图
    allure.attach.file(report_img() + img_name, snapshot_name,
                       attachment_type=allure.attachment_type.JPG)


def assert_report(condition, expected, real, client, node_path, case_name):
    """
    :param condition: 判断条件
    :param real: 实际
    :param expected: 预期
    :param client:
    :param node_path:
    :param case_name: 用例名称
    :return:
    """
    if condition is False:
        if real != expected:
            # except_go_main(client, node_path)
            pytest.fail(case_name + "文本不对应" + "预期为:" + expected + "实际为:" + real)
    else:
        if real == expected:
            # except_go_main(client, node_path)
            pytest.fail(case_name + "文本对比相同" + "预期为:" + expected + "实际为:" + real)


def reconnect_login(client):
    """
    登录步骤
    :param client:
    :return:
    """
    client("DeviceTextField").set_text(login_element()[0]["input_text"])
    client("ConfirmButton").click()
    client("StartGameButton").offspring("StartGameText").click()
    client("WarehouseButtonType1Nested").offspring("WarehouseClickButton").wait()
    time.sleep(3)
    data = app_init("主场景弹窗")[0]
    while exists(Template(img_path() + data.get('name') + '.png',
                    record_pos=(data.get('pos_x'), data.get('pos_y')),
                    resolution=(data.get('resolution_x'), data.get('resolution_y')))) is False:
        client("SufWaveImage").click()
    time.sleep(3)


