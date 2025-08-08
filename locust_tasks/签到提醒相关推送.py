"""
Locust user for tag: 签到提醒相关推送
"""
from locust import HttpUser, task, between
from api_clients import 签到提醒相关推送_api as api


class FfffPushUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_push_sign_signReminder(self):
        api.ffff_push_sign_signReminder(self.client, self.base_url)

    @task
    def ffff_push_sign_missSignReminder(self):
        api.ffff_push_sign_missSignReminder(self.client, self.base_url)
