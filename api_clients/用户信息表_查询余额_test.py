from utils.http_api import HttpClientWrapperSimple


# @allure.title("保存用户是否打过兜底剧")
def ffff_user_reportDefaultShortPlay(client=None, openDefaultShortPlay=None, expected: dict = None):
    """
    保存用户是否打过兜底剧

    :param openDefaultShortPlay: boolean - 是否打开过兜底剧
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/reportDefaultShortPlay", expected,
                       json={"openDefaultShortPlay": openDefaultShortPlay})
    return client, resp


# @allure.title("增加fb上报获取用户信息接口")
def ffff_user_getFBUserInfo(client=None, expected: dict = None):
    """
    增加fb上报获取用户信息接口

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/getFBUserInfo", expected, json={})
    return client, resp


# @allure.title("客户端用户切换语言")
def ffff_user_setUserLanguage(client=None, expected: dict = None):
    """
    客户端用户切换语言

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/setUserLanguage", expected, json={})
    return client, resp


# @allure.title("用户上报gaid和idfa")
def ffff_user_reportUserAdInfo(client=None, idfa=None, gaid=None, expected: dict = None):
    """
    用户上报gaid和idfa

    :param idfa: string - idfa
    :param gaid: string - gaid
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/reportUserAdInfo", expected, json={"idfa": idfa, "gaid": gaid})
    return client, resp


# @allure.title("用户上报活跃时间")
def ffff_user_reportActiveTime(client=None, expected: dict = None):
    """
    用户上报活跃时间

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/reportActiveTime", expected, json={})
    return client, resp


# @allure.title("用户余额查询")
def ffff_user_getUserBalance(client=None, expected: dict = None):
    """
    用户余额查询

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/getUserBalance", expected, json={})
    return client, resp


# @allure.title("获取设备其他充值用户信息")
def ffff_user_getAnotherUserInfo(client=None, expected: dict = None):
    """
    获取设备其他充值用户信息

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/getAnotherUserInfo", expected, json={})
    return client, resp


# @allure.title("迁移1.0旧账号金币")
def ffff_user_migrateAccount(client=None, userId=None, expected: dict = None):
    """
    迁移1.0旧账号金币

    :param userId: string - 1.0旧版本用户id
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/migrateAccount", expected, json={"userId": userId})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_user_reportDefaultShortPlay ...")
    ffff_user_reportDefaultShortPlay()

    print("▶ 调用 ffff_user_getFBUserInfo ...")
    ffff_user_getFBUserInfo()

    print("▶ 调用 ffff_user_setUserLanguage ...")
    ffff_user_setUserLanguage()

    print("▶ 调用 ffff_user_reportUserAdInfo ...")
    ffff_user_reportUserAdInfo()

    print("▶ 调用 ffff_user_reportActiveTime ...")
    ffff_user_reportActiveTime()

    print("▶ 调用 ffff_user_getUserBalance ...")
    ffff_user_getUserBalance()

    print("▶ 调用 ffff_user_getAnotherUserInfo ...")
    ffff_user_getAnotherUserInfo()

    print("▶ 调用 ffff_user_migrateAccount ...")
    ffff_user_migrateAccount()
