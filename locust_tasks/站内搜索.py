"""
Locust user for tag: 站内搜索
"""
from locust import HttpUser, task, between
from api_clients import 站内搜索_api as api


class FfffSearchUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_search_hotSearch(self):
        api.ffff_search_hotSearch(self.client, self.base_url)

    @task
    def ffff_search_searchPage(self):
        api.ffff_search_searchPage(self.client, self.base_url)
