# _*_coding:utf-8_*_
# Author：zyr
# Time：2025/1/10
class UserData:
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)


user_data_store = UserData()
