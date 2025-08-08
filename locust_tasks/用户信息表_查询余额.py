"""
Locust user for tag: 用户信息表_查询余额
"""
from locust import HttpUser, task, between
from api_clients import 用户信息表_查询余额_api as api


class FfffUserUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_user_reportDefaultShortPlay(self):
        api.ffff_user_reportDefaultShortPlay(self.client, self.base_url)

    @task
    def ffff_user_getFBUserInfo(self):
        api.ffff_user_getFBUserInfo(self.client, self.base_url)

    @task
    def ffff_user_setUserLanguage(self):
        api.ffff_user_setUserLanguage(self.client, self.base_url)

    @task
    def ffff_user_reportUserAdInfo(self):
        api.ffff_user_reportUserAdInfo(self.client, self.base_url)

    @task
    def ffff_user_reportActiveTime(self):
        api.ffff_user_reportActiveTime(self.client, self.base_url)

    @task
    def ffff_user_getUserBalance(self):
        api.ffff_user_getUserBalance(self.client, self.base_url)

    @task
    def ffff_user_getAnotherUserInfo(self):
        api.ffff_user_getAnotherUserInfo(self.client, self.base_url)

    @task
    def ffff_user_migrateAccount(self):
        api.ffff_user_migrateAccount(self.client, self.base_url)
