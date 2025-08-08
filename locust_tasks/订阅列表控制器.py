"""
Locust user for tag: 订阅列表控制器
"""
from locust import HttpUser, task, between
from api_clients import 订阅列表控制器_api as api


class FfffSubscriptionUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_subscription_getProductListV3(self):
        api.ffff_subscription_getProductListV3(self.client, self.base_url)
