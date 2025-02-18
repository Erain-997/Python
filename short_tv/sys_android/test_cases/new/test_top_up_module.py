import logging

from common.api.mock_data import MockData
from common.mysql.mysql_tools import update_test_case_info
from common.utils.cmd_tools import *
from common.utils.tools import timestamp
from sys_android.page_objects.top_up_page import TopUpPage
from sys_android.test_cases.new.test_get_yaml import *
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("充值金币模块")
class TestTopUpModule:
    handler = TopUpDataHandler()

    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(":")[0])
        # 付费卡点显示广告解锁，参数为0显示内购+广告+膨胀sku
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams", {"and_without_ad_test": "0"})
        self.proxy_process = start_proxy()
        self.driver = TopUpPage()
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
        # 停止录制视频并保存
        self.driver.stop_and_save_recording(self.test_status)
        # 停止app系统日志记录
        stop_logcat(self.logcat_process, self.log_path)
        stop_proxy(self.proxy_process)
        # 退出驱动
        self.driver.quit()
        if request.node.name == "test_top_up_20":
            self.yaml_file_path = f"{android.test_datas_dir}/top_up_modules.yaml"
            os.remove(self.yaml_file_path)
        # 更新用例
        update_test_case_info(request, self.test_status, self.driver.setup_step_collection,
                              self.driver.case_step_collection, self.driver.tear_down_collection,
                              self.driver.check_collection)

    @pytest.mark.已开发完成
    @allure.title("01-遍历所有充值选项")
    @allure.description("遍历所有充值选项充值——>核对金币数量")
    def test_top_up_01(self):
        """遍历所有充值选项"""
        try:
            self.driver.android_version()
    
            # 进入充值页面
            self.driver.into_top_up_page()
            coins_language = [item.split()[1] for item in self.driver.get_coins_ui_text()][0:1]
            # 遍历充值充值页面金币
            self.driver.top_up_all_coins(coins_language)
            # 进入我的钱包-查看Coin下发记录
            self.driver.into_wallet_page()
            # 断言-【Coin Record】充值记录下发正确
            self.driver.expect_coins_record(coins_language)
            # 断言-【Bonus】记录下发正确
            self.driver.expect_bonus_record()
            self.total_coins = self.driver.expect_sum_coins()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(
            self.total_coins, int(self.driver.get_element_text(self.driver.element.common_page.coins)),
            "断言-【Coins】总数正确显示"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("02-校验金币商城页面购买A1位置sku商品")
    @allure.description("进入金币商城——>购买A1位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_02(self):
        """进入金币商城——>购买A1位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 进入金币商城
            self.driver.into_coins_store()
            self.top_up_coins1 = [item.split()[0] for item in self.driver.get_coins_ui_text()][0]
            # 购买A1位置sku商品
            self.driver.buy_sku_a1()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[0], '+' + str(self.top_up_coins1),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[0],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("03-校验金币商城页面购买B1位置sku商品")
    @allure.description("进入金币商城——>购买B1位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_03(self):
        """进入金币商城——>购买B1位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 进入金币商城
            self.driver.into_coins_store()
            self.top_up_coins = [item.split()[0] for item in self.driver.get_coins_ui_text()][1]
            # 购买A1位置sku商品
            self.driver.buy_sku_b1()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[1], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[1],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("04-校验金币商城页面购买B2位置sku商品")
    @allure.description("进入金币商城——>购买B2位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_04(self):
        """进入金币商城——>购买B2位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 进入金币商城
            self.driver.into_coins_store()
            self.top_up_coins = [item.split()[0] for item in self.driver.get_coins_ui_text()][2]
            # 购买A1位置sku商品
            self.driver.buy_sku_b2()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[2], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[2],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("05-校验金币商城页面购买B3位置sku商品")
    @allure.description("进入金币商城——>购买B3位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_05(self):
        """进入金币商城——>购买B3位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 进入金币商城
            self.driver.into_coins_store()
            self.top_up_coins = [item.split()[0] for item in self.driver.get_coins_ui_text()][3]
            # 购买A1位置sku商品
            self.driver.buy_sku_b3()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[3], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[3],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("06-校验金币商城页面购买B4位置sku商品")
    @allure.description("进入金币商城——>购买B4位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_06(self):
        """进入金币商城——>购买B4位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品
            self.top_up_coins = self.driver.buy_sku_b4()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[4], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[4],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("07-校验金币商城页面购买B5位置sku商品")
    @allure.description("进入金币商城——>购买B5位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_07(self):
        """进入金币商城——>购买B5位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品
            self.top_up_coins = self.driver.buy_sku_b5()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[5], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[5],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("08-校验金币商城页面购买B6位置sku商品")
    @allure.description("进入金币商城——>购买B6位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_08(self):
        """进入金币商城——>购买B6位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品
            self.top_up_coins = self.driver.buy_sku_b6()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[6], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[6],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("09-付费卡点退出触发充值挽留，付费卡点、金币商城展示膨胀sku")
    @allure.description("进入付费卡点并退出——>重新进入付费卡点/金币商城——>金币商城展示膨胀sku")
    def test_top_up_09(self):
        """进入付费卡点并退出——>重新进入付费卡点/金币商城——>金币商城展示膨胀sku"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 断言-付费卡点页面展示膨胀sku
            self.driver.expect_sku()
            # 进入金币商城
            self.driver.into_coins_store()
        except Exception as e:
            logging.error(f"An error: {e}")
        time.sleep(2)
        coins_language = self.driver.get_coins_ui_text()[1]
        self.driver.assert_text_equal(coins_language, self.driver.get_element_text([
            "xpath", f'//android.widget.TextView[contains(@text, "{TopUpPage.handler.top_up_sku_coins[0][0]}")]'
        ]),
                                      "断言-金币商城展示膨胀sku")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("10-付费卡点退出触发充值挽留弹窗，在充值挽留弹窗购买膨胀商品")
    @allure.description("进入付费卡点——>在充值挽留弹窗购买膨胀商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_10(self):
        """进入付费卡点——>在充值挽留弹窗购买膨胀商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 退出付费卡点，触发充值挽留
            self.driver.exit_pay()
            # 充值挽留购买膨胀商品
            self.driver.top_up_retention()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal('+' + TopUpPage.handler.top_up_sku_coins[0][0],
                                      self.driver.get_element_text(self.element.top_up_page.amount_two),
                                      "断言-【Coin Record】充值记录下发正确")

        self.driver.assert_text_equal("-50", self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Coin Record】消费记录下发正确")
        self.driver.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
            "查看Bonus下发记录"
        )
        self.driver.assert_text_equal('+' + TopUpPage.handler.top_up_sku_bonus[0][0],
                                      self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Bonus】记录下发正确")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("11-付费卡点退出触发充值挽留弹窗，在充值页面购买膨胀商品")
    @allure.description("进入付费卡点并退出——>进入充值模块——>购买膨胀商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_11(self):
        """进入付费卡点并退出——>进入充值模块——>购买膨胀商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 退出付费卡点，触发充值挽留
            self.driver.exit_pay()
            # 退出充值挽留，进入充值模块
            self.driver.exit_retention_into_top_up()
            # 充值页面购买膨胀商品
            self.driver.top_up_page_buy_sku()
            # 进入我的钱包-查看Coin/Bonus下发记录
            self.driver.into_wallet_page()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal('+' + TopUpPage.handler.top_up_sku_coins[0][0],
                                      self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Coin Record】充值记录下发正确")
        self.driver.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
            "查看Bonus下发记录"
        )
        self.driver.assert_text_equal('+' + TopUpPage.handler.top_up_sku_bonus[0][0],
                                      self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Bonus】记录下发正确")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("12-付费卡点退出触发充值挽留弹窗，在付费卡点页面购买膨胀商品")
    @allure.description(
        "进入付费卡点并退出——>触发充值挽留弹窗——>重新进入付费卡点——>购买膨胀商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_12(self):
        """进入付费卡点并退出——>触发充值挽留弹窗——>重新进入付费卡点——>购买膨胀商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 付费卡点购买膨胀商品
            self.driver.buy_sku()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal('+' + TopUpPage.handler.top_up_sku_coins[0][0],
                                      self.driver.get_element_text(self.element.top_up_page.amount_two),
                                      "断言-【Coin Record】充值记录下发正确")
        self.driver.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
            "查看Bonus下发记录"
        )
        self.driver.assert_text_equal('+' + TopUpPage.handler.top_up_sku_bonus[0][0],
                                      self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Bonus】记录下发正确")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("13-付费卡点退出触发充值挽留弹窗，在金币商城页面购买膨胀商品")
    @allure.description(
        "进入付费卡点——>触发充值挽留弹窗——>重新进入付费卡点/金币商城——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_13(self):
        """进入付费卡点——>触发充值挽留弹窗——>重新进入付费卡点/金币商城——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 进入金币商城
            self.driver.into_coins_store()
            # 金币商城购买膨胀商品
            self.driver.buy_sku()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal('+' + TopUpPage.handler.top_up_sku_coins[0][0],
                                      self.driver.get_element_text(self.element.top_up_page.amount_two),
                                      "断言-【Coin Record】充值记录下发正确")
        self.driver.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
            "查看Bonus下发记录"
        )
        self.driver.assert_text_equal('+' + TopUpPage.handler.top_up_sku_bonus[0][0],
                                      self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Bonus】记录下发正确")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("14-付费卡点退出触发充值挽留弹窗，在金币商城页面购买A1位置sku商品")
    @allure.description(
        "付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买A1位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_14(self):
        """付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买A1位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品（触发充值挽留）
            self.top_up_coins = self.driver.buy_retention_sku_a1()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[0], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[0],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("15-付费卡点退出触发充值挽留弹窗，在金币商城页面购买B2位置sku商品")
    @allure.description(
        "付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B2位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_15(self):
        """付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B2位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品（触发充值挽留）
            self.top_up_coins = self.driver.buy_retention_sku_b2()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[1], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[1],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("16-付费卡点退出触发充值挽留弹窗，在金币商城页面购买B3位置sku商品")
    @allure.description(
        "付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B3位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_16(self):
        """付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B3位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品（触发充值挽留）
            self.top_up_coins = self.driver.buy_retention_sku_b3()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[2], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[2],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("17-付费卡点退出触发充值挽留弹窗，在金币商城页面购买B4位置sku商品")
    @allure.description(
        "付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B4位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_17(self):
        """付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B4位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品（触发充值挽留）
            self.top_up_coins = self.driver.buy_retention_sku_b4()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[3], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[3],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("18-付费卡点退出触发充值挽留弹窗，在金币商城页面购买B5位置sku商品")
    @allure.description(
        "付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B5位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_18(self):
        """付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B5位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品（触发充值挽留）
            self.top_up_coins = self.driver.buy_retention_sku_b5()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[4], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[4],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("19-付费卡点退出触发充值挽留弹窗，在金币商城页面购买B6位置sku商品")
    @allure.description(
        "付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B6位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_19(self):
        """付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B6位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品（触发充值挽留）
            self.top_up_coins = self.driver.buy_retention_sku_b6()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[5], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[5],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("20-付费卡点退出触发充值挽留弹窗，在金币商城页面购买B7位置sku商品")
    @allure.description(
        "付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B7位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录")
    def test_top_up_20(self):
        """付费卡点退出触发充值挽留弹窗——>进入金币商城——>购买B7位置sku商品——>进入我的钱包——>验证Coin、Bonus下发记录"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧，进入付费卡点
            self.driver.into_pay_page()
            # 触发充值挽留，并重新进入付费卡点
            self.driver.again_pay()
            # 进入金币商城
            self.driver.into_coins_store()
            # 购买A1位置sku商品（触发充值挽留）
            self.top_up_coins = self.driver.buy_retention_sku_b7()
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_text_equal(TopUpPage.handler.coins_data[6], '+' + str(self.top_up_coins),
                                      "断言-【Coin Record】充值记录下发正确")
        time.sleep(2)
        self.driver.swipe_by_percent(0.6356, 0.24, 0.0347, 0.24, 400)
        if self.driver.wait_element(self.element.top_up_page.amount):
            self.driver.click(
                ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
                "查看Bonus下发记录"
            )
            self.driver.assert_text_equal(TopUpPage.handler.bonus_data[6],
                                          self.driver.get_element_text(self.element.top_up_page.amount),
                                          "断言-【Bonus】记录下发正确")
        else:
            allure.attach(self.driver.driver.get_screenshot_as_png(), name="该充值选项无Bonus下发",
                          attachment_type=allure.attachment_type.PNG)
        self.test_status = True
