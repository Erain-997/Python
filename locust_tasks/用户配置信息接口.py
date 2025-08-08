"""
Locust user for tag: 用户配置信息接口
"""
from locust import HttpUser, task, between
from api_clients import 用户配置信息接口_api as api


class FfffUserUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_user_config(self):
        api.ffff_user_config(self.client, self.base_url)

    @task
    def ffff_user_config(self):
        api.ffff_user_config(self.client, self.base_url)
