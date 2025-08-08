"""
Locust user for tag: 获取服务器时间_时间校正
"""
from locust import HttpUser, task, between
from api_clients import 获取服务器时间_时间校正_api as api


class FfffCorrectionUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_correction_time(self):
        api.ffff_correction_time(self.client, self.base_url)
