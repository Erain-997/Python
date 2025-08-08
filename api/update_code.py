# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Author : Z Erain
# Date : 2025-07-21
# Description : 针对 matched_urls.txt 里的接口, 对应生成:
#               1. api_client文件夹: 内部封装了接口测试所需的接口请求
#               2. locust_tasks文件夹: 封装了符合 Locust 调用的接口请求
# ------------------------------------------------------------
import os
import json
import re
from pathlib import Path


def sanitize_name(name):
    return re.sub(r'[,<>:"/\\|?*、-]', '_', name).replace(" ", "_")


def generate_api_client_files(swagger_path, output_root="api_clients"):
    with open(swagger_path, "r", encoding="utf-8") as f:
        swagger = json.load(f)

    paths = swagger.get("paths", {})
    os.makedirs(output_root, exist_ok=True)

    tag_to_functions = {}

    for path, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "")
            if "（非客户端）" in summary:
                continue

            tags = details.get("tags", ["default"])
            tag = sanitize_name(tags[0])
            operation_id = details.get("operationId") or path.strip("/").replace("/", "_")

            parameters = details.get("parameters", [])
            param_list = ["client = None"]
            payload_dict = {}
            doc_params = []

            for param in parameters:
                if param.get("in") == "body":
                    schema = param.get("schema", {})
                    if schema.get("type") == "object":
                        for key, value in schema.get("properties", {}).items():
                            param_list.append(f'{key} = None')
                            payload_dict[key] = key

                            field_type = value.get("type", "Any")
                            field_desc = value.get("description", "").strip()
                            desc_line = f":param {key}: {field_type} - {field_desc}" if field_desc else f":param {key}: {field_type}"
                            doc_params.append(desc_line)

            param_list.append("expected: dict = None")
            doc_params.append(":param expected: dict - 断言期望值")
            doc_params.append(":param client: HttpClientWrapperSimple 实例（自动注入）")
            doc_params.append(":return: client, resp")

            param_str = ", ".join(param_list)
            payload_code = ", ".join(f'"{k}": {v}' for k, v in payload_dict.items())

            docstring = f'    """\n    {summary}\n{details.get("description", "")}\n'
            for line in doc_params:
                docstring += f'    {line}\n'
            docstring += '    """'

            func = f'''
# @allure.title("{summary}")
def {operation_id}({param_str}):
{docstring}
    base_url = "https://api-stress.ffff.team"
    client = HttpClientWrapperSimple() if client is None else client
    resp = client.{method.lower()}(f"{{base_url}}{path}", expected, json={{{payload_code}}})
    return client, resp
'''

            tag_to_functions.setdefault(tag, []).append((operation_id, func))

    for tag, funcs in tag_to_functions.items():
        filepath = Path(output_root) / f"{tag}_test.py"
        with open(filepath, "w", encoding="utf-8") as f:
            # f.write("import requests\n")
            # f.write("import allure\n")
            f.write("from utils.http_api import HttpClientWrapperSimple\n\n")

            for _, func in funcs:
                f.write(func)

            f.write('\n\nif __name__ == "__main__":\n')
            for operation_id, _ in funcs:
                f.write(f'    print("▶ 调用 {operation_id} ...")\n')
                f.write(f'    {operation_id}()\n\n')

    print(f"✅ 所有 API 封装已生成在：{output_root}/")


# ------------------- Locust task 生成 ------------------------

def generate_locust_user_files(swagger_path, output_root="locust_tasks"):
    with open(swagger_path, "r", encoding="utf-8") as f:
        swagger = json.load(f)

    paths = swagger.get("paths", {})
    os.makedirs(output_root, exist_ok=True)

    tag_to_methods = {}
    operation_ids = {}

    for path, methods in paths.items():
        for method, details in methods.items():
            summary = details.get("summary", "")
            if "（非客户端）" in summary:
                continue

            tags = details.get("tags", ["default"])
            tag = sanitize_name(tags[0])
            operation_id = details.get("operationId") or path.strip("/").replace("/", "_")
            tag_to_methods.setdefault(tag, []).append(operation_id)
            if tag not in operation_ids:
                operation_ids[tag] = operation_id

    for tag, method_list in tag_to_methods.items():
        class_base = "".join(part.title() for part in operation_ids[tag].split("_")[:2])
        class_name = f"{class_base}User"
        module_name = f"{tag}_api"

        tag_path = Path(output_root) / f"{tag}.py"
        with open(tag_path, "w", encoding="utf-8") as f:
            f.write(f'''"""
Locust user for tag: {tag}
"""
from locust import HttpUser, task, between
from api_clients import {module_name} as api

class {class_name}(HttpUser):
    wait_time = between(1, 2)
    base_url = "/"
''')
            for method in method_list:
                f.write(f'''
    @task
    def {method}(self):
        api.{method}(self.client, self.base_url)
''')
    print(f"✅ 所有 Locust 用户类已生成在：{output_root}/")


# ------------------- 脚本入口 ------------------------

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    swagger_file = base_dir / "swagger_updated.json"

    generate_api_client_files(swagger_file, str(base_dir.parent / "api_clients"))
    generate_locust_user_files(swagger_file, str(base_dir.parent / "locust_tasks"))
