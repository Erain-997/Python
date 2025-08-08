from utils.http_api import HttpClientWrapperSimple


# @allure.title("保存观看历史记录")
def ffff_watchHistory_saveWatchHistory(client=None, watchTime=None, dramaId=None, expected: dict = None):
    """
    保存观看历史记录

    :param watchTime: integer - 观看的时间数(比如观看到第几秒)
    :param dramaId: integer - 剧集id
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/watchHistory/saveWatchHistory", expected,
                       json={"watchTime": watchTime, "dramaId": dramaId})
    return client, resp


# @allure.title("删除历史记录")
def ffff_watchHistory_delWatchHistory(client=None, businessIdList=None, expected: dict = None):
    """
    删除历史记录

    :param businessIdList: array - 数据唯一id(比如短剧id,剧集id,收藏id,主键id)
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/watchHistory/delWatchHistory", expected,
                       json={"businessIdList": businessIdList})
    return client, resp


# @allure.title("获取观看历史记录")
def ffff_watchHistory_getWatchHistoryList(client=None, pageSize=None, lastTime=None, expected: dict = None):
    """
    获取观看历史记录

    :param pageSize: integer - 每页显示数量
    :param lastTime: integer - 每页最后一条数据的时间戳
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/watchHistory/getWatchHistoryList", expected,
                       json={"pageSize": pageSize, "lastTime": lastTime})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_watchHistory_saveWatchHistory ...")
    ffff_watchHistory_saveWatchHistory()

    print("▶ 调用 ffff_watchHistory_delWatchHistory ...")
    ffff_watchHistory_delWatchHistory()

    print("▶ 调用 ffff_watchHistory_getWatchHistoryList ...")
    ffff_watchHistory_getWatchHistoryList()
