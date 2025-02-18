import logging
import os
import time

import allure
import pytest
from appium.webdriver.common.appiumby import AppiumBy

from common.api.mock_data import MockData
from common.language.lang_mgr import lang_mgr
from common.mysql.mysql_tools import update_test_case_info
from common.utils.arg_parse_func import args
from common.utils.cmd_tools import adb_logcat, stop_logcat, start_proxy, stop_proxy
from common.utils.log_utils import Log
from common.utils.path_config import android
from common.utils.tools import timestamp
from sys_android.page_objects.advertisement_page import AdvertisementPage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("广告相关模块")
class TestAdvertisementModule:
    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(':')[0])
        # and_immersion_page_style_test：沉浸页排版，and_task_test：任务中心入口优化
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams",
                                 {"and_immersion_page_style_test": "1", "and_task_test": "0"})
        # 付费卡点显示广告解锁，参数为0显示内购+广告+膨胀sku
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams", {"and_without_ad_test": "0"})
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams",
                                 {"and_ad_mediation_platform_test": "0"})
        # 安卓端各场景广告开关
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams", {
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
        })
        collection_value = request.node.get_closest_marker("collection_value")
        collection_value = collection_value.args[0] if collection_value else None
        mock_values = {
            0: {"and_immersion_ad_test": "0"},
            1: {"and_immersion_ad_test": "1"},
            2: {"and_immersion_ad_test": "2"},
            3: {"and_immersion_ad_test": "3"}
        }
        if collection_value in mock_values:
            self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams",
                                     mock_values[collection_value])
        self.proxy_process = start_proxy()
        self.driver = AdvertisementPage()
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
    @allure.title("1-校验热启动app，不触发开屏广告")
    @allure.description("搜索剧集——>进入视频沉浸页——>退出短剧——>不触发开屏广告")
    def test_advertisement_1(self):
        """搜索剧集——>进入视频沉浸页——>退出短剧——>不触发开屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 退出视频沉浸页
        self.driver.out_immersion_page()
        # 热启动
        self.driver.hot_start()

        # todo断言有点奇怪 断言不触发开屏广告
        self.driver.assert_text_equal(self.driver.language_search()[args.language],
                                      self.driver.advertisement_module_expect_3(),
                                      "断言-不触发开屏广告-'广告解锁剧集'文本")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("2-校验3次从沉浸页退出，触发插屏、开屏广告")
    @allure.description("搜索剧集——>进入视频沉浸页——>3次从沉浸页退出——>触发插屏广告——>热启动app——>触发开屏广告")
    def test_advertisement_2(self):
        """搜索剧集——>进入视频沉浸页——>3次从沉浸页退出——>触发插屏广告——>热启动app——>触发开屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧
        self.driver.search_shorts()
        # 三次从沉浸页退出
        self.driver.exit_immersion_page_times(3)
        # 断言-三次从沉浸页退出，触发插屏广告（校验UI）
        self.driver.check_trigger_advertisement()
        # 热启动
        self.driver.hot_start()
        # 断言触发开屏广告
        self.driver.assert_element_exists(self.element.drama_page.advertisement_text, "断言-触发开屏广告（校验UI）")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("3-校验2次从沉浸页退出，不触发插屏、开屏广告")
    @allure.description("搜索剧集——>进入视频沉浸页——>2次从沉浸页退出——>不触发插屏广告——>热启动app——>不触发开屏广告")
    def test_advertisement_3(self):
        """搜索剧集——>进入视频沉浸页——>2次从沉浸页退出——>不触发插屏广告——>热启动app——>不触发开屏广告"""

        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧
        self.driver.search_shorts()
        # 2次从沉浸页退出
        self.driver.exit_immersion_page_times(2)
        # 断言-不触发插屏广告（校验UI）
        self.driver.assert_text_equal(self.driver.language_search()[args.language],
                                      self.driver.get_element_text(self.element.common_page.automation_test_text),
                                      "断言-不触发插屏广告（校验UI）")
        # 热启动
        self.driver.hot_start()

        self.driver.assert_text_equal(self.driver.language_search()[args.language],
                                      self.driver.advertisement_module_expect_3(),
                                      "断言-不触发开屏广告-'广告解锁剧集'文本")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("4-校验用户进入付费卡点未付费，触发插屏、开屏广告")
    @allure.description(
        "搜索剧集——>进入视频沉浸页——>进入付费卡点——>退出沉浸页——>触发插屏广告——>热启动app——>触发开屏广告")
    def test_advertisement_4(self):
        """搜索剧集——>进入视频沉浸页——>进入付费卡点——>退出沉浸页——>触发插屏广告——>热启动app——>触发开屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.search_shorts_into_pay_card()
        # 关闭付费卡点弹窗
        self.driver.pay_card_close_popup_window()
        # 退出视频沉浸页
        self.driver.out_immersion_page()
        # 断言-从沉浸页退出，触发插屏广告（校验UI）
        self.driver.check_trigger_advertisement()
        # 热启动
        self.driver.hot_start()

        self.driver.assert_element_exists(self.element.drama_page.advertisement_text, "断言-触发开屏广告（校验UI）")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("5-校验任务中心观看2次激励视频，触发开屏广告")
    @allure.description("进入任务中心——>观看两次激励视频——>触发开屏广告")
    def test_advertisement_5(self):

        """进入任务中心——>观看两次激励视频——>触发开屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 退出视频沉浸页
        self.driver.out_immersion_page()
        self.driver.click(self.element.common_page.back, "返回首页")
        # 返回首页,进入任务中心
        self.driver.into_task_center()
        # 关闭Watch Now
        self.driver.close_watch_now()
        self.driver.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 300)
        # 连续观看两次激励视频
        self.driver.watch_reward_video()
        time.sleep(18)
        self.driver.watch_reward_video()
        # 热启动
        self.driver.hot_start()
        time.sleep(2)
        self.driver.assert_element_exists(self.element.drama_page.advertisement_text, "断言-触发开屏广告（校验UI）")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("6-校验任务中心观看1次激励视频，不触发开屏广告")
    @allure.description("进入任务中心——>观看一次激励视频——>不触发开屏广告")
    def test_advertisement_6(self):
        """进入任务中心——>观看一次激励视频——>不触发开屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 退出视频沉浸页
        self.driver.out_immersion_page()
        self.driver.click(self.element.common_page.back, "返回首页")
        # 返回首页,进入任务中心
        self.driver.into_task_center()
        # 关闭Watch Now
        self.driver.close_watch_now()
        self.driver.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 300)
        # 观看激励视频
        self.driver.watch_reward_video()
        # 热启动
        self.driver.hot_start()
        # 断言不触发开屏广告
        self.driver.assert_text_equal(self.driver.get_element_text(self.element.common_page.watch_ads_text),
                                      self.driver.advertisement_module_expect_7(),
                                      "断言-不触发开屏广告")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.regression
    @allure.title("7-校验任务中心观看奖励翻倍视频+1次激励视频，不触发开屏广告")
    @allure.description("进入任务中心——>观看奖励翻倍视频+激励视频——>不触发开屏广告")
    def test_advertisement_7(self):
        """进入任务中心——>观看奖励翻倍视频+激励视频——>不触发开屏广告"""

        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 退出视频沉浸页
        self.driver.out_immersion_page()
        self.driver.click(self.element.common_page.back, "返回首页")
        # 返回首页,进入任务中心
        self.driver.into_task_center()
        # 观看Watch Now
        self.driver.watch_watch_now()
        # 观看激励视频
        self.driver.watch_reward_video()
        # 热启动
        self.driver.hot_start()

        # 断言不触发开屏广告
        self.driver.assert_text_equal(self.driver.get_element_text(self.element.common_page.watch_ads_text),
                                      self.driver.advertisement_module_expect_7(),
                                      "断言-不触发开屏广告")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("8-校验用户切换tab，广告之间的间隔时长为60s，触发插屏广告，并触发开屏广告")
    @allure.description("进入付费卡点——>进入首页——>切换tab（我的短剧）——>触发插屏——>热启动app——>触发开屏广告")
    def test_advertisement_8(self):
        """进入付费卡点——>进入首页——>切换tab（我的短剧）——>触发插屏——>热启动app——>触发开屏广告"""

        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.search_shorts_into_pay_card()
        # 关闭付费卡点弹窗
        self.driver.pay_card_close_popup_window()
        # 从付费卡点返回首页
        self.driver.pay_card_back_to_home()
        # 等待60秒,切换tab到短剧
        self.driver.wait_60_seconds_switch_tab()
        # 热启动
        self.driver.hot_start()

        # 断言触发开屏广告
        self.driver.assert_element_exists(self.element.drama_page.advertisement_text, "断言-触发开屏广告（校验UI）")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("9-校验在期会员用户不显示插屏、开屏广告")
    @allure.description("进入订阅模块——>订阅周卡——>3次从沉浸页退出——>退出app——>热启动——>不触发开屏广告")
    def test_advertisement_9(self):
        """进入订阅模块——>订阅周卡——>3次从沉浸页退出——>退出app——>热启动——>不触发开屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 订阅周卡Por
        self.driver.subscribe_weekly_method()
        # 搜索短剧
        self.driver.search_shorts()
        # 3次从沉浸页退出
        self.driver.exit_immersion_page_times(3)
        # 断言-不触发插屏广告（校验UI）
        self.driver.assert_text_equal(self.driver.language_search()[args.language],
                                      self.driver.get_element_text(self.element.common_page.automation_test_text),
                                      "断言-不触发插屏广告（校验UI）")
        # 热启动
        self.driver.hot_start()
        # 断言 - 不触发插屏广告（校验UI）
        self.driver.assert_text_equal(self.driver.language_search()[args.language],
                                      self.driver.get_element_text(self.element.common_page.automation_test_text),
                                      "断言-不触发插屏广告（校验UI）")
        # 返回首页,切换tab到短剧
        self.driver.back_to_home_switch_tab()

        # 断言-切换tab不触发插屏广告（校验UI）
        self.driver.assert_element_exists(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.driver.get_tab_button()[3]}"]'),
            "切换tab不触发插屏广告（校验UI）"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("10-校验有余额的充值用户不显示插屏、开屏广告")
    @allure.description("进入充值模块——>充值金币——>3次从沉浸页退出——>退出app——>热启动——>不触发开屏广告")
    def test_advertisement_10(self):
        """进入充值模块——>充值金币——>3次从沉浸页退出——>退出app——>热启动——>不触发开屏广告"""

        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 充值金币
        self.driver.recharge_coins()
        # 搜索短剧
        self.driver.search_shorts()
        # 3次从沉浸页退出
        self.driver.exit_immersion_page_times(3)
        # 断言-不触发插屏广告（校验UI）
        self.driver.assert_text_equal(self.driver.language_search()[args.language],
                                      self.driver.get_element_text(self.element.common_page.automation_test_text),
                                      "断言-不触发插屏广告（校验UI）")
        # 热启动
        self.driver.hot_start()
        # 断言 - 不触发插屏广告（校验UI）
        self.driver.assert_text_equal(self.driver.language_search()[args.language],
                                      self.driver.get_element_text(self.element.common_page.automation_test_text),
                                      "断言-不触发插屏广告（校验UI）")
        # 返回首页,切换tab到短剧
        self.driver.back_to_home_switch_tab()

        # 断言-切换tab不触发插屏广告（校验UI）
        self.driver.assert_element_exists(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.driver.get_tab_button()[3]}"]'),
            "切换tab不触发插屏广告（校验UI）"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("11-校验付费卡点后连续观看2次剧集，显示插屏广告，并触发开屏广告")
    @allure.description("进入付费卡点——>连续解锁2次剧——>触发插屏广告——退出app——>热启动——>触发开屏广告")
    def test_advertisement_11(self):
        """进入付费卡点——>连续解锁2次剧——>触发插屏广告——退出app——>热启动——>触发开屏广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.search_shorts_into_pay_card()
        # 连续解锁2次剧（广告解锁）
        self.driver.unlock_advertisement()
        self.driver.assert_element_exists(
            self.element.advertisement_page.interstitial_advertisement, "断言-下滑至第6集时插屏广告显示成功"
        )
        # 热启动
        self.driver.hot_start()

        # 断言开屏广告元素相等
        self.driver.assert_element_exists(self.element.drama_page.advertisement_text, "断言-触发开屏广告（校验UI）")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("12-校验用户点击右上角礼包，显示广告")
    @allure.description("进入首页——>点击右上角礼包——>显示广告")
    def test_advertisement_12(self):
        """进入首页——>点击右上角礼包——>显示广告"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 首页点击右上角礼包
        self.driver.gift_package()

        # 断言开屏广告元素相等
        self.driver.assert_element_exists(self.element.drama_page.advertisement_text, "断言-触发开屏广告（校验UI）")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("13-校验观看奖励翻倍视频，奖励币翻倍")
    @allure.description("进入任务中心——>观看奖励翻倍视频——>奖励币翻倍")
    def test_advertisement_13(self):
        """进入任务中心——>观看奖励翻倍视频——>奖励币翻倍"""

        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 返回首页,进入任务中心
        self.driver.into_task_center()
        # 关闭Watch Now
        self.driver.close_watch_now()
        # 获取当前金币数量
        self.current_coins = self.driver.get_current_gold()
        # 观看双倍奖励视频
        self.driver.watch_double_reward_video()

        # 断言奖金翻倍后金额
        self.driver.assert_text_equal(self.current_coins * 2, int(self.driver.advertisement_module_expect_13()),
                                      "断言-双倍奖励金币")
        self.driver.advertisement_module_expects_13()
        # todo 时间戳样式根据国家地区下发
        # 获取当前时间戳
        # self.now_time = datetime.now().strftime("%m/%d/%Y")
        # with allure.step("断言-奖励币日期"):
        #     assert self.now_time in self.driver.reward_coins_date_expect()
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("16-校验广告解锁剧集，解锁次数减少")
    @allure.description(
        "搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁剧集——>观看广告——>解锁剧集——>广告解锁次数减少")
    def test_advertisement_16(self):
        """搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁剧集——>观看广告——>解锁剧集——>广告解锁次数减少"""

        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.search_shorts_into_pay_card()
        # 广告解锁剧集
        self.driver.advertisement_unlock_drama()
        # 下滑至下一集
        self.driver.next_page()

        # self.driver.advertisement_module_16()
        # 提取日志key值
        # self.pwd = find_log_value_by_key(self.log_path, "[AppLogger][StringUtil]: [, , 0]")
        # with allure.step(f"秘钥：{self.pwd}"):
        #     allure.attach(f"秘钥：{self.pwd}", name="秘钥")

        # 断言广告解锁次数
        self.driver.assert_expect_in_text("1/8", self.driver.get_element_text(self.element.drama_page.desc_tv),
                                          "广告解锁剩余次数减少")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("17-校验广告解锁次数非继承")
    @allure.description("搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁剧集——>切换影剧——>广告解锁次数非继承")
    def test_advertisement_17(self):
        """搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁剧集——>切换影剧——>广告解锁次数非继承"""
        try:
            # 关闭首页弹窗
            self.driver.android_version()
            # 切换成新账号
            # self.driver.switch_new_account()
            # 搜索短剧，进入付费卡点
            self.driver.search_shorts_into_pay_card()
            # 广告解锁剧集
            self.driver.advertisement_unlock_drama()
            self.driver.return_to_pay_page()
        except Exception as e:
            logging.error(f"An error: {e}")
        # 断言广告解锁次数
        self.driver.assert_expect_in_text("0/8", self.driver.get_element_text(self.element.drama_page.desc_tv),
                                          "断言-广告解锁次数非继承")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("18-校验解锁'后续剧情'给于提示信息")
    @allure.description("搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁剧集——>选择未解锁的后续剧集——>系统给予提示")
    def test_advertisement_18(self):
        """搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁剧集——>选择未解锁的后续剧集——>系统给予提示"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 解锁第五集
        self.driver.unlock_dramas_05()

        # 断言-app提示信息文本
        self.driver.assert_text_equal(
            lang_mgr.episode_list_dialog_fragment_disable_skip_locked_episode(),
            self.driver.wait_element((
                'xpath',
                f'//android.widget.Toast[@text="{lang_mgr.episode_list_dialog_fragment_disable_skip_locked_episode()}"]',
            )).text,
            "断言-toast提示"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("19-校验广告解锁剧集，广告正确加载")
    @allure.description("搜索剧集——>进入视频沉浸页——>广告解锁剧集——>广告正确加载")
    def test_advertisement_19(self):
        """搜索剧集——>进入视频沉浸页——>广告解锁剧集——>广告正确加载"""

        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.search_shorts_into_pay_card()
        self.driver.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集")
        # self.driver.advertisement_module_19()

        # 断言广告正确加载
        self.driver.assert_element_exists(self.element.drama_page.advertisement_text, "断言-广告正确播放（校验UI）")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("20-校验沉浸页，付费卡点出现广告解锁入口")
    @allure.description("搜索剧集——>进入视频沉浸页——>进入付费卡点——>conis store】显示正常")
    def test_advertisement_20(self):
        """搜索剧集——>进入视频沉浸页——>进入付费卡点——>conis store】显示正常"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.search_shorts_into_pay_card()
        # 断言-付费卡点显示正常广告解锁入口（校验UI）
        self.driver.check_advertisement_page_unlock()

        # 断言解锁入口显示正常
        self.driver.assert_text_equal(
            lang_mgr.coin_store_dialog_fragment_free_unlock(),
            self.driver.get_element_text((
                'xpath',
                f'//android.widget.TextView[@text="{lang_mgr.coin_store_dialog_fragment_free_unlock()}"]',
            )),
            "断言-解锁入口显示正常"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("21-校验广告解锁次数的有限性，且广告次数全部消耗后conis store的广告入口消失")
    @allure.description("搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁次数全部消耗——>广告解锁剩余次数为0")
    def test_advertisement_21(self):
        """搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁次数全部消耗——>广告解锁剩余次数为0"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.search_shorts_into_pay_card()
        # 广告解锁剧集（第4-11集）
        self.driver.advertisement_unlock_4_to_11()
        # 断言-付费卡点显示正常
        self.driver.assert_expect_in_text(" 8/8", self.driver.get_element_text(self.element.drama_page.desc_tv),
                                          "断言-广告解锁剩余次数为0")
        time.sleep(2)
        self.driver.click(self.element.drama_page.coin_store, "点击【Conis Store】")
        # 断言-付费卡点显示正常
        self.driver.assert_element_not_exists((AppiumBy.XPATH, '//android.widget.TextView[@text="Free Unlock"]'),
                                              "断言-付费卡点显示正常")
        # with allure.step("断言-付费卡点显示正常"):
        #     try:
        #         self.driver.driver.find_element(AppiumBy.XPATH, '//android.widget.TextView[@text="Free Unlock"]')
        #         # 如果找到了元素，记录断言失败信息
        #         allure.attach("元素存在，断言失败", name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
        #         assert False, "元素存在，断言失败"
        #     except NoSuchElementException:
        #         # 如果没有找到元素，记录断言成功信息
        #         allure.attach("元素不存在，断言成功", name="断言成功信息", attachment_type=allure.attachment_type.TEXT)
        #         assert True, "元素不存在，断言成功"
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("22-校验沉浸页提前观看广告对照组逻辑（and_immersion_ad_test：0）")
    @allure.description("三次从沉浸页退出——>搜索剧集——>进入视频沉浸页——>进入付费卡点——>连续观看广告解锁弹窗不展示")
    @pytest.mark.collection_value(0)
    def test_advertisement_22(self):
        """三次从沉浸页退出——>搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁次数全部消耗——>广告解锁剩余次数为0"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 三次从沉浸页退出
        self.driver.exit_immersion_page_times(3)
        time.sleep(8)
        self.driver.click(self.element.common_page.cancel_login, "关闭插屏广告")
        # 搜索短剧，进入视频沉浸页
        self.driver.into_immersion_page()
        # 滑动进入付费卡点
        self.driver.swipe_into_pay_page()
        self.driver.assert_element_not_exists(self.element.common_page.look_advertisement,
                                              "断言-连续观看广告解锁弹窗不展示")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("23-校验沉浸页提前观看广告对比组逻辑（and_immersion_ad_test：1）")
    @allure.description("三次从沉浸页退出——>搜索剧集——>进入视频沉浸页——>进入付费卡点——>连续观看广告解锁弹窗不展示")
    @pytest.mark.collection_value(1)
    def test_advertisement_23(self):
        """三次从沉浸页退出——>搜索剧集——>进入视频沉浸页——>进入付费卡点——>广告解锁次数全部消耗——>广告解锁剩余次数为0"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 三次从沉浸页退出
        self.driver.exit_immersion_page_times(3)
        time.sleep(8)
        self.driver.click(self.element.common_page.cancel_login, "关闭插屏广告")
        # 搜索短剧，进入视频沉浸页
        self.driver.into_immersion_page()
        # 滑动进入付费卡点
        self.driver.swipe_into_pay_page()
        self.driver.assert_element_not_exists(self.element.common_page.look_advertisement,
                                              "断言-连续观看广告解锁弹窗不展示")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("24-校验到达付费卡点后，唤起连续观看广告弹窗（and_immersion_ad_test：2）")
    @allure.description("三次从沉浸页退出——>搜索剧集——>进入视频沉浸页——>进入付费卡点——>弹出连续观看广告弹窗")
    @pytest.mark.collection_value(2)
    def test_advertisement_24(self):
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 三次从沉浸页退出
        self.driver.exit_immersion_page_times(3)
        time.sleep(8)
        self.driver.click(self.element.common_page.cancel_login, "关闭插屏广告")
        # 搜索短剧，进入视频沉浸页
        self.driver.into_immersion_page()
        # 滑动进入付费卡点
        self.driver.swipe_into_pay_page()
        self.driver.assert_text_equal(
            lang_mgr.unlock_episode_dialog_fragment_watch_ads(),
            self.driver.get_element_text(self.element.drama_page.advertisement_unlock),
            "断言-正确弹出连续观看广告弹窗"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("25-校验观看广告后，唤起连续观看广告挽留弹窗（and_immersion_ad_test：2）")
    @allure.description(
        "三次从沉浸页退出——>搜索剧集——>进入视频沉浸页——>进入付费卡点——>弹出连续观看广告弹窗——>观看广告后——>唤起连续观看广告挽留弹窗")
    @pytest.mark.collection_value(2)
    def test_advertisement_25(self):
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 三次从沉浸页退出
        self.driver.exit_immersion_page_times(3)
        time.sleep(8)
        self.driver.click(self.element.common_page.cancel_login, "关闭插屏广告")
        # 搜索短剧，进入视频沉浸页
        self.driver.into_immersion_page()
        # 滑动进入付费卡点
        self.driver.swipe_into_pay_page()
        # 弹出连续观看广告弹窗-看广告
        self.driver.watch_advertisement()
        time.sleep(8)
        self.driver.click(self.element.common_page.cancel_login, "关闭插屏广告")
        self.driver.assert_text_equal(
            lang_mgr.ad_continue_retention_dialog_fragment_title(),
            self.driver.get_element_text(self.element.common_page.look_advertisement_pop),
            "断言-正确唤起连续观看广告挽留弹窗"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("26-校验观看广告后，唤起广告解锁动态弹窗（and_immersion_ad_test：3）")
    @allure.description(
        "三次从沉浸页退出——>搜索剧集——>进入视频沉浸页——>进入付费卡点——>弹出连续观看广告弹窗——>观看广告后——>唤起广告解锁动态弹窗")
    @pytest.mark.collection_value(3)
    def test_advertisement_26(self):
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 三次从沉浸页退出
        self.driver.exit_immersion_page_times(3)
        time.sleep(8)
        self.driver.click(self.element.common_page.cancel_login, "关闭插屏广告")
        # 搜索短剧，进入视频沉浸页
        self.driver.into_immersion_page()
        # 滑动进入付费卡点
        self.driver.swipe_into_pay_page()
        self.driver.assert_text_equal(
            lang_mgr.ad_free_drama_dialog_fragment_content(),
            self.driver.get_element_text(self.element.common_page.look_advertisement),
            "断言-正确唤起广告解锁动态弹窗"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("27-校验仅支持金币解锁剧集，不唤起连续观看广告弹窗（and_immersion_ad_test：2）")
    @allure.description(
        "三次从沉浸页退出——>搜索仅支持金币解锁剧集——>进入视频沉浸页——>进入付费卡点——>不唤起连续观看广告弹窗")
    @pytest.mark.collection_value(2)
    def test_advertisement_27(self):
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 三次从沉浸页退出
        self.driver.exit_immersion_page_times(3)
        time.sleep(8)
        self.driver.click(self.element.common_page.cancel_login, "关闭插屏广告")
        # 搜索短剧，进入视频沉浸页
        self.driver.into_coins_immersion_page()
        # 滑动进入付费卡点
        self.driver.swipe_into_pay_page()
        self.driver.assert_element_not_exists(self.element.drama_page.advertisement_unlock,
                                              "断言-不唤起连续观看广告弹窗")
        self.test_status = True
