#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/11/23
# @Author  : zxp

import requests

from .tools import SmallTools


@SmallTools.except_output()
def dcsso_api(name, password, app_id, expires="3600", url="https://dcsso.dianchu.com:7676/v1"):
    """
    单点帐号登录
    :param app_id: 跳转参数
    :param expires: 过期时间
    :param name: 用户名
    :param password: 密码
    :param url:
    :return:
    """
    data = {
        "act": "1000",
        "username": name,
        "password": password,
        "appid": "100",
        "exptime": 3600
    }
    with requests.post(url, json=data)as resp:
        login_data = {
            "act": "1100",
            "AppID": app_id,
            "Expires": expires,
            "token": resp.json()['Token']
        }
        with requests.post(url, json=login_data)as login_resp:
            return login_resp.json()['Tokencode']


@SmallTools.except_output()
def ding_api(access_token, data):
    return requests.post(
        url="https://oapi.dingtalk.com/robot"
            "/send?access_token=" + access_token + "",
        json=data)
