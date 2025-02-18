# _*_coding:utf-8_*_
# Author：zyr
# Time：2025/1/10

import functools
import inspect

import allure


class Decorate:

    def __init__(self, collection_name, case_name):
        self.collection_name = collection_name
        self.case_name = case_name
        # self.tear_down_collection = []
        # self.case_step_collection = []
        # self.setup_step_collection = []

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(instance, *args, **kwargs):
            # 确保 instance 是类的实例
            step_collection = getattr(instance, self.collection_name, None)
            if step_collection is not None:
                step_collection.append(self.case_name)

            # 包裹 Allure 步骤
            with allure.step(self.case_name):
                return func(instance, *args, **kwargs)

        return wrapper

    def __enter__(self):
        # 动态获取当前对象的步骤集合
        frame = inspect.currentframe().f_back
        instance = frame.f_locals.get("self", None)
        if instance:
            step_collection = getattr(instance, self.collection_name, None)
            if step_collection is not None:
                step_collection.append(self.case_name)

        # 开始 Allure 步骤 todo 还有优化空间, 进一步整理成动态, 和扩展标签
        self.allure_step = allure.step(self.case_name)
        self.allure_step.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 结束 Allure 步骤
        self.allure_step.__exit__(exc_type, exc_val, exc_tb)

    @classmethod
    def collect_setup(cls, case_name):
        return cls("setup_step_collection", case_name)

    @classmethod
    def collect_teardown(cls, case_name):
        return cls("tear_down_collection", case_name)

    @classmethod
    def collect_test(cls, case_name):
        return cls("case_step_collection", case_name)

    @classmethod
    def collect_check(cls, case_name):
        return cls("check_collection", case_name)
