from utils.http_api import HttpClientWrapperSimple


# @allure.title("校验用户是否记触发新人推荐")
def ffff_recommend_checkNewUserRecommend(client=None, expected: dict = None):
    """
    校验用户是否记触发新人推荐

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/recommend/checkNewUserRecommend", expected, json={})
    return client, resp


# @allure.title("获取新人推荐内容")
def ffff_recommend_getNewUserRecommendInfo(client=None, expected: dict = None):
    """
    获取新人推荐内容

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/recommend/getNewUserRecommendInfo", expected, json={})
    return client, resp


# @allure.title("获取用户触发新人推荐的时间信息")
def ffff_recommend_getNewUserTimeInfo(client=None, expected: dict = None):
    """
    获取用户触发新人推荐的时间信息

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/recommend/getNewUserTimeInfo", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_recommend_checkNewUserRecommend ...")
    ffff_recommend_checkNewUserRecommend()

    print("▶ 调用 ffff_recommend_getNewUserRecommendInfo ...")
    ffff_recommend_getNewUserRecommendInfo()

    print("▶ 调用 ffff_recommend_getNewUserTimeInfo ...")
    ffff_recommend_getNewUserTimeInfo()
