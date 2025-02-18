from common.api.mock_data import MockData
from common.mysql.mysql_tools import update_test_case_info
from common.utils.cmd_tools import *
from common.utils.tools import timestamp
from sys_android.page_objects.reissue_order_page import ReissueOrderPage


@allure.epic("补单模块")
class TestReissueOrderModule:
    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(":")[0])
        self.mock_data.mock_data(
            "test_unlock_drama_01",
            "/app/abtest/getAbtestParams",
            {"and_immersion_page_style_test": "1"},
        )
        self.proxy_process = start_proxy()
        self.driver = ReissueOrderPage()
        # 启动录制视频
        self.driver.start_recording()
        # 采集app系统日志
        self.log_path = os.path.join(android.report_output_dir, args.output_report, "log",
                                     f"logcat日志_{request.node.name}_{timestamp()}.log")
        self.logcat_process = adb_logcat(self.log_path)
        # 初始化测试失败标志
        self.test_status = None
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
        if request.node.name == "test_reissue_order_05":
            self.yaml_file_path = f"{android.test_datas_dir}/top_up_modules.yaml"
            os.remove(self.yaml_file_path)
        # 更新用例
        update_test_case_info(request, self.test_status, self.driver.setup_step_collection,
                              self.driver.case_step_collection, self.driver.tear_down_collection,
                              self.driver.check_collection)

    @pytest.mark.已开发完成
    @allure.title("01-支付掉单,重启app补单成功")
    @allure.description("支付——>掉单(B4)——>重启app——>点击掉单选项——>弹出补单成功——>金币/奖励币断言")
    def test_reissue_order_01(self):
        """支付——>掉单(B4)——>重启app——>点击掉单选项——>弹出补单成功——>金币/奖励币断言"""

        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 支付掉单
        self.driver.reissue_order_B4()
        self.driver.driver.press_keycode(3)
        # 冷启动
        self.driver.hot_start()
        # 点击【restore】按钮
        self.driver.close_pop_ups_restore()
        self.driver.assert_element_exists(self.driver.element.top_up_page.repair_order, "断言-正确通知补单成功")
        order_coins = self.driver.select_sku_max_coins()
        self.driver.assert_text_equal(
            order_coins, int(self.driver.get_element_text(self.driver.element.common_page.coin_number)),
            "断言-补该sku商品最大coins"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("02-支付掉单后，手动点击restore补单成功")
    @allure.description("支付——>掉单(B4)——>点击【restore】——>弹出补单成功——>金币/奖励币断言")
    def test_reissue_order_02(self):
        """支付——>掉单(B4)——>点击【restore】——>弹出补单成功——>金币/奖励币断言"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 支付掉单
        self.driver.reissue_order_B4()
        # 点击【restore】按钮
        self.driver.close_pop_ups_restore()
        self.driver.assert_element_exists(self.driver.element.top_up_page.repair_order, "断言-正确通知补单成功")
        order_coins = self.driver.select_sku_max_coins()
        self.driver.assert_text_equal(
            order_coins, int(self.driver.get_element_text(self.driver.element.common_page.coin_number)),
            "断言-补该sku商品最大coins"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("03-支付掉单后，验证补单赠送bonus最多赠送5次")
    @allure.description("支付——>执行6次补单操作(同一个选项)——>弹出补单成功——>金币/奖励币断言")
    def test_reissue_order_03(self):
        """支付——>执行6次补单操作(同一个选项)——>弹出补单成功——>金币/奖励币断言"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 支付掉单A1六次
        self.driver.reissue_order_A1_loop_6_times()
        self.bonus = self.driver.select_sku_max_bonus()
        self.driver.assert_text_equal(
            self.bonus * 5, int(self.driver.get_element_text(self.driver.element.common_page.bonus)),
            "断言-验证补单赠送bonus最多赠送5次"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("04-付费卡点页面掉单后，补单成功自动解锁剧集")
    @allure.description(
        "支付——>搜索短剧进入选择未解锁剧集——>进入付费卡点——>掉单(A1)——>点击掉单充值(A1)选项——>弹出补单成功——>金币/奖励币/消费记录断言"
    )
    def test_reissue_order_04(self):
        """支付——>搜索短剧进入选择未解锁剧集——>进入付费卡点——>掉单(A1)——>点击掉单充值(A1)选项——>弹出补单成功——>金币/奖励币/消费记录断言"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入视频沉浸页
        self.driver.search_shorts_into_video_immersive()
        # 进入付费卡点,点击掉单测试
        self.driver.into_pay_page_click_reissue_order()
        # 点击【refresh】按钮
        self.driver.close_pop_ups_refresh()
        # 退出沉浸页，进入我的页面
        self.driver.out_immersive_page_into_wallet_page()
        order_coins = self.driver.select_sku_max_coins()
        self.driver.assert_text_equal(
            order_coins - 50, int(self.driver.get_element_text(self.driver.element.common_page.coins)), "断言-金币总数正确显示（扣除解锁剧集后）"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("05-付费卡点页面掉单后，手动点击【Refresh】，补单成功自动解锁剧集")
    @allure.description(
        "支付——>搜索短剧进入选择未解锁剧集——>进入付费卡点——>掉单(A1)——>点击【Refresh】——>弹出补单成功——>金币/奖励币/消费记录断言")
    def test_reissue_order_05(self):
        """支付——>搜索短剧进入选择未解锁剧集——>进入付费卡点——>掉单(A1)——>点击【Refresh】——>弹出补单成功——>金币/奖励币/消费记录断言"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入视频沉浸页
        self.driver.search_shorts_into_video_immersive()
        self.driver.into_pay_page_click_reissue_order()
        # 点击【refresh】按钮
        self.driver.close_pop_ups_refresh()
        # 退出沉浸页，进入我的钱包页面
        self.driver.out_immersive_page_into_wallet_page()
        order_coins = self.driver.select_sku_max_coins()
        self.driver.assert_text_equal(
            order_coins - 50, int(self.driver.get_element_text(self.driver.element.common_page.coins)), "断言-金币总数正确显示（扣除解锁剧集后）"
        )
        self.test_status = True
