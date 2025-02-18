#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2024/10/12
# @Author  : zyr
import json

import requests

from common.utils.arg_parse_func import args
from common.utils.device_tools import get_device_names
from common.utils.report import get_pass_rate, get_app_version,get_modules_name

# 飞书的Webhook地址
webhook_url = "https://open.feishu.cn/open-apis/bot/v2/hook/d348647e-038e-489c-a2cc-0d3511a87211"


def feishu_push(path):
    data = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": f"UI自动化执行完毕-{args.output_report}",
                    "content": [
                        [
                            {"tag": "text", "text": f"设备ip: {args.device} \n"},
                            {"tag": "text", "text": f"设备名称: {get_device_names()} \n"},
                            {"tag": "text", "text": f"APK版本: {get_app_version()} \n"},
                            {"tag": "text", "text": f"模块: {get_modules_name()} \n"},
                            {"tag": "text", "text": f"通过率: {get_pass_rate()}% \n"},
                            {"tag": "a", "text": "结果报告\n",
                             "href": f"http://192.168.120.150:9988/files/{path}/reports/index.html"},
                            # {"tag": "at", "user_id": "all"},
                        ]
                    ],
                }
            }
        },
    }
    # 机器人助手格式
    # data = {
    #     "msg_type": "post",
    #     "content": {"设备":f"**设备:{args.device}**"},
    # }
    # data = {"msg_type":"text","content":{"text":"<at user_id=\"all\"></at> test1"}}
    # 发送HTTP POST请求
    try:
        response = requests.post(webhook_url, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        # 检查响应状态码
        if response.status_code == 200:
            print("消息发送成功")
        else:
            print(f"消息发送失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    feishu_push(1, 1)
