import logging

from selenium.common import TimeoutException

from common.api.mock_data import MockData
from common.language.lang_mgr import lang_mgr
from common.mysql.mysql_tools import update_test_case_info
from common.utils.cmd_tools import *
from common.utils.path_config import android
from common.utils.report import get_app_version
from common.utils.tools import timestamp
from sys_android.page_objects.drama_page import DramaPage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("解锁剧集相关模块")
class TestUnlockDramaModule:
    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        volume_purchase_value = request.node.get_closest_marker("volume_purchase_value")
        volume_purchase_value = volume_purchase_value.args[0] if volume_purchase_value else None
        if volume_purchase_value == 1:
            self.mock_data = MockData(args.device.split(":")[0])
            self.mock_data.mock_data(
                "test_unlock_drama_01", "/app/abtest/getAbtestParams", {"and_volume_purchase_test": "1"}
            )
        elif volume_purchase_value == 2:
            self.mock_data = MockData(args.device.split(":")[0])
            self.mock_data.mock_data(
                "test_unlock_drama_01", "/app/abtest/getAbtestParams", {"and_volume_purchase_test": "2"}
            )
        self.proxy_process = start_proxy()
        self.driver = DramaPage()
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
        # 更新用例
        update_test_case_info(request, self.test_status, self.driver.setup_step_collection,
                              self.driver.case_step_collection, self.driver.tear_down_collection,
                              self.driver.check_collection)

    @pytest.mark.已开发完成
    @allure.title("01-金币解锁单集剧集，解锁成功")
    @allure.description("切换新用户——>充值金币——>金币解锁单集剧集——>解锁成功，金币减少")
    def test_unlock_drama_01(self):
        """切换新用户——>充值金币——>金币解锁单集剧集——>解锁成功，金币减少"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 充值金币
            self.driver.recharge_coins()
            # 搜索短剧，进入沉浸页
            self.driver.into_immersion_page()
            # 金币解锁单级
            self.driver.coins_unlock()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_expect_in_text(
            "4", self.driver.get_element_text(self.element.drama_page.episode_num), "断言-金币解锁单集成功"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.volume_purchase_value(2)
    @allure.title("02-（Ab测试-2）批量解锁2集，解锁成功")
    @allure.description("切换新用户——>批量解锁切换为实验2——>解锁2集——>解锁成功")
    def test_unlock_drama_02(self):
        """切换新用户——>批量解锁切换为实验2——>解锁2集——>解锁成功"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧进入付费卡点
            self.driver.into_pay_page()
            # 批量解锁两集
            self.driver.batch_unlock_two_episodes()
            # 点击选集按钮
            self.driver.click_fragment()
            self.driver.assert_element_exists(self.element.drama_page.unlock_five, "断言-批量解锁两集成功")
            # 进入我的钱包
            self.driver.into_my_wallet()
            self.driver.get_bonus_record()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.volume_purchase_value(2)
    @allure.title("（Ab测试-2）批量解锁5集，解锁成功")
    def test_unlock_drama_03(self):
        """切换新用户——>批量解锁切换为实验2——>解锁5集——>解锁成功"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧进入付费卡点
            self.driver.into_pay_page()
            # 批量解锁5级
            self.driver.batch_unlock_five_episodes()
            # 点击选集按钮
            self.driver.click_fragment()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_element_exists(self.element.drama_page.unlock_eight, "断言-批量解锁五集成功")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.volume_purchase_value(2)
    @allure.title("04-（Ab测试-2）批量解锁整部剧集，解锁成功")
    @allure.description("切换新用户——>批量解锁切换为实验2——>解锁整部剧集——>解锁成功")
    def test_unlock_drama_04(self):
        """切换新用户——>批量解锁切换为实验2——>解锁整部剧集——>解锁成功"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧进入付费卡点
            self.driver.into_pay_page()
            # 批量解锁全员剧集
            self.driver.batch_unlock_all_episodes()
            # 点击选集按钮
            self.driver.click_fragment()
            self.driver.click(self.element.drama_page.twenty_six_thirty, "点击26-30")
            self.driver.click(self.element.drama_page.thirty, "点击第30集")
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_expect_in_text(
            "30", self.driver.get_element_text(self.element.drama_page.episode_num), "断言-批量解锁全部剧集成功"
        )
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.volume_purchase_value(2)
    @allure.title("05-（Ab测试-2）批量解锁10集，解锁成功")
    @allure.description("切换新用户——>批量解锁切换为实验2——>解锁整部剧集——>解锁成功")
    def test_unlock_drama_05(self):
        """切换新用户——>批量解锁切换为实验2——>解锁整部剧集——>解锁成功"""
        try:
            # 前置-关闭首页弹窗，切换新用户
            self.driver.android_version()
    
            # 搜索短剧进入付费卡点
            self.driver.into_pay_page()
            # 批量解锁十集
            self.driver.batch_unlock_ten_episodes()
            # 点击选集按钮
            self.driver.click_fragment()
        except Exception as e:
            logging.error(f"An error: {e}")
        self.driver.assert_element_exists(self.element.drama_page.unlock_thirteen, "断言-批量解锁十集成功")
        self.test_status = True

    @pytest.mark.已开发完成
    @pytest.mark.volume_purchase_value(1)
    @allure.title("06-（Ab测试-1）解锁整部剧集，解锁成功")
    @allure.description("切换新用户——>批量解锁切换为实验1——>解锁整部剧集——>解锁成功")
    def test_unlock_drama_06(self):
        """切换新用户——>批量解锁切换为实验1——>解锁整部剧集——>解锁成功"""

        # 前置-关闭首页弹窗，切换新用户
        self.driver.android_version()

        self.driver.recharge_coins()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        # 解锁全部剧集
        self.driver.batch_unlock_all_episodes()
        # 点击选集按钮
        self.driver.click_fragment()
        self.driver.click(self.element.drama_page.twenty_six_thirty, "点击26-30")
        self.driver.click(self.element.drama_page.thirty, "点击第30集")

        self.driver.assert_expect_in_text(
            "30",
            self.driver.get_element_text(self.driver.element.drama_page.episode_num, "获取集数"),
            "断言-解锁全部剧集成功",
        )
        self.test_status = True
