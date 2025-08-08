from utils.http_api import HttpClientWrapperSimple


# @allure.title("查看签到记录,以及签到情况(新)")
def ffff_sig_signRecord(client=None, expected: dict = None):
    """
    查看签到记录,以及签到情况(新)

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/sig/signRecord", expected, json={})
    return client, resp


# @allure.title("用户签到(新)")
def ffff_sig_sign(client=None, expected: dict = None):
    """
    用户签到(新)

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/sig/sign", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_sig_signRecord ...")
    ffff_sig_signRecord()

    print("▶ 调用 ffff_sig_sign ...")
    ffff_sig_sign()
