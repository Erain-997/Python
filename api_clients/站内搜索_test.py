from utils.http_api import HttpClientWrapperSimple


# @allure.title("大家都在搜")
def ffff_search_hotSearch(client=None, expected: dict = None):
    """
    大家都在搜

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/search/hotSearch", expected, json={})
    return client, resp


# @allure.title("站内搜索")
def ffff_search_searchPage(client=None, pageSize=None, pageNum=None, searchText=None, language=None,
                           expected: dict = None):
    """
    站内搜索

    :param pageSize: integer - 每页显示数量
    :param pageNum: integer - 页码(第几页)
    :param searchText: string
    :param language: string
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/search/searchPage", expected,
                       json={"pageSize": pageSize, "pageNum": pageNum, "searchText": searchText, "language": language})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_search_hotSearch ...")
    ffff_search_hotSearch()

    print("▶ 调用 ffff_search_searchPage ...")
    ffff_search_searchPage()
