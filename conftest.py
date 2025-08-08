import os

from utils.logger_manager import LoggerManager


def pytest_sessionstart(session):
    """
    - 按照执行模块初始化日志
    """
    log_name = None

    # 获取 pytest 启动时的参数
    test_paths = session.config.args

    if not test_paths:
        log_name = "all_tests"
    else:
        # 只传了一个路径
        if len(test_paths) == 1:
            path = test_paths[0]
            if os.path.isfile(path):
                # 单个文件
                log_name = os.path.splitext(os.path.basename(path))[0]
            elif os.path.isdir(path):
                # 整个目录
                log_name = os.path.basename(os.path.normpath(path))
        else:
            # 多个测试目标，统一命名
            log_name = "multiple_tests"

    # 确保日志目录存在
    base_path = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(base_path, "log"), exist_ok=True)

    # 初始化日志
    if log_name:
        LoggerManager().init(filename=os.path.join(log_name))
