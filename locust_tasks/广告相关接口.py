"""
Locust user for tag: 广告相关接口
"""
from locust import HttpUser, task, between
from api_clients import 广告相关接口_api as api


class FfffAdUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_ad_watchAdUnLockComplete(self):
        api.ffff_ad_watchAdUnLockComplete(self.client, self.base_url)

    @task
    def ffff_ad_signWatchAd(self):
        api.ffff_ad_signWatchAd(self.client, self.base_url)
