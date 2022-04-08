# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08
import allure
import pytest
import time
from devices_init.devices_init import args, client_list
from internal.tools.db import login_element, guide_element, module_object, module_element, db_close
from internal.engine.engine_func import EngineFunc
from internal.tools.role import db_role_write
from internal.tools.tool import reconnect_login, case_snapshot
from airtest.core.api import stop_app
from internal.tools.recording import start_recording, stop_recording
from airtest.core.android.adb import *

# import func_timeout
# from func_timeout import func_set_timeout

case_status = False


# @allure.feature("设备号: %s " % args.devices)
# class TestUI(EngineFunc):
#
#     @classmethod
#     def setup_class(cls):
#         # 开启录屏
#         cls.recorder = start_recording()
#         # user_id = db_role_write()
#         # cls.log.info("帐号初始化完成,user_id:%s" % user_id)
#
#     @classmethod
#     def teardown_class(cls):
#         # stop_recording(cls.recorder)
#         db_close()
#         # stop_app(args.package)
#
#     @allure.story("帐号登录")
#     @func_set_timeout(180)
#     def test_login(self):
#         self.log.info("执行:login")
#         data_object = login_element()
#         try:
#             for data in data_object:
#                 self.log.info("data:%s", data)
#                 self.type_func(data)
#             self.log.info("登录模块完成")
#         except Exception as e:
#             self.log.error("登录异常:%s", str(e))
#             stop_app(args.package)
#             client_list.clear()
#             time.sleep(3)
#             self.reconnect(False)
#             self.test_login()
#             pytest.xfail("帐号登录异常" + str(e))
#         except func_timeout.exceptions.FunctionTimedOut:
#             self.log.error("执行函数超时")
#             pytest.xfail('执行函数超时')
#
#     @allure.story("模块用例")
#     @allure.title('模块:{param}')
#     @pytest.mark.parametrize('param', module_object(args.module))
#     def test_data_engine(self, param):
#         global case_status
#         if case_status:
#             self.reconnect(False)
#         self.log.info("执行数据库用例:%s", param)
#         for data in module_element(param):
#             try:
#                 self.log.info("data:%s", data)
#                 self.type_func(data)
#             except Exception as e:
#                 case_status = True
#                 self.log.error("用例异常:%s", str(e))
#                 self.log.error("用例异常模块:%s", data.get(self.case_name))
#                 case_snapshot(data.get(self.case_name))
#                 # stop_app(args.package)
#                 # client_list.clear()
#                 # time.sleep(3)
#                 # self.reconnect(False)
#                 # self.log.error("用例异常重新登录中")
#                 # self.test_login()
#                 # self.log.error("用例异常重新登录完成")
#                 time.sleep(3)
#                 assert False, data.get(self.case_name) + str(e)


from behavioies.demo import TestCases


@allure.feature("设备号: %s " % args.devices)
class TestUI(TestCases):
    @allure.story("模块用例")
    @allure.title('模块:case_1')
    def test_case_1(self):
        self.log.info("执行脚本用例")
        self.case_1()
