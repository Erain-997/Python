"""
Locust user for tag: 落地页上报
"""
from locust import HttpUser, task, between
from api_clients import 落地页上报_api as api


class FfffClickadUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_clickAd_lpReport(self):
        api.ffff_clickAd_lpReport(self.client, self.base_url)
