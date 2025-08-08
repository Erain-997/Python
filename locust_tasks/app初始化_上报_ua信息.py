"""
Locust user for tag: app初始化_上报_ua信息
"""
from locust import HttpUser, task, between
from api_clients import app初始化_上报_ua信息_api as api


class FfffAppreportUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_appReport_lpReport(self):
        api.ffff_appReport_lpReport(self.client, self.base_url)
