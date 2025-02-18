import logging
import os
import time
from datetime import datetime

import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

from common.api.mock_data import MockData
from common.language.lang_mgr import lang_mgr
from common.mysql.mysql import MySQLClient
from common.mysql.mysql_tools import update_test_case_info
from common.utils.arg_parse_func import args
from common.utils.cmd_tools import adb_logcat, stop_logcat, start_proxy, stop_proxy, find_log_value_by_key, adb_shell
from common.utils.log_utils import Log
from common.utils.path_config import android
from common.utils.tools import timestamp
from sys_android.page_objects.window_page import WindowPage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("小窗播放相关模块")
class TestWindowModule:
    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(':')[0])
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams",
                                 {"and_pip_test_1": "2"})
        # 安卓端各场景广告开关
        self.proxy_process = start_proxy()
        self.driver = WindowPage()
        # 启动录制视频
        self.driver.start_recording()
        # 采集app系统日志
        self.log_path = os.path.join(android.report_output_dir, args.output_report, "log",
                                     f"logcat日志_{request.node.name}_{timestamp()}.log")
        self.logcat_process = adb_logcat(self.log_path)
        # 初始化测试失败标志
        self.test_status = None
        self.element = ShortTvElements()
        Log.logger.info(f"\n-----{request.node.name}开始执行-----")

    @allure.step("用例环境清理")
    @pytest.fixture(scope="function", autouse=True)
    def teardown_steps(self, request):
        yield
        # 停止录制视频并保存
        self.driver.stop_and_save_recording(self.test_status)
        # 停止app系统日志记录
        stop_logcat(self.logcat_process, self.log_path)
        stop_proxy(self.proxy_process)
        # 退出驱动
        self.driver.quit()
        # 更新用例
        update_test_case_info(request, self.test_status, self.driver.setup_step_collection,
                              self.driver.case_step_collection, self.driver.tear_down_collection,
                              self.driver.check_collection)

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("01-Android端设备开关【关】+APP开关【关】，主动点击小窗，需要授权")
    @allure.description("系统悬浮窗关闭——>APP画中画开关关闭——>进入视频沉浸页——>主动点击小窗需要授权")
    def test_window_01(self):
        """系统悬浮窗关闭——>APP画中画开关关闭——>进入视频沉浸页——>主动点击小窗需要授权"""
        try:
            # 脚本业务
            self.driver.close_suspended_window()
            self.driver.android_version()
            self.driver.switch_button(False)
            self.driver.press_back_button("返回首页")
            self.driver.into_immersion_page()
            self.driver.click_mini_window()
        except Exception as e:
            logging.error(f"An error: {e}")
        # 获取当前页面activity
        activity = adb_shell("dumpsys activity activities | grep  -E 'mFocusedActivity|Resumed:|Window #'")
        self.driver.assert_expect_in_text("Settings$OverlaySettingsActivity", activity,
                                          "断言-APP需要授权，跳转至授权页面")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("02-Android端设备开关【关】+APP开关【关】，自动进入（回到主屏幕），APP禁止自动进入小窗播放")
    @allure.description("系统悬浮窗关闭——>APP画中画开关关闭——>回到主屏幕——>APP禁止自动进入小窗播放")
    def test_window_02(self):
        """系统悬浮窗关闭——>app画中画开关关闭——>回到主屏幕——>APP禁止自动进入小窗播放"""
        try:
            # 脚本业务
            self.driver.close_suspended_window()
            self.driver.android_version()
            self.driver.switch_button(False)
            self.driver.press_back_button("返回首页")
            self.driver.into_immersion_page()
            self.driver.back_home()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_element_not_exists(self.element.common_page.window, "断言-APP禁止进入小窗播放")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("03-Android端设备开关【关】+APP开关【开】，点击小窗，APP内外均可小窗播放")
    @allure.description("系统悬浮窗关闭——>APP画中画开关开启——>点击小窗——>APP内外均可小窗播放")
    def test_window_03(self):
        try:
            # 脚本业务
            self.driver.android_version()
            adb_shell("appops set com.startshorts.androidplayer SYSTEM_ALERT_WINDOW allow")
            self.driver.switch_button(True)
            self.driver.close_suspended_window()
            self.driver.press_back_button("返回首页")
            self.driver.into_immersion_page()
            self.driver.click_mini_window()
        except Exception as e:
            logging.error(f"An error: {e}")
        # 获取当前页面activity
        activity = adb_shell("dumpsys activity activities | grep  -E 'mFocusedActivity|Resumed:|Window #'")
        self.driver.assert_expect_in_text("Settings$OverlaySettingsActivity", activity,
                                          "断言-APP需要授权，跳转至授权页面")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("04-Android端设备开关【关】+APP开关【开】，自动进入（回到主屏幕），APP内外均可小窗播放")
    @allure.description("系统悬浮窗关闭——>APP画中画开关开启——>回到主屏幕——>APP内外均可小窗播放")
    def test_window_04(self):
        try:
            # 脚本业务
            self.driver.android_version()
            adb_shell("appops set com.startshorts.androidplayer SYSTEM_ALERT_WINDOW allow")
            self.driver.switch_button(True)
            self.driver.close_suspended_window()
            self.driver.press_back_button()
            self.driver.into_immersion_page()
            self.driver.hot_start()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_element_exists(self.element.common_page.window, "断言-APP禁止自动进入小窗播放（校验Ui）")
        self.test_status = True

