from utils.http_api import HttpClientWrapperSimple


# @allure.title("获取资源位配置(特殊版本)")
def ffff_activityResource_resourceListByTypes(client=None, extraTypes=None, supportSkipTypes=None,
                                              expected: dict = None):
    """
    获取资源位配置(特殊版本)

    :param extraTypes: string - 除开屏页、首页弹窗、首页底部悬浮类型其他需要展示的资源类型，逗号分隔,不传不展示额外资源只展示原先3种
3:"底部TAB栏",4:"我的底部横幅",5:"追剧横幅",6:"搜索页横幅"
周年庆版本固定传 3,4,5,6
    :param supportSkipTypes: string - 支持的跳转类型 多个使用逗号分隔
    SHORT_PLAY(0, "短剧"),
    H5(1, "h5"),
    NATIVE(2, "Native"),
    BROWSER_OFFICIAL(3, "端外浏览器(官方)"),
    BROWSER_NOT_OFFICIAL(4, "端外浏览器(非官方)"),
    MARKETING_CAMPAIGN(5, "常规营销活动"),
    BRAND_AD(6, "品牌方广告"),
    PROGRAMMATIC_AD(7, "程序化广告"),
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/activityResource/resourceListByTypes", expected,
                       json={"extraTypes": extraTypes, "supportSkipTypes": supportSkipTypes})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_activityResource_resourceListByTypes ...")
    ffff_activityResource_resourceListByTypes()
