from utils.http_api import HttpClientWrapperSimple


# @allure.title("用户发送邮箱验证码")
def ffff_user_sendEmail(client=None, email=None, otp=None, expected: dict = None):
    """
    用户发送邮箱验证码

    :param email: string - 用户邮箱
    :param otp: string - 验证码
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/sendEmail", expected, json={"email": email, "otp": otp})
    return client, resp


# @allure.title("用户绑定firebase List")
def ffff_user_bindList(client=None, types=None, expected: dict = None):
    """
    用户绑定firebase List

    :param types: string - 版本支持展示的绑定类型
example：10,20,50,60
不传或者空串则取默认值 20,50,60
 10：GG, 20：FB， 50：email，60：phone
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/bindList", expected, json={"types": types})
    return client, resp


# @allure.title("用户绑定firebase check")
def ffff_user_addBind(client=None, idToken=None, authType=None, authToken=None, expected: dict = None):
    """
    用户绑定firebase check

    :param idToken: string - Firebase用户令牌
    :param authType: integer - 授权类型
    :param authToken: string - 授权token
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/addBind", expected,
                       json={"idToken": idToken, "authType": authType, "authToken": authToken})
    return client, resp


# @allure.title("绑定用户手机号")
def ffff_user_bindByPhone(client=None, verificationCode=None, phone=None, areaCode=None, expected: dict = None):
    """
    绑定用户手机号

    :param verificationCode: string - 验证码
    :param phone: string - 手机号码,不带区号
    :param areaCode: string - 手机区号，例如，+86
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/bindByPhone", expected,
                       json={"verificationCode": verificationCode, "phone": phone, "areaCode": areaCode})
    return client, resp


# @allure.title("绑定用户邮箱验证码")
def ffff_user_bindByEmail(client=None, email=None, otp=None, expected: dict = None):
    """
    绑定用户邮箱验证码

    :param email: string - 用户邮箱
    :param otp: string - 验证码
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/user/bindByEmail", expected, json={"email": email, "otp": otp})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_user_sendEmail ...")
    ffff_user_sendEmail()

    print("▶ 调用 ffff_user_bindList ...")
    ffff_user_bindList()

    print("▶ 调用 ffff_user_addBind ...")
    ffff_user_addBind()

    print("▶ 调用 ffff_user_bindByPhone ...")
    ffff_user_bindByPhone()

    print("▶ 调用 ffff_user_bindByEmail ...")
    ffff_user_bindByEmail()
