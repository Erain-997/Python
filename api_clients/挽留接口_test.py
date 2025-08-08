from utils.http_api import HttpClientWrapperSimple


# @allure.title("获取即将播放的剧集")
def ffff_retain_getComingSoonShortPlays(client=None, shortPlayId=None, expected: dict = None):
    """
    获取即将播放的剧集

    :param shortPlayId: integer - 剧集id
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/retain/getComingSoonShortPlays", expected, json={"shortPlayId": shortPlayId})
    return client, resp


# @allure.title("获取退出沉浸页的挽留剧集")
def ffff_retain_getExitRetainShortPlays(client=None, shortPlayId=None, expected: dict = None):
    """
    获取退出沉浸页的挽留剧集

    :param shortPlayId: integer - 剧集id
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/retain/getExitRetainShortPlays", expected, json={"shortPlayId": shortPlayId})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_retain_getComingSoonShortPlays ...")
    ffff_retain_getComingSoonShortPlays()

    print("▶ 调用 ffff_retain_getExitRetainShortPlays ...")
    ffff_retain_getExitRetainShortPlays()
