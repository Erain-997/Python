#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/08/09
# @Author  : zxp
import requests
import socket
from airtest.core.api import *

# 测开
# access_token = "d00578f7cb2ab74a9fa45ab7eadeb5f3b275f76c4ecf6f17d0f015d923833c27"
access_token = "405f6b3dcbfed832aa83c3461835f3d79e789888367d084db3cd78a64e04b956"

def ding_api(info, report_url):
    data = {"msgtype": "markdown",
            "markdown": {"title": info + "外显测试数据",
                         "text": " 外显测试数据详见：\n >"
                                 "[" + info + "外显测试数据报告](" + get_host_ip() + "/reports/" + report_url + "/log.html) \n >"
                                                                                                        "\n > [外显图片资源下载](" + get_host_ip() + "/reports/" + report_url + "/" + report_url + ".zip"")"
                         },
            "at": {"atMobiles": ["15980322542"], "isAtAll": False}}

    with requests.post(
            url="https://oapi.dingtalk.com/robot"
                "/send?access_token=" + access_token + "",
            json=data
    ) as response:
        print(response.json())


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return "http://" + ip + ":8000/"


def ding_exception_api(e, e_info):
    data = {"msgtype": "markdown",
            "markdown": {"title": "外显测试数据",
                         "text": " 外显测试通知：\n >"
                                 "异常通知:" + str(e) + str(e_info)
                         },
            "at": {"atMobiles": ["15980322542"], "isAtAll": False}}

    with requests.post(
            url="https://oapi.dingtalk.com/robot"
                "/send?access_token=d00578f7cb2ab74a9fa45ab7eadeb5f3b275f76c4ecf6f17d0f015d923833c27",
            json=data
    ) as response:
        print(response.json())
