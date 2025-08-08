import threading
import time
from locust import HttpUser, task, between
from locust.exception import StopUser

from locust_cases.behavior.login import init_user_http
from utils.common import COMMON_HEADERS
from utils.http_client import HttpClientWrapper

from utils.login import login_and_get_token
from utils.my_mysql import check_user_unlock_counts, check_db_connection_leak
from utils.logger_manager import LoggerManager

logger = LoggerManager().init(filename="UnlockEpisodeByWatchAd")


def leak_monitor_loop(interval_sec=10):
    while True:
        try:
            leak = check_db_connection_leak()
            if leak:
                logger.warning(
                    "[Leak Monitor] WARNING: Database connection leak detected!"
                )
            else:
                logger.info("[Leak Monitor] No leak detected.")
        except Exception as e:
            logger.error(f"[Leak Monitor] Exception in leak check: {e}")
        time.sleep(interval_sec)


# 启动后台监控线程（确保只启动一次）
def start_leak_monitor():
    monitor_thread = threading.Thread(target=leak_monitor_loop, args=(10,), daemon=True)
    monitor_thread.start()


class UnlockEpisodeByWatchAd(HttpUser):
    wait_time = between(0.5, 1)
    host = "https://api-stress.ffff.team"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.episode_num = 8
        self.http = init_user_http(self.client)

    @task
    def get_tab_home_data(self):
        if not self.http:
            raise StopUser(f"[User {id(self)}] 无有效 http 客户端, 退出用户")

        if self.episode_num >= 8 + 22:  # 上限是20集, 多请求几集看能不能成功
            logger.info(f"[User {id(self)}] 已完成所有集数, 退出用户")
            # 校验
            check_user_unlock_counts(self.http.user_id)
            # 重置用户继续
            self.on_start()
            time.sleep(0.5)

        try:
            resp = self.http.post(
                "/ffff/shortPlay/unlockEpisodeByWatchAd",
                data={"shortPlayId": 728600, "episodeNum": self.episode_num},
                expected_status=[20007, 20028],
            )
            json_data = resp.json()
            if json_data.get("status") != 0:
                logger.warning(
                    f"❌ 解锁第 {self.episode_num} 集失败: traceid: {self.http.headers['traceid']}, user_id: {self.http.user_id}"
                )
                logger.error(f"[User {id(self)}] 解锁第 {self.episode_num} 集失败")
            if json_data.get("status") == 20028:
                self.episode_num += 99
            self.episode_num += 1
        except Exception as e:
            logger.error(f"[User {id(self)}] 请求异常: {e}")


# locust 启动时，先启动后台监控线程
start_leak_monitor()
