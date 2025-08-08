from utils.http_api import HttpClientWrapperSimple


# @allure.title("获取今日可得到的bonus总数")
def ffff_bonusRecord_getBonusTotal(client=None, cumsumViewCase=None, expected: dict = None):
    """
    获取今日可得到的bonus总数

    :param cumsumViewCase: integer - 累计看剧时长实验组 2才显示
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/bonusRecord/getBonusTotal", expected, json={"cumsumViewCase": cumsumViewCase})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_bonusRecord_getBonusTotal ...")
    ffff_bonusRecord_getBonusTotal()
