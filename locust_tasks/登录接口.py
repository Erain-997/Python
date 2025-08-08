"""
Locust user for tag: 登录接口
"""
from locust import HttpUser, task, between
from api_clients import 登录接口_api as api


class FfffLoginUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_login_tripartiteLogin(self):
        api.ffff_login_tripartiteLogin(self.client, self.base_url)

    @task
    def ffff_login_initLogin(self):
        api.ffff_login_initLogin(self.client, self.base_url)

    @task
    def ffff_login_getUserInfo(self):
        api.ffff_login_getUserInfo(self.client, self.base_url)

    @task
    def ffff_login_deleteAccount(self):
        api.ffff_login_deleteAccount(self.client, self.base_url)

    @task
    def ffff_login_loginOut(self):
        api.ffff_login_loginOut(self.client, self.base_url)
