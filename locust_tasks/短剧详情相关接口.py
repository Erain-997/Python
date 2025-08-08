"""
Locust user for tag: 短剧详情相关接口
"""
from locust import HttpUser, task, between
from api_clients import 短剧详情相关接口_api as api


class FfffShortplayUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_shortPlay_shortPlayDetail(self):
        api.ffff_shortPlay_shortPlayDetail(self.client, self.base_url)

    @task
    def ffff_shortPlay_getTopRechargeShortPlays(self):
        api.ffff_shortPlay_getTopRechargeShortPlays(self.client, self.base_url)

    @task
    def ffff_shortPlay_getSearchCarouselPlays(self):
        api.ffff_shortPlay_getSearchCarouselPlays(self.client, self.base_url)

    @task
    def ffff_shortPlay_getPopularShortPlay(self):
        api.ffff_shortPlay_getPopularShortPlay(self.client, self.base_url)
