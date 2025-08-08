import pytest
import allure

from api_cases.tools.tools import login
from api_clients.签到相关接口_test import ffff_sig_signRecord
from api_clients.首页推荐_轮播相关接口_test import ffff_homeData_encrypt_getTabHomeData
from utils.logger_manager import LoggerManager


# @allure.epic("登录模块")
@allure.feature("高频接口汇总")
class TestTop:
    @pytest.fixture(scope="function", autouse=True)
    def environment(self):
        LoggerManager().init(filename="TestTop")
        self.logger = LoggerManager().get_logger(name=__name__)
        with allure.step("用户登录"):
            self.client = login()
        yield
        with allure.step("用例环境清理"):
            self.logger.info("用例环境清理")

    @allure.title("查看签到记录")
    def test_sig_signRecord_success(self):
        ffff_sig_signRecord(self.client)

    @allure.title("获取tab化的首页数据")
    def test_homeData_encrypt_getTabHomeData_success(self):
        ffff_homeData_encrypt_getTabHomeData(self.client)


import pytest
import allure

from api_cases.tools.tools import login
from api_clients.签到相关接口_test import ffff_sig_signRecord
from api_clients.首页推荐_轮播相关接口_test import ffff_homeData_encrypt_getTabHomeData
from utils.logger_manager import LoggerManager


# @allure.epic("登录模块")
@allure.feature("高频接口汇总")
class TestTop:
    @pytest.fixture(scope="function", autouse=True)
    def environment(self):
        LoggerManager().init(filename="TestTop")
        self.logger = LoggerManager().get_logger(name=__name__)
        with allure.step("用户登录"):
            self.client = login()
        yield
        with allure.step("用例环境清理"):
            self.logger.info("用例环境清理")

    @allure.title("查看签到记录")
    def test_sig_signRecord_success(self):
        ffff_sig_signRecord(self.client)

    @allure.title("获取tab化的首页数据")
    def test_homeData_encrypt_getTabHomeData_success(self):
        ffff_homeData_encrypt_getTabHomeData(self.client)
