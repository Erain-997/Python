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
from sys_android.page_objects.shorts_page import ShortsPage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("沉浸页入口")
class TestShortsEntrance:

    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(':')[0])
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams",
                                 {"and_clarity_free_switch_test": "1", "and_immersion_page_style_test": "1"})

        self.proxy_process = start_proxy()
        self.driver = ShortsPage()
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
    @allure.title("01-feed流预告片点击跳转到预告片沉浸页，下滑播放该短剧第一集")
    @allure.description("shorts界面查找预告片——>通过预告进入视频沉浸页——>播放第一集——>校验播放进度")
    def test_shorts_entrance_01(self):
        """shorts界面查找预告片——>通过预告进入视频沉浸页——>播放第一集-->校验播放进度"""
        self.driver.android_version()

        # 寻找feeds流预告片
        self.driver.search_shorts_trailer(True)
        self.driver.assert_element_not_exists(self.element.shorts_page.shorts_headshot_stub,
                                              "断言-预期预告片不存在头像")
        # 下滑查看第一集
        self.driver.swipe_to_first_episode()

        self.driver.assert_element_exists(self.element.shorts_page.shorts_headshot_stub, "断言-预期第一集存在头像")
        self.driver.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "点击选集按钮")
        # TODO 可能会出现少于25集的剧
        self.driver.assert_element_exists(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="1-25"]'),
            "断言-25集分页"
        )

        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("02-从feed流预告片进入沉浸页, 并检查历史记录进度继承")
    @allure.description("shorts界面查找预告片——>通过预告进入视频沉浸页——>播放至第3集——>查看历史播放记录——>校验播放进度")
    def test_shorts_entrance_02(self):
        """shorts界面查找预告片——>通过预告进入视频沉浸页——>播放第一集-->校验播放进度"""
        self.driver.android_version()

        # 寻找feeds流预告片
        self.driver.search_shorts_trailer(True)
        self.driver.assert_element_not_exists(self.element.shorts_page.shorts_headshot_stub,
                                              "断言-预期预告片不存在头像")
        show_name, episode_num = self.driver.shorts_name_progress()
        self.driver.exit_immersion_page()

        self.driver.assert_text_equal(
            show_name,
            self.driver.get_element_text(self.driver.element.immersion_page.shorts_name, "获取剧名"),
            f"断言-最近播放显示该短剧:{show_name}",
        )
        self.driver.click(self.driver.element.immersion_page.shorts_name, "点击播放视频")
        self.driver.assert_text_equal(
            episode_num,
            self.driver.get_element_text(self.driver.element.drama_page.episode_num, "获取集数"),
            f"断言-最近播放集数衔接历史记录:{episode_num}",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("03-feed流预告片播完自动进入第一集")
    @allure.description("shorts界面查找预告片——>播放完预告片——>播放第1集")
    def test_shorts_entrance_03(self):
        """shorts界面查找预告片——>通过预告进入视频沉浸页——>播放第一集-->校验播放进度"""
        self.driver.android_version()

        # 寻找feeds流预告片
        self.driver.search_shorts_trailer()
        # 在shorts界面看完预告片
        show_name = self.driver.watch_trailer_in_shorts()
        self.driver.assert_element_exists(self.element.shorts_page.shorts_headshot_stub, "断言-预期第一集存在头像")
        self.driver.assert_expect_in_text(
            self.driver.get_element_text(self.driver.element.immersion_page.shorts_name, "获取剧名"),
            show_name,
            f"断言-播完预告片自动进入第一集:{show_name}",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("04-feed短剧未播放完跳转, 进入正片继续播放")
    @allure.description("shorts界面查找短剧——>播放完当前集数——>自动跳转播放下一集")
    def test_shorts_entrance_04(self):
        """shorts界面查找短剧——>播放完当前集数——>自动跳转播放下一集"""
        self.driver.android_version()

        # 寻找feeds流预告片
        show_name, episode_now, episode_sum = self.driver.search_shorts_drama()
        # 点击集数进入正片播放
        self.driver.into_shorts_drama(episode_now, episode_sum)

        self.driver.assert_text_equal(
            show_name,
            self.driver.get_element_text(self.driver.element.immersion_page.shorts_name, "获取剧名"),
            f"断言-最近播放显示该短剧:{show_name}",
        )
        episode_num_text = self.driver.get_element_text(self.driver.element.drama_page.episode_num, "获取集数")
        episode_num_now, _ = self.driver.deal_with_episode_num(episode_num_text)
        self.driver.assert_text_equal(str(episode_now), str(episode_num_now),
                                      f"断言-最近播放集数衔接历史记录:{episode_now}")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("05-feed短剧播放完自动进入第二集")
    @allure.description("shorts界面查找短剧——>播放完当前集数——>自动跳转播放下一集")
    def test_shorts_entrance_05(self):
        """shorts界面查找短剧——>播放完当前集数——>自动跳转播放下一集"""
        self.driver.android_version()

        # 寻找feeds流预告片
        show_name, episode_num, _ = self.driver.search_shorts_drama()
        # 快速播完
        self.driver.to_next_drama()


        self.driver.assert_text_equal(
            show_name,
            self.driver.get_element_text(self.driver.element.immersion_page.shorts_name, "获取剧名"),
            f"断言-最近播放显示该短剧:{show_name}",
        )
        episode_num_text = self.driver.get_element_text(self.driver.element.drama_page.episode_num, "获取集数")
        episode_num_now, _ = self.driver.deal_with_episode_num(episode_num_text)
        self.driver.assert_text_equal(str(episode_num + 1), str(episode_num_now),
                                      f"断言-继续播放下一集:{episode_num_now}")

        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("06-feed短剧播放完跳转播放另一个剧集")
    @allure.description("shorts界面查找短剧——>播放完当前剧集——>自动跳转播放下一集——>播放完当前剧——>自动跳转到另一部剧")
    # TODO 该用例目前的视频资源刚好是一个两集不用解锁的, 后期可能视频资源变了可能会导致用例失效
    def test_shorts_entrance_06(self):
        self.driver.android_version()

        # 寻找feeds流预告片
        show_name, episode_num, _ = self.driver.search_shorts_drama()
        # 快速播完
        self.driver.to_next_drama()

        self.driver.assert_text_equal(
            show_name,
            self.driver.get_element_text(self.driver.element.immersion_page.shorts_name, "获取剧名"),
            f"断言-最近播放显示该短剧:{show_name}",
        )
        episode_num_text = self.driver.get_element_text(self.driver.element.drama_page.episode_num, "获取集数")
        episode_num_now, _ = self.driver.deal_with_episode_num(episode_num_text)
        self.driver.assert_text_equal(str(episode_num + 1), str(episode_num_now),
                                      f"断言-继续播放下一集:{episode_num_now}")

        self.driver.sleep_and_wait()
        another = self.driver.get_element_text(self.driver.element.immersion_page.shorts_name, "获取剧名")
        self.driver.assert_text_not_equal(
            show_name,
            another,
            f"断言-已经在播放另一部短剧:{another}",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("07-首页查看剧集, 进入短剧界面后继续播放该短剧")
    @allure.description("shorts界面查找短剧——>播放当前剧集——>推出剧集, 进入短剧后继续播放该剧")
    def test_shorts_entrance_07(self):
        """shorts界面查找短剧——>播放当前剧集——>推出剧集, 进入短剧后继续播放该剧"""
        self.driver.android_version()

        show_name, episode = self.driver.search_shorts_in_home()
        self.driver.exit_immersion_page_into_shorts()
        self.driver.assert_text_equal(
            self.driver.get_element_text(self.driver.element.immersion_page.shorts_name, "获取剧名"),
            show_name,
            f"断言-进入短剧后继续播放上次播放的短剧:{show_name}",
        )
        episode_num = self.driver.get_element_text(self.element.drama_page.episode_num, f"获取短剧集数")
        episode_now, episode_sum = self.driver.deal_with_episode_num(episode_num)
        self.driver.assert_text_equal(
            episode,
            episode_now,
            f"断言-最近播放集数衔接之前观看记录:{episode_now}",
        )

        self.test_status = True
