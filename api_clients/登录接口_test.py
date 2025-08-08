from utils.http_api import HttpClientWrapperSimple


# @allure.title("三方授权登录")
def ffff_login_tripartiteLogin(client=None, authType=None, firebaseSource=None, authToken=None, idToken=None,
                               userCode=None, registerCode=None, secretKey=None, gaid=None, idfa=None, firstName=None,
                               lastName=None, expected: dict = None):
    """
    三方授权登录

    :param authType: integer - 授权类型 10代表google  20代表facebook登录 80代表apple登录 1000代表firebase登录
    :param firebaseSource: integer - firebase下的授权类型 10代表google  20代表facebook登录 80代表apple登录
    :param authToken: string - 授权token
    :param idToken: string - Firebase用户令牌
    :param userCode: string - 用户编号(游客第一次绑定的时候需要传)
    :param registerCode: string - 注册码
    :param secretKey: string
    :param gaid: string - gaid
    :param idfa: string - idfa
    :param firstName: string - 姓
    :param lastName: string - 名
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/login/tripartiteLogin", expected,
                       json={"authType": authType, "firebaseSource": firebaseSource, "authToken": authToken,
                             "idToken": idToken, "userCode": userCode, "registerCode": registerCode,
                             "secretKey": secretKey, "gaid": gaid, "idfa": idfa, "firstName": firstName,
                             "lastName": lastName})
    return client, resp


# @allure.title("初始化注册登录")
def ffff_login_initLogin(client=None, deviceId=None, secretKey=None, gaid=None, idfa=None, expected: dict = None):
    """
    初始化注册登录

    :param deviceId: string - 设备唯一编号
    :param secretKey: string
    :param gaid: string - gaid
    :param idfa: string - idfa
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/login/initLogin", expected,
                       json={"deviceId": deviceId, "secretKey": secretKey, "gaid": gaid, "idfa": idfa})
    return client, resp


# @allure.title("用户信息查询")
def ffff_login_getUserInfo(client=None, expected: dict = None):
    """
    用户信息查询

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/login/getUserInfo", expected, json={})
    return client, resp


# @allure.title("账号删除")
def ffff_login_deleteAccount(client=None, expected: dict = None):
    """
    账号删除

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/login/deleteAccount", expected, json={})
    return client, resp


# @allure.title("退出登录")
def ffff_login_loginOut(client=None, expected: dict = None):
    """
    退出登录

    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/login/loginOut", expected, json={})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_login_tripartiteLogin ...")
    ffff_login_tripartiteLogin()

    print("▶ 调用 ffff_login_initLogin ...")
    ffff_login_initLogin()

    print("▶ 调用 ffff_login_getUserInfo ...")
    ffff_login_getUserInfo()

    print("▶ 调用 ffff_login_deleteAccount ...")
    ffff_login_deleteAccount()

    print("▶ 调用 ffff_login_loginOut ...")
    ffff_login_loginOut()
