import logging
import time
from time import sleep

from common.language.lang_mgr import lang_mgr
from common.utils.cmd_tools import *
from common.utils.decorator import Decorate
from common.utils.device_tools import *
from common.utils.report import get_app_version
from sys_android.page_objects.common_page import CommonPage


class AdvertisementPage(CommonPage):

    @Decorate.collect_test("退出视频沉浸页")
    def out_immersion_page(self):
        self.press_back_button("退出视频沉浸页")
        self.click(self.element.common_page.later, "点击Later按钮")

    def exit_immersion_page_times(self, num):
        with Decorate.collect_test(f"{num}次从沉浸页进入退出"):
            for i in range(num):
                self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
                precise_sleep(4)
                self.press_back_button("退出视频沉浸页")
                self.click(self.element.common_page.later, "点击Later按钮")

    @Decorate.collect_check("断言-从沉浸页退出，触发插屏广告（校验UI）")
    def check_trigger_advertisement(self):
        sleep(6)
        self.assert_element_exists(self.element.drama_page.advertisement_text,
                                   "断言-从沉浸页退出，触发插屏广告（校验UI）")
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")

    @Decorate.collect_test("返回首页,进入任务中心")
    def into_task_center(self):
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
        self.click(self.element.reward_page.reward_button, "进入任务中心")

    @Decorate.collect_test("关闭Watch Now")
    def close_watch_now(self):
        if self.wait_element(self.element.reward_page.cancel_button, "等待Watch Now按钮出现", 3):
            self.click(self.element.reward_page.cancel_button, "关闭Watch Now")

    @Decorate.collect_test("观看Watch Now")
    def watch_watch_now(self):
        self.click(self.element.reward_page.watch_now_button, "点击watch Now")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(3)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 300)

    @Decorate.collect_test("观看激励视频")
    def watch_reward_video(self):
        sleep(1)
        self.click(self.element.advertisement_page.watch_reward_video_1, "观看第一次激励视频")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭激励视频")

    @Decorate.collect_test("搜索短剧，进入付费卡点")
    def search_shorts_into_pay_card(self):
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        for k, j in self.language_search().items():
            if k == args.language:
                self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
        sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "查看影集列表")
        self.click(self.element.drama_page.unlock_dramas_04, "进入付费卡点")
        # precise_sleep(4)
        # self.press_back_button()
        # if self.wait_element(self.element.advertisement_page.close_discount, "判断登录页面出现").text is not None:
        #     self.press_back_button()
        # precise_sleep(4)

    @Decorate.collect_test("付费卡点界面关闭弹窗")
    def pay_card_close_popup_window(self):
        precise_sleep(4)
        self.press_back_button()
        if self.wait_element(self.element.advertisement_page.close_discount, "判断登录页面出现").text is not None:
            self.press_back_button()
        precise_sleep(4)

    @Decorate.collect_test("从付费卡点返回首页")
    def pay_card_back_to_home(self):
        self.press_back_button("返回首页")

        self.click(self.element.common_page.later, "点击Later按钮")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        self.press_back_button()

    @Decorate.collect_test("等待60秒,切换tab到短剧")
    def wait_60_seconds_switch_tab(self):
        sleep(59)
        # self.click(self.element.common_page.my_button, "切换我的模块")

        self.click(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[1]}"]'),
            "切换tab到短剧"
        )

    @Decorate.collect_test("返回首页,切换tab到短剧")
    def back_to_home_switch_tab(self):
        self.click(self.element.common_page.back, "返回首页")

        self.click(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[1]}"]'),
            "切换tab到短剧"
        )

    @Decorate.collect_test("连续解锁2次剧（广告解锁）")
    def unlock_advertisement(self):
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(2)
        self.press_back_button("关闭登录弹窗")
        sleep(2)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(2)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(2)

    @Decorate.collect_test("首页点击右上角礼包")
    def gift_package(self):
        self.click(self.element.advertisement_page.gift_button, "点击右上角礼包")
        sleep(2)

    @Decorate.collect_test("右上角礼包关闭插屏广告,关闭Watch Now")
    def gift_package_close_advertisement_and_watch_now(self):
        self.click(self.element.advertisement_page.gift_button, "点击右上角礼包")

        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(2)
        # try:
        #     self.wait_element(self.element.reward_page.cancel_button, "关闭Watch Now", 4).click()
        # except Exception as e:
        #     logging.error(f"An error：{e}")

        if self.wait_element(self.element.reward_page.cancel_button, "是否出现Watch Now", 4):
            self.click(self.element.reward_page.cancel_button, "关闭Watch Now", 4)

    # 原需求看6个, 实际看3次就看完了
    @Decorate.collect_test("观看【看广告，赢奖励】3个广告")
    def advertisement_lock(self):
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.07, 500)
        sleep(1)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.07, 500)
        test = self.get_find_elements(
            ('xpath', '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/watch_button"]'))

        print(
            '---------------------',
            test
        )
        for i in range(len(test)):
            self.click(self.element.advertisement_page.watch_reward_video_1, f"观看第{i}次激励视频")
            sleep(12)
            self.click(self.element.common_page.cancel_login, "关闭激励视频")
        sleep(2)
        self.swipe_by_percent(0.28, 0.3, 0.28, 0.7, 400)
        sleep(1)
        self.swipe_by_percent(0.28, 0.3, 0.28, 0.73, 400)
        sleep(2)

    @Decorate.collect_test("观看双倍奖励视频")
    def watch_double_reward_video(self):
        self.click(self.element.reward_page.double_reward_button, "观看双倍奖励视频")
        time.sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭原生广告")
        time.sleep(2)

    @Decorate.collect_test("观看广告解锁")
    def unlock_common(self):
        self.android_version()
        self.switch_new_account()

        with allure.step("搜索短剧，进入付费卡点"):
            self.click(self.element.common_page.index_search, "点击首页搜索框")
            for k, j in self.language_search().items():
                if k == args.language:
                    self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
            sleep(2)
            self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
            self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
            self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                       "查看影集列表")
            self.click(self.element.drama_page.unlock_dramas_04, "进入付费卡点")

    @Decorate.collect_test("广告解锁剧集")
    def advertisement_unlock_drama(self):
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集")

        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        if self.wait_element(self.element.drama_page.close_login, "判断登录弹窗出现", 3):
            self.click(self.element.drama_page.close_login, "关闭登录弹窗出现")

    @Decorate.collect_check("断言-轻敲屏幕,断言视频进度条文本")
    def check_progress_bar_text(self):
        text = self.get_current_time_tv()
        self.assert_text_not_equal("00:01", text, "断言-视频进度条文本")

    @Decorate.collect_test("下滑至下一集")
    def next_page(self):
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(2)

    @Decorate.collect_test("切换剧集并进入沉浸页")
    def return_to_pay_page(self):
        self.press_back_button("退出视频沉浸页")
        self.click(self.element.common_page.later, "点击Later按钮")
        sleep(6)
        self.wait_element(self.element.common_page.cancel_login, "关闭插屏广告").click()
        self.click(self.element.common_page.clear_search_box, "清空搜索内容")
        j = self.language_search_shorts()[args.language]
        self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
        time.sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "查看影集列表")
        self.click(self.element.drama_page.unlock_dramas_04, "进入付费卡点")

    @Decorate.collect_test("解锁第五集")
    def unlock_dramas_05(self):
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "查看影集列表")
        self.click(self.element.drama_page.unlock_dramas_05, "解锁第五集")

    @Decorate.collect_check("断言-付费卡点显示正常广告解锁入口（校验UI）")
    def check_advertisement_page_unlock(self):
        self.assert_element_exists(self.element.drama_page.desc_tv,
                                   "断言-付费卡点显示正常广告解锁入口（校验UI）")

        self.click(self.element.drama_page.coin_store, "点击【Conis Store】")
        sleep(2)

    @Decorate.collect_test("滑动进入付费卡点")
    def swipe_into_pay_page(self):
        for i in range(3):
            time.sleep(2)
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)

    @Decorate.collect_test("看广告")
    def watch_advertisement(self):
        self.click(self.element.drama_page.advertisement_unlock)

    @Decorate.collect_test("广告解锁剧集（第4-11集）")
    def advertisement_unlock_4_to_11(self):
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集-第4集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(2)
        self.press_back_button("关闭登录弹窗")
        sleep(2)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(1)
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集-第5集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(4)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(6)
        try:
            self.wait_element(self.element.common_page.cancel_login, "关闭插屏广告", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集-第6集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(1)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(1)
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集-第7集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(1)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(6)
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集-第8集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(2)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集-第9集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(1)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集-第10集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(1)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(6)
        self.click(self.element.drama_page.advertisement_unlock, "广告解锁剧集-第11集")
        sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
        sleep(1)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(2)

    def get_current_gold(self):
        """获取当前金币数量"""
        gold_text = self.assert_element_exists(self.element.reward_page.double_reward_expect, "获取奖励币数量").text
        try:
            gold_amount = int(gold_text)
        except ValueError:
            print(f"无法将文本 '{gold_text}' 转换为整数")
            gold_amount = None  # 或者你可以选择返回一个默认值，比如 0
        return gold_amount

    def get_bonus(self):
        a = int(self.assert_element_exists(self.element.advertisement_page.a, "+25").text)
        b = int(self.assert_element_exists(self.element.advertisement_page.b, "+10").text)
        c = int(self.assert_element_exists(self.element.advertisement_page.c, "+25").text)
        d = int(self.assert_element_exists(self.element.advertisement_page.d, "+25").text)
        e = int(self.assert_element_exists(self.element.advertisement_page.e, "+25").text)
        f = int(self.assert_element_exists(self.element.advertisement_page.f, "+25").text)
        g = int(self.assert_element_exists(self.element.advertisement_page.g, "+25").text)
        sum_bonus = a + b + c + d + e + f + g
        return sum_bonus

    def advertisement_module_expect_3(self):
        return self.assert_element_exists(self.element.common_page.automation_test_text,
                                          "断言-不触发开屏广告（校验UI）").text

    def advertisement_module_expect_7(self):
        return self.assert_element_exists(self.element.common_page.watch_ads_text, "断言-不触发开屏广告（校验UI）").text

    def advertisement_module_expect_13(self):
        return self.assert_element_exists(self.element.reward_page.double_reward_expect, "断言-奖励币翻倍正确", 10).text

    def advertisement_module_expects_13(self):
        self.click(self.element.common_page.back_subscribe, "退出任务中心")
        self.click(self.element.common_page.wallet, "进入我的钱包")
        self.click(self.element.common_page.reward_records, "查看bonus记录")
