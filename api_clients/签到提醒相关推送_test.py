from utils.http_api import HttpClientWrapperSimple


# @allure.title("签到提醒接口，依赖客户端调接口（当地时间6点），返回推送内容")
def ffff_push_sign_signReminder(client=None, expected: dict = None):
    """
    签到提醒接口，依赖客户端调接口（当地时间6点），返回推送内容

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/push/sign/signReminder", expected, json={})
    return client, resp


# @allure.title("错过签到提醒接口，依赖客户端调接口（当地时间12点），返回推送内容")
def ffff_push_sign_missSignReminder(client=None, expected: dict = None):
    """
    错过签到提醒接口，依赖客户端调接口（当地时间12点），返回推送内容

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/push/sign/missSignReminder", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_push_sign_signReminder ...")
    ffff_push_sign_signReminder()

    print("▶ 调用 ffff_push_sign_missSignReminder ...")
    ffff_push_sign_missSignReminder()
