from utils.http_api import HttpClientWrapperSimple


# @allure.title("短剧详情")
def ffff_shortPlay_shortPlayDetail(client=None, businessId=None, scene=None, expected: dict = None):
    """
    短剧详情

    :param businessId: integer - 短剧id,在banner为banner主键id
    :param scene: string - 查询的场景：埋点对应的场景，例如collections，recently，deeplink
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/shortPlay/shortPlayDetail", expected,
                       json={"businessId": businessId, "scene": scene})
    return client, resp


# @allure.title("获取充值金额前30名的短剧")
def ffff_shortPlay_getTopRechargeShortPlays(client=None, expected: dict = None):
    """
    获取充值金额前30名的短剧
<p>
1. 推荐当前语言区充值前30名的剧，按顺序从高到低轮询
3. 文案中人数为该剧的追剧数
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/shortPlay/getTopRechargeShortPlays", expected, json={})
    return client, resp


# @allure.title("获取搜索栏轮播剧名")
def ffff_shortPlay_getSearchCarouselPlays(client=None, expected: dict = None):
    """
    获取搜索栏轮播剧名
<p>
1. 优先展示后台配置的搜索推荐剧
2. 若配置不足10个，则取最近1天当前app语言对应的消耗最多的短剧，补充够10个
3. 用于搜索栏5秒一次的轮播展示
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/shortPlay/getSearchCarouselPlays", expected, json={})
    return client, resp


# @allure.title("获取消耗最高的短剧,兜底剧使用这个接口")
def ffff_shortPlay_getPopularShortPlay(client=None, expected: dict = None):
    """
    获取消耗最高的短剧,兜底剧使用这个接口

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/shortPlay/getPopularShortPlay", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_shortPlay_shortPlayDetail ...")
    ffff_shortPlay_shortPlayDetail()

    print("▶ 调用 ffff_shortPlay_getTopRechargeShortPlays ...")
    ffff_shortPlay_getTopRechargeShortPlays()

    print("▶ 调用 ffff_shortPlay_getSearchCarouselPlays ...")
    ffff_shortPlay_getSearchCarouselPlays()

    print("▶ 调用 ffff_shortPlay_getPopularShortPlay ...")
    ffff_shortPlay_getPopularShortPlay()
