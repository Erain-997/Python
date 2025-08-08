"""
Locust user for tag: 奖励币过期推送接口
"""
from locust import HttpUser, task, between
from api_clients import 奖励币过期推送接口_api as api


class FfffPushUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_push_bonusExpiring_getPushInfo(self):
        api.ffff_push_bonusExpiring_getPushInfo(self.client, self.base_url)
