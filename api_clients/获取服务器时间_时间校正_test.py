from utils.http_api import HttpClientWrapperSimple


# @allure.title("correctionTime")
def ffff_correction_time(client=None, localTimeLong=None, expected: dict = None):
    """
    correctionTime

    :param localTimeLong: integer - 本地时间 客户端设备时间
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/correction/time", expected, json={"localTimeLong": localTimeLong})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_correction_time ...")
    ffff_correction_time()
