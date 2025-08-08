from locust import HttpUser, task, between
from utils.common import COMMON_HEADERS
from utils.http_client import HttpClientWrapper
from utils.login import login_and_get_token
from utils import report_saver
import time
import logging


class AuthAPIUser(HttpUser):
    wait_time = between(2, 4)
    host = "https://api-stress.ffff.team"

    def on_start(self):
        max_retries = 5
        retry_interval = 1  # 秒
        for i in range(max_retries):
            try:
                token, _, _, _ = login_and_get_token(self.client)
                if token:
                    self.http = HttpClientWrapper(
                        self.client, token=token, default_headers=COMMON_HEADERS
                    )
                    logging.info(f"[User {id(self)}] 登录成功")
                    return
                else:
                    logging.warning(f"[User {id(self)}] 登录失败, 返回空 token")
            except Exception as e:
                logging.error(f"[User {id(self)}] 登录异常: {e}")

            time.sleep(retry_interval)

        # 如果重试完还不成功, 打印并标记为空盒子
        logging.critical(f"[User {id(self)}] 登录失败,  用户将无法执行后续任务")
        self.http = None

    @task
    def sign_record(self):
        self.http.post("/ffff/sig/signRecord", api_name="signRecord")

    @task
    def get_tab_home_data(self):
        self.http.post(
            "/ffff/homeData/encrypt/getTabHomeData",
            api_name="getTabHomeData",
            data={"newbieShowType": 1},
        )

    @task
    def get_user_balance(self):
        self.http.post("/ffff/user/getUserBalance", api_name="getUserBalance")

    @task
    def save_watch_history(self):
        self.http.post(
            "/ffff/watchHistory/saveWatchHistory", api_name="saveWatchHistory",
            data={"dramaId": 410360, "watchTime": 999}
        )

    @task
    def get_config_by_key(self):
        self.http.post(
            "/ffff/system/getConfigByKey",
            api_name="getConfigByKey",
            data={"key": "ios.start.config"},
        )

    # todo
    @task
    def lp_report(self):
        self.http.post(
            "/ffff/clickAd/lpReport",
            api_name="lpReport",
            data={"adId": 1, "type": "click"},
        )

    # #/ffff/shortPlay/unlockByCoin  重置解锁状态
    # @task
    # def unlock_by_coin(self):
    #     self.http.post(
    #         "/ffff/shortPlay/unlockByCoin",
    #         api_name="unlockByCoin",
    #         data={"coin": 1},
    # )
    @task
    def get_page_config(self):
        self.http.get(
            "/ffff/campaignLink/getPageConfig",
            api_name="getPageConfig",
        )
