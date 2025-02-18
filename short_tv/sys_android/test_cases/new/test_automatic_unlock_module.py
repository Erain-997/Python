import logging

from common.api.mock_data import MockData
from common.mysql.mysql_tools import update_test_case_info
from common.utils.cmd_tools import *
from common.utils.tools import timestamp
from sys_android.page_objects.drama_page import DramaPage


@allure.epic("自动解锁剧集相关模块")
class TestAutomaticUnlockModule:
    @allure.step("用例执行初始化")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request) -> None:
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(":")[0])
        self.mock_data.mock_data(
            "test_unlock_drama_01",
            "/app/abtest/getAbtestParams",
            {"and_immersion_page_style_test": "1", "and_ad_mediation_platform_test": "0"},
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
    @allure.title("01-通过广告解锁短剧，打开“自动解锁”权限")
    @allure.description("切换新用户——>搜索剧集并进入——>进入付费卡点——>广告解锁——>返回首页——>设置页面自动解锁权限已打开")
    def test_automatic_unlock_01(self):
        """切换新用户——>搜索剧集并进入——>进入付费卡点——>充值金币解锁——>返回首页——>设置页面自动解锁权限已打开"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.into_pay_page()
        # 搜索短剧，广告解锁剧集并返回首页
        self.driver.automatic_unlock_page_return_to_home()
        # 进入我的设置
        self.driver.into_my_setting()
        is_switch = self.driver.automatic_episode_button(1)
        self.driver.assert_text_equal(True, is_switch, "断言-自动解锁权限打开")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("02-通过金币解锁短剧，打开“自动解锁”权限")
    @allure.description(
        "切换新用户——>搜索剧集并进入——>进入付费卡点——>充值金币解锁——>返回首页——>设置页面自动解锁权限已打开"
    )
    def test_automatic_unlock_02(self):
        """通过金币解锁短剧，打开“自动解锁”权限"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.into_pay_page()
        # 金币解锁剧集并返回首页
        self.driver.coin_unlock_page_return_to_home()
        # 进入我的设置
        self.driver.into_my_setting()
        is_switch = self.driver.automatic_episode_button(1)
        self.driver.assert_text_equal(True, is_switch, "断言-自动解锁权限打开")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("03-通过膨胀挽留弹窗，打开自动解锁")
    @allure.description(
        "切换新用户——>搜索剧集并进入——>进入付费卡点——>退出弹出充值挽留弹窗——>充值挽留充值——>设置页面自动解锁权限已打开"
    )
    def test_automatic_unlock_03(self):
        """通过膨胀挽留弹窗，打开自动解锁"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.into_pay_page()
        # 充值挽留解锁剧集并返回首页
        self.driver.charge_unlock_page_return_to_home()
        # 进入我的设置
        self.driver.into_my_setting()
        is_switch = self.driver.automatic_episode_button(1)
        self.driver.assert_text_equal(True, is_switch, "断言-自动解锁权限打开")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("04-通过付费解锁卡点入口手动关闭“自动解锁”权限成功")
    @allure.description(
        "切换新用户——>搜索剧集并进入——>进入付费卡点——>点击“自动解锁剧集”按钮——>广告解锁——>返回首页——>设置页面自动解锁权限关闭"
    )
    def test_automatic_unlock_04(self):
        """通过付费解锁卡点入口手动关闭“自动解锁”权限成功"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.into_pay_page()
        # 广告解锁剧集并返回首页
        self.driver.advertisement_unlock_page_return_to_home()
        # 进入我的设置
        self.driver.into_my_setting()
        is_switch = self.driver.automatic_episode_button(1)
        self.driver.assert_text_equal(False, is_switch, "断言-自动解锁权限关闭")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("05-通过coins store入口手动关闭“自动解锁”权限成功")
    @allure.description(
        "切换新用户——>搜索剧集并进入——>进入付费卡点——>进入【Coins Store】——>点击“自动解锁剧集”按钮——>广告解锁——>返回首页——>设置页面自动解锁权限关闭"
    )
    def test_automatic_unlock_05(self):
        """通过coins store入口手动关闭“自动解锁”权限成功"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 搜索短剧，进入付费卡点
        self.driver.into_pay_page()
        # 进入Coins Store，广告解锁剧集并返回首页
        self.driver.into_coin_store_advertisement_unlock()
        # 进入我的设置
        self.driver.into_my_setting()
        is_switch = self.driver.automatic_episode_button(1)
        self.driver.assert_text_equal(False, is_switch, "断言-自动解锁权限关闭")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("06-通过设置入口打开“自动解锁”权限成功")
    @allure.description(
        "切换新用户——>设置页面打开自动解锁权限——>搜索剧集并进入——>进入付费卡点——>进入【Coins Store】——>广告解锁"
    )
    def test_automatic_unlock_06(self):
        """通过设置入口打开“自动解锁”权限成功"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入设置，打开自动解锁权限
        self.driver.open_auto_unlock_permission()
        # 搜索短剧
        self.driver.search_shorts()
        # 进入付费卡点，进入Coins Store
        self.driver.into_coin_store()
        self.driver.assert_element_not_exists(self.driver.element.automatic_unlock_page.auto_unlock_episode, "断言-自动解锁按钮不存在")
        self.test_status = True

    @pytest.mark.已开发完成
    @allure.title("07-已打开过“自动解锁”权限，膨胀挽留弹窗无自动解锁按钮")
    @allure.description("切换新用户——>设置页面打开自动解锁权限——>搜索剧集并进入——>进入付费卡点——>退出付费卡点页面")
    def test_automatic_unlock_07(self):
        """已打开过“自动解锁”权限，膨胀挽留弹窗无自动解锁按钮"""
        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号

        # 进入设置，打开自动解锁权限
        self.driver.open_auto_unlock_permission()
        # 搜索短剧，进入付费卡点并退出
        self.driver.search_shorts_into_automatic_unlock()
        self.driver.assert_element_not_exists(self.driver.element.automatic_unlock_page.auto_unlock_episode, "断言-自动解锁按钮不存在")
        self.test_status = True
