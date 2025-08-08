import uuid
import pytest
import allure

from api_clients.登录接口_test import ffff_login_initLogin
from api_clients.短剧详情相关接口_test import ffff_shortPlay_shortPlayDetail
from utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(name=__name__)


@allure.epic("登录模块")
@allure.feature("用户登录")
class TestLogin:
    @pytest.fixture(scope="function", autouse=True)
    def environment(self):
        LoggerManager().init(filename="login")
        self.logger = LoggerManager().get_logger(name=__name__, )
        with allure.step("用户登录"):
            self.login()
        yield
        with allure.step("用例环境清理"):
            logger.info("用例环境清理")

    def login(self):
        self.client, resp = ffff_login_initLogin(deviceId=str(uuid.uuid4()))
        if resp["status"] != 0:
            pytest.fail(f"Login failed: {resp}")
        self.client.token = resp["data"]["token"]

    @allure.title("剧集解锁成功")
    def test_ffff_shortPlay_shortPlayDetail(self):
        ffff_shortPlay_shortPlayDetail(self.client, 728600, 8)
