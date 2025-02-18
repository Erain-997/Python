import logging
import os

import allure
import pytest

from common.api.mock_data import MockData
from common.mysql.mysql_tools import update_test_case_info
from common.utils.arg_parse_func import args
from common.utils.cmd_tools import stop_logcat, stop_proxy, start_proxy, adb_logcat
from common.utils.log_utils import Log
from common.utils.path_config import android
from common.utils.tools import language_name, timestamp
from sys_android.page_objects.pages_screenshot_page import PagesScreenshotPage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("页面截图模块")
class TestPagesScreenshotModule:
    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:

        os.system(f"adb -s {args.device} logcat -c")
        self.traverse_value = request.node.get_closest_marker("traverse_value")
        self.traverse_value = self.traverse_value.args[0] if self.traverse_value else None
        if self.traverse_value == 1 or self.traverse_value == 2:
            self.mock_data = MockData(args.device.split(":")[0])
            self.mock_data.mock_data(
                "test_unlock_drama_01",
                "/app/abtest/getAbtestParams",
                {
                    "and_immersion_page_style_test": "1",
                    "and_without_ad_test": "0",
                    "and_sku_template_test_2": "2",
                    "and_drama_introduction_test": "1",
                    "and_missison_center_test_2": "1",
                    "feature_android": "{'ratingEnable':'true'}",
                },
            )
        elif self.traverse_value == 3:
            self.mock_data = MockData(args.device.split(":")[0])
            self.mock_data.mock_data(
                "test_unlock_drama_01",
                "/app/abtest/getAbtestParams",
                {
                    "and_immersion_page_style_test": "1",
                    "and_without_ad_test": "0",
                    "and_sku_template_test_2": "2",
                    "and_drama_introduction_test": "1",
                    "feature_android": "{'ratingEnable':'true'}",
                    "and_task_test": "1",
                },
            )
            self.mock_data.mock_data(
                "test_unlock_drama_02",
                "/app/homeData/getHomeConfig",
                {"ggLoginBonus": "", "metaLoginBonus": "", "notificationsBonus": "", "userAccountMergeBonus": ""},
            )
        self.proxy_process = start_proxy()
        self.driver = PagesScreenshotPage(False)
        # 启动录制视频
        self.driver.start_recording()
        # 采集app系统日志
        self.log_path = os.path.join(android.report_output_dir, args.output_report, "log",
                                     f"logcat日志_{request.node.name}_{timestamp()}.log")
        self.logcat_process = adb_logcat(self.log_path)
        self.screenshot_path = "screenshots/" + args.language + "_screenshot"
        if not os.path.exists(self.screenshot_path):
            os.makedirs(self.screenshot_path)
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
        # 退出驱动
        self.driver.quit()
        # TODO 压缩待完善
        if self.traverse_value == 4:
            self.driver.attach_folder_as_zip(self.screenshot_path, f"screenshots_{timestamp()}.zip")
            self.driver.remove_folder(self.screenshot_path)
        stop_proxy(self.proxy_process)
        # 更新用例
        update_test_case_info(request, self.test_status, self.driver.setup_step_collection,
                              self.driver.case_step_collection, self.driver.tear_down_collection,
                              self.driver.check_collection)

    @pytest.mark.已开发完成
    @pytest.mark.traverse_value(1)
    @allure.title("01-页面截图1")
    def test_pages_screenshot_01(self):
        self.zip_status = 1
        allure.dynamic.description(
            f"当前语言：{language_name()[args.language]}—>首页—>兑换码—>搜索历史—短剧—>追剧—>沉浸页—>设置，页面截图")
        try:
            # 脚本业务
            self.driver.pages_screenshot_01(self.screenshot_path)
        except Exception as e:
            logging.error(f"An error: {e}")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.traverse_value(2)
    @allure.title("02-页面截图2")
    def test_pages_screenshot_02(self):
        allure.dynamic.description(f"当前语言：{language_name()[args.language]}—>登录—>订阅—>充值—>我的钱包—>任务中心")
        try:
            # 脚本业务
            self.driver.pages_screenshot_02(self.screenshot_path)
        except Exception as e:
            logging.error(f"An error: {e}")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.traverse_value(3)
    @allure.title("03-campaign解锁类型弹窗")
    def test_pages_screenshot_03(self):
        allure.dynamic.description(f"当前语言：{language_name()[args.language]}")
        try:
            # 脚本业务
            self.driver.pages_screenshot_03(self.screenshot_path)
        except Exception as e:
            logging.error(f"An error: {e}")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.traverse_value(4)
    @allure.title("04-覆盖安装新版本，换位引导")
    def test_pages_screenshot_04(self):
        allure.dynamic.description(f"当前语言：{language_name()[args.language]}—>卸载当前apk—>安装低版本—>覆盖安装新版本")
        try:
            # 脚本业务
            self.driver.pages_screenshot_07(self.screenshot_path)
        except Exception as e:
            logging.error(f"An error: {e}")
        self.test_status = True
