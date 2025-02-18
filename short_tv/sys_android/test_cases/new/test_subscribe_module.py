import logging
from time import sleep

from common.api.mock_data import MockData
from common.language.lang_mgr import lang_mgr
from common.mysql.mysql_tools import update_test_case_info, mysql_execute_2
from common.utils.cmd_tools import *
from common.utils.tools import timestamp
from sys_android.page_objects.subscribe_page import SubscribePage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("订阅模块")
class TestSubscribeModule:
    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(":")[0])
        # and_immersion_page_style_test：沉浸页排版，and_task_test：任务中心入口优化
        self.mock_data.mock_data(
            "test_unlock_drama_01",
            "/app/abtest/getAbtestParams",
            {"and_immersion_page_style_test": "1", "and_without_ad_test": "0"},
        )
        self.mock_data.mock_data(
            "test_unlock_drama_01", "/app/abtest/getAbtestParams", {"and_ad_mediation_platform_test": "0"}
        )
        # 安卓端各场景广告开关
        self.mock_data.mock_data(
            "test_unlock_drama_01",
            "/app/abtest/getAbtestParams",
            {
                "adActionCount_android_v2": """
            {
              "action": {
                "exitImmersionPage": 3,
                "noPaidUnlockVideo": 1,
                "noPaidAndWatchAdEarnBonus": 2
              },
              "scene": {
                "exitImmersionPageEnable": true,
                "exitImmersionPageCount": 1,
                "switchTabEnable": true,
                "switchTabCount": 1,
                "unlockVideoEnable": true,
                "unlockVideoCount": 2,
                "homeRewardIconEnable": true,
                "homeRewardIconCount": 1,
                "shortsEnable": true,
                "shortsIntervalCount": 5,
                "discoverHorizontalVideoPreviewEnable": true,
                "immersionFullScreenNativeEnable": true,
                "immersionMediaVideoLoadTimeout": 2000,
                "immersionPreRollEnable": true,
                "immersionPreRollUnlockCount": 1,
                "immersionPostRollEnable": true,
                "immersionPostRollUnlockCount": 1
              },
              "gap": {
                "interstitial": 60000,
                "preloadAppOpen": 600000
              },
              "gdpr": {
                "showRate": 100
              }
            }
            """
            },
        )
        # and_subscription_details_test 订阅ab测
        test_cases = {"test_subscribe_37": "0", "test_subscribe_38": "2"}
        if request.node.name in test_cases:
            self.mock_data.mock_data(
                "test_unlock_drama_01",
                "/app/abtest/getAbtestParams",
                {"and_subscription_details_test": test_cases[request.node.name]},
            )
        self.proxy_process = start_proxy()
        self.driver = SubscribePage()
        # 启动录制视频
        self.driver.start_recording()
        # 采集app系统日志
        self.log_path = os.path.join(
            android.report_output_dir, args.output_report, "log", f"logcat日志_{request.node.name}_{timestamp()}.log"
        )
        self.logcat_process = adb_logcat(self.log_path)
        # 初始化测试失败标志
        self.test_status = None
        self.element = ShortTvElements()
        Log.logger.info(f"\n-----{request.node.name}开始执行-----")

        # 业务
        self.subscribe_goods = self.driver.get_subscribe_goods_text()[args.language]

    @allure.step("用例环境清理")
    @pytest.fixture(scope="function", autouse=True)
    def teardown_steps(self, request):
        yield
        # 停止录制视频并保存
        self.driver.stop_and_save_recording(self.test_status, f"{request.node.name}")
        # 停止app系统日志记录
        stop_logcat(self.logcat_process, self.log_path)
        stop_proxy(self.proxy_process)
        # 退出驱动
        self.driver.quit()
        # 更新用例
        update_test_case_info(
            request,
            self.test_status,
            self.driver.setup_step_collection,
            self.driver.case_step_collection,
            self.driver.tear_down_collection,
            self.driver.check_collection,
        )

    @pytest.mark.已开发完成
    @allure.title("07-付费卡点订阅周卡pro，剧集全场免费看")
    @allure.description("进入付费卡点——>订阅周卡pro——>所有剧集解锁")
    def test_subscribe_07(self):
        """进入付费卡点——>订阅周卡pro——>所有剧集解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.into_pay_page()
        # 订阅周卡Pro
        self.driver.subscribe_weekly_pro()
        # 进入我的模块，查看订阅状态
        self.driver.into_my_list_show_subscribe_status()

        try:
            self.driver.wait_element(self.element.common_page.cancel_login, "关闭登录弹窗", 8).click()
        except Exception as e:
            logging.error(f"An error：{e}")

        self.driver.assert_text_equal(
            f"{self.subscribe_goods["weekly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅周卡Pro成功",
        )

        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()
        self.driver.assert_text_equal(
            "30", self.driver.get_element_text(self.element.drama_page.thirty), "断言-所有剧集已全部解锁"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("08-付费卡点订阅月卡pro，剧集全场免费看")
    @allure.description("进入付费卡点——>订阅月卡pro——>所有剧集解锁")
    def test_subscribe_08(self):
        """进入付费卡点——>订阅月卡pro——>所有剧集解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.into_pay_page()
        # 订阅月卡Pro
        self.driver.subscribe_monthly_pro()
        try:
            self.driver.wait_element(self.element.common_page.cancel_login, "关闭登录弹窗", 8).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        # 进入我的模块，查看订阅状态
        self.driver.into_my_list_show_subscribe_status()

        self.driver.assert_text_equal(
            f"{self.subscribe_goods["monthly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅月卡Pro成功",
        )
        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()
        self.driver.assert_text_equal(
            "30", self.driver.get_element_text(self.element.drama_page.thirty), "断言-所有剧集已全部解锁"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("09-付费卡点订阅年卡pro，剧集全场免费看")
    @allure.description("进入付费卡点——>订阅年卡pro——>所有剧集解锁")
    def test_subscribe_09(self):
        """进入付费卡点——>订阅年卡pro——>所有剧集解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.into_pay_page()
        # 订阅年卡Pro
        self.driver.subscribe_annual_pro()
        try:
            self.driver.wait_element(self.element.common_page.cancel_login, "关闭登录弹窗", 8).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        # 进入我的模块，查看订阅状态
        self.driver.into_my_list_show_subscribe_status()
        self.driver.assert_text_equal(
            f"{self.subscribe_goods["annual_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅年卡Pro成功",
        )
        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()
        self.driver.assert_text_equal(
            "30", self.driver.get_element_text(self.element.drama_page.thirty), "断言-所有剧集已全部解锁"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("16-订阅模块下订阅周卡pro，剧集全场免费看")
    @allure.description("进入订阅模块——>订阅周卡pro——>所有剧集解锁")
    def test_subscribe_16(self):
        """进入订阅模块——>订阅周卡pro——>所有剧集解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅周卡Pro
        self.driver.subscribe_weekly_pro()

        time.sleep(1.5)
        self.driver.press_back_button("退出订阅模块")

        self.driver.assert_text_equal(
            f"{self.subscribe_goods["weekly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅周卡Pro成功",
        )
        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()

        self.driver.assert_text_equal(
            "30", self.driver.get_element_text(self.element.drama_page.thirty), "断言-所有剧集已全部解锁"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("17-订阅模块下订阅月卡pro，剧集全场免费看")
    @allure.description("进入订阅模块——>订阅月卡pro——>所有剧集解锁")
    def test_subscribe_17(self):
        """进入订阅模块——>订阅月卡pro——>所有剧集解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅月卡Pro
        self.driver.subscribe_monthly_pro()

        self.driver.click(self.element.common_page.navigation_back, "退出订阅模块")

        self.driver.assert_text_equal(
            f"{self.subscribe_goods["monthly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅月卡Pro成功",
        )

        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()

        self.driver.assert_text_equal(
            "30", self.driver.get_element_text(self.element.drama_page.thirty), "断言-所有剧集已全部解锁"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("18-订阅模块下订阅年卡pro，剧集全场免费看")
    @allure.description("进入订阅模块——>订阅年卡pro——>所有剧集解锁")
    def test_subscribe_18(self):
        """进入订阅模块——>订阅年卡pro——>所有剧集解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅年卡Pro
        self.driver.subscribe_annual_pro()

        self.driver.click(self.element.common_page.navigation_back, "退出订阅模块")

        self.driver.assert_text_equal(
            f"{self.subscribe_goods["annual_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅年卡Pro成功",
        )
        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()

        self.driver.assert_text_equal(
            "30", self.driver.get_element_text(self.element.drama_page.thirty), "断言-所有剧集已全部解锁"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("19-Top Up订阅周卡pro，剧集全场免费看")
    @allure.description("进入Top Up——>订阅周卡pro——>所有剧集解锁")
    def test_subscribe_19(self):
        """进入Top Up——>订阅周卡pro——>所有剧集解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 　进入我的模块的Top Up
        self.driver.into_top_up()
        # 订阅周卡Pro
        self.driver.subscribe_weekly_pro(False)

        try:
            self.driver.wait_element(self.element.common_page.cancel_login, "关闭登录弹窗", 8).click()
        except Exception as e:
            logging.error(f"An error：{e}")

        time.sleep(1.5)
        self.driver.press_back_button("退出Top Up模块")

        self.driver.assert_text_equal(
            f"{self.subscribe_goods["weekly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅周卡Pro成功",
        )
        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()

        self.driver.assert_text_equal(
            "30", self.driver.get_element_text(self.element.drama_page.thirty), "断言-所有剧集已全部解锁"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("20-Top Up订阅月卡pro，剧集全场免费看")
    @allure.description("进入Top Up——>订阅月卡pro——>所有剧集解锁")
    def test_subscribe_20(self):
        """进入Top Up——>订阅月卡pro——>所有剧集解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 　进入我的模块的Top Up
        self.driver.into_top_up()

        # 订阅月卡Pro
        self.driver.subscribe_monthly_pro(False)
        try:
            self.driver.wait_element(self.element.common_page.cancel_login, "关闭登录弹窗", 8).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.driver.click(self.element.common_page.navigation_back, "退出Top Up模块")

        self.driver.assert_text_equal(
            f"{self.subscribe_goods["monthly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅月卡Pro成功",
        )
        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()
        self.driver.assert_text_equal(
            "30", self.driver.get_element_text(self.element.drama_page.thirty), "断言-所有剧集已全部解锁"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("21-Top Up订阅年卡pro，剧集全场免费看")
    @allure.description("进入Top Up——>订阅年卡pro——>所有剧集解锁")
    def test_subscribe_21(self):
        """进入Top Up——>订阅年卡pro——>所有剧集解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 　进入我的模块的Top Up
        self.driver.into_top_up()

        # 订阅年卡Pro
        self.driver.subscribe_annual_pro(False)

        try:
            self.driver.wait_element(self.element.common_page.cancel_login, "关闭登录弹窗", 8).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.driver.click(self.element.common_page.navigation_back, "退出Top Up模块")

        self.driver.assert_text_equal(
            f"{self.subscribe_goods["annual_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅年卡Pro成功",
        )

        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()

        self.driver.assert_text_equal(
            "30", self.driver.get_element_text(self.element.drama_page.thirty), "断言-所有剧集已全部解锁"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("28-周卡Pro订阅过期，校验全场免费看剧集有效性")
    @allure.description("订阅周卡Pro——>数据库修改周卡Pro状态——>进入视频沉浸页——>播放最后一集——>免费看剧权益失效")
    def test_subscribe_28(self):
        """周卡Pro订阅过期，校验全场免费看剧集有效性页——>播放最后一集——>免费看剧权益失效"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅周卡Pro
        self.driver.subscribe_weekly_pro()
        time.sleep(1.5)
        self.driver.press_back_button("退出订阅模块")
        self.driver.assert_text_equal(
            f"{self.subscribe_goods["weekly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅周卡Pro成功",
        )
        # 数据库修改用户订阅状态
        self.driver.modify_user_status()
        self.driver.cold_start()
        try:
            self.driver.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.driver.click(
            ("xpath", f'//android.widget.TextView[@text="{self.driver.get_tab_button()[3]}"]'), "进入我的模块"
        )
        user_id = self.driver.get_element_text(self.element.common_page.user_uid)[-6:]
        query = f"SELECT end_time, end_time_real FROM hi_subscription_user WHERE user_id = (SELECT id FROM hi_user WHERE user_code = {user_id})"
        results = mysql_execute_2(query, [])
        end_time = results[0]["end_time"]
        end_time_real = results[0]["end_time_real"]
        self.driver.assert_text_equal(end_time, end_time_real, "断言-该用户周卡Pro状态为已过期")
        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()
        self.driver.click(self.element.drama_page.thirty, "播放最后一集")
        # 断言-免费看剧权益失效
        text = lang_mgr.episode_list_dialog_fragment_disable_skip_locked_episode()
        self.driver.assert_text_equal(
            text,
            self.driver.get_element_text(("xpath", f'//android.widget.Toast[@text="{text}"]')),
            "断言-免费看剧权益失效",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("29-月卡Pro订阅过期，校验全场免费看剧集有效性")
    @allure.description("订阅月卡Pro——>数据库修改月卡Pro状态——>进入视频沉浸页——>播放最后一集——>免费看剧权益失效")
    def test_subscribe_29(self):
        """订阅月卡Pro——>数据库修改月卡Pro状态——>进入视频沉浸页——>播放最后一集——>免费看剧权益失效"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅月卡Pro
        self.driver.subscribe_monthly_pro()
        self.driver.click(self.element.common_page.navigation_back, "退出订阅模块")
        self.driver.assert_text_equal(
            f"{self.subscribe_goods["monthly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅月卡Pro成功",
        )
        # 数据库修改用户订阅状态
        self.driver.modify_user_status()
        # 冷启动
        self.driver.cold_start()
        try:
            self.driver.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.driver.click(
            ("xpath", f'//android.widget.TextView[@text="{self.driver.get_tab_button()[3]}"]'), "进入我的模块"
        )
        user_id = self.driver.get_element_text(self.element.common_page.user_uid)[-6:]
        query = f"SELECT end_time, end_time_real FROM hi_subscription_user WHERE user_id = (SELECT id FROM hi_user WHERE user_code = {user_id})"
        results = mysql_execute_2(query, [])
        end_time = results[0]["end_time"]
        end_time_real = results[0]["end_time_real"]
        self.driver.assert_text_equal(end_time, end_time_real, "断言-该用户周卡Pro状态为已过期")
        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()
        self.driver.click(self.element.drama_page.thirty, "播放最后一集")
        # 断言-免费看剧权益失效
        text = lang_mgr.episode_list_dialog_fragment_disable_skip_locked_episode()
        self.driver.assert_text_equal(
            text,
            self.driver.get_element_text(("xpath", f'//android.widget.Toast[@text="{text}"]')),
            "断言-免费看剧权益失效",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("30-年卡Pro订阅过期，校验全场免费看剧集有效性")
    @allure.description("订阅年卡Pro——>数据库修改年卡Pro状态——>进入视频沉浸页——>播放最后一集——>免费看剧权益失效")
    def test_subscribe_30(self):
        """订阅年卡Pro——>数据库修改年卡Pro状态——>进入视频沉浸页——>播放最后一集——>免费看剧权益失效"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅周卡Pro
        self.driver.subscribe_annual_pro()
        self.driver.click(self.element.common_page.navigation_back, "退出订阅模块")
        self.driver.assert_text_equal(
            f"{self.subscribe_goods["annual_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅年卡Pro成功",
        )
        # 数据库修改用户订阅状态
        self.driver.modify_user_status()
        # 冷启动
        self.driver.cold_start()
        try:
            self.driver.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.driver.click(
            ("xpath", f'//android.widget.TextView[@text="{self.driver.get_tab_button()[3]}"]'), "进入我的模块"
        )
        user_id = self.driver.get_element_text(self.element.common_page.user_uid)[-6:]
        query = f"SELECT end_time, end_time_real FROM hi_subscription_user WHERE user_id = (SELECT id FROM hi_user WHERE user_code = {user_id})"
        results = mysql_execute_2(query, [])
        end_time = results[0]["end_time"]
        end_time_real = results[0]["end_time_real"]
        self.driver.assert_text_equal(end_time, end_time_real, "断言-该用户年卡Pro状态为已过期")
        # 进入视频沉浸页，播放最后一集
        self.driver.into_video_immersive_play_last_episode()
        self.driver.click(self.element.drama_page.thirty, "播放最后一集")
        # 断言-免费看剧权益失效
        text = lang_mgr.episode_list_dialog_fragment_disable_skip_locked_episode()
        self.driver.assert_text_equal(
            text,
            self.driver.get_element_text(("xpath", f'//android.widget.Toast[@text="{text}"]')),
            "断言-免费看剧权益失效",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("31-周卡Pro订阅过期，显示插屏、开屏广告")
    @allure.description(
        "订阅周卡Pro——>数据库修改周卡Pro状态——>三次从沉浸页退出——>触发插屏广告——>热启动app——>触发插屏广告——>切换tab——>触发插屏广告"
    )
    def test_subscribe_31(self):
        """订阅周卡Pro——>数据库修改周卡Pro状态——>三次从沉浸页退出——>触发插屏广告——>热启动app——>触发插屏广告——>切换tab——>触发插屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅周卡Pro
        self.driver.subscribe_weekly_pro()
        time.sleep(1.5)
        self.driver.press_back_button("退出订阅模块")
        self.driver.assert_text_equal(
            f"{self.subscribe_goods["weekly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅周卡Pro成功",
        )
        # 数据库修改用户订阅状态
        self.driver.modify_user_status()
        # 冷启动
        self.driver.cold_start()
        try:
            self.driver.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.driver.click(
            ("xpath", f'//android.widget.TextView[@text="{self.driver.get_tab_button()[3]}"]'), "进入我的模块"
        )
        user_id = self.driver.get_element_text(self.element.common_page.user_uid)[-6:]
        query = f"SELECT end_time, end_time_real FROM hi_subscription_user WHERE user_id = (SELECT id FROM hi_user WHERE user_code = {user_id})"
        results = mysql_execute_2(query, [])
        end_time = results[0]["end_time"]
        end_time_real = results[0]["end_time_real"]
        self.driver.assert_text_equal(end_time, end_time_real, "断言-该用户周卡Pro状态为已过期")
        # 三次从沉浸页退出
        self.driver.search_shorts_exit_immersive_page_3_times()
        time.sleep(6)
        # 断言-触发开屏广告（校验UI）
        self.driver.check_open_advertisement()
        self.driver.click(self.element.common_page.back, "返回首页")
        # 热启动
        self.driver.hot_start()
        # 断言-触发开屏广告（校验UI）
        self.driver.check_open_advertisement()
        # 等待60秒, 并切换tab
        self.driver.wait_and_switch_tab()
        # 断言-触发开屏广告（校验UI）
        self.driver.check_open_advertisement()
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("32-月卡Pro订阅过期，显示插屏、开屏广告")
    @allure.description(
        "订阅月卡Pro——>数据库修改月卡Pro状态——>三次从沉浸页退出——>触发插屏广告——>热启动app——>触发插屏广告——>切换tab——>触发插屏广告"
    )
    def test_subscribe_32(self):
        """订阅月卡Pro——>数据库修改月卡Pro状态——>三次从沉浸页退出——>触发插屏广告——>热启动app——>触发插屏广告——>切换tab——>触发插屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅月卡Pro
        self.driver.subscribe_monthly_pro()
        self.driver.click(self.element.common_page.navigation_back, "退出订阅模块")
        self.driver.assert_text_equal(
            f"{self.subscribe_goods["monthly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅月卡Pro成功",
        )
        # 数据库修改用户订阅状态
        self.driver.modify_user_status()
        # 冷启动
        self.driver.cold_start()
        try:
            self.driver.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.driver.click(
            ("xpath", f'//android.widget.TextView[@text="{self.driver.get_tab_button()[3]}"]'), "进入我的模块"
        )
        user_id = self.driver.get_element_text(self.element.common_page.user_uid)[-6:]
        query = f"SELECT end_time, end_time_real FROM hi_subscription_user WHERE user_id = (SELECT id FROM hi_user WHERE user_code = {user_id})"
        results = mysql_execute_2(query, [])
        end_time = results[0]["end_time"]
        end_time_real = results[0]["end_time_real"]
        self.driver.assert_text_equal(end_time, end_time_real, "断言-该用户月卡Pro状态为已过期")
        # 三次从沉浸页退出
        self.driver.search_shorts_exit_immersive_page_3_times()
        time.sleep(6)
        # 断言-触发开屏广告（校验UI）
        self.driver.check_open_advertisement()
        self.driver.click(self.element.common_page.back, "返回首页")
        # 热启动
        self.driver.hot_start()
        # 断言-触发开屏广告（校验UI）
        self.driver.check_open_advertisement()
        # 等待60秒, 并切换tab
        self.driver.wait_and_switch_tab()
        # 断言-触发开屏广告（校验UI）
        self.driver.check_open_advertisement()
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("33-年卡Pro订阅过期，显示插屏、开屏广告")
    @allure.description(
        "订阅年卡Pro——>数据库修改年卡Pro状态——>三次从沉浸页退出——>触发插屏广告——>热启动app——>触发插屏广告——>切换tab——>触发插屏广告"
    )
    def test_subscribe_33(self):
        """订阅年卡Pro——>数据库修改年卡Pro状态——>三次从沉浸页退出——>触发插屏广告——>热启动app——>触发插屏广告——>切换tab——>触发插屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅年卡Pro
        self.driver.subscribe_annual_pro()
        self.driver.click(self.element.common_page.navigation_back, "退出订阅模块")
        self.driver.assert_text_equal(
            f"{self.subscribe_goods["annual_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅年卡Pro成功",
        )
        # 数据库修改用户订阅状态
        self.driver.modify_user_status()
        # 冷启动
        self.driver.cold_start()
        try:
            self.driver.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.driver.click(
            ("xpath", f'//android.widget.TextView[@text="{self.driver.get_tab_button()[3]}"]'), "进入我的模块"
        )
        user_id = self.driver.get_element_text(self.element.common_page.user_uid)[-6:]
        query = f"SELECT end_time, end_time_real FROM hi_subscription_user WHERE user_id = (SELECT id FROM hi_user WHERE user_code = {user_id})"
        results = mysql_execute_2(query, [])
        end_time = results[0]["end_time"]
        end_time_real = results[0]["end_time_real"]
        self.driver.assert_text_equal(end_time, end_time_real, "断言-该用户年卡Pro状态为已过期")
        # 三次从沉浸页退出
        self.driver.search_shorts_exit_immersive_page_3_times()
        # 断言-触发开屏广告（校验UI）
        self.driver.check_open_advertisement()
        self.driver.click(self.element.common_page.back, "返回首页")
        # 热启动
        self.driver.hot_start()
        # 断言-触发开屏广告（校验UI）
        self.driver.check_open_advertisement()
        # 等待60秒, 并切换tab
        self.driver.wait_and_switch_tab()
        # 断言-触发开屏广告（校验UI）
        self.driver.check_open_advertisement()
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("34-校验低版本购买pro商品成功后，升级到高版本，可正常升级订阅商品")
    @allure.description("安装低版本apk——>订阅周卡Pro——>选择价格更高订阅商品进行升级——>可正常升级订阅商品")
    def test_subscribe_34(self):
        """安装低版本apk——>订阅周卡Pro——>安装高版本apk——>选择价格跟高订阅商品进行升级——>可正常升级订阅商品"""
        # 卸载当前apk 安装低版本
        self.driver.uninstall_and_install_apk()
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅周卡Pro
        self.driver.subscribe_weekly_pro()
        # 升级高版本apk，v2.0.9
        self.driver.upgrade_apk()
        # 关闭首页弹窗
        self.driver.android_version()
        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 选择价格跟高订阅商品进行升级
        self.driver.confirm_change_subscribe()
        self.driver.click(self.element.common_page.confirm, "确定更改订阅")
        self.driver.click(self.element.common_page.cocnfirm_button, "确定订阅")
        self.driver.assert_text_equal(
            lang_mgr.subscription_detail_activity_subs_update_success(),
            self.driver.get_element_text(
                (
                    "xpath",
                    f'//android.widget.Toast[@text="{lang_mgr.subscription_detail_activity_subs_update_success()}"]',
                )
            ),
            "断言-升级订阅商品成功",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("35-校验订阅金额更高的pro商品属于升级 && 确认更改订阅弹框展示信息检查")
    @allure.description("订阅金额更高的pro商品——>成功弹出“确认更改订阅”弹框（显示内容正确）")
    def test_subscribe_35(self):
        """订阅金额更高的pro商品——>成功弹出“确认更改订阅”弹框（显示内容正确）"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅周卡Pro
        self.driver.subscribe_weekly_pro()
        # 订阅金额更高的pro商品
        self.driver.confirm_change_subscribe()
        self.driver.assert_text_equal(
            lang_mgr.subs_update_dialog_title(),
            self.driver.get_element_text(self.element.common_page.title),
            "断言-成功弹出“确认更改订阅”弹框（显示内容正确）",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("37-校验订阅走对照组，原订阅样式订阅逻辑，保持不变")
    @allure.description("订阅走对照组——>校验订阅样式订阅逻辑")
    def test_subscribe_37(self):
        """订阅金额更高的pro商品——>成功弹出“确认更改订阅”弹框（显示内容正确）"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅周卡Pro
        self.driver.subscribe_weekly_pro()
        time.sleep(1.5)
        self.driver.press_back_button("退出订阅模块")
        self.driver.assert_text_equal(
            f"{self.subscribe_goods["weekly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅周卡Pro成功",
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("38-校验订阅走实验组，未订阅下，数据取值正确")
    @allure.description("订阅走实验组——>未订阅商品")
    def test_subscribe_38(self):
        """订阅金额更高的pro商品——>成功弹出“确认更改订阅”弹框（显示内容正确）"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        self.driver.assert_text_equal(
            lang_mgr.subscription_detail_activity_privilege_new_5_title(),
            self.driver.get_element_text(('xpath',
                                          f'//android.widget.TextView[@text="{lang_mgr.subscription_detail_activity_privilege_new_5_title()}"]')),
            "断言-订阅商品配置只会配置全场免费看的订阅商品"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("39-校验升级时掉单，可正常恢复订阅状态")
    @allure.description("订阅周卡Peo——>掉单升级订阅商品")
    def test_subscribe_39(self):
        """订阅周卡Peo——>掉单升级订阅商品"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入订阅模块
        self.driver.into_subscribe_module()
        # 订阅周卡Pro
        self.driver.subscribe_weekly_pro()
        # 选择价格跟高订阅商品进行升级
        self.driver.confirm_change_subscribe()
        self.driver.click(self.element.common_page.confirm, "确定更改订阅")
        self.driver.click(self.element.top_up_page.negative_button, "掉单")
        self.driver.click(self.element.common_page.retry_button, "恢复购买")
        self.driver.press_back_button("退出订阅模块")
        self.driver.assert_text_equal(
            f"{self.subscribe_goods["monthly_pro"]}",
            self.driver.get_element_text(self.element.common_page.title),
            "断言-订阅月卡Pro成功",
        )
        self.test_status = True
