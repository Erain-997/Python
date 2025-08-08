from utils.http_api import HttpClientWrapperSimple


# @allure.title("用户设备信息上报，token,语言，时区")
def ffff_userRegistrationToken_report(client=None, type=None, token=None, model=None, iosPushTest=None, apnsToken=None,
                                      expected: dict = None):
    """
    用户设备信息上报，token,语言，时区

    :param type: number - 类型 10代表 google推送  20代表 xiaomi推送
    :param token: string - 推送token
    :param model: string - 手机型号
    :param iosPushTest: integer - push AB测 0为对照组，1为实验组
    :param apnsToken: string - apns Token
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/userRegistrationToken/report", expected,
                       json={"type": type, "token": token, "model": model, "iosPushTest": iosPushTest,
                             "apnsToken": apnsToken})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_userRegistrationToken_report ...")
    ffff_userRegistrationToken_report()
