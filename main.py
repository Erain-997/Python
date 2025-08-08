import time
import pytest
import os
import shutil
import subprocess


### todo
### 统一下路径: 日志, 工具包, 用例分层
### pytest框架完善
### 优化下http底层封装
### 优化下接口调用封装

def run_tests():
    output_dir = "reports"
    allure_output_dir = os.path.join(output_dir, "allure")
    # 创建 reports 目录
    os.makedirs(output_dir, exist_ok=True)
    # 创建 reports/allure 目录
    os.makedirs(allure_output_dir, exist_ok=True)

    time_now = time.strftime("%Y%m%d%H%M%S", time.localtime())

    allure_results_dir = os.path.join(allure_output_dir, time_now, "allure-results")
    allure_report_dir = os.path.join(allure_output_dir, time_now, "allure-report")

    # 2. 执行 Pytest 并生成 allure-results
    pytest_cmd = ["-v", "-s", "api_cases/1_2_8/test_top.py", f"--alluredir={allure_results_dir}"]
    pytest.main(pytest_cmd)

    # 3. 生成 Allure 报告（HTML）
    subprocess.run(["allure", "generate", f"{allure_results_dir}", "-o", f"{allure_report_dir}", "--clean"], check=True)

    # 4. 打开报告
    subprocess.run(["allure", "open", f"{allure_report_dir}"])


if __name__ == "__main__":
    run_tests()
