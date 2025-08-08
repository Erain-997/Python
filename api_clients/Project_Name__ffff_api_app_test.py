from utils.http_api import HttpClientWrapperSimple


# @allure.title("剧集详情, 未解锁时不返回播放地址")
def ffff_dramaInfo_dramaDetailV2(client=None, shortPlayId=None, episodeNum=None, expected: dict = None):
    """
    剧集详情, 未解锁时不返回播放地址

    :param shortPlayId: integer
    :param episodeNum: integer
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/dramaInfo/dramaDetailV2", expected,
                       json={"shortPlayId": shortPlayId, "episodeNum": episodeNum})
    return client, resp


# @allure.title("剧集详情,支持全场免费看，支持单集解锁配置，播放地址加密")
def ffff_dramaInfo_encrypt_dramaDetail(client=None, businessId=None, scene=None, expected: dict = None):
    """
    剧集详情,支持全场免费看，支持单集解锁配置，播放地址加密

    :param businessId: integer - 短剧id,在banner为banner主键id
    :param scene: string - 查询的场景：埋点对应的场景，例如collections，recently，deeplink
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/dramaInfo/encrypt/dramaDetail", expected,
                       json={"businessId": businessId, "scene": scene})
    return client, resp


# @allure.title("根据短剧id 获取用户当前观看第几集的剧集id 或者短剧第一集的剧集id")
def ffff_dramaInfo_getDramaIdByShortPlayId(client=None, businessId=None, scene=None, expected: dict = None):
    """
    根据短剧id 获取用户当前观看第几集的剧集id 或者短剧第一集的剧集id

    :param businessId: integer - 短剧id,在banner为banner主键id
    :param scene: string - 查询的场景：埋点对应的场景，例如collections，recently，deeplink
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/dramaInfo/getDramaIdByShortPlayId", expected,
                       json={"businessId": businessId, "scene": scene})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_dramaInfo_dramaDetailV2 ...")
    ffff_dramaInfo_dramaDetailV2()

    print("▶ 调用 ffff_dramaInfo_encrypt_dramaDetail ...")
    ffff_dramaInfo_encrypt_dramaDetail()

    print("▶ 调用 ffff_dramaInfo_getDramaIdByShortPlayId ...")
    ffff_dramaInfo_getDramaIdByShortPlayId()
