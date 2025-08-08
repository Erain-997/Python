import pytest
import allure

from api_cases.tools.tools import login
from api_clients.短剧解锁相关接口_test import ffff_shortPlay_unlockEpisodeByWatchAd
from utils.logger_manager import LoggerManager


@allure.epic("登录模块")
@allure.feature("广告解锁剧集")
class TestUnlockEpisodeByWatchAd:
    @pytest.fixture(scope="function", autouse=True)
    def environment(self):
        LoggerManager().init(filename="TestUnlockEpisodeByWatchAd")
        self.logger = LoggerManager().get_logger(name=__name__)
        with allure.step("用户登录"):
            self.client = login()
        yield
        with allure.step("用例环境清理"):
            self.logger.info("用例环境清理")

    @allure.title("解锁失败, 剧集不存在")
    def test_short_play_unlock_episode_by_watch_ad_not_exist(self):
        ffff_shortPlay_unlockEpisodeByWatchAd(self.client, 1111, 7,
                                              {"status": 20013, "message": "Short Drama has been removed"})

    # todo 这个后端没处理
    # @allure.title("解锁失败, 集数不对")
    # def test_short_play_unlock_episode_by_watch_ad_has_unlocked_2(self):
    #     ffff_shortPlay_unlockEpisodeByWatchAd(self.client, 728600, -1)
    @allure.title("解锁失败, 已经解锁")
    def test_short_play_unlock_episode_by_watch_ad_has_unlocked(self):
        ffff_shortPlay_unlockEpisodeByWatchAd(self.client, 728600, 7,
                                              {"status": 20020, "message": "The episode has been unlocked"})

    @allure.title("解锁成功, 剧集正常解锁")
    def test_short_play_unlock_episode_by_watch_ad_success(self):
        ffff_shortPlay_unlockEpisodeByWatchAd(self.client, 728600, 8)

    @allure.title("解锁失败, 不科越级")
    def test_short_play_unlock_episode_by_watch_ad_failure(self):
        ffff_shortPlay_unlockEpisodeByWatchAd(self.client, 728600, 9,
                                              {"status": 20028, "message": "please unlock the previous episode first"})
