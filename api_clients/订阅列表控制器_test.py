from utils.http_api import HttpClientWrapperSimple


# @allure.title("订阅商品列表列表V3,升降级版本对照组接口")
def ffff_subscription_getProductListV3(client=None, isShowSubscript=None, expected: dict = None):
    """
    订阅商品列表列表V3,升降级版本对照组接口
过滤普通商品
    :param isShowSubscript: integer - 是否需要展示角标0或null不展示, 1-展示
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/subscription/getProductListV3", expected,
                       json={"isShowSubscript": isShowSubscript})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_subscription_getProductListV3 ...")
    ffff_subscription_getProductListV3()
