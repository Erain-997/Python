"""
Locust user for tag: sku_相关接口
"""
from locust import HttpUser, task, between
from api_clients import sku_相关接口_api as api


class FfffSkuUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_sku_getCoinsStoreListAndAdInfoBySkuModel(self):
        api.ffff_sku_getCoinsStoreListAndAdInfoBySkuModel(self.client, self.base_url)

    @task
    def ffff_sku_getUnlockedPageSkuList(self):
        api.ffff_sku_getUnlockedPageSkuList(self.client, self.base_url)

    @task
    def ffff_sku_getCoinsStoreListBySkuModel(self):
        api.ffff_sku_getCoinsStoreListBySkuModel(self.client, self.base_url)
