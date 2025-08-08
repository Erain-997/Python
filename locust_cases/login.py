from locust import HttpUser, task, between
from utils.common import COMMON_HEADERS, generate_device_id
from utils.http_client import HttpClientWrapper
from utils.login import login_and_get_token

SECRET_KEY = "h7zkahQvCb05lYZvt11lYbmpndozqDZy66V8krAxEfhDBwjYpuDyp2iAukogTl3EyZFTW57X2zRDSkxg+ODSFF5asZdoVV0WCFLXpHMkxu8dX0UD2ZmsL44btSmdgFa+h8Caj/0RCt+GvgW7z5Gxpzs+Yxv0uCiUdUS//EhV6MY="


class LoginStressUser(HttpUser):
    wait_time = between(2, 4)
    host = "https://api-stress.ffff.team"

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.http = None

    def on_start(self):
        token, _ = login_and_get_token(self.client)
        self.http = HttpClientWrapper(
            self.client, token=token, default_headers=COMMON_HEADERS
        )

    @task
    def haha(self):
        pass
