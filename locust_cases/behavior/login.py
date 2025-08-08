# utils/login_helper.py
import time
from utils.login import login_and_get_token
from utils.http_client import HttpClientWrapper
from utils.common import COMMON_HEADERS
from utils.logger_manager import LoggerManager

logger = LoggerManager().get_logger(name=__name__)


def init_user_http(client, max_retries=5, retry_interval=1):
    trace_id = None

    for i in range(max_retries):
        try:
            token, _, trace_id, user_id = login_and_get_token(client)
            if token:
                logger.info(
                    f"[User {id(client)}] 登录成功: user_id={user_id}, trace_id={trace_id}"
                )
                return HttpClientWrapper(
                    client,
                    token=token,
                    user_id=user_id,
                    default_headers=COMMON_HEADERS,
                )
            else:
                logger.warning(
                    f"[User {id(client)}] 登录失败（空 token）, trace_id={trace_id}"
                )
        except Exception as e:
            logger.error(
                f"[User {id(client)}] 登录异常: {e}, trace_id={trace_id}"
            )

        time.sleep(retry_interval)

    logger.critical(
        f"[User {id(client)}] 登录失败，用户将无法执行后续任务，trace_id={trace_id}"
    )
    return None
