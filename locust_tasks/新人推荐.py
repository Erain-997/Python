"""
Locust user for tag: 新人推荐
"""
from locust import HttpUser, task, between
from api_clients import 新人推荐_api as api


class FfffRecommendUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_recommend_checkNewUserRecommend(self):
        api.ffff_recommend_checkNewUserRecommend(self.client, self.base_url)

    @task
    def ffff_recommend_getNewUserRecommendInfo(self):
        api.ffff_recommend_getNewUserRecommendInfo(self.client, self.base_url)

    @task
    def ffff_recommend_getNewUserTimeInfo(self):
        api.ffff_recommend_getNewUserTimeInfo(self.client, self.base_url)
