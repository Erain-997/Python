from utils.http_api import HttpClientWrapperSimple


# @allure.title("deepLinkReport")
def ffff_adMatch_deepLinkReport(client=None, expected: dict = None):
    """
    deepLinkReport

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/adMatch/deepLinkReport", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_adMatch_deepLinkReport ...")
    ffff_adMatch_deepLinkReport()
