"""
Locust user for tag: 用户设备信息_相关接口
"""
from locust import HttpUser, task, between
from api_clients import 用户设备信息_相关接口_api as api


class FfffUserregistrationtokenUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_userRegistrationToken_report(self):
        api.ffff_userRegistrationToken_report(self.client, self.base_url)
