from utils.http_api import HttpClientWrapperSimple


# @allure.title("android 平台订阅")
def ffff_subscription_android(client=None, token=None, skuId=None, productId=None, source=None, receiveType=None,
                              recover=None, shortPlayId=None, episode=None, oldToken=None, changeMode=None,
                              newProductId=None, marketingCampaignId=None, activityId=None, expected: dict = None):
    """
    android 平台订阅

    :param token: string
    :param skuId: string
    :param productId: integer
    :param source: string - 订阅场景
    :param receiveType: integer - 奖level=0是对照组，只能领取当天
level=1是实验组，可以领取之前所有未领取的天数的
    :param recover: boolean - 是否补单
    :param shortPlayId: integer - 短剧id
    :param episode: integer - 集数
    :param oldToken: string - 老订阅购买token,升降级时需要传
    :param changeMode: integer - 升降级模式   ,升降级时需要传
0-降级，1-升级,2-普通购买
    :param newProductId: integer - 降级时需要传，传新productId
    :param marketingCampaignId: integer - 常规营销活动
    :param activityId: string - 活动id (包含常规营销活动id)
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/subscription/android", expected,
                       json={"token": token, "skuId": skuId, "productId": productId, "source": source,
                             "receiveType": receiveType, "recover": recover, "shortPlayId": shortPlayId,
                             "episode": episode, "oldToken": oldToken, "changeMode": changeMode,
                             "newProductId": newProductId, "marketingCampaignId": marketingCampaignId,
                             "activityId": activityId})
    return client, resp


# @allure.title("ios 平台订阅V2 -- 增加升降级处理")
def ffff_subscription_iosV2(client=None, receiptData=None, skuType=None, extra=None, source=None, receiveType=None,
                            skuId=None, payAmount=None, currency=None, quantity=None, introPayAmount=None,
                            introCurrency=None, shortPlayId=None, episode=None, skuProductId=None, activityId=None,
                            orderNo=None, isRestore=None, expected: dict = None):
    """
    ios 平台订阅V2 -- 增加升降级处理

    :param receiptData: string - 支付回执
    :param skuType: integer
    :param extra: string
    :param source: string - 订阅场景
    :param receiveType: integer - level=0是对照组，只能领取当天
level=1是实验组，可以领取之前所有未领取的天数的
    :param skuId: string - skuId
    :param payAmount: string - 支付金额
    :param currency: string - 货币代码
    :param quantity: string - 数量
    :param introPayAmount: string - 首充等intro活动价格
    :param introCurrency: string - 首充等intro活动价格单位
    :param shortPlayId: integer - 短剧id
    :param episode: integer - 集数
    :param skuProductId: string
    :param activityId: string - 活动ID
    :param orderNo: string
    :param isRestore: string
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/subscription/iosV2", expected,
                       json={"receiptData": receiptData, "skuType": skuType, "extra": extra, "source": source,
                             "receiveType": receiveType, "skuId": skuId, "payAmount": payAmount, "currency": currency,
                             "quantity": quantity, "introPayAmount": introPayAmount, "introCurrency": introCurrency,
                             "shortPlayId": shortPlayId, "episode": episode, "skuProductId": skuProductId,
                             "activityId": activityId, "orderNo": orderNo, "isRestore": isRestore})
    return client, resp


# @allure.title("查询用户订阅信息")
def ffff_subscription(client=None, expected: dict = None):
    """
    查询用户订阅信息

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.get(f"{base_url}/ffff/subscription", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_subscription_android ...")
    ffff_subscription_android()

    print("▶ 调用 ffff_subscription_iosV2 ...")
    ffff_subscription_iosV2()

    print("▶ 调用 ffff_subscription ...")
    ffff_subscription()
