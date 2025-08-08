"""
Locust user for tag: 观看历史记录
"""
from locust import HttpUser, task, between
from api_clients import 观看历史记录_api as api


class FfffWatchhistoryUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_watchHistory_saveWatchHistory(self):
        api.ffff_watchHistory_saveWatchHistory(self.client, self.base_url)

    @task
    def ffff_watchHistory_delWatchHistory(self):
        api.ffff_watchHistory_delWatchHistory(self.client, self.base_url)

    @task
    def ffff_watchHistory_getWatchHistoryList(self):
        api.ffff_watchHistory_getWatchHistoryList(self.client, self.base_url)
