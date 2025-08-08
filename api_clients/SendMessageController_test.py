from utils.http_api import HttpClientWrapperSimple


# @allure.title("给用户发送验证码短信")
def ffff_message_sendMessageVerificationCode(client=None, phone=None, token=None, areaCode=None, sendTimes=None,
                                             expected: dict = None):
    """
    给用户发送验证码短信

    :param phone: string - 手机号码，不带区号
    :param token: string - firebase token
    :param areaCode: string - 手机区号，例如，+86
    :param sendTimes: integer - 第几次发送
    :param expected: dict - 断言期望值
    :param client: HttpClientWrapperSimple 实例（自动注入）
    :return: client, resp
    """
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.post(f"{base_url}/ffff/message/sendMessageVerificationCode", expected,
                       json={"phone": phone, "token": token, "areaCode": areaCode, "sendTimes": sendTimes})
    return client, resp


if __name__ == "__main__":
    print("▶ 调用 ffff_message_sendMessageVerificationCode ...")
    ffff_message_sendMessageVerificationCode()
