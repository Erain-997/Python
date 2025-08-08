import sys


def get_user_class(case_map: dict, default_case: str = "top_9"):
    """
    解析命令行参数 --case=xxx, 动态导入对应 User 类。
    """
    case_key = None
    for arg in sys.argv:
        if arg.startswith("--case="):
            case_key = arg.split("=")[-1]

    case_key = case_key or default_case

    if case_key not in case_map:
        raise ValueError(f"用例选择错误: {case_key}, 支持: {list(case_map.keys())}")

    from importlib import import_module

    module_path, class_name = case_map[case_key].rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, class_name)
