# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08
import _thread
import logging
from airtest.core.api import *
from poco.drivers.unity3d import UnityPoco
from internal.tools.tool import except_output, allure_snapshot
from internal.tools.project_path import project_directory
from internal.engine.engine_part import wait_func
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from internal.tools.arg_parse_func import get_arg_parse
from airtest.core.android.recorder import *
from airtest.core.android.adb import *

args = get_arg_parse()
client_list = {}
retry = []


class DevicesInit(object):

    @classmethod
    @except_output
    def devices_poco(cls, install_state=True):
        try:
            connect_dev = connect_device("Android://127.0.0.1:5037/" + args.devices + "?cap_method=JAVACAP")
            # if install_state:
            #     try:
            #         uninstall(args.package)
            #     except Exception as e:
            #         pass
            #     # 安装apk
            #     install(args.apk)
            # # 启动app
            # start_app(args.package)
            # # 启动闪屏等待
            # wait_func("启动闪屏等待")
            # 获取操作实例(这边要跟adb连接进行拆分,否则报主机已连接错误)
            cls.poco = UnityPoco(('', 5001), device=connect_dev)
            cls.android_poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
            client_list["poco"] = cls.poco
            client_list["adb_client"] = connect_dev
            client_list["android_poco"] = cls.android_poco
            return cls.poco, connect_dev, cls.android_poco
        except Exception as e:
            print("任务失败,执行重试机制.", e)
            log("连接设备失败:%s" % str(e), snapshot=True)
            retry.append(e)
            # connect_dev.shell(f"am force-stop {args.package}")
            # time.sleep(2)
            # # 控制重试次数
            if len(retry) > 2:
                assert False
            return cls.devices_poco()


def client_poco(install_state=True):
    if client_list:
        return client_list.get("poco"), client_list.get("adb_client"), client_list.get("android_poco")
    else:
        client, connect_dev, android_poco = DevicesInit.devices_poco(install_state)
        return client, connect_dev, android_poco


class GetClient:
    poco, adb_client, android_poco = client_poco()

    def reconnect(self, install_state=True):
        self.poco, self.adb_client, self.android_poco = client_poco(install_state)


def except_function(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # 异常消息通知
            # _thread.start_new_thread(_grpc_send_ex_msg, (e, "except_output捕获异常"))
            allure_snapshot(project_directory(os.path.dirname(__file__)))
            # client_list.get("poco")("ForAutomatedTest_UIText_DotnotMindMe").set_text(
            #     "PytestCommunicateWithAppViaPoco_return_main_scene")
            # todo 客户端暂未支持返回主场景故临时处理
            time.sleep(5)
            assert False, e

    return wrapper
