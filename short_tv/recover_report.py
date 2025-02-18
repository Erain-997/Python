# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/12/30
import json
import os
import subprocess
import sys
import time

from common.mysql.mysql import MySQLClient
from common.utils.arg_parse_func import args
from common.utils.log_utils import Log
from common.utils.path_config import android
from common.utils.report import set_report_env_on_results, set_report_executor_on_results, rename_video, get_app_version

'''
当任务异常中断时, 手动继续生成报告, 基于已有allure_results数据源的情况下
执行命令, 在当前文件夹下: python recover_report.py 172.16.9.35:9999 172_16_9_25_9999_2024_12_27_17_34_59 -task_id 7
'''
if __name__ == '__main__':
    # 生成报告
    testing_module = ["修复"]
    args.modules=testing_module
    path = os.path.join(android.report_output_dir, args.output_report)
    # 生成报告中的环境信息
    set_report_env_on_results(path, [], None)
    set_report_executor_on_results(path)
    rename_video()
    try:
        # 生成Allure报告 --single-file
        cmd = f"allure generate {path}/allure-results -o {path}/reports --clean"
        os.system(cmd)

    except subprocess.CalledProcessError as e:
        Log.logger.info(f"生成allure报告失败, 请检查{path}数据源\n", str(e))
    time.sleep(3)

    client = MySQLClient()
    client.connect()
    report_path = f"files/{args.output_report}/reports/index.html"
    result = client.execute_query("SELECT * FROM test_plan WHERE id = %s", [args.task_id])
    if not result:
        Log.logger.info("脚本报告入库失败, 报告地址:%s", report_path)
    else:
        if result[0]["report"]:
            report = json.loads(result[0]["report"])
            report.append(report_path)
        else:
            report = [report_path]
        client.execute_non_query(
            f"UPDATE test_plan SET version=%s,report= %s,status='Completed',last_report = %s WHERE id = %s",
            [get_app_version(), json.dumps(report), f"files/{args.output_report}/reports/index.html", args.task_id])
    if args.task_id:
        client.execute_non_query(
            f"INSERT INTO report (plan_id, old_name, new_name) VALUES (%s, %s, %s);",
            [args.task_id, f"files/{args.output_report}/reports/index.html",
             f"files/{args.output_report}/reports/index.html"])
    client.close()

    # 记录结束时间
    end_time = time.time()

    Log.logger.info("脚本运行结束")
    sys.exit(0)
