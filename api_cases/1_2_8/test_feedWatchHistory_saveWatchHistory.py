import pytest
import allure

from api_clients.feed流观看历史记录_test import ffff_feedWatchHistory_saveWatchHistory
from api_cases.tools.tools import login
from api_clients.短剧解锁相关接口_test import ffff_shortPlay_unlockEpisodeByWatchAd
from utils.logger_manager import LoggerManager


# @allure.epic("登录模块")
@allure.feature("保存feed流观看历史记录")
class TestSaveWatchHistory:
    @pytest.fixture(scope="function", autouse=True)
    def environment(self):
        LoggerManager().init(filename="TestSaveWatchHistory")
        self.logger = LoggerManager().get_logger(name=__name__)
        with allure.step("用户登录"):
            self.client = login()
        yield
        with allure.step("用例环境清理"):
            self.logger.info("用例环境清理")

    @allure.title("保存成功")
    def test_feed_watch_history_save_watch_history_success(self):
        ffff_feedWatchHistory_saveWatchHistory(self.client, 999, 410360, )

    @allure.title("保存失败, 剧集不存在")
    def test_feed_watch_history_save_watch_history_not_exist(self):
        ffff_feedWatchHistory_saveWatchHistory(self.client, 999, 410360999,
                                               {"status": 20012, "message": "Series has been removed"})

    # todo 后端没处理
    @allure.title("保存失败, 时间参数不对")
    # ffff_feedWatchHistory_saveWatchHistory
    def test_feed_watch_history_save_watch_history_time_error(self):
        ffff_feedWatchHistory_saveWatchHistory(self.client, 0, 410360,
                                               )
