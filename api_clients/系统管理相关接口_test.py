from utils.http_api import HttpClientWrapperSimple


# @allure.title("获取系统配置参数信息")
def ffff_system_getConfigByKey(client=None, key=None, expected: dict = None):
    """
    获取系统配置参数信息

    :param key: string
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/system/getConfigByKey", expected, json={"key": key})
    return client, resp


# @allure.title("获取请求的客户端是否需要更新的信息")
def ffff_system_getUpgradeVersionManageInfo(client=None, version=None, expected: dict = None):
    """
    获取请求的客户端是否需要更新的信息

    :param version: string - 客户端当前的app版本号,例如:1.5.0
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/system/getUpgradeVersionManageInfo", expected, json={"version": version})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_system_getConfigByKey ...")
    ffff_system_getConfigByKey()

    print("▶ 调用 ffff_system_getUpgradeVersionManageInfo ...")
    ffff_system_getUpgradeVersionManageInfo()
