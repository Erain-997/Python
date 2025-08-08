"""
Locust user for tag: 任务相关接口
"""
from locust import HttpUser, task, between
from api_clients import 任务相关接口_api as api


class FfffApptaskUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_appTask_getAppTaskList(self):
        api.ffff_appTask_getAppTaskList(self.client, self.base_url)

    @task
    def ffff_appTask_receiveRewards(self):
        api.ffff_appTask_receiveRewards(self.client, self.base_url)
