#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/08/09
# @Author  : zxp
import requests
import socket
from airtest.core.api import *

# 测开
# access_token = "5caa287d0b9fbb21c4e1603bf32f72f3982d9490139533460f2fa6bbd00b6506"



access_token = "405f6b3dcbfed832aa83c3461835f3d79e789888367d084db3cd78a64e04b956"


def ding_api(info, report_url, name, skin, version):
    version = f"<font face=‘华云彩绘’ color=#00CED1>{version}</font>"
    name = f"<font face=‘华云彩绘’ color=#D9006C>{name}</font>"
    skin = f"<font face=‘华云彩绘’ color=#D9006C>{skin}</font>"
    data = {"msgtype": "markdown",
            "markdown": {"title": info + "外显测试数据",
                         "text": f"## **外显测试数据**\n **测试对象** \n \n测试分支:{version} \n \n大臣名称:{name} \n\n 皮肤名称:{skin}\n\n**详见附件** \n\n>"
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
            "at": {"atMobiles": [], "isAtAll": True}}

    with requests.post(
            url=f"https://oapi.dingtalk.com/robot/send?access_token={access_token}",
            json=data
    ) as response:
        print(response.json())


if __name__ == '__main__':
    # ding_exception_api("","")
    ding_api("苏丹", "test", "d", "dd", "d")
