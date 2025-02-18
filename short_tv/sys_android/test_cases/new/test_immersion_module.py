import logging
import time

from common.api.mock_data import MockData
from common.language.lang_mgr import lang_mgr
from common.mysql.mysql_tools import update_test_case_info
from common.utils.cmd_tools import *
from common.utils.report import get_app_version, compare_versions
from sys_android.page_objects.immersion_page import ImmersionPage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("沉浸页模块")
class TestImmersionModule:
    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        collection_value = request.node.get_closest_marker("collection_value")
        collection_value = collection_value.args[0] if collection_value else None
        self.mock_data = MockData(args.device.split(":")[0])
        mock_data_mapping = {
            0: {"and_immersion_page_style_test": "0"},
            1: {"and_immersion_page_style_test": "1"},
            2: {"and_immersion_page_style_test": "1", "and_drama_introduction_test": "1"},
            3: {"and_favorite_test_2": "0"},
            4: {"and_favorite_test_2": "1"},
            5: {"and_favorite_test_2": "2"},
        }
        default_data = {"and_drama_introduction_test": "0", "and_immersion_page_style_test": "1"}
        data = mock_data_mapping.get(collection_value, default_data)
        self.mock_data.mock_data(
            "test_unlock_drama_01",
            "/app/abtest/getAbtestParams",
            data
        )
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams",
                                 {"and_ad_mediation_platform_test": "0"})
        self.proxy_process = start_proxy()
        self.driver = ImmersionPage()
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
        time.sleep(3)
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
    @pytest.mark.collection_value(0)
    @allure.title("01-校验沉浸页可正确切换分辨率（and_immersion_page_style_test：0）")
    @allure.description("搜索短剧——>切换分辨率——>验证分辨率")
    def test_immersion_01(self):
        """ab-0，沉浸页切换分辨率并验证"""
        try:
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.driver.click_resolution_button()
            self.driver.switch_4080p()
        except Exception as e:
            logging.error(f"An error: {e}")
        if compare_versions():
            self.driver.assert_text_equal(
                "480p", self.driver.get_element_text(self.driver.element.subscribe_page.new_resolution), "断言-正确切换分辨率"
            )
        else:
            self.driver.assert_text_equal(
                "480p", self.driver.get_element_text(self.driver.element.subscribe_page.resolution), "断言-正确切换分辨率"
            )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("02-校验沉浸页可正确切换分辨率（and_immersion_page_style_test：1）")
    @allure.description("搜索短剧——>切换分辨率——>验证分辨率")
    def test_immersion_02(self):
        """ab-1，沉浸页切换分辨率并验证"""
        try:
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.driver.click_resolution_button()
            self.driver.switch_4080p()
        except Exception as e:
            logging.error(f"An error: {e}")
        if compare_versions():
            self.driver.assert_text_equal(
                "480p", self.driver.get_element_text(self.driver.element.subscribe_page.new_resolution), "断言-正确切换分辨率"
            )
        else:
            self.driver.assert_text_equal(
                "480p", self.driver.get_element_text(self.driver.element.subscribe_page.resolution), "断言-正确切换分辨率"
            )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.collection_value(0)
    @allure.title("03-校验沉浸页可正确切换倍速（and_immersion_page_style_test：0）")
    @allure.description("搜索短剧——>切换倍速——>验证倍速")
    def test_immersion_03(self):
        """ab-0，沉浸页切换倍速并验证"""
        try:
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.driver.switch_half_speed()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            "0.5X", self.driver.get_element_text(self.driver.element.immersion_page.half_speed), "断言-正确切换倍速"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("04-校验沉浸页可正确切换倍速（and_immersion_page_style_test：1）")
    @allure.description("搜索短剧——>切换倍速——>验证倍速")
    def test_immersion_04(self):
        """ab-1，沉浸页切换倍速并验证"""
        try:
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.driver.switch_half_speed()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            "0.5X", self.driver.get_element_text(self.driver.element.immersion_page.half_speed), "断言-正确切换倍速"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("05-校验沉浸页长按屏幕，1.5倍速播放")
    @allure.description("搜索短剧——>长按改变倍速——>验证视频播放进度")
    def test_immersion_05(self):
        """沉浸页长按切换倍速并验证"""
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        speed = self.driver.get_speed_tips_tv(6)
        text = lang_mgr.play_episode_activity_speed_playing_unit()
        expect_text = lang_mgr.play_episode_activity_speed_playing().replace(text, "")
        self.driver.assert_expect_in_text(expect_text, speed, "断言-倍速为1.5倍速")
        time_now = self.driver.get_current_time_tv()
        self.driver.assert_more_than("00:09", time_now, "断言-加速播放6秒,进度不止9秒")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("07-检验沉浸页点击头像拉起剧集列表")
    @allure.description("搜索短剧——>进入视频沉浸页——>点击头像拉起剧集列表页面")
    def test_immersion_07(self):
        """检验沉浸页新增简介ab测实验组点击头像拉起剧集列表"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.driver.click_headshot()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_element_exists(self.driver.element.common_page.tab, "断言-剧集列表正确显示（校验Ui）")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.collection_value(2)
    @allure.title("08-检验沉浸页点击头像拉起简介页面（and_drama_introduction_test：1）")
    @allure.description("搜索短剧——>进入视频沉浸页——>点击头像拉起视频简介页面")
    def test_immersion_08(self):
        """检验沉浸页新增简介ab测实验组点击头像拉起简介页面"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.driver.click_headshot()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_element_exists(self.driver.element.common_page.introduction,
                                          "断言-剧简介正确显示（校验Ui）")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.collection_value(0)
    @allure.title("09-沉浸页收藏短剧并验证（and_immersion_page_style_test：0）")
    @allure.description("沉浸页点击收藏按钮——>查看收藏列表")
    def test_immersion_09(self):
        """(Ab测试-0)沉浸页收藏短剧并验证"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.show_name = self.driver.get_element_text(self.element.immersion_page.shorts_name,
                                                          "获取短剧名称")
            self.driver.click_collect()
            self.driver.exit_immersion_page()

        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.show_name, self.driver.get_element_text(self.driver.element.immersion_page.shorts_name), "断言-收藏列表显示该短剧"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.collection_value(1)
    @allure.title("10-沉浸页收藏短剧并验证（and_immersion_page_style_test：1）")
    @allure.description("沉浸页连续观看两集——>查看收藏列表")
    def test_immersion_10(self):
        """(Ab测试-1)沉浸页收藏短剧并验证"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.show_name = self.driver.get_element_text(self.element.immersion_page.shorts_name,
                                                          "获取短剧名称")
            self.driver.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            time.sleep(2)
            self.driver.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            time.sleep(2)
            self.driver.click_collect()
            self.driver.exit_immersion_page()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.show_name, self.driver.get_element_text(self.driver.element.immersion_page.shorts_name),
            "断言-收藏列表显示该短剧"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("11-观看短剧，在最近观看展示")
    @allure.description("沉浸页观看短剧——>查看最近播放")
    def test_immersion_11(self):
        """观看短剧，在最近观看展示"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.show_name = self.driver.get_element_text(self.element.immersion_page.shorts_name,
                                                          "获取短剧名称")
            self.driver.exit_immersion_page()
            self.driver.click_play()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.show_name,
            self.driver.get_element_text(self.driver.element.immersion_page.shorts_name, "获取短剧名称"),
            "断言-最近播放显示改短剧",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("12-收藏短剧，并在收藏页面成功移除该短剧")
    @allure.description("沉浸页点击收藏按钮——>进入收藏页面——>移除收藏的短剧")
    def test_immersion_12(self):
        """收藏短剧移除收藏的短剧"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.driver.click_collect()
            self.driver.exit_immersion_page()
            self.driver.delete_history()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_element_exists(
            self.driver.element.immersion_page.go_home_button, "断言-该短剧已被正确移除（校验Ui）"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("13-观看短剧，查看并删除历史记录")
    @allure.description("搜索短剧观看——>进入历史记录——>删除历史记录")
    def test_immersion_13(self):
        """短剧观看后进入历史记录删除记录"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.into_immersion_page()
            time.sleep(8)
            self.driver.click_collect()
            self.driver.exit_immersion_page()
            self.driver.click_play()
            self.driver.delete_history()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_element_exists(
            self.driver.element.immersion_page.go_home_button, "断言-该短剧历史记录正确删除（校验Ui）"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("14-检验shorts页面，收藏成功")
    @allure.description("进入shorts页面——>点击收藏页面——>进入我的追剧验证")
    def test_immersion_14(self):
        """检验shorts页面，收藏成功"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.enter_shorts()
            self.show_name = self.driver.get_element_text(self.element.immersion_page.shorts_name, "获取短剧名称")
            self.driver.click_collect()
            self.driver.enter_chase_shorts()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.show_name, self.driver.get_element_text(self.driver.element.immersion_page.shorts_name), "断言-该短剧正确收藏"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("15-检验shorts页面，取消收藏成功")
    @allure.description("进入shorts页面——>点击2次收藏按钮——>进入我的追剧验证")
    def test_immersion_15(self):
        """检验shorts页面，取消收藏成功"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.enter_shorts()
            self.driver.click_collect()
            self.driver.click_collect()
            self.driver.enter_chase_shorts()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_element_not_exists(
            self.driver.element.immersion_page.go_home_button, "断言-该短剧取消收藏成功（校验Ui）"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.collection_value(2)
    @allure.title("16-检验沉浸页新增简介ab测实验组点击头像拉起简介页面，收藏成功")
    @allure.description("搜索短剧——>进入视频沉浸页——>点击头像拉起视频简介——>点击收藏——>返回首页进入我的追剧")
    def test_immersion_16(self):
        """检验沉浸页新增简介ab测实验组点击头像拉起简介页面，收藏成功"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.into_immersion_page()
            self.show_name = self.driver.get_element_text(self.element.immersion_page.shorts_name, "获取短剧名称")
            self.driver.click_headshot()
            self.driver.back_home()
            self.driver.enter_chase_shorts()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.show_name, self.driver.get_element_text(self.driver.element.immersion_page.shorts_name), "断言-该短剧收藏成功"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("17-检验shorts页面，点击下方剧集条，进入沉浸页")
    @allure.description("进入shorts页面——>点击下方剧集条——>进入沉浸页唤起选集列表——>断言剧名和剧集")
    def test_immersion_17(self):
        """检验shorts页面，点击下方剧集条，进入沉浸页"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.enter_shorts()
            self.show_name = self.driver.get_element_text(self.element.immersion_page.shorts_name, "获取短剧名称")
            self.driver.click_episode_num_view()
            self.driver.assert_element_exists(self.element.immersion_page.slide, "断言-唤起选集列表（校验Ui）")
            self.driver.press_back_button("退出选集列表")
            self.driver.get_play_progress()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.show_name, self.driver.get_element_text(self.driver.element.immersion_page.shorts_name), "断言-短剧名称"
        )
        self.driver.assert_expect_in_text(
            "1", self.driver.get_element_text(self.driver.element.drama_page.episode_num), "断言-短剧播放集数"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("18-检验shorts页面，点击右侧List，进入沉浸页")
    @allure.description("进入shorts页面——>点击右侧List——>进入沉浸页唤起选集列表——>断言剧名和剧集")
    def test_immersion_18(self):
        """检验shorts页面，点击右侧List，进入沉浸页"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.enter_shorts()
            self.show_name = self.driver.get_element_text(self.element.immersion_page.shorts_name, "获取短剧名称")
            self.driver.click_shorts_list()
            self.driver.assert_element_exists(self.element.immersion_page.slide, "断言-唤起选集列表")
            self.driver.press_back_button("退出选集列表")
            self.driver.get_play_progress()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.show_name, self.driver.get_element_text(self.driver.element.immersion_page.shorts_name), "断言-短剧名称"
        )
        self.driver.assert_expect_in_text(
            "1", self.driver.get_element_text(self.driver.element.drama_page.episode_num), "断言-短剧播放集数"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("19-检验shorts页面，点击头像，进入沉浸页")
    @allure.description("进入shorts页面——>点击头像——>进入沉浸页唤起选集列表——>断言剧名和剧集")
    def test_immersion_19(self):
        """检验shorts页面，点击头像，进入沉浸页"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.enter_shorts()
            self.show_name = self.driver.get_element_text(self.element.immersion_page.shorts_name, "获取短剧名称")
            self.driver.click_shorts_headshot()
            self.driver.assert_element_exists(self.element.immersion_page.slide, "断言-唤起选集列表")
            self.driver.press_back_button("退出选集列表")
            self.driver.get_play_progress()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.show_name, self.driver.get_element_text(self.driver.element.immersion_page.shorts_name), "断言-短剧名称"
        )
        self.driver.assert_expect_in_text(
            "1", self.driver.get_element_text(self.driver.element.drama_page.episode_num), "断言-短剧播放集数"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("20-检验shorts页面，拖动进度条，进入沉浸页")
    @allure.description("进入shorts页面——>拖动进度条——>进入沉浸页唤起选集列表——>断言剧名和剧集")
    def test_immersion_20(self):
        """检验shorts页面，拖动进度条，进入沉浸页"""
        try:
            # 脚本业务
            self.driver.android_version()

            self.driver.enter_shorts()
            self.show_name = self.driver.get_element_text(self.element.immersion_page.shorts_name, "获取短剧名称")
            self.driver.drag_progress_bar()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.show_name, self.driver.get_element_text(self.driver.element.immersion_page.shorts_name), "断言-短剧名称"
        )
        self.driver.assert_expect_in_text(
            "2", self.driver.get_element_text(self.driver.element.drama_page.episode_num), "断言-短剧播放集数"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("21-沉浸页观看广告解锁新集, 滑动切换旧集播放")
    @allure.description("进入沉浸页——>解锁新集——>断言新集已解锁——>滑动返回旧集继续观看——>断言旧集播放进度")
    def test_immersion_21(self):
        """检验shorts页面，拖动进度条，进入沉浸页"""
        self.driver.android_version()

        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        _, time_now_03 = self.driver.immersion_page_into_pay_card()
        self.driver.unlock_by_advertisement()
        self.driver.check_4_and_3_play(time_now_03)

        self.test_status = True

    @pytest.mark.自动化用例开发中
    @pytest.mark.collection_value(3)
    @allure.title("22-校验沉浸页连续播放两集，展示收藏滑条（and_favorite_test_2：0）")
    @allure.description("进入沉浸页——>连续播放两集——>进入沉浸页唤起选集列表——>断言剧名和剧集")
    def test_immersion_22(self):
        """校验沉浸页连续播放两集，展示收藏滑条"""
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 连续播放两集
        self.driver.play_two_episodes()
        self.driver.assert_text_equal(
            lang_mgr.play_episode_collect_tips_1(),
            self.driver.get_element_text(self.driver.element.common_page.collect_tips),
            "断言-正确展示收藏滑条"
        )
        self.test_status = True

    @pytest.mark.自动化用例开发中
    @pytest.mark.collection_value(3)
    @allure.title("23-校验点击收藏滑条，且沉浸页右侧按钮变为选中")
    @allure.description("进入沉浸页——>连续播放两集——>点击收藏滑条——>沉浸页右侧按钮变为选中")
    def test_immersion_23(self):
        """校验点击收藏滑条，且沉浸页右侧按钮变为选中"""
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 滑动前选集按键文本
        strat_expect_text = self.driver.get_find_elements(self.element.common_page.episode_button)[0]
        # 连续播放两集
        self.driver.play_two_episodes()
        # 点击收藏滑动条
        self.driver.click_collect_swipe()
        time.sleep(2)
        # 滑动后选集按键文本
        end_expect_text = self.driver.get_find_elements(self.element.common_page.episode_button)[0]
        self.driver.assert_expect_text_not_equal(
            strat_expect_text, end_expect_text, "断言-沉浸页右侧按钮变为选中"
        )
        self.test_status = True

    @pytest.mark.自动化用例开发中
    @pytest.mark.collection_value(3)
    @allure.title("24-校验10秒内无用户操作，收藏滑动条自动收起消失（and_favorite_test_2：0）")
    @allure.description("进入沉浸页——>等待10秒——>提示自动收起消失")
    def test_immersion_24(self):
        """校验10秒内无用户操作，提示自动收起消失（AB测参数-0）"""
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 连续播放两集
        self.driver.play_two_episodes()
        # 等待10秒
        self.driver.wait_10s()
        self.driver.assert_element_not_exists(
            self.element.common_page.collect_tips, "断言-收藏滑条自动收起消失"
        )
        self.test_status = True

    @pytest.mark.自动化用例开发中
    @pytest.mark.collection_value(3)
    @allure.title("25-校验已收藏该剧时，不展示收藏滑条")
    @allure.description("进入沉浸页——>收藏该剧集——>连续播放两集——>不展示收藏滑条")
    def test_immersion_25(self):
        """校验已收藏该剧时，不展示收藏滑条"""
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 点击收藏按钮
        self.driver.click_collect()
        # 连续播放两集
        self.driver.play_two_episodes()
        self.driver.assert_element_not_exists(
            self.element.common_page.collect_tips, "断言-收藏滑条自动收起消失"
        )
        self.test_status = True

    @pytest.mark.自动化用例开发中
    @pytest.mark.collection_value(4)
    @allure.title("26-校验沉浸页连续播放两集，展示收藏滑条（and_favorite_test_2：1）")
    @allure.description("进入沉浸页——>连续播放两集——>进入沉浸页唤起选集列表——>断言剧名和剧集")
    def test_immersion_26(self):
        """校验沉浸页连续播放两集，展示收藏滑条"""
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 连续播放两集
        self.driver.play_two_episodes()
        self.driver.assert_text_equal(
            lang_mgr.play_episode_collect_tips_1(),
            self.driver.get_element_text(self.driver.element.common_page.collect_tips),
            "断言-正确展示收藏滑条"
        )
        self.test_status = True

    @pytest.mark.自动化用例开发中
    @pytest.mark.collection_value(4)
    @allure.title("27-校验10秒内无用户操作，收藏滑条自动收起消失（and_favorite_test_2：1）")
    @allure.description("进入沉浸页——>等待10秒——>提示自动收起消失")
    def test_immersion_27(self):
        """校验10秒内无用户操作，提示自动收起消失（AB测参数-0）"""
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 连续播放两集
        self.driver.play_two_episodes()
        # 等待10秒
        self.driver.wait_10s()
        self.driver.assert_element_not_exists(
            self.element.common_page.collect_tips, "断言-收藏滑条自动收起消失"
        )
        self.test_status = True

    @pytest.mark.自动化用例开发中
    @pytest.mark.collection_value(5)
    @allure.title("28-校验沉浸页连续播放两集，不展示收藏滑条（and_favorite_test_2：2）")
    @allure.description("进入沉浸页——>连续播放两集——>展示收藏滑条——>该剧自动添加至追剧列表")
    def test_immersion_28(self):
        """校验沉浸页连续播放两集，展示收藏滑条，该剧自动添加至追剧列表"""
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 连续播放两集
        self.driver.play_two_episodes()
        self.driver.assert_element_not_exists(
            self.element.common_page.collect_tips, "断言-不展示收藏滑条"
        )

        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("30-沉浸页观看广告解锁新集, 跳转旧集播放")
    @allure.description("进入沉浸页——>解锁新集——>断言新集已解锁——>跳转返回旧集继续观看——>断言旧集播放进度")
    def test_immersion_30(self):
        """检验shorts页面，拖动进度条，进入沉浸页"""
        self.driver.android_version()

        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        time_now_02, _ = self.driver.immersion_page_into_pay_card()
        self.driver.unlock_by_advertisement()
        self.driver.check_4_and_2_play(time_now_02)

        self.test_status = True
