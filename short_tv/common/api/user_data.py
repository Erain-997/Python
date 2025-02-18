import json

from common.api.rc4_kt import RC4Kit
from common.utils.cmd_tools import find_log_value_by_key
from common.utils.path_config import android


class UserData:
    def __init__(self):
        self.file_path = f'{android.api_dir}/flow_data.json'

        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.api_data = json.load(f)

    def get_data(self, log_path, url):
        for index, flow in self.api_data.items():
            if flow['request']['url'] == url:
                result_data = json.loads(flow['response']['body'].encode('utf-8'))['result']
                pwd = find_log_value_by_key(log_path, "[AppLogger][StringUtil]: [, , 0]")
                # print("***********************result_data*************\n", result_data, "\n************************************\n")
                # print("***************************pwd*********\n", pwd, "\n************************************\n")
                decrypted = RC4Kit.decrypt(
                    result_data,
                    pwd,
                )
                return decrypted

    def get_authorization(self):
        for index, flow in self.api_data.items():
            return flow['request']['headers']['Authorization']


if __name__ == '__main__':
    a = UserData()
    print(a.get_data("http://test-api.shorttv.live/app/hiUserDevice/reportUserDevice"))
    res = a.get_data("http://test-api.shorttv.live/app/hiUserDevice/reportUserDevice")
    res_j = json.loads(res.encode('utf-8'))
    print(res_j['result'])
