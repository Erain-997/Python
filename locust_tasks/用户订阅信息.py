"""
Locust user for tag: 用户订阅信息
"""
from locust import HttpUser, task, between
from api_clients import 用户订阅信息_api as api


class FfffSubscriptionUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_subscription_android(self):
        api.ffff_subscription_android(self.client, self.base_url)

    @task
    def ffff_subscription_iosV2(self):
        api.ffff_subscription_iosV2(self.client, self.base_url)

    @task
    def ffff_subscription(self):
        api.ffff_subscription(self.client, self.base_url)
