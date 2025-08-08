"""
Locust user for tag: SendMessageController
"""
from locust import HttpUser, task, between
from api_clients import SendMessageController_api as api


class FfffMessageUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_message_sendMessageVerificationCode(self):
        api.ffff_message_sendMessageVerificationCode(self.client, self.base_url)
