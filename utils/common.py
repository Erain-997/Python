import random
import string
import uuid


# 生成随机 deviceId
def generate_device_id(length=32):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


COMMON_HEADERS = {
    "Connection": "keep-alive",
    "clientplatform": "android",
    "language": "en",
    "content-type": "application/json",
    "traceid": "Locust-" + str(uuid.uuid4()),
    # "traceid": "cf9effe3-1857-4411-b4d8-1f6e8c8eaf59",
    # "vefcode": "76d3fc4",
    # "timezone": "+08",
    # "afversion": "1",
    # "User-Agent": "Dart/3.6 (dart:io)",
    # "isr": "false",
    # "Accept-Encoding": "gzip",
    # "locale": "en_GB",
    # "system_country_code": "GB",
    # "X-Amz-Cf-Id": "7PBPAspMf5_PKfc3Ky_EJp4VD8AZzNbca0W8G17VwOs2K1sDJznZcQ==",
    # "model": "samsung SM-A165F",
    # "Accept": "application/json",
    # "X-Forwarded-Proto": "http",
    # "Host": "api-stress.ffff.team",
    # "X-Forwarded-Port": "80",
    # "X-Amzn-Trace-Id": "Root=1-67fb1dfd-7b7524387001e27d0756ee2a",
    # "androidversion": "1.1.0",
    # "Via": "1.1 cloudfront.net (CloudFront)",
    # "environment": "prod",
    # "buildvalue": "1.1.0",
    # "X-Forwarded-For": "111.65.63.55, 130.176.187.8",
    # "ise": "true",
    # "isd": "true"
}
