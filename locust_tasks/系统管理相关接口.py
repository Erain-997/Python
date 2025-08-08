"""
Locust user for tag: 系统管理相关接口
"""
from locust import HttpUser, task, between
from api_clients import 系统管理相关接口_api as api


class FfffSystemUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_system_getConfigByKey(self):
        api.ffff_system_getConfigByKey(self.client, self.base_url)

    @task
    def ffff_system_getUpgradeVersionManageInfo(self):
        api.ffff_system_getUpgradeVersionManageInfo(self.client, self.base_url)
