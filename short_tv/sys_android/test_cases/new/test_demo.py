from common.api.mock_data import MockData
from common.mysql.mysql_tools import update_test_case_info
from common.utils.cmd_tools import *
from common.utils.decorator import Decorate
from sys_android.page_objects.subscribe_page import SubscribePage
from sys_android.test_datas.short_tv_elements import ShortTvElements


@allure.epic("测试模块")
class TestDemo:

    @Decorate.collect_setup("初始化驱动")
    @pytest.fixture(scope="function", autouse=True)
    def setup_steps(self, request):
        os.system(f"adb -s {args.device} logcat -c")
        self.mock_data = MockData(args.device.split(":")[0])
        # and_immersion_page_style_test：沉浸页排版，and_task_test：任务中心入口优化
        self.mock_data.mock_data(
            "test_unlock_drama_01", "/app/abtest/getAbtestParams",
            {"and_immersion_page_style_test": "1",
             "and_without_ad_test": "0"}
        )
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams",
                                 {"and_ad_mediation_platform_test": "0"})
        # 安卓端各场景广告开关
        self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams", {
            "adActionCount_android_v2": """
                    {
                      "action": {
                        "exitImmersionPage": 3,
                        "noPaidUnlockVideo": 1,
                        "noPaidAndWatchAdEarnBonus": 2
                      },
                      "scene": {
                        "exitImmersionPageEnable": true,
                        "exitImmersionPageCount": 1,
                        "switchTabEnable": true,
                        "switchTabCount": 1,
                        "unlockVideoEnable": true,
                        "unlockVideoCount": 2,
                        "homeRewardIconEnable": true,
                        "homeRewardIconCount": 1,
                        "shortsEnable": true,
                        "shortsIntervalCount": 5,
                        "discoverHorizontalVideoPreviewEnable": true,
                        "immersionFullScreenNativeEnable": true,
                        "immersionMediaVideoLoadTimeout": 2000,
                        "immersionPreRollEnable": true,
                        "immersionPreRollUnlockCount": 1,
                        "immersionPostRollEnable": true,
                        "immersionPostRollUnlockCount": 1
                      },
                      "gap": {
                        "interstitial": 60000,
                        "preloadAppOpen": 600000
                      },
                      "gdpr": {
                        "showRate": 100
                      }
                    }
                    """
        })
        self.proxy_process = start_proxy()
        self.driver = SubscribePage()
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

        # 业务
        self.subscribe_goods = self.driver.get_subscribe_goods_text()[args.language]

        # 关闭首页弹窗
        self.driver.android_version()
        # 切换成新账号
        self.driver.switch_new_account()

    @Decorate.collect_teardown("清理环境:关闭驱动")
    @pytest.fixture(scope="function", autouse=True)
    def teardown_steps(self, request):
        yield
        # 停止录制视频并保存
        self.driver.stop_and_save_recording(self.test_status, f"{request.node.name}")
        # 停止app系统日志记录
        stop_logcat(self.logcat_process, self.log_path)
        stop_proxy(self.proxy_process)
        # 退出驱动
        # self.driver.quit()
        # 更新用例
        update_test_case_info(request, self.test_status, self.driver.setup_step_collection,
                              self.driver.case_step_collection, self.driver.tear_down_collection,
                              self.driver.check_collection)

    @allure.feature("主页广告关闭")
    @allure.feature("测试feature")
    @allure.story("测试story")
    @allure.title("测试title")
    @pytest.mark.自动化用例调试中
    def test_demo_01(self):
        # 关闭首页弹窗
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        latiao = ["id", 'com.startshorts.androidplayer:id/seekbar_viewstub']
        pos = self.driver.wait_element(latiao).location
        self.driver.tap(400, 600, "轻敲屏幕", 200)
        # print("开始长按")
        # self.driver.tap(pos["x"]+100, pos["y"], "长按屏幕", 10000)
        # print("结束长按")
        # self.driver.tap(400, 600, "轻敲屏幕", 200)
        # pos = self.driver.wait_element(latiao).location
        # print("开始滑动")
        # self.driver.swipe(pos["x"] + 500, pos["y"], pos["x"], pos["y"], 100)
        # print("结束滑动")

        text = self.driver.get_current_time_tv()
        print("当前进度", text)
        self.driver.tap(400, 600, "轻敲屏幕", 200)
        time.sleep(5)
        text = self.driver.get_current_time_tv()
        print("当前进度", text)
        self.driver.tap(400, 600, "轻敲屏幕", 200)
        time.sleep(5)
        text = self.driver.get_current_time_tv()
        print("当前进度", text)
        self.driver.tap(400, 600, "轻敲屏幕", 200)
        time.sleep(5)

        self.driver.tap(400, 600, "轻敲屏幕", 200)
        print("测试完成")

    @allure.feature("主页广告关闭")
    @allure.feature("测试feature")
    @allure.story("测试story")
    @allure.title("测试title")
    @pytest.mark.已开发完成
    def test_demo_02(self):
        # 关闭首页弹窗
        self.driver.android_version()
        # 搜索短剧，进入沉浸页
        self.driver.into_immersion_page()
        latiao = ["id", 'com.startshorts.androidplayer:id/seekbar_viewstub']
        pos = self.driver.wait_element(latiao).location
        # self.driver.tap(400, 600, "轻敲屏幕", 200)
        # print("开始长按")
        # self.driver.tap(400, 600, "长按屏幕", 10000)
        # print("结束长按")
        # self.driver.tap(400, 600, "轻敲屏幕", 200)
        # pos = self.driver.wait_element(latiao).location
        # print("开始滑动")
        # self.driver.swipe(pos["x"] + 500, pos["y"], pos["x"], pos["y"], 100)
        # print("结束滑动")
        text = self.driver.get_speed_tips_tv()
        print("当前进度", text)
        # self.driver.tap(400, 600, "轻敲屏幕", 200)
        time.sleep(5)
        text = self.driver.get_speed_tips_tv()
        print("当前进度", text)
        # self.driver.tap(400, 600, "轻敲屏幕", 200)
        time.sleep(5)
        text = self.driver.get_current_time_tv()
        print("当前进度", text)
        self.driver.tap(400, 600, "轻敲屏幕", 200)
        time.sleep(5)

    @allure.feature("主页广告关闭")
    @allure.feature("测试feature")
    @allure.story("测试story")
    @allure.title("测试title")
    @pytest.mark.已开发完成
    def test_demo_03(self):
        # self.driver.click(["id", "com.startshorts.androidplayer:id/bg_iv"],"点击")
        time.sleep(50)
