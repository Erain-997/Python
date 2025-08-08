"""
Locust user for tag: 收藏相关接口
"""
from locust import HttpUser, task, between
from api_clients import 收藏相关接口_api as api


class FfffCollectUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_collect_cancelCollect(self):
        api.ffff_collect_cancelCollect(self.client, self.base_url)

    @task
    def ffff_collect_batchCancelCollect(self):
        api.ffff_collect_batchCancelCollect(self.client, self.base_url)

    @task
    def ffff_collect_collectOp(self):
        api.ffff_collect_collectOp(self.client, self.base_url)

    @task
    def ffff_collect_collectList(self):
        api.ffff_collect_collectList(self.client, self.base_url)
