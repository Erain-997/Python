from utils.http_api import HttpClientWrapperSimple


# @allure.title("ConisStore 根据模板获取列表数据及广告相关 全场免费看，不支持低分模版， 支持剧集解锁配置")
def ffff_sku_getCoinsStoreListAndAdInfoBySkuModel(client=None, businessId=None, scene=None, dramaId=None,
                                                  reelPlaySource=None, expected: dict = None):
    """
    ConisStore 根据模板获取列表数据及广告相关 全场免费看，不支持低分模版， 支持剧集解锁配置
解锁页商品列表
    :param businessId: integer - 短剧id,在banner为banner主键id
    :param scene: string - 查询的场景：埋点对应的场景，例如collections，recently，deeplink
    :param dramaId: integer - 剧集id
    :param reelPlaySource: string - 播放页面来源
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/sku/getCoinsStoreListAndAdInfoBySkuModel", expected,
                       json={"businessId": businessId, "scene": scene, "dramaId": dramaId,
                             "reelPlaySource": reelPlaySource})
    return client, resp


# @allure.title("待解锁页-实验组")
def ffff_sku_getUnlockedPageSkuList(client=None, businessId=None, scene=None, dramaId=None, reelPlaySource=None,
                                    expected: dict = None):
    """
    待解锁页-实验组

    :param businessId: integer - 短剧id,在banner为banner主键id
    :param scene: string - 查询的场景：埋点对应的场景，例如collections，recently，deeplink
    :param dramaId: integer - 剧集id
    :param reelPlaySource: string - 播放页面来源
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/sku/getUnlockedPageSkuList", expected,
                       json={"businessId": businessId, "scene": scene, "dramaId": dramaId,
                             "reelPlaySource": reelPlaySource})
    return client, resp


# @allure.title("根据归因模板ID获取CoinsStore列表数据 ,支持低分模版")
def ffff_sku_getCoinsStoreListBySkuModel(client=None, expected: dict = None):
    """
    根据归因模板ID获取CoinsStore列表数据 ,支持低分模版
商店商品列表
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/sku/getCoinsStoreListBySkuModel", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_sku_getCoinsStoreListAndAdInfoBySkuModel ...")
    ffff_sku_getCoinsStoreListAndAdInfoBySkuModel()

    print("▶ 调用 ffff_sku_getUnlockedPageSkuList ...")
    ffff_sku_getUnlockedPageSkuList()

    print("▶ 调用 ffff_sku_getCoinsStoreListBySkuModel ...")
    ffff_sku_getCoinsStoreListBySkuModel()
