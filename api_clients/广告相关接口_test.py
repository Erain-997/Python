from utils.http_api import HttpClientWrapperSimple


# @allure.title("广告解锁倒计时观看完成")
def ffff_ad_watchAdUnLockComplete(client=None, id=None, expected: dict = None):
    """
    广告解锁倒计时观看完成

    :param id: integer - 广告id
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/ad/watchAdUnLockComplete", expected, json={"id": id})
    return client, resp


# @allure.title("签到完成看广告")
def ffff_ad_signWatchAd(client=None, expected: dict = None):
    """
    签到完成看广告

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/ad/signWatchAd", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_ad_watchAdUnLockComplete ...")
    ffff_ad_watchAdUnLockComplete()

    print("▶ 调用 ffff_ad_signWatchAd ...")
    ffff_ad_signWatchAd()
