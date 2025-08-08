from utils.http_api import HttpClientWrapperSimple


# @allure.title("落地页 客户端点击")
def ffff_clickAd_lpReport(client=None, clientWidth=None, clientHeight=None, devicePixelRatio=None, ttp=None,
                          intranetIp=None, languageCode=None, userAgent=None, deviceId=None, clipboard=None,
                          installReferrer=None, idfa=None, requestId=None, urlParam=None, app_clickId=None,
                          pageType=None, shortPlayId=None, eventType=None, transitType=None, externalId=None,
                          deviceInfo=None, pixel_version=None, expected: dict = None):
    """
    落地页 客户端点击

    :param clientWidth: string - 分辨率
    :param clientHeight: string
    :param devicePixelRatio: string - 像素比
    :param ttp: string
    :param intranetIp: string - 内网ip
    :param languageCode: string - 系统语言
    :param userAgent: string - ua头
    :param deviceId: string - 设备gaid,ios 为idfa
    :param clipboard: string - 剪贴板内容
    :param installReferrer: string - 谷歌透传参数
    :param idfa: string - idfa
    :param requestId: string - 请求唯一标识
    :param urlParam: string - url 完整地址,包含url 参数
    :param app_clickId: string - ttclickId
    :param pageType: integer - 1广告2分享
    :param shortPlayId: integer - 短剧id
    :param eventType: integer - 1 页面打开 2点击按钮 3跳转
    :param transitType: integer - 中转形式(10:跳过落地页，20:显示落地页)
    :param externalId: string
    :param deviceInfo: object
    :param pixel_version: string
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/clickAd/lpReport", expected,
                       json={"clientWidth": clientWidth, "clientHeight": clientHeight,
                             "devicePixelRatio": devicePixelRatio, "ttp": ttp, "intranetIp": intranetIp,
                             "languageCode": languageCode, "userAgent": userAgent, "deviceId": deviceId,
                             "clipboard": clipboard, "installReferrer": installReferrer, "idfa": idfa,
                             "requestId": requestId, "urlParam": urlParam, "app_clickId": app_clickId,
                             "pageType": pageType, "shortPlayId": shortPlayId, "eventType": eventType,
                             "transitType": transitType, "externalId": externalId, "deviceInfo": deviceInfo,
                             "pixel_version": pixel_version})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_clickAd_lpReport ...")
    ffff_clickAd_lpReport()
