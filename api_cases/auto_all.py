import os
import re

API_CLIENT_DIR = "../api_clients"
OUTPUT_TEST_FILE = "./test_all_apis.py"

# 匹配接口函数的正则，简单匹配 def 函数名(
FUNC_PATTERN = re.compile(r"def\s+(ffff_[\w_]+)\s*\(")


def find_api_functions(file_path):
    funcs = []
    with open(file_path, encoding="utf-8") as f:
        content = f.read()
    funcs = FUNC_PATTERN.findall(content)
    return funcs


def generate_test_case_code():
    imports = [
        "import pytest",
        "import allure",
        "from api_cases.tools.tools import login",
        "from utils.logger_manager import LoggerManager",
    ]

    # 遍历所有api_clients下的.py文件，收集函数名及模块名
    api_functions = []  # (module_name, func_name)
    for root, _, files in os.walk(API_CLIENT_DIR):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(full_path, '.').replace(os.sep, '.').replace("...", ''))[
                    0]
                # 例如 api_clients.签到相关接口_test
                funcs = find_api_functions(full_path)
                for func in funcs:
                    api_functions.append((module_name, func))

    # 构建import语句，分模块导入对应函数
    module_funcs_map = {}
    for module_name, func_name in api_functions:
        module_funcs_map.setdefault(module_name, []).append(func_name)

    for module_name, funcs in module_funcs_map.items():
        imports.append(f"from {module_name} import {', '.join(funcs)}")

    # 生成测试类和测试函数代码
    lines = []
    lines.append("")
    lines.append('@allure.feature("高频接口汇总 - 自动生成")')
    lines.append("class TestAllApis:")
    lines.append("    @pytest.fixture(scope='function', autouse=True)")
    lines.append("    def environment(self):")
    lines.append('        LoggerManager().init(filename="TestAllApis")')
    lines.append('        self.logger = LoggerManager().get_logger(name=__name__)')
    lines.append('        with allure.step("用户登录"):')
    lines.append('            self.client = login()')
    lines.append('        yield')
    lines.append('        with allure.step("用例环境清理"):')
    lines.append('            self.logger.info("用例环境清理")')
    lines.append("")

    for _, func_name in api_functions:
        lines.append(f'    @allure.title("{func_name} 接口测试")')
        lines.append(f'    def test_{func_name}_success(self):')
        lines.append(f'        {func_name}(self.client)')
        lines.append("")

    # 合成最终脚本
    full_code = "\n".join(imports) + "\n" + "\n".join(lines)
    return full_code


if __name__ == "__main__":
    code = generate_test_case_code()
    with open(OUTPUT_TEST_FILE, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"自动生成测试用例脚本完成，文件路径: {OUTPUT_TEST_FILE}")
