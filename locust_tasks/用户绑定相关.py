"""
Locust user for tag: 用户绑定相关
"""
from locust import HttpUser, task, between
from api_clients import 用户绑定相关_api as api


class FfffUserUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_user_sendEmail(self):
        api.ffff_user_sendEmail(self.client, self.base_url)

    @task
    def ffff_user_bindList(self):
        api.ffff_user_bindList(self.client, self.base_url)

    @task
    def ffff_user_addBind(self):
        api.ffff_user_addBind(self.client, self.base_url)

    @task
    def ffff_user_bindByPhone(self):
        api.ffff_user_bindByPhone(self.client, self.base_url)

    @task
    def ffff_user_bindByEmail(self):
        api.ffff_user_bindByEmail(self.client, self.base_url)
