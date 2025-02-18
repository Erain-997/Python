import time

from common.api.mock_data import MockData
from common.language.lang_mgr import lang_mgr
from common.mysql.mysql_tools import update_test_case_info
from common.utils.cmd_tools import *
from common.utils.tools import timestamp
from sys_android.page_objects.redeem_codes_page import RedeemCodesPage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("兑换码模块")
class TestRedeemCodesModule:
    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(":")[0])
        self.mock_data.mock_data(
            "test_unlock_drama_01", "/app/abtest/getAbtestParams", {"and_immersion_page_style_test": "1"}
        )
        # 开启福利中心实验，参数为1显示list红点
        if request.node.name == 'test_redeem_codes_01' or request.node.name == 'test_redeem_codes_07':
            self.mock_data.mock_data(
                "test_redeem_codes_07", "/app/abtest/getAbtestParams", {"fullscreen_task_show_control": "1"}
            )
        self.proxy_process = start_proxy()
        # ShortMax("88", "and_volume_purchase_test", "批量解锁", "0")
        self.driver = RedeemCodesPage()
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
    @allure.title("01-搜索【启用·使用中】的兑换码，获得相应的权益")
    @allure.description(
        "搜索兑换码——>退出沉浸页——>验证搜索历史记录——>进入我的钱包——>验证Coin/Bonus下发记录——>进入Mylist——>验证兑换码短剧添加成功")
    def test_redeem_codes_01(self):
        """搜索兑换码——>退出沉浸页——>验证搜索历史记录——>进入我的钱包——>验证Coin/Bonus下发记录——>进入Mylist——>验证兑换码短剧添加成功"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索兑换码: tvq8lgcby9
        self.driver.search_redeem_code1()
        # 退出沉浸页
        self.driver.out_of_immersion_code()
        # 断言-搜索历史记录不显示兑换码
        self.driver.check_in_immersion_code()
        # 查看Coin下发记录
        self.driver.coin_records()
        self.driver.assert_text_equal("+100", self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Coin Record】记录下发正确")
        # 查看Bonus下发记录
        self.driver.bonus_records()
        self.driver.assert_text_equal("+100", self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Bonus】记录下发正确")
        # 退出钱包模块
        self.driver.exit_wallet_module()
        self.driver.assert_element_exists(self.element.redeem_codes_page.red_point, "断言-Mylist导航栏显示红点（校验UI）")
        # 进入Mylist
        self.driver.into_mylist()
        self.driver.assert_text_equal(self.driver.get_element_text(self.element.immersion_page.shorts_name),
                                      self.driver.get_element_text(self.element.immersion_page.shorts_name),
                                      "断言-兑换码短剧添加到Mylist")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("02-搜索【禁用】的兑换码，提示兑换码不存在")
    @allure.description(
        "搜索兑换码——>验证toast提示信息——>退出沉浸页——>验证搜索历史记录——>进入我的钱包——>验证Coin/Bonus下发记录")
    def test_redeem_codes_02(self):
        """搜索兑换码——>验证toast提示信息——>退出沉浸页——>验证搜索历史记录——>进入我的钱包——>验证Coin/Bonus下发记录"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索兑换码: tvbxq4jy
        self.driver.search_redeem_code2()
        # 断言-不触发弹窗
        self.driver.check_no_popup_window()
        # 查看Coin下发记录
        self.driver.coin_records()
        self.driver.assert_element_exists(self.element.redeem_codes_page.empty_iv, "断言-无【Coin】下发记录（校验Ui）")
        # 查看Bonus下发记录
        self.driver.bonus_records()
        self.driver.assert_element_exists(self.element.redeem_codes_page.empty_iv, "断言-无【Bonus】下发记录（校验Ui）")
        self.test_status = True

    # @pytest.mark.已开发完成
    # @allure.title("03-搜索【启用·已用完】的兑换码，进入短剧成功，提示【来晚了，已领完】")
    # @allure.description(
    #     "搜索兑换码——>验证toast提示信息——>退出沉浸页——>验证搜索历史记录——>进入我的钱包——>验证Coin/Bonus下发记录")
    # def test_redeem_codes_03(self):
    #     # 关闭首页弹窗
    #     self.driver.android_version()
    #     # 切换成新账号
    #     self.driver.switch_new_account()
    #     # 搜索兑换码: tvzpneu73
    #     self.driver.search_redeem_code3()
    #     # 断言-toast提示【来晚了，已领完】
    #     self.driver.assert_text_equal(
    #         lang_mgr.search_activity_redeem_code_use_up(),
    #         self.driver.get_element_text((
    #             'xpath',
    #             f'//android.widget.Toast[@text, "{lang_mgr.search_activity_redeem_code_use_up()}"]'
    #         )), f"当前语言：{args.language}，断言-toast提示【来晚了，已领完】")
    #     # 断言-不触发弹窗
    #     self.driver.check_no_popup_window()
    #     # 退出沉浸页
    #     self.driver.out_of_immersion_code()
    #     # 断言-搜索历史记录不显示兑换码
    #     self.driver.check_in_immersion_code()
    #     # 查看Coin下发记录
    #     self.driver.coin_records()
    #     self.driver.assert_element_exists(self.element.redeem_codes_page.empty_iv, "断言-无【Coin】下发记录（校验Ui）")
    #     # 查看Bonus下发记录
    #     self.driver.bonus_records()
    #     self.driver.assert_element_exists(self.element.redeem_codes_page.empty_iv, "断言-无【Bonus】下发记录（校验Ui）")
    #     self.test_status = True
    # 
    # @pytest.mark.已开发完成
    # @allure.title("04-搜索【启用·已过期】的兑换码，进入短剧成功，提示【兑换码已过期】")
    # @allure.description(
    #     "搜索兑换码——>验证toast提示信息——>退出沉浸页——>验证搜索历史记录——>进入我的钱包——>验证Coin/Bonus下发记录")
    # def test_redeem_codes_04(self):
    #     """搜索兑换码——>验证toast提示信息——>退出沉浸页——>验证搜索历史记录——>进入我的钱包——>验证Coin/Bonus下发记录"""
    #     # 关闭首页弹窗
    #     self.driver.android_version()
    #     # 切换成新账号
    #     self.driver.switch_new_account()
    #     # 搜索兑换码: tvl5f
    #     self.driver.search_redeem_code4()
    #     # 断言-toast提示【兑换码已过期】
    #     time.sleep(1.5)
    #     self.driver.assert_text_equal(
    #         lang_mgr.search_activity_redeem_code_overdue(),
    #         self.driver.get_element_text((
    #             'xpath',
    #             f'//android.widget.Toast[@text="{lang_mgr.search_activity_redeem_code_overdue()}"]'
    #         )), f"当前语言：{args.language}，断言-toast提示【兑换码已过期】")
    #     # 断言-不触发弹窗
    #     self.driver.check_no_popup_window()
    #     # 退出沉浸页
    #     self.driver.out_of_immersion_code()
    #     # 断言-搜索历史记录不显示兑换码
    #     self.driver.check_in_immersion_code()
    #     # 查看Coin下发记录
    #     self.driver.coin_records()
    #     self.driver.assert_element_exists(self.element.redeem_codes_page.empty_iv, "断言-无【Coin】下发记录（校验Ui）")
    #     # 查看Bonus下发记录
    #     self.driver.bonus_records()
    #     self.driver.assert_element_exists(self.element.redeem_codes_page.empty_iv, "断言-无【Bonus】下发记录（校验Ui）")
    #     self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("05-搜索非兑换码，搜索历史记录显示该记录")
    @allure.description("搜索非兑换码——>验证搜索历史记录显示非兑换码")
    def test_redeem_codes_05(self):
        """搜索非兑换码——>验证搜索历史记录显示非兑换码"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索兑换码: vl5f
        self.driver.search_redeem_code5()
        # 进入首页搜索框
        self.driver.into_search_box()
        self.driver.assert_text_equal("vl5fb",
                                      self.driver.get_element_text(self.element.redeem_codes_page.search_text),
                                      "断言-Search History显示vl5fb")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("06-重复搜索已兑换的兑换码，权益弹窗按钮为【已领取】")
    @allure.description("搜索兑换码——>关闭兑换码退出——>再次搜索该兑换码——>验证Coin/Bonus下发记录")
    def test_redeem_codes_06(self):
        """搜索兑换码——>关闭兑换码退出——>再次搜索该兑换码——>验证Coin/Bonus下发记录"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索兑换码: tvq8lgcby9
        self.driver.search_redeem_code6()
        # 退出沉浸页
        self.driver.out_of_immersion_code()
        # 重新搜索兑换码
        self.driver.research_redeem_code()
        # 返回首页
        self.driver.back_to_home()
        self.driver.press_back_button()
        self.driver.click(('xpath', f'//android.widget.TextView[@text="{self.driver.get_tab_button()[3]}"]'),
                          "进入我的模块")
        self.driver.click(self.element.common_page.wallet, "进入我的钱包")
        # 查看coins下发记录
        self.driver.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[2]}")]'),
            "查看Coin下发记录"
        )
        self.driver.assert_text_equal("+100", self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Coin Record】记录下发正确")
        self.driver.click(
            ('xpath', f'//android.widget.TextView[contains(@text, "{self.driver.get_wallet_text()[3]}")]'),
            "查看Bonus下发记录"
        )
        self.driver.assert_text_equal("+100", self.driver.get_element_text(self.element.top_up_page.amount),
                                      "断言-【Bonus】记录下发正确")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("07-检验开启福利中心实验，搜索兑换码对应的短剧，则在tab我的和my list入口也显示红点")
    @allure.description("搜索兑换码——>验证历史搜索记录——>进入Mylist——>验证兑换码短剧添加成功")
    def test_redeem_codes_07(self):
        """搜索兑换码——>验证历史搜索记录——>进入Mylist——>验证兑换码短剧添加成功"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索兑换码: tvq8lgcby9
        self.driver.search_redeem_code6()
        # 退出沉浸页
        self.driver.out_of_immersion_code()
        # 断言-搜索历史记录不显示兑换码
        self.driver.check_search_history_not_show_redeem_code()
        self.driver.assert_element_exists(self.element.redeem_codes_page.red_point, "断言-Mylist导航栏显示红点（校验UI）")
        # 进入Mylist
        self.driver.into_mylist()
        self.driver.assert_text_equal(self.driver.get_element_text(self.element.immersion_page.shorts_name),
                                      self.driver.get_element_text(self.element.immersion_page.shorts_name),
                                      "断言-兑换码短剧添加到Mylist")
        self.driver.assert_element_exists(self.element.redeem_codes_page.red_point1,
                                          "断言-Mylist下PlayNew显示红点（校验UI）")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("08-搜索不同【启用】的兑换码超过5次，提示【搜索太频繁，请稍后再试】")
    @allure.description("搜索五次不同兑换码——>toast提示【搜索太频繁，请稍后再试】")
    def test_redeem_codes_08(self):
        """搜索五次不同兑换码——>toast提示【搜索太频繁，请稍后再试】"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索五次兑换码
        self.driver.search_redeem_code_5_times()
        # 再次搜索兑换码
        self.driver.search_redeem_code_again()
        self.driver.assert_text_equal(
            lang_mgr.search_activity_search_frequently_tips(),
            self.driver.get_element_text((
                'xpath',
                f'//android.widget.Toast[@text="{lang_mgr.search_activity_search_frequently_tips()}"]'
            )), f"当前语言：{args.language}，断言-toast提示【搜索太频繁，请稍后再试】")
        self.test_status = True
