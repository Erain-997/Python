import uuid
from utils.common import COMMON_HEADERS, generate_device_id

SECRET_KEY = "h7zkahQvCb05lYZvt11lYbmpndozqDZy66V8krAxEfhDBwjYpuDyp2iAukogTl3EyZFTW57X2zRDSkxg+ODSFF5asZdoVV0WCFLXpHMkxu8dX0UD2ZmsL44btSmdgFa+h8Caj/0RCt+GvgW7z5Gxpzs+Yxv0uCiUdUS//EhV6MY="


def login_and_get_token(client):
    device_id = generate_device_id()
    payload = {"deviceId": device_id, "secretKey": SECRET_KEY}
    header = COMMON_HEADERS
    header["traceid"] = "Locust-" + str(uuid.uuid4())
    with client.post(
            "/ffff/login/initLogin", headers=header, json=payload, catch_response=True
    ) as resp:
        if resp.status_code != 200:
            resp.failure(f"Login failed: {resp.status_code}, traceid: {header['traceid']}")
            return None, None, header["traceid"], None
        try:
            data = resp.json()
            token = data["data"]["token"]
            user_id = data["data"]["userResponse"]["userId"]
            if not token:
                resp.failure(f"Login failed: {resp}, traceid: {header['traceid']}")
                return None, None, header["traceid"], None
            resp.success()
            return token, device_id, header["traceid"], user_id
        except Exception as e:
            resp.failure(f"Failed to parse login response: {str(e)}, traceid: {header['traceid']}")
            return None, None, header["traceid"], None
