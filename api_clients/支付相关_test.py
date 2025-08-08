from utils.http_api import HttpClientWrapperSimple


# @allure.title("充值恢复 android")
def ffff_pay_android_recover(client=None, payRecoverAndroidInfoRequests=None, expected: dict = None):
    """
    充值恢复 android

    :param payRecoverAndroidInfoRequests: array
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/pay/android/recover", expected,
                       json={"payRecoverAndroidInfoRequests": payRecoverAndroidInfoRequests})
    return client, resp


# @allure.title("充值恢复 ios")
def ffff_pay_iOS_recover(client=None, receiptData=None, skuId=None, expected: dict = None):
    """
    充值恢复 ios

    :param receiptData: string - 支付回执
    :param skuId: string - skuId
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/pay/iOS/recover", expected, json={"receiptData": receiptData, "skuId": skuId})
    return client, resp


# @allure.title("将本地币种按照汇率转成美元")
def ffff_pay_localDollarCurrencyConversion(client=None, payAmount=None, currencyCode=None, expected: dict = None):
    """
    将本地币种按照汇率转成美元

    :param payAmount: string - 本地币种支付金额
    :param currencyCode: string - 货币代码，USD
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/pay/localDollarCurrencyConversion", expected,
                       json={"payAmount": payAmount, "currencyCode": currencyCode})
    return client, resp


# @allure.title("支付验证 Sku android")
def ffff_pay_android_coinSkuBuy(client=None, purchaseData=None, signature=None, currency=None, price=None,
                                skuProductId=None, skuModelConfigId=None, isRetain=None, activitySkuConfigId=None,
                                skuType=None, prizeId=None, extra=None, shortPlayId=None, episode=None,
                                expected: dict = None):
    """
    支付验证 Sku android

    :param purchaseData: string - 支付回执
    :param signature: string - signature
    :param currency: string
    :param price: string
    :param skuProductId: string
    :param skuModelConfigId: string
    :param isRetain: boolean - 是否膨胀商品true：是；false：否
    :param activitySkuConfigId: string - 活动 sku配置ID
    :param skuType: integer
    :param prizeId: integer
    :param extra: string
    :param shortPlayId: integer - 短剧id
    :param episode: integer - 集数
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/pay/android/coinSkuBuy", expected,
                       json={"purchaseData": purchaseData, "signature": signature, "currency": currency, "price": price,
                             "skuProductId": skuProductId, "skuModelConfigId": skuModelConfigId, "isRetain": isRetain,
                             "activitySkuConfigId": activitySkuConfigId, "skuType": skuType, "prizeId": prizeId,
                             "extra": extra, "shortPlayId": shortPlayId, "episode": episode})
    return client, resp


# @allure.title("支付验证 Sku ios")
def ffff_pay_iOS_coinSkuBuy(client=None, receiptData=None, skuId=None, payAmount=None, currency=None, quantity=None,
                            skuProductId=None, skuModelConfigId=None, isRetain=None, activitySkuConfigId=None,
                            skuType=None, prizeId=None, extra=None, shortPlayId=None, episode=None,
                            expected: dict = None):
    """
    支付验证 Sku ios

    :param receiptData: string - 支付回执
    :param skuId: string - skuId
    :param payAmount: string - 支付金额
    :param currency: string - 货币代码
    :param quantity: string - 数量
    :param skuProductId: string
    :param skuModelConfigId: string
    :param isRetain: boolean - 是否膨胀商品true：是；false：否
    :param activitySkuConfigId: string - 活动ID
    :param skuType: integer
    :param prizeId: integer
    :param extra: string
    :param shortPlayId: integer - 短剧id
    :param episode: integer - 集数
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/pay/iOS/coinSkuBuy", expected,
                       json={"receiptData": receiptData, "skuId": skuId, "payAmount": payAmount, "currency": currency,
                             "quantity": quantity, "skuProductId": skuProductId, "skuModelConfigId": skuModelConfigId,
                             "isRetain": isRetain, "activitySkuConfigId": activitySkuConfigId, "skuType": skuType,
                             "prizeId": prizeId, "extra": extra, "shortPlayId": shortPlayId, "episode": episode})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_pay_android_recover ...")
    ffff_pay_android_recover()

    print("▶ 调用 ffff_pay_iOS_recover ...")
    ffff_pay_iOS_recover()

    print("▶ 调用 ffff_pay_localDollarCurrencyConversion ...")
    ffff_pay_localDollarCurrencyConversion()

    print("▶ 调用 ffff_pay_android_coinSkuBuy ...")
    ffff_pay_android_coinSkuBuy()

    print("▶ 调用 ffff_pay_iOS_coinSkuBuy ...")
    ffff_pay_iOS_coinSkuBuy()
