import requests

import requests
import json

# 全局变量，保存 cookie
session = requests.Session()


def login_yapi(username: str, password: str) -> bool:
    """
    登录 YAPI，保存 Cookie 到全局 session
    """
    url = "https://yapi.ffff.team/api/user/login"
    payload = {
        "email": username,
        "password": password
    }

    try:
        resp = session.post(url, json=payload)
        resp.raise_for_status()

        if resp.status_code == 200 and resp.json().get("errcode") == 0:
            print("✅ 登录成功")
            return True
        else:
            print("❌ 登录失败:", resp.text)
            return False

    except requests.RequestException as e:
        print("❌ 登录请求失败:", e)
        return False


def download_swagger_json(pid: int, output_file: str = None) -> dict:
    """
    下载 Swagger JSON 并可选保存为本地文件（需要已登录）
    """
    url = "https://yapi.ffff.team/api/plugin/exportSwagger"
    params = {
        "type": "OpenAPIV2",
        "pid": pid,
        "status": "all",
        "isWiki": "false"
    }

    try:
        resp = session.get(url, params=params)
        resp.raise_for_status()
        swagger_json = resp.json()

        if output_file:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(swagger_json, f, ensure_ascii=False, indent=2)
            print(f"✅ Swagger JSON 已保存到 {output_file}")

        return swagger_json

    except requests.RequestException as e:
        print("❌ 下载失败:", e)
        return {}
    except ValueError as e:
        print("❌ JSON 解析失败:", e)
        return {}


if __name__ == '__main__':
    if login_yapi(username="zhengyirun@team.com", password="ZHb8AHH7"):
        swagger_data = download_swagger_json(pid=30, output_file="swaggerApi.json")
