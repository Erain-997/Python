from locust import HttpUser, TaskSet, between

url = "http://10.6.27.69:6060/test"


def login(l):
    l.client.post(url, {})


def logout(l):
    l.client.post("/logout", {"username": "ellen_key", "password": "education"})


def index(l):
    l.client.get("/")


def profile(l):
    l.client.get("/profile")


# 用户
class UserBehavior(TaskSet):
    tasks = {index: 2, profile: 1}

    # 用户行为
    def on_start(self):
        login(self)

    def on_stop(self):
        logout(self)

    on_start()
    # print(11)


# 继承locust类,并添加client属性,用于发出http请求
class WebsiteUser(HttpUser):
    task_set = UserBehavior
    wait_time = between(5.0, 9.0)
