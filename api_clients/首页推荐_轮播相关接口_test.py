from utils.http_api import HttpClientWrapperSimple


# @allure.title("获取banner 的more数据,支持返回加密视频")
def ffff_homeData_encrypt_getBannerMore(client=None, businessId=None, scene=None, bannerId=None, experimentKey=None,
                                        experimentParam=None, recommendId=None, expected: dict = None):
    """
    获取banner 的more数据,支持返回加密视频

    :param businessId: integer - 短剧id,在banner为banner主键id
    :param scene: string - 查询的场景：埋点对应的场景，例如collections，recently，deeplink
    :param bannerId: integer
    :param experimentKey: string - 客户端实验key
    :param experimentParam: integer - 实验参数
    :param recommendId: integer - 若返回中该字段为空则传0
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/homeData/encrypt/getBannerMore", expected,
                       json={"businessId": businessId, "scene": scene, "bannerId": bannerId,
                             "experimentKey": experimentKey, "experimentParam": experimentParam,
                             "recommendId": recommendId})
    return client, resp


# @allure.title("获取tab化的首页数据  ;支持多tab的首页,支持视频加密")
def ffff_homeData_encrypt_getTabHomeData(client=None, experimentKey=None, experimentParam=None, newbieShowType=None,
                                         installTime=None, isCodeStarted=None, expected: dict = None):
    """
    获取tab化的首页数据  ;支持多tab的首页,支持视频加密

    :param experimentKey: string - 客户端实验key
    :param experimentParam: integer - 实验参数
    :param newbieShowType: integer - 新人信息展示类型；1-新人页面，2-新人tab
    :param installTime: integer - 用户安装时间， 毫秒的时间戳
    :param isCodeStarted: boolean - 是否冷启动
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/homeData/encrypt/getTabHomeData", expected,
                       json={"experimentKey": experimentKey, "experimentParam": experimentParam,
                             "newbieShowType": newbieShowType, "installTime": installTime,
                             "isCodeStarted": isCodeStarted})
    return client, resp


# @allure.title("首页相关配置接口")
def ffff_homeData_getHomeConfig(client=None, expected: dict = None):
    """
    首页相关配置接口

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/homeData/getHomeConfig", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_homeData_encrypt_getBannerMore ...")
    ffff_homeData_encrypt_getBannerMore()

    print("▶ 调用 ffff_homeData_encrypt_getTabHomeData ...")
    ffff_homeData_encrypt_getTabHomeData()

    print("▶ 调用 ffff_homeData_getHomeConfig ...")
    ffff_homeData_getHomeConfig()
