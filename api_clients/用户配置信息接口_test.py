from utils.http_api import HttpClientWrapperSimple


# @allure.title("修改用户自动解锁配置")
def ffff_user_config(client=None, autoUnlock=None, expected: dict = None):
    """
    修改用户自动解锁配置

    :param autoUnlock: boolean - 自动解锁是否开启
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user_config", expected, json={"autoUnlock": autoUnlock})
    return client, resp


# @allure.title("查看用户自动解锁配置")
def ffff_user_config(client=None, expected: dict = None):
    """
    查看用户自动解锁配置

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.get(f"{base_url}/ffff/user_config", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_user_config ...")
    ffff_user_config()

    print("▶ 调用 ffff_user_config ...")
    ffff_user_config()
