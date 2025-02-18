import json
import re

import requests

from common.utils.path_config import android


class ApiAll:
    def __init__(self):
        self.file_path = f'{android.api_dir}/api_all.json'
        self.yapi_login_url = "https://yapi.shorttv.live/api/user/login"
        self.yapi_login_data = {"email": "xxx@163.com", "password": "yapi.pro"}
        self.yapi_login_download = 'https://yapi.shorttv.live/api/plugin/export?type=json&pid=11&status=all&isWiki=false'
        self.host = "http://test-api.shorttv.live"

        self.headers = {
            'session_id': '1651892832746_7849d1681f37cb9c8d158afd1f38a93f',
            'TraceId': 'a628a07d-5f3d-4c3c-9338-be095d042261',
            'Authorization': '1pkeeporqzC4ou7Jk1fWnuZOfTmmPzFXbRKqbYUFKCbaHJFVMkjd0nlWvoPxQjUXOP3tkiCXSNnXb6JYwd05IX3woU+Nz+Q8PAYMA8YSwEqaUxaSuyALXzUfZQimNNY9ejQmLkzfRBLs5k6laVduMpU1FO42oviNPIeJ6l4o1JyATMWC5HBS11ifWLAnZuQKCuWOfrneJWMn1nO3GWHAlOZ6aLrBQKnTA68ljadRPKzvW26YYHA+M4V2Df8Mxp1nOxWGpRFycCakxTJzBC4EWdVkshCvIMonWp4GyAd6MKgD2Giuq0EilH/byBRumJ1YdcG33cw5cQ0ILl2hKRAOUca2BFUT+H8hmMTjVr+uHtXs7JomFe/JMxV29HXT862qHAYNMh1nC58JW6e4OfTO53Vglkny7Fg3icoXEubNGw5lmEsXH6inQxMv8UpyytGevlkXhxXJin7UR9pnjSB8BQFkOXrHuGtO8qqtvLX0UDw/147eET397JCj1VT8lR3HwkA7NWI3IGY5+26bzon/ozHWkp2IlhHFfkW2yAop++sFB5vMNZv/kFHz0NEXR4+JWXV+GUfH8F7N2GPZ/XQNE2sUJhgOSPS5DdH3JFus11YPzQH4I2cEoasvhFpSBCY2i3Mpyriz9hWeZxwhOhnD6A==',
            'language': 'en',
            'gaid': 'dc9f3ed8-8d0c-43f6-9f24-420da32030b3',
            'deviceId': '7849d1681f37cb9c8d158afd1f38a93f',
            'systemVersion': '11',
            'clientPlatform': 'android',
            'androidVersion': '1.9.7',
            'model': 'SM-A127F',
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'test-api.shorttv.live',
            'Connection': 'Keep-Alive',
            'Accept-Encoding': 'gzip',
            'User-Agent': 'okhttp/4.10.0',
            'Content-Length': '0'
        }

    def login_yapi_api(self):
        res = requests.post(self.yapi_login_url, json=self.yapi_login_data)
        c = {
            "_yapi_token": re.search(r'_yapi_token=([^;]+)', res.headers['Set-Cookie']).groups(1)[0],
            "_yapi_uid": re.search(r'_yapi_uid=([^;]+)', res.headers['Set-Cookie']).groups(1)[0]
        }

        return c

    def download_yapi_api(self, cookies):
        # 创建一个会话对象
        session = requests.Session()
        # 设置 Cookie
        session.cookies.set('_yapi_token', cookies['_yapi_token'])
        session.cookies.set('_yapi_uid', cookies['_yapi_uid'])
        # 发送HTTP GET请求
        with session.get(self.yapi_login_download, stream=True) as r:
            r.raise_for_status()  # 检查请求是否成功
            with open(self.file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

    def api_request(self, path, headers=None, payload=None):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        for api_list in json_data:
            for api_info in api_list['list']:
                if api_info['query_path']['path'] == path:
                    api_url = self.host + api_info['path']
                    api_body = {}
                    if headers:
                        for key, value in headers.items():
                            self.headers[key] = headers[key]
                    if "req_body_other" in api_info:
                        for key, value in payload.items():
                            api_info['req_body_other'][key] = payload[key]

                    # 发送API请求
                    response = requests.post(api_url, headers=self.headers, data=api_body)

                    # 打印响应内容
                    print(response.text)

                    return response


if __name__ == '__main__':
    # TODO 动态更新token, 届时用的时候调整下执行的顺序
    headers = {
        # 'gaid': 'dc9f3ed8-8d0c-43f6-9f24-420da32030b3',
        'Authorization': '1pkeeporqzC4ou7Jk1fWnuZOfTmmPzFXbRKqbYUFKCbaHJFVMkjd0nlWvoPxQjUXOP3tkiCXSNnXb6JYwd05IX3woU+Nz+Q8PAYMA8YSwEpim++x+Nvz0vC6KIQP/XaXfUByP/y/vxa+KRzk6+nZewj5x//W+EIkTHLQ3iFfkC9bkggmt8Rg5Z2+XmdPqDWhhL3RHX2AC7en5e5A6H1aJmOXebgiq3s6gfT0MexiL1qD4L5R8qLnBjZQP85pc7dBV+qzCcZ2c/h9+MjG8ZdfJDqtbYOb6Xk58X9KAXXkGXYnJzgt2+HaHzZ3JQC1s0rMerrJLoXfNPuKKE1MN0r6P65JEVUACtcOwsYVNFneDNshBSbsROFA+gJm4WD7K/Xl7Eq4gsy5MFwjG5+SqckNfk4W0KpNNJ/vl94Cs9WXzRfgUzY6wBycwJg7gTx34LM9TiUMUJfLg+i0v0DZGVceRIQJMieeWzwF7zxcthcStMx8Fh+HjPmXPU/G3ZZJsYWFHboyklqhvfJYPQi0Ux+cDwU3MO1gSPm4BWFTVA83X13MiR0B2WG75U6s1xrVI+8/SZxZBdNB8z0GaQ3yIhFrobKuxL1gG5si7qiIROyzw9d2BVNbl/+f1FiMTzkQm0bt01zeu2Ld/xvjd8wVc2wJPA==',
    }
    payload = {}
    #
    a = ApiAll()

    cook = a.login_yapi_api()
    a.download_yapi_api(cook)
    a.api_request("/app/login/v2/getUserInfo", headers=headers, payload=payload)
