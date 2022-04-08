#!/usr/bin/env python
# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08
import requests
from internal.tools.db import login_role_write


def role_creation():
    u = "http://10.6.27.69:6060/ui_account"
    with requests.post(url=u, json={
        "server_id": 8045,
        "run_activity": True,
    }) as resp:
        return resp.json()


def db_role_write():
    user_id = role_creation().get("data").get("user_id")
    if user_id is not None:
        login_role_write(user_id)
        return user_id
    else:
        print("注册失败")
        return "注册失败"


if __name__ == '__main__':
    user_id = role_creation().get("data").get("user_id")
    print(user_id)
