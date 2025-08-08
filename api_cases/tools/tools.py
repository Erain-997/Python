import uuid
import pytest

from api_clients.登录接口_test import ffff_login_initLogin


def login():
    client, resp = ffff_login_initLogin(deviceId=str(uuid.uuid4()))
    if resp["status"] != 0:
        pytest.fail(f"Login failed: {resp}")
    client.token = resp["data"]["token"]
    client.user_id = resp["data"]["userResponse"]["userId"]
    return client
