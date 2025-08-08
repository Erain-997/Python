"""
Locust user for tag: 首页推荐_轮播相关接口
"""
from locust import HttpUser, task, between
from api_clients import 首页推荐_轮播相关接口_api as api


class FfffHomedataUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_homeData_encrypt_getBannerMore(self):
        api.ffff_homeData_encrypt_getBannerMore(self.client, self.base_url)

    @task
    def ffff_homeData_encrypt_getTabHomeData(self):
        api.ffff_homeData_encrypt_getTabHomeData(self.client, self.base_url)

    @task
    def ffff_homeData_getHomeConfig(self):
        api.ffff_homeData_getHomeConfig(self.client, self.base_url)
