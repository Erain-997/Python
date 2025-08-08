"""
Locust user for tag: 支付相关
"""
from locust import HttpUser, task, between
from api_clients import 支付相关_api as api


class FfffPayUser(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"

    @task
    def ffff_pay_android_recover(self):
        api.ffff_pay_android_recover(self.client, self.base_url)

    @task
    def ffff_pay_iOS_recover(self):
        api.ffff_pay_iOS_recover(self.client, self.base_url)

    @task
    def ffff_pay_localDollarCurrencyConversion(self):
        api.ffff_pay_localDollarCurrencyConversion(self.client, self.base_url)

    @task
    def ffff_pay_android_coinSkuBuy(self):
        api.ffff_pay_android_coinSkuBuy(self.client, self.base_url)

    @task
    def ffff_pay_iOS_coinSkuBuy(self):
        api.ffff_pay_iOS_coinSkuBuy(self.client, self.base_url)
