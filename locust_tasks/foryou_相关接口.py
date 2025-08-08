"""
Locust user for tag: foryou_相关接口
"""
from locust import HttpUser, task, between
from api_clients import foryou_相关接口_api as api


class FfffForyouUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_forYou_encrypt_getForYouListOnlyOne(self):
        api.ffff_forYou_encrypt_getForYouListOnlyOne(self.client, self.base_url)

    @task
    def ffff_forYou_encrypt_getForYouListPageNewV2(self):
        api.ffff_forYou_encrypt_getForYouListPageNewV2(self.client, self.base_url)
