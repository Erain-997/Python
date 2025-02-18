import logging
import os
from time import sleep

import allure
from selenium.common import TimeoutException

from common.language.lang_mgr import lang_mgr
from common.mysql.mysql import MySQLClient2
from common.mysql.mysql_tools import mysql_execute_2
from common.utils.arg_parse_func import args
from common.utils.cmd_tools import adb_shell, install_apk
from common.utils.decorator import Decorate
from common.utils.log_utils import Log
from common.utils.report import get_app_version
from sys_android.page_objects.common_page import CommonPage


class SubscribePage(CommonPage):
    client = MySQLClient2()

    @Decorate.collect_test("订阅周卡Pro")
    def subscribe_weekly_pro(self, boolean=True):
        sleep(2)
        # 当前语言的订阅商品信息
        subscribe_goods = self.get_subscribe_goods_text()[args.language]
        element = [
            'xpath',
            f'//android.widget.TextView[@text="{subscribe_goods["weekly_pro"]}"]'
        ]

        swipe_percent = (0.5556, 0.3686, 0.0347, 0.3686) if boolean else (0.6356, 0.24, 0.0347, 0.24)
        for i in range(8):
            if self.wait_element(element, "是否出现周卡订阅按钮"):
                if self.get_element_text(element, 1.5) == subscribe_goods["weekly_pro"]:
                    self.click(
                        ('xpath', f'//android.widget.TextView[@text="{subscribe_goods["weekly_pro"]}"]'),
                        "订阅周卡Pro"
                    )
                    break
            else:
                self.swipe_by_percent(*swipe_percent, 500)

        self.click(self.element.common_page.cocnfirm_button, "确定订阅")

        try:
            self.wait_element(self.element.common_page.cancel_login, "关闭登录弹窗", 8).click()
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    @Decorate.collect_test("数据库修改用户订阅状态")
    def modify_user_status(self):
        user_id = self.get_element_text(self.element.common_page.user_uid)[-6:]
        sql_result = f'UPDATE hi_subscription_user SET end_time = "0", end_time_real = "0" WHERE user_id = (SELECT id FROM hi_user WHERE user_code ={user_id})'

        mysql_execute_2(sql_result, [])
        allure.attach(sql_result, name="SQL", attachment_type=allure.attachment_type.TEXT)

    @Decorate.collect_test("订阅月卡Pro")
    def subscribe_monthly_pro(self, boolean=True):
        sleep(2)
        # 当前语言的订阅商品信息
        subscribe_goods = self.get_subscribe_goods_text()[args.language]
        element = [
            'xpath',
            f'//android.widget.TextView[@text="{subscribe_goods["monthly_pro"]}"]'
        ]

        swipe_percent = (0.5556, 0.3686, 0.0347, 0.3686) if boolean else (0.6356, 0.24, 0.0347, 0.24)
        print(swipe_percent)
        for i in range(8):
            if self.wait_element(element, "是否出现月卡订阅按钮"):
                if self.get_element_text(element, 1.5) == subscribe_goods["monthly_pro"]:
                    self.click(
                        ('xpath',
                         f'//android.widget.TextView[@text="{subscribe_goods["monthly_pro"]}"]'),
                        "订阅月卡Pro"
                    )
                    break
            else:
                self.swipe_by_percent(*swipe_percent, 500, "滑动查找月卡")
        self.click(self.element.common_page.cocnfirm_button, "确定订阅")

    @Decorate.collect_test("订阅年卡Pro")
    def subscribe_annual_pro(self, boolean=True):
        sleep(2)
        # 当前语言的订阅商品信息

        subscribe_goods = self.get_subscribe_goods_text()[args.language]
        element = [
            'xpath',
            f'//android.widget.TextView[@text="{subscribe_goods["annual_pro"]}"]'
        ]

        swipe_percent = (0.5556, 0.3686, 0.0347, 0.3686) if boolean else (0.6356, 0.24, 0.0347, 0.24)
        for i in range(8):
            if self.wait_element(element):
                if self.get_element_text(element, 1.5) == subscribe_goods["annual_pro"]:
                    self.click(
                        ('xpath',
                         f'//android.widget.TextView[@text="{subscribe_goods["annual_pro"]}"]'),
                        "订阅年卡Pro"
                    )
                    break
            else:
                self.swipe_by_percent(*swipe_percent, 500)
        self.click(self.element.common_page.cocnfirm_button, "确定订阅")
        try:
            self.wait_element(self.element.common_page.cancel_login, "关闭登录弹窗", 8).click()
        except Exception as e:
            logging.error(f"An error：{e}")

    @Decorate.collect_test("进入我的模块，查看订阅状态")
    def into_my_list_show_subscribe_status(self):
        sleep(4)
        self.press_back_button("退出视频沉浸页")
        try:
            self.wait_element(self.element.common_page.later, "点击Later按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
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

    @Decorate.collect_test("进入视频沉浸页，播放最后一集")
    def into_video_immersive_play_last_episode(self):
        self.click(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[0]}"]'),
            "进入首页"
        )
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        j = self.language_search()[args.language]
        self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
        sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
        try:
            self.wait_element(self.element.common_page.close_iv, "关闭订阅到期弹窗", 3).click()
        except Exception as e:
            Log.logger.error(f"An error：{e}")
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "查看影集列表")
        self.click(self.element.drama_page.twenty_six_thirty, "点击列表分页26-30")

    @Decorate.collect_test("进入订阅模块")
    def into_subscribe_module(self):
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
        self.click(self.element.common_page.subscribe_now, "进入订阅模块")

    @Decorate.collect_test("进入我的模块的Top Up")
    def into_top_up(self):
        self.click(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]'),
            "进入我的模块"
        )

        top_up = self.get_find_elements(self.element.subscribe_page.top_up)
        self.click(
            ('xpath',
             f'//android.widget.TextView[@text="{lang_mgr.profile_fragment_top_up()}"]'),
            "进入Top Up"
        )

    @Decorate.collect_test("搜索短剧，三次从沉浸页退出")
    def search_shorts_exit_immersive_page_3_times(self):
        self.click(
            ('xpath',
             f'//android.widget.TextView[@text="{self.get_tab_button()[0]}"]'),
            "进入首页"
        )
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        j = self.language_search()[args.language]
        self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
        sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
        self.click(self.element.common_page.cancel_login, "关闭订阅过期提示弹窗")
        sleep(2)
        self.press_back_button("退出视频沉浸页")
        try:
            self.wait_element(self.element.common_page.later, "点击Later按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        for i in range(2):
            self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
            sleep(3)
            self.press_back_button("退出视频沉浸页")
            try:
                self.wait_element(self.element.common_page.later, "点击Later按钮", 3).click()
            except Exception as e:
                logging.error(f"An error：{e}")

    @Decorate.collect_test("等待60秒, 并切换tab")
    def wait_and_switch_tab(self):
        sleep(59)
        self.click(
            ('xpath',
             f'//android.widget.TextView[@text="{self.get_tab_button()[1]}"]'),
            "切换tab"
        )

    @Decorate.collect_test("选择价格跟高订阅商品进行升级")
    def confirm_change_subscribe(self, boolean=True):
        sleep(2)
        # 当前语言的订阅商品信息
        subscribe_goods = self.get_subscribe_goods_text()[args.language]
        element = [
            'xpath',
            f'//android.widget.TextView[@text="{subscribe_goods["monthly_pro"]}"]'
        ]

        swipe_percent = (0.5556, 0.3686, 0.0347, 0.3686) if boolean else (0.6356, 0.24, 0.0347, 0.24)
        print(swipe_percent)
        for i in range(8):
            if self.wait_element(element):
                if self.get_element_text(element, 1.5) == subscribe_goods["monthly_pro"]:
                    self.click(
                        ('xpath',
                         f'//android.widget.TextView[@text="{subscribe_goods["monthly_pro"]}"]'),
                        "订阅月卡Pro"
                    )
                    break
            else:
                self.swipe_by_percent(*swipe_percent, 500, "滑动查找月卡")

    @Decorate.collect_test("订阅降级")
    def subscribe_downgrade(self, boolean=True):
        sleep(2)
        # 当前语言的订阅商品信息
        subscribe_goods = self.get_subscribe_goods_text()[args.language]
        element = [
            'xpath',
            f'//android.widget.TextView[@text="{subscribe_goods["weekly_pro"]}"]'
        ]

        swipe_percent = (0.5556, 0.3686, 0.0347, 0.3686) if boolean else (0.6356, 0.24, 0.0347, 0.24)
        for i in range(8):
            if self.wait_element(element, "是否出现周卡订阅按钮"):
                if self.get_element_text(element, 1.5) == subscribe_goods["weekly_pro"]:
                    self.click(
                        ('xpath', f'//android.widget.TextView[@text="{subscribe_goods["weekly_pro"]}"]'),
                        "订阅周卡Pro"
                    )
                    break
            else:
                self.swipe_by_percent(*swipe_percent, 500, "滑动查找周卡")
        self.click(self.element.common_page.confirm, "确定更改订阅")
        self.click(self.element.common_page.cocnfirm_button, "确定订阅")

    @Decorate.collect_test("订阅相同金额的pro商品")
    def subscribe_same_amount_pro_goods(self, boolean=True):
        sleep(2)
        swipe_percent = (0.5556, 0.3686, 0.0347, 0.3686) if boolean else (0.6356, 0.24, 0.0347, 0.24)
        for i in range(8):
            try:
                if self.wait_element(('id', 'com.startshorts.androidplayer:id/current_price_tv')):
                    self.click(
                        ('id', 'com.startshorts.androidplayer:id/current_price_tv'),
                        "订阅周卡Pro"
                    )
                    break
            except TimeoutException:
                self.swipe_by_percent(*swipe_percent, 500)

        self.click(self.element.common_page.cocnfirm_button, "确定订阅")

        try:
            self.wait_element(self.element.common_page.cancel_login, "关闭登录弹窗", 8).click()
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    @Decorate.collect_test("卸载当前apk，安装v2.0.8")
    def uninstall_and_install_apk(self):
        os.system(f"adb -s {args.device} uninstall com.startshorts.androidplayer")
        sleep(5)
        install_apk("/var/ftp/pub/short_tv_apk/android_QA/2.0.8多语言测试.apk")
        sleep(5)
        adb_shell(
            f"am start com.startshorts.androidplayer/.ui.activity.RoutingActivity --es is_auto_test_running true --es app_language {args.language} --es disable_home_pop_dialogs false --es disable_campaign_parse false")

    @Decorate.collect_test("升级高版本apk，v2.0.10")
    def upgrade_apk(self):
        sleep(5)
        install_apk("/var/ftp/pub/short_tv_apk/android_QA/v2.0.10_支持自动化标识.apk")
        sleep(5)
        adb_shell(
            f"am start com.startshorts.androidplayer/.ui.activity.RoutingActivity --es is_auto_test_running true --es app_language {args.language} --es disable_home_pop_dialogs false --es disable_campaign_parse false")

    @Decorate.collect_check("断言-触发开屏广告（校验UI）")
    def check_open_advertisement(self):
        self.assert_element_exists(self.element.drama_page.advertisement_text, "断言-触发开屏广告（校验UI）")
        sleep(7)
        self.click(self.element.common_page.cancel_login, "关闭插屏广告")
