# -*- encoding=utf8 -*-
# Time：'2022/9/30'
# __author__ = "Erain"


import http.client

conn = http.client.HTTPConnection("10,6,27,69")

payload = "{\n    \"server_id\": 8045\n}"

headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "32732603-945c-4c7e-b0d0-01c2fa08be3d"
    }

conn.request("POST", "test", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))