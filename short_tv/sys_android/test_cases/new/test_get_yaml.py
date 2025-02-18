import os

import yaml

from common.utils.path_config import android


class TopUpDataHandler:
    def __init__(self):
        self.yaml_file_path = f"{android.test_datas_dir}/top_up_modules.yaml"
        self.coins_data = []
        self.bonus_data = []
        self.top_up_sku_coins = []
        self.top_up_sku_bonus = []

        # 创建文件（如果文件不存在）
        if not os.path.exists(self.yaml_file_path):
            with open(self.yaml_file_path, 'w') as file:
                data = {
                    "TopUpPage": {
                        "top_up_sku_coins": ['0'],
                        "top_up_sku_bonus": ['0'],
                        "top_up_coins1": ['xpath', '0'],
                        "top_up_coins2": ['xpath', '0'],
                        "top_up_coins3": ['xpath', '0'],
                        "top_up_coins4": ['xpath', '0'],
                        "top_up_coins5": ['xpath', '0'],
                        "top_up_coins6": ['xpath', '0'],
                        "top_up_coins7": ['xpath', '0'],
                        "top_up_bonus1": ['0'],
                        "top_up_bonus3": ['0'],
                        "top_up_bonus4": ['0'],
                        "top_up_bonus5": ['0'],
                        "top_up_bonus6": ['0'],
                        "top_up_bonus7": ['0'],
                        "top_up_bonus2": ['0']
                    }
                }
                yaml.dump(data, file, default_flow_style=False)

        # 初始化时读取 YAML 文件内容
        self._load_data()

    def _load_data(self):
        # 读取 YAML 文件内容
        with open(self.yaml_file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        # 将数据转换为列表
        top_up_page_data = data['TopUpPage']

        # 提取 coins 和 bonus 数据
        self.coins_data = []
        self.bonus_data = []
        self.top_up_sku_coins = []
        self.top_up_sku_bonus = []
        self.gp_sku_id = []

        for key, value in top_up_page_data.items():
            if key.startswith('gp_skuId'):
                self.gp_sku_id.append(value[0])
            if key.startswith('top_up_coins'):
                if len(value) > 1:
                    self.coins_data.append(value[1])
                else:
                    self.coins_data.append(value[0])
            elif key.startswith('top_up_bonus'):
                if len(value) > 1:
                    self.bonus_data.append(value[1])
                else:
                    self.bonus_data.append(value[0])
            elif key.startswith('top_up_sku_coins'):
                self.top_up_sku_coins.append(value)
            elif key.startswith('top_up_sku_bonus'):
                self.top_up_sku_bonus.append(value)

    def refresh_data(self):
        # 刷新数据
        self._load_data()
