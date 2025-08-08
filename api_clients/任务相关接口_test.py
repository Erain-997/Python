from utils.http_api import HttpClientWrapperSimple


# @allure.title("获取任务列表")
def ffff_appTask_getAppTaskList(client=None, expected: dict = None):
    """
    获取任务列表

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/appTask/getAppTaskList", expected, json={})
    return client, resp


# @allure.title("领取奖励")
def ffff_appTask_receiveRewards(client=None, taskId=None, expected: dict = None):
    """
    领取奖励

    :param taskId: integer - 任务id
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/appTask/receiveRewards", expected, json={"taskId": taskId})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_appTask_getAppTaskList ...")
    ffff_appTask_getAppTaskList()

    print("▶ 调用 ffff_appTask_receiveRewards ...")
    ffff_appTask_receiveRewards()
