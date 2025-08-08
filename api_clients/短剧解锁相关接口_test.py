from utils.http_api import HttpClientWrapperSimple


# @allure.title("广告解锁剧集")
def ffff_shortPlay_unlockEpisodeByWatchAd(client=None, shortPlayId=None, episodeNum=None, expected: dict = None):
    """
    广告解锁剧集

    :param shortPlayId: integer - 短剧id
    :param episodeNum: integer - 剧集数
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/shortPlay/unlockEpisodeByWatchAd", expected,
                       json={"shortPlayId": shortPlayId, "episodeNum": episodeNum})
    return client, resp


# @allure.title("查询用户当天可观看广告解锁短剧次数")
def ffff_shortPlay_watchAdUnlockInfo(client=None, businessId=None, scene=None, expected: dict = None):
    """
    查询用户当天可观看广告解锁短剧次数

    :param businessId: integer - 短剧id,在banner为banner主键id
    :param scene: string - 查询的场景：埋点对应的场景，例如collections，recently，deeplink
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/shortPlay/watchAdUnlockInfo", expected,
                       json={"businessId": businessId, "scene": scene})
    return client, resp


# @allure.title("观看广告解锁剧集")
def ffff_shortPlay_unlockByWatchAd(client=None, businessId=None, autoUnlock=None, expected: dict = None):
    """
    观看广告解锁剧集

    :param businessId: integer - 剧集id
    :param autoUnlock: boolean - 自动解锁是否开启，充值或观看广告时会携带是否勾选自动解锁，如果此字段不为空，则更新用户自动解锁配置
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/shortPlay/unlockByWatchAd", expected,
                       json={"businessId": businessId, "autoUnlock": autoUnlock})
    return client, resp


# @allure.title("金币解锁剧集")
def ffff_shortPlay_unlockByCoin(client=None, businessId=None, autoUnlock=None, expected: dict = None):
    """
    金币解锁剧集

    :param businessId: integer - 剧集id
    :param autoUnlock: boolean - 自动解锁是否开启，充值或观看广告时会携带是否勾选自动解锁，如果此字段不为空，则更新用户自动解锁配置
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/shortPlay/unlockByCoin", expected,
                       json={"businessId": businessId, "autoUnlock": autoUnlock})
    return client, resp


# @allure.title("金币解锁剧集")
def ffff_shortPlay_unlockEpisodeByGold(client=None, shortPlayId=None, episodeNum=None, expected: dict = None):
    """
    金币解锁剧集

    :param shortPlayId: integer - 短剧id
    :param episodeNum: integer - 剧集数
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/shortPlay/unlockEpisodeByGold", expected,
                       json={"shortPlayId": shortPlayId, "episodeNum": episodeNum})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_shortPlay_unlockEpisodeByWatchAd ...")
    ffff_shortPlay_unlockEpisodeByWatchAd()

    print("▶ 调用 ffff_shortPlay_watchAdUnlockInfo ...")
    ffff_shortPlay_watchAdUnlockInfo()

    print("▶ 调用 ffff_shortPlay_unlockByWatchAd ...")
    ffff_shortPlay_unlockByWatchAd()

    print("▶ 调用 ffff_shortPlay_unlockByCoin ...")
    ffff_shortPlay_unlockByCoin()

    print("▶ 调用 ffff_shortPlay_unlockEpisodeByGold ...")
    ffff_shortPlay_unlockEpisodeByGold()
