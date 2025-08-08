from utils.http_api import HttpClientWrapperSimple


# @allure.title("取消收藏")
def ffff_collect_cancelCollect(client=None, businessId=None, scene=None, colletType=None, collectSource=None,
                               expected: dict = None):
    """
    取消收藏

    :param businessId: integer - 短剧id,在banner为banner主键id
    :param scene: string - 查询的场景：埋点对应的场景，例如collections，recently，deeplink
    :param colletType: integer - 1 收藏 2点赞
    :param collectSource: integer - 1 短剧 2剧集 3花絮 4高能
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/collect/cancelCollect", expected,
                       json={"businessId": businessId, "scene": scene, "colletType": colletType,
                             "collectSource": collectSource})
    return client, resp


# @allure.title("批量取消收藏")
def ffff_collect_batchCancelCollect(client=None, businessIdList=None, expected: dict = None):
    """
    批量取消收藏

    :param businessIdList: array - 数据唯一id(比如短剧id,剧集id,收藏id,主键id)
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/collect/batchCancelCollect", expected, json={"businessIdList": businessIdList})
    return client, resp


# @allure.title("收藏")
def ffff_collect_collectOp(client=None, businessId=None, scene=None, colletType=None, collectSource=None,
                           watchTime=None, dramaId=None, expected: dict = None):
    """
    收藏

    :param businessId: integer - 短剧id,在banner为banner主键id
    :param scene: string - 查询的场景：埋点对应的场景，例如collections，recently，deeplink
    :param colletType: integer - 1 收藏 2点赞
    :param collectSource: integer - 1 短剧 2剧集 3花絮 4高能
    :param watchTime: integer - 观看的时间数(比如观看到第几秒)
    :param dramaId: integer - 剧集id
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/collect/collectOp", expected,
                       json={"businessId": businessId, "scene": scene, "colletType": colletType,
                             "collectSource": collectSource, "watchTime": watchTime, "dramaId": dramaId})
    return client, resp


# @allure.title("收藏列表")
def ffff_collect_collectList(client=None, pageSize=None, lastTime=None, colletType=None, collectSource=None,
                             expected: dict = None):
    """
    收藏列表

    :param pageSize: integer - 每页显示数量
    :param lastTime: integer - 每页最后一条数据的时间戳
    :param colletType: integer - 1 收藏 2点赞
    :param collectSource: array - 1 短剧 2剧集 3花絮 4高能
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/collect/collectList", expected,
                       json={"pageSize": pageSize, "lastTime": lastTime, "colletType": colletType,
                             "collectSource": collectSource})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_collect_cancelCollect ...")
    ffff_collect_cancelCollect()

    print("▶ 调用 ffff_collect_batchCancelCollect ...")
    ffff_collect_batchCancelCollect()

    print("▶ 调用 ffff_collect_collectOp ...")
    ffff_collect_collectOp()

    print("▶ 调用 ffff_collect_collectList ...")
    ffff_collect_collectList()
