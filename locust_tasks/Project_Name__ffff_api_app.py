"""
Locust user for tag: Project_Name__ffff_api_app
"""
from locust import HttpUser, task, between
from api_clients import Project_Name__ffff_api_app_api as api


class FfffDramainfoUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_dramaInfo_dramaDetailV2(self):
        api.ffff_dramaInfo_dramaDetailV2(self.client, self.base_url)

    @task
    def ffff_dramaInfo_encrypt_dramaDetail(self):
        api.ffff_dramaInfo_encrypt_dramaDetail(self.client, self.base_url)

    @task
    def ffff_dramaInfo_getDramaIdByShortPlayId(self):
        api.ffff_dramaInfo_getDramaIdByShortPlayId(self.client, self.base_url)
