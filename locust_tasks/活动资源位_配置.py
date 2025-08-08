"""
Locust user for tag: 活动资源位_配置
"""
from locust import HttpUser, task, between
from api_clients import 活动资源位_配置_api as api


class FfffActivityresourceUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_activityResource_resourceListByTypes(self):
        api.ffff_activityResource_resourceListByTypes(self.client, self.base_url)
