# -*- encoding=utf8 -*-
# Time：'2022/10/31'
# __author__ = "Erain"

from locust import HttpUser, TaskSet, task, between, SequentialTaskSet


# 继承 locust 类 TaskSet 属性
class UserBehaviorRandom(TaskSet):
    # weight = 1  # 设置权重
    def on_start(self):  # 启动前置
        print("Executing on_start")

    def on_stop(self):  # 优雅关闭
        print("Executing on_stop")

    # 声明任务
    @task
    def test_login(self):
        print("login")
        res = self.client.post("/Login", json={"username": "cxm", "password": "123456"})
        print(res)

    @task
    def test_logout(self):
        print("logout")
        res = self.client.post("/Logout", json={"username": "cxm", "password": "123456"})
        print(res)


# 继承locust类TaskSet属性
class UserBehaviorSequential(SequentialTaskSet):
    # weight = 1  # 设置权重
    def on_start(self):  # 启动前置
        print("Executing on_start")

    def on_stop(self):  # 优雅关闭
        print("Executing on_stop")

    # 声明任务
    @task
    def test_login(self):
        print("login")
        res = self.client.post("/Login", json={"username": "erain", "password": "123456"})
        print("Response status code:", res.status_code)
        print("Response text:", res.text)
        # print("Response content:", res.content) # 非明文

    @task
    def test_logout(self):
        print("logout")
        with self.client.post("/Logout", json={"username": "erain", "password": "123456"}, catch_response=True) as res:
            if res.status_code == 200:
                res.success()
                print(res.text)
            else:
                res.failure("No Response")


class WebSiteUser(HttpUser):
    host = "http://10.6.27.69:6065"
    # tasks = [UserBehaviorRandom]  # 如果将tasks属性指定为列表，那么每次执行任务时，都将从tasks属性中随机选择该任务。
    tasks = [UserBehaviorSequential]  # 顺序执行task
    # min_wait = 2000
    # max_wait = 5000
    wait_time = between(3, 5)  # 直接设置执行间隔
