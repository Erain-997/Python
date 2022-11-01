from locust import HttpUser, TaskSet, task, between


class UserBehaviour(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    @task(1)
    def login(self):
        self.client.post("/Login", {"username": "cxm", "password": "123456"})

    @task(2)
    def logout(self):
        self.client.post("/Logout", {"username": "cxm", "password": "123456"})

    # @task(2)
    def index(self):
        self.client.get("/")

    # @task(1)
    def profile(self):
        self.client.get("/profile")


class WebsiteUser(HttpUser):
    task_set = UserBehaviour
    wait_time = between(5, 9)
