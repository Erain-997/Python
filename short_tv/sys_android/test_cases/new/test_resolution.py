import logging
import os
import time

import allure
import pytest

from common.api.mock_data import MockData
from common.language.lang_mgr import lang_mgr
from common.mysql.mysql_tools import update_test_case_info
from common.utils.arg_parse_func import args
from common.utils.cmd_tools import adb_logcat, stop_logcat, start_proxy, stop_proxy
from common.utils.log_utils import Log
from common.utils.path_config import android
from common.utils.tools import timestamp
from sys_android.page_objects.resolution_page import ResolutionPage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("分辨率1080p限免")
class TestResolution:

    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(':')[0])
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams",
                                 {"and_clarity_free_switch_test": "1", "and_immersion_page_style_test": "1"})

        self.proxy_process = start_proxy()
        self.driver = ResolutionPage()
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
        time.sleep(5)
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
    @allure.title("01-校验1080p始终展示“限免”气泡字样Ui更新")
    @allure.description("搜索剧集——>进入视频沉浸页——>查看1080p'限免'字样")
    def test_resolution_01(self):
        """搜索剧集——>进入视频沉浸页——>查看1080p"限免"字样"""
        try:
            self.driver.android_version()
    
            self.driver.into_immersion_page()
            self.driver.versio_limit_free()

        except Exception as e:
            logging.error(f"An error: {e}")
        # 断言-1080p始终展示“限免”气泡字样
        self.driver.assert_text_equal(
            self.driver.get_element_text((
                'xpath', f'//android.widget.TextView[@text="{lang_mgr.immersion_activity_free_clarity_1080p()}"]')),
            self.driver.get_element_text(self.element.resolution_page.resolution_1080p),
            f"校验: “限免”断言-1080p始终展示“限免”气泡字样, 当前语言：{args.language}"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("02-校验非会员支持使用1080p")
    @allure.description("搜索剧集——>进入视频沉浸页——>切换1080p播放")
    def test_resolution_02(self):
        """搜索剧集——>进入视频沉浸页——>切换1080p播放"""
        try:
            # 脚本业务
            self.driver.android_version()
    
            self.driver.into_immersion_page()
            self.driver.version_1080p_play()

        except Exception as e:
            logging.error(f"An error: {e}")

        # 断言-非会员均可使用1080p分辨率播放
        self.driver.assert_text_equal(
            lang_mgr.play_episode_activity_switch_resolution_tip(),
            self.driver.get_element_text((
                'xpath',
                f'//android.widget.Toast[@text="{lang_mgr.play_episode_activity_switch_resolution_tip()}"]'
            )),
            f"校验: 切换分辨率toast提示多语言展示正常, 当前语言：{args.language}"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("03-校验切换1080p不发生跳转")
    @allure.description("搜索剧集——>进入视频沉浸页——>切换1080p播放——>切换1080p不发生跳转")
    def test_resolution_03(self):
        """搜索剧集——>进入视频沉浸页——>切换1080p播放——>切换1080p不发生跳转"""
        try:
            # 脚本业务
            self.driver.android_version()
    
            self.driver.into_immersion_page()
            self.driver.version_1080p_play()

        except Exception as e:
            logging.error(f"An error: {e}")

        # 断言-非会员点切换1080p, 不跳转至订阅模块
        self.driver.assert_text_equal(
            lang_mgr.play_episode_activity_switch_resolution_tip(),
            self.driver.get_element_text((
                'xpath',
                f'//android.widget.Toast[@text="{lang_mgr.play_episode_activity_switch_resolution_tip()}"]'
            )),
            f"校验: 非会员点切换1080p, 不跳转至订阅模块, 当前语言：{args.language}"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("04-校验“限免”气泡同步多语言展示")
    @allure.description("搜索剧集——>进入视频沉浸页——>查看1080p'限免'字样——>切换1080p播放——>toast提示多语言展示")
    def test_resolution_04(self):
        """搜索剧集——>进入视频沉浸页——>查看1080p"限免"字样——>切换1080p播放——>toast提示多语言展示"""
        try:
            # 脚本业务
            self.driver.android_version()
    
            self.driver.into_immersion_page()
            self.driver.versio_limit_free()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.driver.get_element_text((
                'xpath', f'//android.widget.TextView[@text="{lang_mgr.immersion_activity_free_clarity_1080p()}"]')),
            self.driver.get_element_text(self.element.resolution_page.resolution_1080p),
            f"校验: “限免”气泡同步多语言展示, 当前语言：{args.language}"
        )
        self.test_status = True

    # @pytest.mark.已开发完成
    # @pytest.mark.regression
    # @allure.title("校验1080p限免参数AB实验值为2, 不展示“限免”气泡字样")
    # @allure.description("搜索剧集——>进入视频沉浸页——>查看1080p'限免'字样")
    # def test_resolution_05(self):
    #     """搜索剧集——>进入视频沉浸页——>查看1080p"限免"字样"""
    #     try:
    #         # 脚本业务
    #         self.driver.resolution_05()
    #     except Exception as e:
    #         logging.error(f"An error: {e}")
    #     # 断言-1080p不展示“限免”气泡字样
    #     self.driver.assert_element_exists(self.element.resolution_page.resolution_1080p_vip,
    #                                       "不展示“限免”气泡字样（校验UI）")
    #
    # @pytest.mark.已开发完成
    # @pytest.mark.regression
    # @allure.title("校验1080p限免参数AB实验值为2, 切换1080p跳转至订阅模块")
    # @allure.description("搜索剧集——>进入视频沉浸页——>切换1080p播放——>跳转至订阅模块")
    # def test_resolution_06(self):
    #     """搜索剧集——>进入视频沉浸页——>切换1080p播放——>跳转至订阅模块"""
    #     try:
    #         # 脚本业务
    #         self.driver.resolution_06()
    #     except Exception as e:
    #         logging.error(f"An error: {e}")
    #     # 断言-非会员点切换1080p, 跳转至订阅模块
    #     self.driver.assert_element_exists(self.element.common_page.subscribe_icon,
    #                                       "断言-非会员点切换1080p, 跳转至订阅模块（校验UI）")
