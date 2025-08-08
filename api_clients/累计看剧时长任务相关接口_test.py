from utils.http_api import HttpClientWrapperSimple


# @allure.title("获取任务配置")
def ffff_watchTimeTask_getTaskConfig(client=None, expected: dict = None):
    """
    获取任务配置

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/watchTimeTask/getTaskConfig", expected, json={})
    return client, resp


# @allure.title("领取奖励")
def ffff_watchTimeTask_receiveReward(client=None, taskIds=None, expected: dict = None):
    """
    领取奖励

    :param taskIds: array - 任务id
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/watchTimeTask/receiveReward", expected, json={"taskIds": taskIds})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_watchTimeTask_getTaskConfig ...")
    ffff_watchTimeTask_getTaskConfig()

    print("▶ 调用 ffff_watchTimeTask_receiveReward ...")
    ffff_watchTimeTask_receiveReward()
