"""
Locust user for tag: 短剧解锁相关接口
"""
from locust import HttpUser, task, between
from api_clients import 短剧解锁相关接口_api as api


class FfffShortplayUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_shortPlay_unlockEpisodeByWatchAd(self):
        api.ffff_shortPlay_unlockEpisodeByWatchAd(self.client, self.base_url)

    @task
    def ffff_shortPlay_watchAdUnlockInfo(self):
        api.ffff_shortPlay_watchAdUnlockInfo(self.client, self.base_url)

    @task
    def ffff_shortPlay_unlockByWatchAd(self):
        api.ffff_shortPlay_unlockByWatchAd(self.client, self.base_url)

    @task
    def ffff_shortPlay_unlockByCoin(self):
        api.ffff_shortPlay_unlockByCoin(self.client, self.base_url)

    @task
    def ffff_shortPlay_unlockEpisodeByGold(self):
        api.ffff_shortPlay_unlockEpisodeByGold(self.client, self.base_url)
