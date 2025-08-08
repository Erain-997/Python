from locust import HttpUser, task, between

from utils.report_saver import start_report_monitoring
from utils.logger_manager import LoggerManager
from locust_cases.behavior.login import init_user_http


class SaveWatchHistory(HttpUser):
    wait_time = between(0.5, 1)
    host = "https://api-stress.ffff.team"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        filename = "SaveWatchHistory"
        self.logger = LoggerManager().init(filename)
        self.http = init_user_http(self.client)
        start_report_monitoring(filename)

    @task
    def save_watch_history(self):
        if self.http:
            self.http.post(
                "/ffff/feedWatchHistory/saveWatchHistory",
                api_name="saveWatchHistory",
                data={"dramaId": 410360, "watchTime": 999},
            )
