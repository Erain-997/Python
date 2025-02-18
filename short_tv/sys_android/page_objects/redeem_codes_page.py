import logging
import time

import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

from common.language.lang_mgr import lang_mgr
from common.utils.arg_parse_func import args
from common.utils.decorator import Decorate
from common.utils.log_utils import Log
from sys_android.page_objects.common_page import CommonPage


class RedeemCodesPage(CommonPage):
    @Decorate.collect_test("搜索兑换码: tvq8lgcby9")
    def search_redeem_code1(self):
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        self.wait_element(self.element.common_page.search, "输入兑换码：tvq8lgcby9").send_keys("tvq8lgcby9")
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        if self.wait_element(self.element.common_page.close_iv, "等待兑换码弹窗出现", 3):
            self.click(self.element.common_page.close_iv, "关闭兑换码弹窗")

    @Decorate.collect_test("退出沉浸页")
    def out_of_immersion_code(self):
        self.press_back_button()
        self.click(self.element.common_page.later, "点击Later按钮")

    @Decorate.collect_check("断言-搜索历史记录不显示兑换码")
    def check_in_immersion_code(self):
        self.click(self.element.common_page.back, "退出搜索界面")
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        try:
            self.driver.find_element(AppiumBy.ID, 'com.startshorts.androidplayer:id/history_clear_iv')
            # 如果找到了元素，记录断言失败信息
            allure.attach("元素存在，断言失败", name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
            assert False, "元素存在，断言失败"
        except NoSuchElementException:
            # 如果没有找到元素，记录断言成功信息
            allure.attach("元素不存在，断言成功", name="断言成功信息", attachment_type=allure.attachment_type.TEXT)
            assert True, "元素不存在，断言成功"

    @Decorate.collect_test("查看Coin下发记录")
    def coin_records(self):
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
        self.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.get_wallet_text()[2]}")]'),
            "查看Coin下发记录"
        )

    @Decorate.collect_test("查看Bonus下发记录")
    def bonus_records(self):
        self.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.get_wallet_text()[3]}")]'),
            "查看Bonus下发记录"
        )

    @Decorate.collect_test("退出钱包模块")
    def exit_wallet_module(self):
        self.click(self.element.common_page.navigation_back, "退出钱包模块")

    @Decorate.collect_test("进入Mylist")
    def into_mylist(self):
        self.click(self.element.redeem_codes_page.red_point, "进入Mylist")

    @Decorate.collect_test("搜索兑换码: tvbxq4jy")
    def search_redeem_code2(self):
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        self.wait_element(self.element.common_page.search, "输入兑换码：tvbxq4jy").send_keys("tvbxq4jy")
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.assert_text_equal(
            lang_mgr.search_activity_redeem_code_disabled(),
            self.get_element_text((
                'xpath',
                f'//android.widget.Toast[@text="{lang_mgr.search_activity_redeem_code_disabled()}"]'
            )),
            f"当前语言：{args.language}，断言-toast提示【兑换码不存在】"
        )

    @Decorate.collect_check("断言-不触发弹窗")
    def check_no_popup_window(self):
        try:
            self.driver.find_element(AppiumBy.ID, 'com.startshorts.androidplayer:id/close_iv')
            # 如果找到了元素，记录断言失败信息
            allure.attach("元素存在，断言失败", name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
            assert False, "元素存在，断言失败"
        except NoSuchElementException:
            # 如果没有找到元素，记录断言成功信息
            allure.attach("元素不存在，断言成功", name="断言成功信息", attachment_type=allure.attachment_type.TEXT)
            assert True, "元素不存在，断言成功"

    @Decorate.collect_test("搜索兑换码: tvzpneu73")
    def search_redeem_code3(self):
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        self.wait_element(self.element.common_page.search, "输入兑换码：tvzpneu73").send_keys("tvzpneu73")
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")

    @Decorate.collect_test("搜索兑换码: tvl5fb")
    def search_redeem_code4(self):
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        self.wait_element(self.element.common_page.search, "输入兑换码：tvl5fb").send_keys("tvl5fb")
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")

    @Decorate.collect_test("搜索兑换码: vl5fb")
    def search_redeem_code5(self):
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        self.wait_element(self.element.common_page.search, "输入兑换码：vl5fb").send_keys("vl5fb")
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")

    @Decorate.collect_test("进入首页搜索框")
    def into_search_box(self):
        self.click(self.element.common_page.back, "返回首页")
        self.click(self.element.common_page.index_search, "进入首页搜索框")

    @Decorate.collect_test("搜索兑换码: tvq8lgcby9")
    def search_redeem_code6(self):
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        self.wait_element(self.element.common_page.search, "输入兑换码：tvq8lgcby9").send_keys("tvq8lgcby9")
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        if self.wait_element(self.element.common_page.close_iv, "等待权益弹窗出现", 3):
            self.click(self.element.common_page.close_iv, "关闭权益弹窗")

    @Decorate.collect_test("重新搜索兑换码")
    def research_redeem_code(self):
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.assert_element_exists(self.element.redeem_codes_page.received, "校验权益弹窗Ui")
        if self.wait_element(self.element.common_page.close_iv, "等待权益弹窗出现", 3):
            self.click(self.element.common_page.close_iv, "关闭权益弹窗")

    @Decorate.collect_test("返回首页")
    def back_to_home(self):
        self.press_back_button()
        self.click(self.element.common_page.later, "点击Later按钮")

    @Decorate.collect_check("断言-搜索历史记录不显示兑换码")
    def check_search_history_not_show_redeem_code(self):
        self.click(self.element.common_page.back, "退出搜索界面")
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        try:
            self.driver.find_element(AppiumBy.ID, 'com.startshorts.androidplayer:id/history_clear_iv')
            # 如果找到了元素，记录断言失败信息
            allure.attach("元素存在，断言失败", name="断言失败信息", attachment_type=allure.attachment_type.TEXT)
            assert False, "元素存在，断言失败"
        except NoSuchElementException:
            # 如果没有找到元素，记录断言成功信息
            allure.attach("元素不存在，断言成功", name="断言成功信息", attachment_type=allure.attachment_type.TEXT)
            assert True, "元素不存在，断言成功"
        self.click(self.element.common_page.back, "返回首页")

    @Decorate.collect_test("搜索五次兑换码")
    def search_redeem_code_5_times(self):
        code_data = ['tvq8lgcby9', 'tvjt4sb', 'tvggtt', 'tvbc1eo', 'tvhlq7c']
        self.click(self.element.common_page.index_search, "点击首页搜索框")
        for code in code_data[0:3]:
            with allure.step(f"输入兑换码：{code}"):
                self.wait_element(self.element.common_page.search, f"输入兑换码：{code}").send_keys(code)
                self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
                try:
                    self.wait_element(self.element.redeem_codes_page.received, "点击已领取").click()
                except Exception as e:
                    logging.error(f"An error: {e}")
                time.sleep(1.5)
                self.press_back_button("退出视频沉浸页")
                try:
                    self.wait_element(self.element.common_page.later, "点击Later按钮").click()
                except Exception as e:
                    logging.error(f"An error: {e}")
        time.sleep(7)
        try:
            self.wait_element(self.element.common_page.cancel_login, "关闭插屏广告", 3).click()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.click(self.element.common_page.clear_search_box, "清空搜索内容")
        for code in code_data[3:5]:
            with allure.step(f"输入兑换码：{code}"):
                self.wait_element(self.element.common_page.search, f"输入兑换码：{code}").send_keys(code)
                self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
                try:
                    self.wait_element(self.element.redeem_codes_page.received, "点击已领取").click()
                except Exception as e:
                    logging.error(f"An error: {e}")
                time.sleep(1.5)
                self.press_back_button("退出视频沉浸页")
                try:
                    self.click(self.element.common_page.later, "点击Later按钮")
                except Exception as e:
                    logging.error(f"An error: {e}")

    @Decorate.collect_test("再次搜索兑换码")
    def search_redeem_code_again(self):
        code = 'tvooo111'
        self.click(self.element.common_page.clear_search_box, "清空搜索内容")
        self.wait_element(self.element.common_page.search, f"输入兑换码：{code}").send_keys(code)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
