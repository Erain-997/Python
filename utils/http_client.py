import json
import uuid
from locust.clients import ResponseContextManager
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

import requests

from utils.common import COMMON_HEADERS
from utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(name=__name__)


# locust压测用
class HttpClientWrapper:
    def __init__(
            self,
            client=requests.Session(),
            token=None,
            user_id=None,
            default_headers=COMMON_HEADERS,
    ):
        self.client = client
        self.token = token
        self.user_id = user_id
        self.traceid = "default_traceid"
        self.headers = default_headers

    def _build_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        final = self.headers.copy()
        if headers:
            final.update(headers)
        if self.token:
            final["Authorization"] = self.token
        # 添加 traceid, 每次调用都会生成新值
        final["traceid"] = "Locusts-" + str(uuid.uuid4())
        return final

    def get(
            self,
            url: str,
            headers: Optional[Dict[str, str]] = None,
            api_name: str = "GET API",
    ) -> ResponseContextManager:
        final_headers = self._build_headers(headers)
        with self.client.get(
                url, headers=final_headers, catch_response=True
        ) as response:
            self.check_response(response, api_name=api_name, method="GET", url=url)
        return response

    def post(
            self,
            url: str,
            data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            api_name: str = "POST API",
            json_body: bool = True,
            expected_status=None,  # ✅ 新增参数
    ) -> ResponseContextManager:
        final_headers = self._build_headers(headers)
        payload = json.dumps(data) if (json_body and data) else data

        with self.client.post(
                url, headers=final_headers, data=payload, catch_response=True
        ) as response:
            self.check_response(
                response=response,
                api_name=api_name,
                method="POST",
                url=url,
                request_data=data,
                headers=final_headers,
                expected_status=expected_status,  # ✅ 传入
            )
        return response

    def check_response(
            self,
            response,
            api_name: str = "API",
            method: str = "",
            url: str = "",
            request_data: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            expected_status=None,  # ✅ 新增
    ):
        try:
            json_data = response.json()
        except Exception as e:
            logger.info(
                f"时间: {datetime.now()}: ❌ {api_name} 响应解析失败: {e}\n{response.text}, traceid: {headers["traceid"]}"
            )
            response.failure(f"❌ {api_name} 响应解析失败: {e}\n{response.text}")
            return

        actual_status = json_data.get("status")
        if actual_status == 0:
            response.success()
        elif expected_status is not None and actual_status in expected_status:
            # ✅ 预期的失败, 作为单独统计
            api_name = f"{url}(status: {actual_status})"
            # response._locust_name = name  # ✅ 修改 locust UI 中的名称
            response.request_meta["name"] = api_name  # ✅ 更新面板名称
            response.success()
        else:
            err_log = {
                "api": api_name,
                "method": method,
                "url": url,
                "request_data": request_data,
                "response": json_data,
                "traceid": headers["traceid"],
                "token": headers["Authorization"],
            }
            logger.info(
                f"时间: {datetime.now()}: ❌ {api_name} 响应失败: {json.dumps(err_log, ensure_ascii=False, indent=2)}"
            )
            response.failure(json.dumps(err_log, ensure_ascii=False, indent=2))
