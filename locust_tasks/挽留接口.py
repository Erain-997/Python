"""
Locust user for tag: 挽留接口
"""
from locust import HttpUser, task, between
from api_clients import 挽留接口_api as api


class FfffRetainUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_retain_getComingSoonShortPlays(self):
        api.ffff_retain_getComingSoonShortPlays(self.client, self.base_url)

    @task
    def ffff_retain_getExitRetainShortPlays(self):
        api.ffff_retain_getExitRetainShortPlays(self.client, self.base_url)
