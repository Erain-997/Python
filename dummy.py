# -*- encoding=utf8 -*-
# Time：'2022/10/31'
# __author__ = "Erain"

from locust import User, task

class Dummy(User):
    @task(20)
    def hello(self):
        pass