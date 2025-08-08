from utils.http_api import HttpClientWrapperSimple


# @allure.title("getBonusExpiringPush")
def ffff_push_bonusExpiring_getPushInfo(client=None, expected: dict = None):
    """
    getBonusExpiringPush

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.get(f"{base_url}/ffff/push/bonusExpiring/getPushInfo", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_push_bonusExpiring_getPushInfo ...")
    ffff_push_bonusExpiring_getPushInfo()
