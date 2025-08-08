from utils.http_api import HttpClientWrapperSimple


# @allure.title("保存feed流观看历史记录")
def ffff_feedWatchHistory_saveWatchHistory(client=None, watchTime=None, dramaId=None, expected: dict = None):
    """
    保存feed流观看历史记录

    :param watchTime: integer - 观看的时间数(比如观看到第几秒)
    :param dramaId: integer - 剧集id
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/feedWatchHistory/saveWatchHistory", expected,
                       json={"watchTime": watchTime, "dramaId": dramaId})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_feedWatchHistory_saveWatchHistory ...")
    ffff_feedWatchHistory_saveWatchHistory()
