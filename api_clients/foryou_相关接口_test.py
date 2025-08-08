from utils.http_api import HttpClientWrapperSimple


# @allure.title("推送池随机获取一条数据 -加密接口")
def ffff_forYou_encrypt_getForYouListOnlyOne(client=None, expected: dict = None):
    """
    推送池随机获取一条数据 -加密接口

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/forYou/encrypt/getForYouListOnlyOne", expected, json={})
    return client, resp


# @allure.title("新版feed流，实验组，加密接口")
def ffff_forYou_encrypt_getForYouListPageNewV2(client=None, pageSize=None, pageNum=None, isColdBoot=None,
                                               lastShortPlayId=None, consecutiveTimes=None, realLanguageCode=None,
                                               expected: dict = None):
    """
    新版feed流，实验组，加密接口

    :param pageSize: integer - 每页显示数量
    :param pageNum: integer - 页码(第几页)
    :param isColdBoot: integer - 是否冷启动 1是2否
    :param lastShortPlayId: integer - 分页最后一条的剧id,请求第一页时不用传
    :param consecutiveTimes: integer - 剧在末尾出现次数,请求第一页时不用传
    :param realLanguageCode: string - 用户实际请求语言，用于兜底语言逻辑，请求第一页时不用传，
后续页请求根据前页响应体里的该字段赋值
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/forYou/encrypt/getForYouListPageNewV2", expected,
                       json={"pageSize": pageSize, "pageNum": pageNum, "isColdBoot": isColdBoot,
                             "lastShortPlayId": lastShortPlayId, "consecutiveTimes": consecutiveTimes,
                             "realLanguageCode": realLanguageCode})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_forYou_encrypt_getForYouListOnlyOne ...")
    ffff_forYou_encrypt_getForYouListOnlyOne()

    print("▶ 调用 ffff_forYou_encrypt_getForYouListPageNewV2 ...")
    ffff_forYou_encrypt_getForYouListPageNewV2()
