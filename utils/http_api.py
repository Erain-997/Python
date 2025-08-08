from copy import deepcopy
import time
from typing import Dict, Optional
import uuid
import pytest
import requests
import allure
from requests.exceptions import RequestException

from utils.common import COMMON_HEADERS
from utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(name=__name__)


class HttpClientWrapperSimple:
    def __init__(
            self, token=None, retries=3, retry_interval=1, timeout=10, headers=None
    ):
        self.session = requests.Session()
        self.retries = retries
        self.retry_interval = retry_interval
        self.timeout = timeout
        self.user_id = None

        # 基于 COMMON_HEADERS 构建 headers
        final_headers = deepcopy(COMMON_HEADERS)
        if headers:
            final_headers.update(headers)
        if token:
            final_headers["Authorization"] = f"{token}"
            self.token = token
        else:
            self.token = None

        self.headers = final_headers
        self.session.headers.update(self.headers)

    def _build_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        final = self.headers.copy()
        if headers:
            final.update(headers)
        if self.token:
            final["Authorization"] = self.token
        # 添加 traceid, 每次调用都会生成新值
        final["traceid"] = "Locusts-" + str(uuid.uuid4())
        return final

    def _request(self, headers, method, url, expected: dict = None, **kwargs):
        logger.info(f"🚀 发起 {method.upper()} 请求: {url}")
        last_exception = None

        for attempt in range(1, self.retries + 1):
            try:
                with allure.step(f"第 {attempt} 次, 路径:{url} 预期返回: {expected}"):
                    if "timeout" not in kwargs:
                        kwargs["timeout"] = self.timeout

                    kwargs["headers"] = headers
                    response = self.session.request(method, url, **kwargs)
                    self._log_allure_request_response(url, method, kwargs, response)

                    try:
                        json_data = response.json()
                        actual_status = json_data.get("status")
                        actual_message = json_data.get("message")

                        # 判断是否有预期校验
                        if expected:
                            mismatch_fields = []
                            for key, val in expected.items():
                                if json_data.get(key) != val:
                                    mismatch_fields.append(
                                        f"{key}期望是 {val}，实际是 {json_data.get(key)}"
                                    )

                            if mismatch_fields:
                                error_message = "❌ 响应不符合预期: " + "; ".join(
                                    mismatch_fields
                                )
                                self._log_allure_error(error_message)
                            else:
                                logger.info(f"✅ 响应符合预期: {expected}")
                        else:
                            expected = {"status": 0}
                            if actual_status == 0:
                                logger.info(f"✅ 接口返回成功: {actual_message}")
                            else:
                                self._log_allure_error(
                                    f"❌ 接口返回错误状态码: {actual_status} - {actual_message} \n实际响应: {json_data} \n预期响应: {expected}"
                                )

                        return json_data

                    except ValueError:
                        self._log_allure_error(
                            f"❌ 无法解析 JSON，响应为: {response.text}"
                        )
                        return {"status": -1, "message": "JSON解析失败", "data": None}

            except (RequestException, AssertionError) as e:
                last_exception = e
                self._log_allure_error(f"⚠️ 请求异常: {str(e)}")
                time.sleep(self.retry_interval)

        self._log_allure_error(f"❌ 所有请求重试失败: {str(last_exception)}")
        return {"status": -1, "message": "请求失败", "data": None}

    # todo  这里日志不准, 应该打印self里的
    def _log_allure_request_response(self, url, method, kwargs, response):
        allure.attach(
            f"{method.upper()} {url}\nHeaders: {kwargs.get('headers')}\nPayload: {kwargs.get('json') or kwargs.get('data')}",
            name="📤 请求详情",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            f"Status Code: {response.status_code}\nBody: {response.text} \n实际响应: {response}",
            name="📥 响应详情",
            attachment_type=allure.attachment_type.TEXT,
        )

    def _log_allure_error(self, message):
        logger.info(message)
        allure.attach(
            message, name="❗错误日志", attachment_type=allure.attachment_type.TEXT
        )
        pytest.fail(message)

    def get(self, url, expected: dict = None, **kwargs):
        if "headers" in kwargs:
            headers = self._build_headers(kwargs["headers"])
        else:
            headers = self._build_headers(self.headers)
        return self._request(headers, "get", url, expected, **kwargs)

    def post(self, url, expected: dict = None, **kwargs):
        if "headers" in kwargs:
            headers = self._build_headers(kwargs["headers"])
        else:
            headers = self._build_headers(self.headers)
        return self._request(headers, "post", url, expected, **kwargs)
