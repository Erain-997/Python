import logging

from common.language.lang_mgr import lang_mgr
from common.utils.cmd_tools import *
from common.utils.decorator import Decorate
from common.utils.report import get_app_version
from sys_android.page_objects.common_page import CommonPage
from sys_android.test_cases.new.test_get_yaml import *


class TopUpPage(CommonPage):
    handler = TopUpDataHandler()

    @Decorate.collect_test("进入充值页面")
    def into_top_up_page(self):
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
        self.click(self.element.common_page.top_up, "进入充值页面")
        TopUpPage.handler.refresh_data()

    @Decorate.collect_test("遍历充值充值页面金币")
    def top_up_all_coins(self, coins_language):
        with allure.step(f"当前国家为：{lang_mgr.app_language_code}"):
            if self.wait_element(self.element.common_page.title, "等待充值页面加载", 6) is not None:
                self.swipe_by_percent(0.28, 0.33, 0.28, 0.1, 600)
            coins_ui_text = self.get_coins_ui_text()
            # 将列表转换为字符串
            coins_data_str = "\n".join(coins_ui_text)
            allure.attach(coins_data_str, name="当前国家充值金额", attachment_type=allure.attachment_type.TEXT)
        with allure.step("遍历充值所有金币"):
            top_up_coins1 = coins_ui_text[0].replace(f' {coins_language}', "")
            self.click(
                ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[0]}"]'),
                f"充值{top_up_coins1}"
            )
            self.click(self.element.common_page.cocnfirm_button, "确认支付")
            self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
            time.sleep(1)
            for coins in coins_ui_text[1:5]:
                coin_value = coins.replace(f' {coins_language}', "")
                self.click(
                    ('xpath',
                     f'//android.widget.TextView[@text="{coins}"]'),
                    f"充值{coin_value}"
                )
                self.click(self.element.common_page.cocnfirm_button, "确认支付")
            time.sleep(2)
            self.swipe_by_percent(0.28, 0.33, 0.28, 0.1, 300)
            top_up_coins6 = coins_ui_text[5].replace(f' {coins_language}', "")
            self.click(
                ('xpath', f'//android.widget.TextView[@text="{coins_ui_text[5]}"]'),
                f"充值{top_up_coins6}"
            )
            self.click(self.element.common_page.cocnfirm_button, "确认支付")
            time.sleep(2)
            self.swipe_by_percent(0.28, 0.33, 0.28, 0.1, 300)
            top_up_coins7 = coins_ui_text[6].replace(f' {coins_language}', "")
            self.click(
                ('xpath', f'//android.widget.TextView[@text="{coins_ui_text[6]}"]'),
                f"充值{top_up_coins7}"
            )
            self.click(self.element.common_page.cocnfirm_button, "确认支付")
            time.sleep(1)

    @Decorate.collect_test("进入我的钱包-查看Coin/Bonus下发记录")
    def into_wallet_page(self):
        self.click(self.element.common_page.navigation_back, "退出充值页面")
        self.click(self.element.common_page.wallet, "进入我的钱包")


    def expect_coins_record(self, coins_language):
        with allure.step("断言-【Coin Record】充值记录下发正确"):
            self.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.get_wallet_text()[2]}")]'),
                "查看Coin下发记录"
            )
            for item in TopUpPage.handler.coins_data:
                try:
                    self.assert_text_equal(
                        # 接口返回值：预期结果
                        str(item),
                        self.get_element_text(
                            [
                                "xpath",
                                f'//android.widget.TextView[@text="{item.replace(f' {coins_language}', "")}"]',
                            ]
                        ),
                        f"{item}",
                    )
                except AssertionError as e:
                    Log.logger.error(f"Assertion failed for {item}: {e}")
                except Exception as e:
                    Log.logger.error(f"An error occurred while checking {item}: {e}")

    def expect_bonus_record(self):
        self.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.get_wallet_text()[3]}")]'),
            "查看Bonus下发记录"
        )
        with allure.step("断言-【Bonus】记录下发正确"):
            # 倒序处理 bonus_data 列表
            bonus_data_reversed = TopUpPage.handler.bonus_data[::-1]
            for item in bonus_data_reversed:
                if item == "+0":  # 如果 item 是 0，则跳过
                    continue
                try:
                    self.assert_text_equal(
                        # 接口返回值：预期结果
                        str(item),
                        self.get_element_text(
                            [
                                "xpath",
                                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/amount_tv" and @text="{item}"]'
                                # f'//android.widget.TextView[@text="{bonus_ui_text[item].replace(" Bonus", "")}"]',
                            ]
                        ),
                        f"{item}",
                    )
                except AssertionError as e:
                    Log.logger.error(f"Assertion failed for {item} : {e}")
                except Exception as e:
                    Log.logger.error(f"An error occurred while checking {item} : {e}")

    def expect_sum_coins(self):
        self.click(self.element.common_page.navigation_back, "退出消费记录页面")
        int_coins_data = [int(value.replace('+', '').strip()) for value in TopUpPage.handler.coins_data]
        # 计算总和
        total_coins = sum(int_coins_data)
        return total_coins

    def expect_sku(self):
        sku = TopUpPage.handler.top_up_sku_coins[0][0]
        coins_language = self.get_coins_ui_text()[0]
        self.assert_text_equal(coins_language, self.get_element_text([
            "xpath", f'//android.widget.TextView[contains(@text, "{sku}")]'
        ]), "断言-付费卡点页面展示膨胀sku")

    @Decorate.collect_test("进入金币商城")
    def into_coins_store(self):
        self.click(self.element.drama_page.coin_store, "进入金币商城")

    @Decorate.collect_test("进入我的钱包")
    def into_my_wallet(self):
        time.sleep(1)
        self.press_back_button()
        self.click(self.element.common_page.later, "点击Later")
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

    @Decorate.collect_test("购买A1位置sku商品")
    def buy_sku_a1(self):
        top_up_coins1 = [item.split()[0] for item in self.get_coins_ui_text()][0]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[0]}"]'),
            f"购买A1位置sku商品:{top_up_coins1}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")

    @Decorate.collect_test("购买B1位置sku商品")
    def buy_sku_b1(self):
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][1]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[1]}"]'),
            f"购买B1位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")

    @Decorate.collect_test("购买B2位置sku商品")
    def buy_sku_b2(self):
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][2]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[2]}"]'),
            f"购买B2位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")

    @Decorate.collect_test("购买B3位置sku商品")
    def buy_sku_b3(self):
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][3]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[3]}"]'),
            f"购买B3位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")

    @Decorate.collect_test("购买B4位置sku商品")
    def buy_sku_b4(self):
        time.sleep(1.5)
        self.swipe_by_percent(0.7, 0.8, 0.1, 0.8, 300)
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][2]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[2]}"]'),
            f"购买B4位置sku商品::{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("购买B5位置sku商品")
    def buy_sku_b5(self):
        time.sleep(1.5)
        self.swipe_by_percent(0.7, 0.8, 0.1, 0.8, 300)
        time.sleep(1)
        self.swipe_by_percent(0.7, 0.8, 0.2, 0.8, 300)
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][2]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[2]}"]'),
            f"购买B5位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("购买B6位置sku商品")
    def buy_sku_b6(self):
        time.sleep(1.5)
        self.swipe_by_percent(0.7, 0.8, 0.1, 0.8, 300)
        time.sleep(1)
        self.swipe_by_percent(0.7, 0.8, 0.2, 0.8, 300)
        time.sleep(1)
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][3]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[3]}"]'),
            f"购买B6位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("购买膨胀商品")
    def buy_sku(self):
        self.click(
            ('xpath',
             f'//android.widget.TextView[contains(@text, "{TopUpPage.handler.top_up_sku_coins[0][0]}")]'),
            "购买膨胀商品"
        )
        self.click(self.element.common_page.cocnfirm_button, "确认支付")
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        time.sleep(2)

    @Decorate.collect_test("购买A1位置sku商品（触发充值挽留）")
    def buy_retention_sku_a1(self):
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][0]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[0]}"]'),
            f"购买A1位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("购买B2位置sku商品（触发充值挽留）")
    def buy_retention_sku_b2(self):
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][2]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[2]}"]'),
            f"购买B2位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("购买B3位置sku商品（触发充值挽留）")
    def buy_retention_sku_b3(self):
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][3]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[3]}"]'),
            f"购买B3位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("购买B4位置sku商品（触发充值挽留）")
    def buy_retention_sku_b4(self):
        time.sleep(1.5)
        self.swipe_by_percent(0.7, 0.8, 0.1, 0.8, 300)
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][2]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[2]}"]'),
            f"购买B4位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("购买B5位置sku商品（触发充值挽留）")
    def buy_retention_sku_b5(self):
        time.sleep(1.5)
        self.swipe_by_percent(0.7, 0.8, 0.1, 0.8, 300)
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][3]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[3]}"]'),
            f"购买B5位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("购买B6位置sku商品（触发充值挽留）")
    def buy_retention_sku_b6(self):
        time.sleep(1.5)
        # 使用屏幕百分比执行滑动操作
        self.swipe_by_percent(0.7, 0.8, 0.1, 0.8, 300)
        time.sleep(1)
        self.swipe_by_percent(0.7, 0.8, 0.4, 0.8, 300)
        time.sleep(1)
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][3]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[3]}"]'),
            f"购买B6位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("购买B7位置sku商品（触发充值挽留）")
    def buy_retention_sku_b7(self):
        time.sleep(1.5)
        self.swipe_by_percent(0.7, 0.8, 0.1, 0.8, 300)
        time.sleep(1)
        self.swipe_by_percent(0.7, 0.8, 0.3, 0.8, 200)
        time.sleep(1)
        top_up_coins = [item.split()[0] for item in self.get_coins_ui_text()][3]
        self.click(
            ('xpath', f'//android.widget.TextView[@text="{self.get_coins_ui_text()[3]}"]'),
            f"购买B7位置sku商品:{top_up_coins}"
        )
        self.click(self.element.common_page.confirm_payment, "确认支付")
        try:
            self.click(self.element.common_page.cancel_login, "关闭登录弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        return top_up_coins

    @Decorate.collect_test("触发充值挽留，并重新进入付费卡点")
    def again_pay(self):
        if self.wait_element(self.element.advertisement_page.privileges_text, "等待付费页面加载",
                             10) is not None:
            self.press_back_button("退出付费卡点")
        try:
            self.click(self.element.common_page.cancel_login, "关闭充值挽留弹窗")
        except Exception as e:
            logging.error(f"An error：{e}")
        self.click(self.element.drama_page.unlock_drama_04, "重新进入付费卡点")

    @Decorate.collect_test("退出付费卡点，触发充值挽留")
    def exit_pay(self):
        if self.wait_element(self.element.advertisement_page.privileges_text, "等待付费页面加载",
                             10) is not None:
            self.press_back_button("退出付费卡点")

    @Decorate.collect_test("充值挽留购买膨胀商品")
    def top_up_retention(self):
        self.click(self.element.top_up_page.purchase_button, "购买膨胀商品")
        self.click(self.element.common_page.cocnfirm_button, "确认支付")
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
        time.sleep(1.5)

    @Decorate.collect_test("退出充值挽留，进入充值页面")
    def exit_retention_into_top_up(self):
        self.click(self.element.common_page.cancel_login, "关闭充值挽留弹窗")
        self.click(self.element.my_page.navigation_back, "退出付费卡点")
        self.click(self.element.common_page.later, "点击Later")
        time.sleep(6)
        try:
            self.wait_element(self.element.common_page.cancel_login, "关闭插屏广告").click()
        except Exception as e:
            Log.logger.info(f"error : {e}")
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
        self.click(self.element.common_page.top_up, "进入充值模块")

    @Decorate.collect_test("充值页面购买膨胀商品")
    def top_up_page_buy_sku(self):
        self.click(
            ('xpath',
             f'//android.widget.TextView[contains(@text, "{TopUpPage.handler.top_up_sku_coins[0][0]}")]'),
            "购买膨胀商品"
        )
        self.click(self.element.common_page.cocnfirm_button, "确认支付")
        self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
