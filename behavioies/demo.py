# -*- encoding=utf8 -*-
# Time：'2022/4/8'
# __author__ = "2021099"

from internal.engine.behavior_func import BehaviorFunc
from time import sleep
import allure


class TestCases(BehaviorFunc):
    def case_1(self):
        # 获取操作类型
        self.client_func("")

        # 这是直接写方法
        # with allure.step("进入关卡"):
        #     self.node_path('(text="STAGE")').click()
        # sleep(1)
        # with allure.step("退出关卡"):
        #     self.node_path('(nameMatches="BackButton*")').click()

        # 这是嵌套了步骤打印的

        self.execute("点击关卡", '(text="STAGE")', "click", "")
        sleep(2)
        self.execute("退出关卡", '(nameMatches="BackButton*")', "click", "")
