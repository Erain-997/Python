"""
Locust user for tag: 累计看剧时长任务相关接口
"""
from locust import HttpUser, task, between
from api_clients import 累计看剧时长任务相关接口_api as api


class FfffWatchtimetaskUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_watchTimeTask_getTaskConfig(self):
        api.ffff_watchTimeTask_getTaskConfig(self.client, self.base_url)

    @task
    def ffff_watchTimeTask_receiveReward(self):
        api.ffff_watchTimeTask_receiveReward(self.client, self.base_url)
