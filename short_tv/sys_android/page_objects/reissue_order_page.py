from common.language.lang_mgr import lang_mgr
from common.mysql.mysql_tools import mysql_execute_2
from common.utils.cmd_tools import *
from common.utils.decorator import Decorate
from sys_android.page_objects.common_page import CommonPage
from sys_android.test_cases.new.test_get_yaml import TopUpDataHandler


class ReissueOrderPage(CommonPage):
    handler = TopUpDataHandler()

    @Decorate.collect_test("支付掉单B4")
    def reissue_order_B4(self):
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
        self.click(self.element.common_page.top_up, "进入充值页面")
        coins_one = self.get_find_elements(self.element.top_up_page.coins_text)[0]
        self.click(("xpath", f'//android.widget.TextView[contains(@text, "{coins_one}")]'), f"点击充值{coins_one}选项")
        self.click(self.element.top_up_page.negative_button, "点击掉单测试")

    @Decorate.collect_test("点击【restore】按钮")
    def close_pop_ups_restore(self):
        self.click(self.element.common_page.close_iv, "关闭【重试】弹窗")
        self.click(self.element.top_up_page.restore, "点击【restore】按钮")

    @Decorate.collect_test("点击【Refresh】按钮")
    def close_pop_ups_refresh(self):
        self.click(self.element.common_page.close_iv, "关闭【重试】弹窗")
        self.click(self.element.top_up_page.refresh, "点击【Refresh】")

    @Decorate.collect_test("支付掉单A1六次")
    def reissue_order_A1(self):
        """支付——>掉单(A1)——>点击掉单充值(A1)选项——>弹出补单成功——>金币/奖励币断言"""
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
        self.click(self.element.common_page.top_up, "进入充值页面")
        coins_one = self.get_find_elements(self.element.top_up_page.coins_text)[1]
        bonus_one = self.get_element_text(self.element.top_up_page.bonus_text)
        self.click(("xpath", f'//android.widget.TextView[contains(@text, "{coins_one}")]'), f"点击充值{coins_one}选项")
        time.sleep(1)
        self.click(self.element.top_up_page.negative_button, "点击掉单测试")

        # self.click(("xpath", f'//android.widget.TextView[contains(@text, "{coins_one}")]'), f"点击充值{coins_one}选项")
        return int(self.extract_num(coins_one)), int(self.extract_num(bonus_one))

    @Decorate.collect_test("掉单测试6次")
    def reissue_order_A1_loop_6_times(self):
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
        self.click(self.element.common_page.top_up, "进入充值页面")
        coins_one = self.get_find_elements(self.element.top_up_page.coins_text)[1]
        with allure.step(f"{coins_one}选项掉单(循环6次)"):
            for i in range(6):
                time.sleep(5)
                self.click(
                    ("xpath", f'//android.widget.TextView[contains(@text, "{coins_one}")]'), f"点击充值{coins_one}选项"
                )
                time.sleep(1)
                self.click(self.element.top_up_page.negative_button, "点击掉单测试")
                self.click(self.element.common_page.close_iv, "关闭【重试】弹窗")
                self.click(self.element.top_up_page.restore, "点击【restore】按钮")

    @Decorate.collect_test("搜索短剧，进入视频沉浸页")
    def search_shorts_into_video_immersive(self):
        self.click(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[0]}"]'),
            "进入首页"
        )

        self.click(self.element.common_page.index_search, "点击首页搜索框")
        for k, j in self.language_search().items():
            if k == args.language:
                self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
        time.sleep(2)
        self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
        self.click(self.element.advertisement_page.video_detail, "进入视频沉浸页")
        time.sleep(1)

    @Decorate.collect_test("进入付费卡点,点击掉单测试")
    def into_pay_page_click_reissue_order(self):
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "查看影集列表")
        self.click(self.element.drama_page.four_episodes, "点击第4集")
        coins_one = self.get_find_elements(self.element.top_up_page.coins_text)[0]
        time.sleep(2)
        self.click(("xpath", f'//android.widget.TextView[contains(@text, "{coins_one}")]'), f"点击充值{coins_one}选项")
        time.sleep(1)
        self.click(self.element.top_up_page.negative_button, "点击掉单测试")

    @Decorate.collect_test("退出沉浸页，进入我的页面")
    def out_immersive_page_into_wallet_page(self):
        self.click(self.element.common_page.close_iv, "关闭提示弹窗")
        time.sleep(5)
        self.press_back_button("退出沉浸页")
        self.click(self.element.common_page.later, "点击Later按钮")
        self.click(self.element.common_page.back, "退出搜索页面")
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

    @Decorate.collect_test("断言-【Coin Record】消费记录下发正确")
    def check_coin_record(self, coins_one):
        self.assert_text_equal("-50", self.get_element_text(self.element.top_up_page.amount_one),
                               "断言-【Coin Record】正确")
        self.assert_text_equal(str(coins_one), self.get_element_text(self.element.top_up_page.amount_two),
                               "断言-【Coin Record】正确")

    @Decorate.collect_test("断言-【Bonus】记录下发正确")
    def check_bonus_record(self, bonus_one):
        self.click(self.element.common_page.reward_records, "点击奖励币记录")
        self.assert_text_equal(str(bonus_one), self.get_element_text(self.element.top_up_page.amount),
                               "断言-【Bonus Record】正确")
        self.click(self.element.common_page.navigation_back, "退出我的钱包")

    @Decorate.collect_test("查询sku商品赠送最大Coins")
    def select_sku_max_coins(self):
        sku_id = ReissueOrderPage.handler.gp_sku_id[0].replace("+", "")
        # 找最大的coins补
        select_max_coins = 'SELECT MAX(coins) FROM hi_sku_product WHERE gp_sku_id = %s'
        results = mysql_execute_2(select_max_coins, sku_id)
        coins = results[0]['MAX(coins)']
        allure.attach(f"{coins}", name="最大Coins值")
        return results[0]['MAX(coins)']

    @Decorate.collect_test("查询sku商品赠送最大Bonus")
    def select_sku_max_bonus(self):
        sku_id = ReissueOrderPage.handler.gp_sku_id[0].replace("+", "")
        # 找最大的coins补
        select_max_coins = 'SELECT MAX(give_coins) FROM hi_sku_product WHERE gp_sku_id = %s'
        results = mysql_execute_2(select_max_coins, sku_id)
        bonus = results[0]['MAX(give_coins)']
        allure.attach(f"{bonus}", name="最大Bonus值")
        return results[0]['MAX(give_coins)']
