"""
Locust user for tag: _p_
"""
from locust import HttpUser, task, between
from api_clients import _p__api as api


class FfffBonusrecordUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_bonusRecord_getBonusTotal(self):
        api.ffff_bonusRecord_getBonusTotal(self.client, self.base_url)
