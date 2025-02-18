import json
import sys
import time

import pytest

from common.mysql.mysql import MySQLClient
from common.mysql.mysql_tools import update_device, mysql_execute
from common.utils.arg_parse_func import args
from common.utils.cmd_tools import wait_for_appium_to_start, install_apk, is_appium_running_and_kill
from common.utils.feishu import feishu_push
from common.utils.log_utils import Log
from common.utils.path_config import android
from common.utils.report import generate_report, get_app_version, get_cases_num, get_pass_rate, \
    get_run_time, get_modules_name

# 优雅关闭
# def graceful_shutdown(signum, frame):
#     Log.logger.info("正在清理环境...")

#     # 终止 Appium 进程
#     try:
#         is_appium_running_and_kill(args.port)
#         Log.logger.info("终止 Appium 进程")
#     except Exception as e:
#         Log.logger.error(f"Error terminating appium process: {e}")

#     # 更新数据库中的设备状态
#     try:
#         query, params = update_device(args.device, {"testing_status": None})
#         mysql_execute(query, params)
#         Log.logger.info("更新数据库中设备状态")
#     except Exception as e:
#         Log.logger.error(f"Error updating device status: {e}")

#     # 更新数据库中的测试计划状态
#     try:
#         mysql_execute(f"UPDATE test_plan SET status='Stop' WHERE id = %s", [args.task_id])
#     except Exception as e:
#         Log.logger.error(f"Error closing MySQL connection: {e}")

#     # 更新手机代理
#     try:
#         subprocess.check_output(["adb", "-s", args.device, "shell", "settings", "put", "global", "http_proxy", ":0"])
#         Log.logger.error(f"清空代理")
#     except Exception as e:
#         Log.logger.error(f"清空代理失败: {e}")

#     Log.logger.info("清理环境 completed.")
#     sys.exit(0)


# # 注册信号处理器
# signal.signal(signal.SIGINT, graceful_shutdown)  # 处理 Ctrl+C
# signal.signal(signal.SIGTERM, graceful_shutdown)  # 处理 kill 命令
if __name__ == "__main__":
    # 打印所有args参数
    for key, value in vars(args).items():
        Log.logger.info(f"{key}: {value}")

    if args.get_cases:
        pytest.main(["-v", "sys_android/test_cases/new/", "--co", "--setup-show"])
        sys.exit(0)

    testing_module = ""
    try:
        # appium
        wait_for_appium_to_start(args.port)
        # 更新app
        if args.apk:
            install_apk(args.apk)

        # 重定向标准输出
        sys.stdout = Log
        command = [
            "-s",
            "-v",
            # 展示描述
            "--setup-show",
            "--capture=no",
            "--continue-on-collection-errors",
            f"--alluredir={android.report_output_dir}/{args.output_report}/allure-results",
            # 单用例
            # "sys_android/test_cases/v1_9_11/test_demo.py::TestDemo::test_demo_02",
            # 单文件
            # "sys_android/test_cases/v1_9_11/test_all.py",
            # 单文件夹
            # "sys_android/test_cases/v1_9_11/test_advertisement_module.py",
            # "sys_android/test_cases/v1_9_11/test_demo.py",
            # 只收集不跑
            # "--co",
            # pytest日志
            # "--log-file", f"{f"{android.report_output_dir}/{args.output_report}"}/log_pytest.log",
        ]
        command.extend([*args.modules])

        if args.k:
            command.extend([args.root_path, "-k", args.kl])
            testing_module = f"正则匹配: {args.k}"
        elif args.m:
            command.extend([args.root_path, "-m", args.m])
            testing_module = f"根据pytest标签执行: {args.m}"
        elif args.allure_features:
            features = ','.join(args.allure_features)
            command.extend([args.root_path, f"--allure-features={features}"])
            testing_module = f"根据allure标签执行: allure-features={features}"
        elif args.allure_stories:
            stories = ','.join(args.allure_stories)
            command.extend([args.root_path, f"--allure-stories={stories}"])
            testing_module = f"根据allure标签执行: allure-stories={stories}"
        else:
            testing_module = ""
        if args.rerun != "0":
            command.extend(["--reruns", args.rerun])

        Log.logger.info("开始执行测试, 执行设备: %s,   %s", args.device, args.modules)
        Log.logger.info("运行pytest框架: %s", command)
        # 开始
        query, params = update_device(args.device, {"testing_status": str(get_modules_name()) + testing_module})
        mysql_execute(query, params)

        pytest.main(command)
        # 结束
        query, params = update_device(args.device, {"testing_status": None})
        mysql_execute(query, params)

    # 恢复标准输出到控制台
    # sys.stdout = sys.__stdout__
    except Exception as e:
        Log.logger.info(f"测试失败:{e}")

    try:
        is_appium_running_and_kill(args.port)
        Log.logger.info(f"appium_process结束")
    except Exception as e:
        Log.logger.info(f"appium_process结束错误:{e}")

    # 记录开始时间
    start_time = time.time()

    # 生成报告
    generate_report([], testing_module)
    time.sleep(3)

    # # 启动allure服务
    # allure_server(get_local_ip(), args.port)

    # 通知飞书
    if args.feishu:
        feishu_push(args.output_report)

    client = MySQLClient()
    client.connect()
    report_path = f"files/{args.output_report}/reports/index.html"
    result = client.execute_query("SELECT * FROM test_plan WHERE id = %s", [args.task_id])
    if not result:
        Log.logger.info("脚本报告入库失败, 报告地址:%s", report_path)
    else:
        if result[0]["report"]:
            report = json.loads(result[0]["report"])
            report.insert(0, report_path)
        else:
            report = [report_path]
        client.execute_non_query(
            f"UPDATE test_plan SET version=%s,report= %s,status='Completed',last_report = %s WHERE id = %s",
            [get_app_version(), json.dumps(report), report_path, args.task_id])

    if args.task_id != "默认":
        client.execute_non_query(
            f"INSERT INTO report (plan_id, old_name, new_name,test_cases,case_num,pass_rate,apk_version,run_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);",
            [args.task_id, report_path, report_path, str(get_modules_name()) + testing_module, get_cases_num(),
             get_pass_rate(), get_app_version(), get_run_time()])
    client.close()

    # 记录结束时间
    end_time = time.time()

    # 计算并打印运行时间
    elapsed_time = end_time - start_time
    print(f"代码运行时间为: {elapsed_time} 秒")

    Log.logger.info("脚本运行结束")
    sys.exit(0)
