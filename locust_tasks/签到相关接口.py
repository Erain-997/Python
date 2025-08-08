"""
Locust user for tag: 签到相关接口
"""
from locust import HttpUser, task, between
from api_clients import 签到相关接口_api as api


class FfffSigUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_sig_signRecord(self):
        api.ffff_sig_signRecord(self.client, self.base_url)

    @task
    def ffff_sig_sign(self):
        api.ffff_sig_sign(self.client, self.base_url)
