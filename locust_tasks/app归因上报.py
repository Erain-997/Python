"""
Locust user for tag: app归因上报
"""
from locust import HttpUser, task, between
from api_clients import app归因上报_api as api


class FfffAdmatchUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_adMatch_deepLinkReport(self):
        api.ffff_adMatch_deepLinkReport(self.client, self.base_url)
