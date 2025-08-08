import pytest
import allure

from api_clients.登录接口_test import ffff_login_initLogin
from utils.logger_manager import LoggerManager


@allure.epic("登录模块")
@allure.feature("用户登录")
class TestLogin:
    @pytest.fixture(scope="function", autouse=True)
    def setup_method(self):
        LoggerManager().init(filename="login")
        self.logger = LoggerManager().get_logger(name=__name__, )
        with allure.step("用例执行初始化"):
            self.logger.info("用例执行初始化")
        yield
        with allure.step("用例环境清理"):
            self.logger.info("用例环境清理")

    @allure.title("用户登录成功")
    def test_login_success(self):
        ffff_login_initLogin(deviceId=None)

    @allure.title("用户登录失败")
    def test_login_fail(self):
        # todo 传字典还是字段
        #### todo  还没搞好header怎么处理比较好
        ffff_login_initLogin(expected={"status": 1})
