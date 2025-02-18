import logging
import time
from datetime import datetime

import allure

from common.language.lang_mgr import lang_mgr
from common.utils.arg_parse_func import args
from common.utils.decorator import Decorate
from common.utils.log_utils import Log
from common.utils.report import get_app_version
from sys_android.page_objects.common_page import CommonPage


class DramaPage(CommonPage):

    def top_up_coins_bonus(self, spend=0):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
            ),
            "进入我的模块",
        )
        self.click(self.element.common_page.top_up, "进入充值页面")
        coins_list = self.get_find_elements(self.element.top_up_page.coins_text)
        bonus_one = self.get_element_text(self.element.top_up_page.bonus1)
        bonus_list = self.get_find_elements(self.element.top_up_page.bonus_text)
        bonus_list.insert(0, bonus_one)
        c = [
            int(self.extract_num(coins_list[i])) + int(self.extract_num(bonus_list[i])) for i in range(len(coins_list))
        ]
        min_coin = float("inf")
        a_index = -1
        for i, num in enumerate(c):
            if spend <= num < min_coin:
                min_coin = num
                a_index = i
        coins = self.extract_num(coins_list[a_index])
        bonus = self.extract_num(bonus_list[a_index])
        self.click(self.element.common_page.navigation_back, "退出充值页面")
        return coins, bonus

    @Decorate.collect_test("金币解锁单级")
    def coins_unlock(self):
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "点击选集按钮")
        self.click(self.element.drama_page.four_episodes, "点击第4集")

    @Decorate.collect_test("退出沉浸页，进入我的模块")
    def exit_immersion_page_into_my_module(self):
        self.press_back_button("退出沉浸页")
        try:
            self.wait_element(self.element.common_page.close_iv, "关闭画中画提示弹窗").click()
        except Exception as e:
            Log.logger.error(f"Error closing MySQL connection: {e}")
        time.sleep(5)
        self.press_back_button("退出沉浸页")
        self.click(self.element.common_page.later, "点击Later按钮")
        self.click(self.element.common_page.back, "退出搜索页面")
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
            ),
            "进入我的模块",
        )

    @Decorate.collect_test("批量解锁两集")
    def batch_unlock_two_episodes(self):
        self.click(self.element.top_up_page.one_top_up, "批量解锁两集")
        self.click(self.element.common_page.cocnfirm_button, "点击确认")
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")

    @Decorate.collect_test("批量解锁五集")
    def batch_unlock_five_episodes(self):
        self.click(self.element.top_up_page.two_top_up, "选择解锁5集")
        self.click(self.element.common_page.cocnfirm_button, "确认解锁")
        nowtime = datetime.now().strftime("%m/%d/%Y %I:%M %p")
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        time.sleep(2)

    @Decorate.collect_test("批量解锁全部剧集")
    def batch_unlock_all_episodes(self):
        for i in range(12):
            element = ['xpath',
                       f'//android.widget.TextView[@text="{lang_mgr.unlock_episode_dialog_fragment_coin_store()}"]']
            if self.wait_element(element):
                if self.get_element_text(element,
                                                1.5) == lang_mgr.unlock_episode_dialog_fragment_coin_store():
                    break
            else:
                self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        self.click(self.element.top_up_page.three_top_up, "选择解锁全部剧集选项")
        self.click(self.element.common_page.cocnfirm_button, "点击确认按钮")
        try:
            self.wait_element(self.element.common_page.close_iv, "关闭提示登录弹窗").click()
        except Exception as e:
            logging.error(f"An error：{e}")

    @Decorate.collect_test("批量解锁十集")
    def batch_unlock_ten_episodes(self):
        self.click(self.element.top_up_page.four_top_up, "选择解锁10集选项")
        self.click(self.element.common_page.cocnfirm_button, "点击确认按钮")
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        time.sleep(2)

    @Decorate.collect_test("点击选集按钮")
    def click_fragment(self):
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "点击选集按钮")

    @Decorate.collect_test("进入我的钱包")
    def into_my_wallet(self):
        self.press_back_button()
        time.sleep(2)
        self.press_back_button("退出视频沉浸页")
        self.click(self.element.common_page.later, "点击Later按钮")
        self.click(self.element.common_page.back, "返回首页")
        self.click(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]'),
            "进入我的模块"
        )
        try:
            if self.wait_element(self.element.common_page.logo, "等待登录引导出现", 3):
                self.press_back_button()
        except Exception as e:
            Log.logger.error(f"An error：{e}")
        self.click(self.element.common_page.wallet, "进入我的钱包")

    @Decorate.collect_test("充值金币，并全部消费")
    def top_up_coins(self):
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
        self.click(
            ('xpath',
             f'//android.widget.TextView[@text="{lang_mgr.profile_fragment_top_up()}"]'),
            "进入Top Up"
        )
        coins_list = self.get_find_elements(self.element.top_up_page.coins_text)
        bonus_one = self.get_element_text(self.element.top_up_page.bonus1)
        bonus_list = self.get_find_elements(self.element.top_up_page.bonus_text)
        bonus_list.insert(0, bonus_one)
        c = [
            int(self.extract_num(coins_list[i])) + int(self.extract_num(bonus_list[i])) for i in
            range(len(coins_list))
        ]
        # 使用 min() 函数找到最小值
        min_number = min(c)
        # 使用 index() 方法找到最小值的索引
        min_index = c.index(min_number)
        self.click(
            ("xpath", f'//android.widget.TextView[contains(@text, "{coins_list[min_index]}")]'),
            f"点击充值{coins_list[min_index]}选项",
        )
        self.click(self.element.common_page.cocnfirm_button, "点击确认按钮")
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        self.click(self.element.common_page.navigation_back, "退出充值页面")
        with allure.step("搜索短剧，进入视频沉浸页"):
            self.click(
                ('xpath',
                 f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[0]}"]'),
                "进入首页"
            )
            self.click(self.element.common_page.index_search, "点击首页搜索框")
            for k, j in self.language_search().items():
                if k == args.language:
                    self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
            time.sleep(1)
            time.sleep(2)
            self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
            self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
            time.sleep(3)
        with allure.step("消费完所有金币"):
            for i in range(1, int(min_number / 50) + 4):
                time.sleep(2)
                self.swipe_by_percent(0.28, 0.7, 0.28, 0.1, 400)

    @Decorate.collect_test("搜索短剧，广告解锁剧集并返回首页")
    def automatic_unlock_page_return_to_home(self):
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集")
        time.sleep(8)
        if self.wait_element(self.element.reward_page.cancel_button, "等待广告出现"):
            self.click(self.element.reward_page.cancel_button, "关闭广告")
            time.sleep(3)
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        time.sleep(1)

        self.assert_expect_in_text(
            "4", self.get_element_text(self.element.drama_page.episode_num), "断言-正在播放第四集"
        )
        self.swipe_by_percent(0.28, 0.7, 0.28, 0.1, 400)
        # 校验自动解锁剧集按钮不在
        # self.assert_text_equal(
        #     "False",
        #     self.decide_exist(self.element.automatic_unlock_page.auto_unlock_episode, "查找自动解锁按钮"),
        #     "断言-自动解锁按钮不存在",
        # )
        self.press_back_button("退出付费卡点页面")
        self.click(self.element.common_page.close_iv, "关闭充值挽留提示")
        self.press_back_button("退出沉浸页")
        self.click(self.element.common_page.later, "点击Later按钮")
        time.sleep(8)
        if self.wait_element(self.element.reward_page.cancel_button, "等待广告出现"):
            self.click(self.element.reward_page.cancel_button, "关闭广告")
            time.sleep(2)
        self.click(self.element.common_page.back, "退出搜索页面")

    @Decorate.collect_test("进入我的设置")
    def into_my_setting(self):
        if self.wait_element(self.element.common_page.logo, "等待首页logo出现") is None:
            self.press_back_button()
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
            ),
            "进入我的页面",
        )
        try:
            if self.wait_element(self.element.common_page.logo, "等待登录引导出现", 3):
                self.press_back_button()
        except Exception as e:
            Log.logger.error(f"An error：{e}")
        time.sleep(1)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[3]}"]',
            ),
            "点击设置",
        )

    @Decorate.collect_test("进入影集详情,点击第4集")
    def check_auto_unlock_button_exist(self):
        time.sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索图标")
        time.sleep(1)
        self.click(self.element.drama_page.video_detail, "进入影集详情")
        time.sleep(1)
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "点击选集按钮")
        self.click(self.element.drama_page.four_episodes, "点击第4集")

    @Decorate.collect_test("金币解锁剧集并返回首页")
    def coin_unlock_page_return_to_home(self):
        self.click(self.element.top_up_page.one_top_up, "充值金币解锁剧集")
        self.click(self.element.common_page.cocnfirm_button, "点击确认按钮")
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        time.sleep(1)

        self.assert_expect_in_text(
            "4", self.get_element_text(self.element.drama_page.episode_num), "正在播放第四集"
        )
        self.press_back_button("退出沉浸页")
        try:
            self.click(self.element.common_page.later, "点击Later按钮")
        except Exception as e:
            pass
        self.click(self.element.common_page.back, "退出搜索页面")

    @Decorate.collect_test("充值挽留解锁剧集并返回首页")
    def charge_unlock_page_return_to_home(self):
        time.sleep(3)
        self.press_back_button("退出充值页面")

        self.click(self.element.automatic_unlock_page.purchase_button, "点击充值挽留按钮")
        self.click(self.element.common_page.cocnfirm_button, "点击确定按钮")
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        time.sleep(3)
        self.press_back_button("退出沉浸页")
        self.click(self.element.common_page.later, "点击Later按钮")
        self.click(self.element.common_page.back, "退出搜索页面")

    @Decorate.collect_test("广告解锁剧集并返回首页")
    def advertisement_unlock_page_return_to_home(self):
        time.sleep(1)
        self.click(self.element.automatic_unlock_page.auto_unlock_episode, "点击自动解锁剧集按钮")
        time.sleep(1)
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集")
        time.sleep(8)
        if self.wait_element(self.element.reward_page.cancel_button, "等待广告出现"):
            self.click(self.element.reward_page.cancel_button, "关闭广告")
            time.sleep(3)
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        time.sleep(1)

        self.assert_expect_in_text(
            "4", self.get_element_text(self.element.drama_page.episode_num), "正在播放第四集"
        )
        self.swipe_by_percent(0.28, 0.7, 0.28, 0.1, 400)

        self.press_back_button("退出付费卡点页面")
        self.click(self.element.common_page.close_iv, "关闭充值挽留提示")
        self.press_back_button("退出沉浸页")
        self.click(self.element.common_page.later, "点击Later按钮")
        time.sleep(8)
        if self.wait_element(self.element.reward_page.cancel_button, "等待广告出现"):
            self.click(self.element.reward_page.cancel_button, "关闭广告")
            time.sleep(2)
        self.click(self.element.common_page.back, "退出搜索页面")

    @Decorate.collect_test("进入Coins Store，广告解锁剧集并返回首页")
    def into_coin_store_advertisement_unlock(self):

        time.sleep(3)
        self.click(self.element.automatic_unlock_page.coins_store, "点击【Coins Store】")

        time.sleep(1)
        self.click(self.element.automatic_unlock_page.auto_unlock_episode, "点击自动解锁剧集按钮")
        time.sleep(2)
        self.click(self.element.automatic_unlock_page.free_unlock, "广告解锁剧集")
        time.sleep(8)
        if self.wait_element(self.element.reward_page.cancel_button, "等待广告出现"):
            self.click(self.element.reward_page.cancel_button, "关闭广告")
            time.sleep(3)
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        time.sleep(1)

        self.assert_expect_in_text(
            "4", self.get_element_text(self.element.drama_page.episode_num), "正在播放第四集"
        )
        self.swipe_by_percent(0.28, 0.7, 0.28, 0.1, 400)

        self.press_back_button("退出付费卡点页面")
        self.click(self.element.common_page.close_iv, "关闭充值挽留提示")
        self.press_back_button("退出沉浸页")
        self.click(self.element.common_page.later, "点击Later按钮")
        time.sleep(8)
        if self.wait_element(self.element.reward_page.cancel_button, "等待广告出现"):
            self.click(self.element.reward_page.cancel_button, "关闭广告")
            time.sleep(2)
        self.click(self.element.common_page.back, "退出搜索页面")

    @Decorate.collect_test("进入设置，打开自动解锁权限")
    def open_auto_unlock_permission(self):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
            ),
            "进入我的页面",
        )
        time.sleep(3)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[3]}"]',
            ),
            "点击设置",
        )
        self.click(self.element.automatic_unlock_page.auto_unlock_switch, "开启自动解锁权限")
        self.click(self.element.common_page.navigation_back, "退出设置页面")

    @Decorate.collect_test("进入付费卡点，进入Coins Store")
    def into_coin_store(self):
        time.sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索图标")
        time.sleep(1)
        self.click(self.element.drama_page.video_detail, "进入影集详情")
        time.sleep(1)
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "点击选集按钮")
        time.sleep(1)
        self.click(self.element.drama_page.four_episodes, "点击第4集")
        time.sleep(3)
        self.click(self.element.automatic_unlock_page.coins_store, "点击【Coins Store】")
        # self.assert_text_equal(
        #     "False",
        #     self.decide_exist(self.element.automatic_unlock_page.auto_unlock_episode, "查找自动解锁按钮"),
        #     "断言-自动解锁按钮不存在",
        # )
        self.click(self.element.automatic_unlock_page.free_unlock, "广告解锁剧集")
        time.sleep(8)
        if self.wait_element(self.element.reward_page.cancel_button, "等待广告出现"):
            self.click(self.element.reward_page.cancel_button, "关闭广告")
            time.sleep(3)
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        self.assert_expect_in_text(
            "4", self.get_element_text(self.element.drama_page.episode_num), "正在播放第四集"
        )
        time.sleep(1)
        self.swipe_by_percent(0.28, 0.7, 0.28, 0.1, 400)
        time.sleep(1)

    @Decorate.collect_test("进入设置，打开自动解锁权限")
    def open_auto_unlock_permission(self):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
            ),
            "进入我的页面",
        )
        time.sleep(3)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[3]}"]',
            ),
            "点击设置",
        )
        self.click(self.element.automatic_unlock_page.auto_unlock_switch, "开启自动解锁权限")
        self.click(self.element.common_page.navigation_back, "退出设置页面")
        time.sleep(1)

    @Decorate.collect_test("搜索短剧，进入付费卡点并退出")
    def search_shorts_into_automatic_unlock(self):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[0]}"]',
            ),
            "进入首页",
        )
        time.sleep(1)
        self.search_shorts()
        time.sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索图标")
        time.sleep(1)
        self.click(self.element.drama_page.video_detail, "进入影集详情")
        time.sleep(1)
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "点击选集按钮")
        time.sleep(1)
        self.click(self.element.drama_page.four_episodes, "点击第4集")
        time.sleep(3)
        self.press_back_button("退出付费卡点页面")
        try:
            self.click(self.element.common_page.cancel_login, "关闭充值挽留弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
