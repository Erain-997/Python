import allure
import yaml

from common.utils.path_config import android


# mock数据的记录, 写入到文件里
class MockData:
    def __init__(self, ip=None):
        # Mock域名
        self.host = "test-api.shorttv.live"
        # 检查文件是否存在
        self.config = None
        self.file_path = f'{android.mock_dir}/mock_{ip}.yaml'

    @allure.step("mock修改数据")
    def mock_data(self, case_mame, api_path, data):
        """
        :param case_mame: 用例名称, 直接用case函数名
        :param api_path: 接口地址, 格式: /app/abtest/getAbtestParams
        :param api_path: 初始值
        :param data: 需要mock的值
        :return:
        """

        # 记录
        if not self.config:
            self.config = {"TARGET_HOST": self.host}
        if case_mame not in self.config:
            self.config[case_mame] = {api_path: data}
        elif case_mame in self.config and api_path in self.config[case_mame]:
            for key, value in data.items():
                self.config[case_mame][api_path][key] = value

        # 写回
        with open(self.file_path, 'w') as file:
            yaml.safe_dump(self.config, file, default_flow_style=False)

        # for case_name, api_info in self.config.items():
        #     if case_name != "TARGET_HOST":
        #         for api_path, values in api_info.items():
        #             for k, v in values.items():
        #                 return k, v

        # print("YAML file updated successfully.")

    def get_config(self):
        with open(self.file_path, 'r') as file:
            self.config = yaml.safe_load(file)
            return self.config


if __name__ == '__main__':
    a = MockData()
    a.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams", {"and_task_test": "0", "and_task_test2": "999"})
