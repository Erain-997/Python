import requests


def ding_push():
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title": "维京闪退",
            "text": "维京启动闪退了"
        },
        "at": {
            "atMobiles": [
                "15980322542"
            ],
            "isAtAll": True
        }
    }

    with requests.post(
            url="https://oapi.dingtalk.com/robot/send?access_token=d00578f7cb2ab74a9fa45ab7eadeb5f3b275f76c4ecf6f17d0f015d923833c27",
            json=data) as resp:
        print(resp.json())
