"""
Locust user for tag: feed流观看历史记录
"""
from locust import HttpUser, task, between
from api_clients import feed流观看历史记录_api as api


class FfffFeedwatchhistoryUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_feedWatchHistory_saveWatchHistory(self):
        api.ffff_feedWatchHistory_saveWatchHistory(self.client, self.base_url)
