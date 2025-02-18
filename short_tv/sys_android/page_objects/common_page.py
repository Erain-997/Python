import base64
import logging
import queue
import re
import threading
import time
from io import BytesIO

import allure
import pytest
from PIL import Image
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from common.base.test_base import TestBase
from common.language.lang_mgr import lang_mgr
from common.utils.cmd_tools import adb_shell
from common.utils.decorator import Decorate
from common.utils.device_tools import *
from common.utils.log_utils import Log
from common.utils.report import get_app_version


class CommonPage(TestBase, Decorate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 调用父类构造方法
        self.setup_step_collection = []  # 确保初始化
        self.tear_down_collection = []
        self.case_step_collection = []
        self.check_collection = []

    @Decorate.collect_test("热启动")
    def hot_start(self):
        self.driver.press_keycode(3)
        time.sleep(2)
        adb_shell("am start com.startshorts.androidplayer/.ui.activity.RoutingActivity")
        time.sleep(4)

    @Decorate.collect_test("冷启动")
    def cold_start(self):
        adb_shell("am force-stop com.startshorts.androidplayer")
        time.sleep(2)
        adb_shell(
            "am start -n com.startshorts.androidplayer/.ui.activity.RoutingActivity --es is_auto_test_running true --es disable_home_pop_dialogs true --es disable_campaign_parse true")
        time.sleep(6)

    # 点击弹窗关闭按钮
    def click_close_button(self):
        try:
            self.click(self.element.common_page.close_iv, "有就关闭广告弹窗", 2)
        except:
            pass

    def android_version(self):
        """判断安卓手机型号-关闭首页弹窗"""
        if get_device_version() == AndroidVersion_13:
            self.close_home_advertisement()
        elif get_device_version() == AndroidVersion_14:
            self.close_home_dialogs()
        elif get_device_version() == AndroidVersion_12:
            self.close_home_advertisement_12()
        else:
            self.close_home_advertisement_12()

    @Decorate.collect_setup("关闭首页弹窗-Android14")
    def close_home_dialogs(self):
        """安卓14机型 关闭首页广告（无缓存）"""
        try:
            self.wait_element(self.element.common_page.allow, "点击allow按钮", 4).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        try:
            self.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        for i in range(6):
            time.sleep(1)
            if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                self.press_back_button()
            else:
                break

    @Decorate.collect_setup("关闭首页弹窗-Android13")
    def close_home_advertisement(self):
        """安卓13机型 关闭首页广告（无缓存）"""
        try:
            self.wait_element(self.element.common_page.allow, "点击allow按钮", 4).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        try:
            self.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        for i in range(8):
            time.sleep(1)
            if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                self.press_back_button()
            else:
                break

    @Decorate.collect_setup("关闭首页弹窗-Android12")
    def close_home_advertisement_12(self):
        """安卓12机型 关闭首页广告（无缓存）"""
        try:
            self.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        time.sleep(3)
        for i in range(8):
            time.sleep(1)
            if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                self.press_back_button()
            else:
                break

    @Decorate.collect_test("搜索短剧，进入沉浸页")
    def into_immersion_page(self):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[0]}"]',
            ),
            "进入首页",
        )
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        j = self.language_search()[args.language]
        self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
        time.sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
        time.sleep(3)

    @Decorate.collect_test("搜索仅支持金币解锁短剧，进入沉浸页")
    def into_coins_immersion_page(self):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[0]}"]',
            ),
            "进入首页",
        )
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        j = self.language_coins_search()[args.language]
        self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
        time.sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
        time.sleep(3)

    @Decorate.collect_test("搜索短剧，进入付费卡点")
    def into_pay_page(self):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[0]}"]',
            ),
            "进入首页",
        )
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        j = self.language_search()[args.language]
        self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
        time.sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
        time.sleep(3)
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "查看影集列表")
        self.click(self.element.drama_page.unlock_dramas_04, "进入付费卡点")

    @Decorate.collect_setup("切换新账号")
    def switch_new_account(self):
        # 新包不支持这个了, 自带新用户
        # return
        """切换成新账号"""
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
            ),
            "进入我的模块",
        )
        time.sleep(1)
        try:
            if self.wait_element(self.element.common_page.logo, "等待登录引导出现", 3):
                self.press_back_button()
        except Exception as e:
            Log.logger.error(f"An error：{e}")
        # self.swipe_by_percent(0.3, 0.7, 0.3, 0.4, 300)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[3]}"]',
            ),
            "点击设置",
        )
        self.click(self.element.common_page.switch_new_button, "切换成新账号")
        self.click(self.element.common_page.switch_button, "切换")
        time.sleep(1)
        for i in range(6):
            time.sleep(0.5)
            if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                self.press_back_button()
            else:
                break

    @Decorate.collect_test("订阅周卡Por")
    def subscribe_weekly_method(self):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
            ),
            "进入我的模块",
        )
        try:
            if self.wait_element(self.element.common_page.logo, "等待登录引导出现", 3):
                self.press_back_button()
        except Exception as e:
            Log.logger.error(f"An error：{e}")
        self.click(self.element.common_page.subscribe_now, "进入订阅模块")
        time.sleep(2)
        # 当前语言的订阅商品信息
        subscribe_goods = self.get_subscribe_goods_text()[args.language]
        element = ["xpath", f'//android.widget.TextView[@text="{subscribe_goods["weekly_pro"]}"]']
        for i in range(8):
            try:
                if self.get_element_text(element, 2) == subscribe_goods["weekly_pro"]:
                    self.click(
                        ("xpath", f'//android.widget.TextView[@text="{subscribe_goods["weekly_pro"]}"]'), "订阅周卡Pro"
                    )
                    break
            except TimeoutException:
                self.swipe_by_percent(0.5556, 0.3686, 0.0347, 0.3686, 500)
        self.click(self.element.common_page.cocnfirm_button, "确定订阅")
        # TODO 加一个是否订阅成功, 避免每次都排查是不是后端配置导致订阅失败
        time.sleep(2)
        self.press_back_button("退出订阅模块")

    @Decorate.collect_test("充值金币")
    def recharge_coins(self):
        """充值金币"""
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
            ),
            "进入我的模块",
        )
        try:
            if self.wait_element(self.element.common_page.logo, "等待登录引导出现", 3):
                self.press_back_button()
        except Exception as e:
            Log.logger.error(f"An error：{e}")
        self.click(self.element.common_page.top_up, "进入充值页面")
        self.click(("xpath", f'//android.widget.TextView[@text="{self.get_coins_ui_text()[0]}"]'), "充值金币")
        self.click(self.element.common_page.cocnfirm_button, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "判断取消登录出现")
        except Exception as e:
            logging.error(f"An error：{e}")
        self.click(self.element.common_page.cancel_recharge, "退出充值模块")

    # 提取字符串数字
    def extract_num(self, str):
        numbers = re.findall(r"\d+", str)
        return numbers[0]

    @Decorate.collect_test("退出任务中心,查看bonus记录")
    def out_task_center_bonus_records(self):
        self.click(self.element.common_page.back_subscribe, "退出任务中心")
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
            ),
            "进入我的模块",
        )
        time.sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭原生广告")
        time.sleep(1)
        self.click(self.element.common_page.wallet, "进入我的钱包")
        self.click(self.element.common_page.reward_records, "查看bonus记录")

    @Decorate.collect_test("查看Coin下发记录")
    def get_bonus_record(self):
        self.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.get_wallet_text()[2]}")]'),
            "查看Coin下发记录"
        )

    def get_tab_button(self):
        # 底部导航栏tab元素列表 ['发现', '短剧', '追剧', '我的']
        tab_text = self.get_find_elements(self.element.common_page.my_buttons)
        return tab_text

    def get_my_button_text(self):
        # 我的/元素列表 ['奖励', '反馈', '语言', '设置']
        my_test = self.get_find_elements(self.element.common_page.settings_buttons)
        return my_test

    def get_coins_ui_text(self):
        """获取coins文本"""
        coins_ui_text = self.get_find_elements(self.element.top_up_page.coins_text)
        return coins_ui_text

    def get_bonus_ui_text(self):
        """获取bonus文本"""
        bonus_ui_text = self.get_find_elements(self.element.top_up_page.bonus_text)
        return bonus_ui_text

    def get_wallet_text(self):
        """获取wallet下导航栏文本"""
        wallet_text = self.get_find_elements(self.element.subscribe_page.bonus_records)
        return wallet_text

    def automatic_episode_button(self, index):
        ele = self.wait_element(["xpath",
                                 f'(//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/status_iv"])[{index}]'],
                                "获取自动解锁权限按钮元素")
        # 获取元素的截图
        screenshot_base64 = ele.screenshot_as_base64
        # 将base64字符串转换为PIL图像对象
        image_data = base64.b64decode(screenshot_base64)
        image = Image.open(BytesIO(image_data))
        # 定义开关开启和关闭状态下的颜色阈值
        # 这里的阈值需要根据实际情况进行调整
        green_threshold = (40, 50, 50, 90, 255, 255)
        gray_threshold = (0, 0, 40, 180, 40, 100)
        # 初始化像素计数
        green_pixels = 0
        gray_pixels = 0
        # 遍历图像中的每个像素
        for pixel in image.getdata():
            # 检查像素是否在绿色阈值范围内
            if (
                    green_threshold[0] <= pixel[0] <= green_threshold[3]
                    and green_threshold[1] <= pixel[1] <= green_threshold[4]
                    and green_threshold[2] <= pixel[2] <= green_threshold[5]
            ):
                green_pixels += 1
            # 检查像素是否在灰色阈值范围内
            elif (
                    gray_threshold[0] <= pixel[0] <= gray_threshold[3]
                    and gray_threshold[1] <= pixel[1] <= gray_threshold[4]
                    and gray_threshold[2] <= pixel[2] <= gray_threshold[5]
            ):
                gray_pixels += 1
        # 假设如果绿色像素数量大于灰色像素数量，则认为开关是开启的
        is_switch_on = green_pixels > gray_pixels
        return is_switch_on

    def language_search_shorts(self):
        """“限免”气泡多语言"""
        language_search_shorts = {
            "zh_cn": "AutoTest",  # 简体中文
            "en": "AutoTest",  # 英语
            "zh": "AutoTest",  # 繁体中文
            "fil": "AutoTest",  # 菲律宾
            "ja": "オートテスト",  # 日文
            "ko": "AutoTest",  # 韩文
            "in": "AutoTest",  # 印度尼西亚
            "hi": "ऑटोटेस्ट",  # 印地语
            "th": "AutoTest",  # 泰语
            "ar": "AutoTest",  # 阿拉伯语
            "pt": "AutoTest",  # 葡萄牙语
            "es": "AutoTest",  # 西班牙语
            "vi": "AutoTest",  # 越南语
            "de": "AutoTest",  # 德语
            "fr": "AutoTest",  # 法语
        }
        return language_search_shorts

    def language_coins_search(self):
        """搜索仅支持金币解锁剧集多语言"""
        language_search = {
            "en": "Good Stuff",
            "zh_cn": "好东西",
            "th": "สิ่งดีๆ",
            "zh": "好東西",
            "es": "Buenas cosas",
            "fil": "Mabuting Bagay",
            "ko": "좋은 것",
            "ja": "良いもの",
            "in": "Barang Bagus",
            "hi": "अच्छी चीज",
            "ar": "أشياء جيدة",
            "pt": "Coisa boa",
            "vi": "Đồ tốt",
            "de": "Gute Sachen",
            "fr": "Bonnes choses",
            "ms": "Barang Baik",
            "ru": "Хорошие вещи",
            "it": "Buona roba",
        }
        return language_search

    def language_search(self):
        """搜索剧集多语言"""
        language_search = {
            "en": "AutomationTest",
            "zh_cn": "广告解锁剧集",
            "th": "โฆษณาปลดล็อคตอน",
            "zh": "廣告解鎖劇集",
            "es": "Anuncios Desbloquean Episodios",
            "fil": "Ad Unlock Episode",
            "ko": "광고 해제 드라마",
            "ja": "広告でドラマを解除",
            "in": "Iklan Membuka Episode",
            "hi": "विज्ञापन अनलॉक एपिसोड",
            "ar": "إعلانات تفتح الحلقات",
            "pt": "Episódios desbloqueados por anúncios",
            "vi": "Quảng cáo mở khóa tập phim",
            "de": "Werbung entsperrt Episoden",
            "fr": "Publicité débloque l'épisode",
            "ms": "Ujian Automasi (Jangan Bergerak!!)",
            "ru": "Автоматизированное тестирование (Не трогай!!)",
            "it": "Test automatizzato (Non toccare!!)",
        }
        return language_search

    @Decorate.collect_test("搜索短剧")
    def search_shorts(self):
        self.click(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[0]}"]'),
            "进入首页"
        )
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        j = self.language_search()[args.language]
        self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
        time.sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")

    def get_subscribe_goods_text(self):
        """订阅商品信息"""
        languages = ["zh_cn", "en", "zh", "fil", "ja", "ko", "in", "hi", "th", "ar", "pt", "es", "vi", "de", "fr", "ms",
                     "ru", "it"]

        get_subscribe_goods_text = {
            lang: {
                "weekly": lang_mgr.profile_subscription_view_weekly_card(),
                "monthly": lang_mgr.profile_subscription_view_monthly_card(),
                "annual": lang_mgr.profile_subscription_view_annual_card(),
                "weekly_pro": lang_mgr.profile_subscription_view_weekly_pro_card(),
                "monthly_pro": lang_mgr.profile_subscription_view_monthly_pro_card(),
                "annual_pro": lang_mgr.profile_subscription_view_annual_pro_card(),
            }
            for lang in languages
        }

        return get_subscribe_goods_text

    def assert_element_exists(self, loc, case_name="默认等待", timeout=6):
        try:
            with Decorate.collect_check(case_name):
                return WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*loc))
        except Exception as e:
            self.allure_attach_fail(loc, e, case_name)

    def assert_expect_text_not_equal(self, expect_text, actual_element_text, expect_name):
        try:
            assert expect_text != actual_element_text
            with Decorate.collect_check("断言-" + expect_name):
                allure.attach(
                    name=f"预期:{expect_text} != {actual_element_text} , 实际:{expect_text} != {actual_element_text}",
                    body=f"预期:{expect_text} != {actual_element_text} , 实际:{expect_text} != {actual_element_text}",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            with Decorate.collect_check("断言-" + expect_name + "--校验失败"):
                allure.attach(
                    name=f"预期:{expect_text} != {actual_element_text} , 实际:{expect_text} != {actual_element_text}",
                    body=f"预期:{expect_text} != {actual_element_text} , 实际:{expect_text} != {actual_element_text}",
                    attachment_type=allure.attachment_type.TEXT,
                )
            pytest.fail(str(e))

    # TODO 重新娶个好名字
    def check_retry_button(self, timeout=6):
        loc = self.element.common_page.retry_button
        try:
            if WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*loc)):
                with allure.step("出现重试弹窗, 购买失败"):
                    self.allure_attach_fail(loc, "弹窗出现, 请检查环境", "出现重试弹窗, 购买失败")
        except Exception as e:
            # 功能正常, 继续
            pass

    def deal_retry_button(self, timeout=6):
        loc = self.element.common_page.retry_button
        try:
            if WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*loc)):
                WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*loc)).click()
        except Exception as e:
            # 功能正常, 继续
            pass

    def assert_expect_in_text(self, expect_text, actual_element_text, expect_name):
        try:
            assert expect_text in actual_element_text
            with Decorate.collect_check("断言-" + expect_name):
                allure.attach(
                    name=f"预期包含:{expect_text}, 实际{actual_element_text}包含{expect_text}",
                    body=f"预期包含:{expect_text}, 实际{actual_element_text}包含{expect_text}",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            with Decorate.collect_check("断言-" + expect_name + "--校验失败"):
                allure.attach(
                    name=f"预期包含:{expect_text}, 实际{actual_element_text}不包含{expect_text}",
                    body=f"预期包含:{expect_text}, 实际{actual_element_text}不包含{expect_text}",
                    attachment_type=allure.attachment_type.TEXT,
                )
            raise e

    # @Decorate.collect_test("校验")
    def assert_text_equal(self, expected, actual, expect_name):
        try:
            assert expected == actual
            with Decorate.collect_check(expect_name) as decorator:  # 确保正确使用上下文管理器
                allure.attach(
                    name=f"预期:{expected} 实际:{actual}",
                    body=f"预期:{expected} 实际:{actual}",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            with Decorate.collect_check(expect_name + "--校验失败"):
                allure.attach(
                    name=f"预期:{expected} 实际:{actual}",
                    body=f"预期:{expected} 实际:{actual}",
                    attachment_type=allure.attachment_type.TEXT,
                )
                pytest.fail(str(e))

    def assert_text_not_equal(self, expected, actual, expect_name):
        try:
            assert expected != actual
            with Decorate.collect_check(expect_name) as decorator:  # 确保正确使用上下文管理器
                allure.attach(
                    name=f"之前:{expected} 现在:{actual}",
                    body=f"之前:{expected} 现在:{actual}",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            with Decorate.collect_check(expect_name + "--校验失败"):
                allure.attach(
                    name=f"之前:{expected} 现在:{actual}",
                    body=f"之前:{expected} 现在:{actual}",
                    attachment_type=allure.attachment_type.TEXT,
                )
                pytest.fail(str(e))

    def assert_less_than(self, expected, actual, expect_name):
        try:
            assert expected > actual
            with Decorate.collect_check(expect_name):
                allure.attach(
                    name=f"预期:{expected}<{actual}, 实际{expected}<{actual}",
                    body=f"预期:{expected}<{actual}, 实际{expected}<{actual}",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            with Decorate.collect_check(expect_name + "--校验失败"):
                allure.attach(
                    name=f"预期:{expected}<{actual}, 实际{expected}!<{actual}",
                    body=f"预期:{expected}!<{actual}, 实际{expected}!<{actual}",
                    attachment_type=allure.attachment_type.TEXT,
                )
                pytest.fail(str(e))

    def assert_more_than(self, expected, actual, expect_name):
        try:
            assert expected < actual
            with Decorate.collect_check(expect_name):
                allure.attach(
                    name=f"实际比预期大",
                    body=f"预期:{expected}<实际:{actual}",
                    attachment_type=allure.attachment_type.TEXT,
                )
        except Exception as e:
            with Decorate.collect_check(expect_name + "--校验失败"):
                allure.attach(
                    name=f"实际比预期大",
                    body=f"预期:{expected}!<实际:{actual}",
                    attachment_type=allure.attachment_type.TEXT,
                )
                pytest.fail(str(e))

    def assert_element_not_exists(self, loc, expect_name):
        try:
            WebDriverWait(self.driver, 3).until(lambda d: d.find_element(*loc))
            # 如果找到了元素，记录断言失败信息
            with Decorate.collect_check(expect_name + "--元素存在，断言失败"):
                allure.attach("元素存在，断言失败", name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
            assert False, "元素存在，断言失败"
        except Exception as e:
            # 如果没有找到元素，记录断言成功信息
            with Decorate.collect_check(expect_name + "（校验Ui）"):
                allure.attach("元素不存在，断言成功", name="断言成功信息", attachment_type=allure.attachment_type.TEXT)
            assert True, "元素不存在，断言成功"

    def decide_exist(self, loc, case_name):
        with Decorate.collect_check(case_name):
            if self.wait_element(loc, case_name) is None:
                assert False, "元素不存在，断言失败"
            else:
                assert True, "元素存在，断言成功"

    def get_current_time_tv(self):
        """ 获取当前视频时间进度 """

        def get_element_text(driver, element_id, result_queue):
            """获取指定元素的文本，并将结果放入队列"""
            try:
                text_element = driver.wait_element(element_id, "获取当前时间文本")
                print(f"当前时间文本: {text_element.text}")
                result_queue.put(text_element.text)  # 将结果放入队列
            except Exception as e:
                print(f"获取文本时发生错误: {e}")
                result_queue.put(None)  # 在发生错误时返回 None

        # 元素的 ID
        seekbar_id = ["id", "com.startshorts.androidplayer:id/seekbar_viewstub"]
        current_time_id = ["id", "com.startshorts.androidplayer:id/current_time_tv"]

        # 创建一个队列来存储返回值
        result_queue = queue.Queue()

        # 创建线程
        long_press_thread = threading.Thread(target=self.long_press_element, args=(seekbar_id, 5, "长按进度条"))
        # 下述代码会变成顺序执行, 具体原因未知
        # pos = self.wait_element(seekbar_id).location
        # long_press_thread = threading.Thread(target=self.tap, args=(pos["x"]+100, pos["y"], "轻敲屏幕", 5000))
        get_text_thread = threading.Thread(target=get_element_text, args=(self, current_time_id, result_queue))

        # 启动线程
        long_press_thread.start()
        get_text_thread.start()

        # 等待线程完成
        long_press_thread.join()
        get_text_thread.join()

        # 从队列中获取返回的文本
        text = result_queue.get()  # 获取返回的文本

        return text  # 返回获取到的文本

    def get_speed_tips_tv(self, duration=5):
        """ 获取长按加速倍率 """

        def get_element_text(driver, element_id, result_queue):
            """获取指定元素的文本，并将结果放入队列"""
            try:
                text_element = driver.wait_element(element_id, "获取当前加速倍率文本")
                print(f"获取当前加速倍率文本: {text_element.text}")
                result_queue.put(text_element.text)  # 将结果放入队列
            except Exception as e:
                print(f"获取文本时发生错误: {e}")
                result_queue.put(None)  # 在发生错误时返回 None

        # 元素的 ID
        current_time_id = ["id", "com.startshorts.androidplayer:id/speed_tips_tv"]

        # 创建一个队列来存储返回值
        result_queue = queue.Queue()

        # 创建线程
        long_press_thread = threading.Thread(target=self.long_press_coordinate,
                                             args=(50, 50, duration, "长按屏幕加速"))
        # long_press_thread = threading.Thread(target=self.long_press_coordinate_2, args=(400, 600, "长按屏幕", 5000))
        get_text_thread = threading.Thread(target=get_element_text, args=(self, current_time_id, result_queue))

        # 启动线程
        long_press_thread.start()
        get_text_thread.start()

        # 等待线程完成
        long_press_thread.join()
        get_text_thread.join()

        # 从队列中获取返回的文本
        text = result_queue.get()  # 获取返回的文本

        return text  # 返回获取到的文本

    # @Decorate.collect_check("断言-短剧正片预期有头像/收藏/选集/分享按钮")
    # def check(self):
    #     self.driver.assert_element_exists(self.element.shorts_page.shorts_headshot_stub, "断言-预期第一集存在头像")
    #     self.driver.assert_element_exists(self.element.shorts_page.shorts_headshot_stub, "断言-预期第一集存在头像")
    #     self.driver.assert_element_exists(self.element.shorts_page.new_episodes, "断言-预期第一集存在头像")
    #     self.driver.assert_element_exists(self.element.shorts_page.shorts_headshot_stub, "断言-预期第一集存在头像")


if __name__ == "__main__":
    pass
