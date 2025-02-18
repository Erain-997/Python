import json
import subprocess
import time

from common.mysql.mysql import MySQLClient
from common.mysql.mysql_tools import mysql_execute
from common.utils.arg_parse_func import args
from common.utils.device_tools import get_device_names, get_device_version
from common.utils.log_utils import Log
from common.utils.path_config import android
from common.utils.tools import *


def get_app_version():
    try:
        # 运行 adb 命令并获取完整输出
        full_output = subprocess.check_output(
            ["adb", "-s", args.device, "shell", "dumpsys", "package", "com.startshorts.androidplayer"],
            text=True,  # 返回字符串而不是字节
        )

        # 在 Python 中搜索版本行
        for line in full_output.splitlines():
            if "versionName=" in line:
                return line.split("=")[-1].strip()
    except subprocess.CalledProcessError:
        return None

def compare_versions(v1=get_app_version(), v2="2.0.5"):
    parts1 = v1.split('.')
    parts2 = v2.split('.')
    # 将版本号部分转换为整数进行比较
    for p1, p2 in zip(parts1, parts2):
        if int(p1) >= int(p2):
            return True
        elif int(p1) < int(p2):
            return False
    # 如果所有对应的部分都相等，则比较长度（处理如 1.0 和 1.0.0 的情况）
    if len(parts1) >= len(parts2):
        return True
    elif len(parts1) < len(parts2):
        return False
    else:
        return False


def set_report_executor_on_results(report_path):
    """
    在allure-results报告的目录下生成一个写入了执行人的文件：executor.json
    """
    # 需要写入的执行人信息
    allure_executor = {
        "name": "张三",
        "type": "gitlab",
        "url": "https://gitlab.shorttv.live/shorttv/tools/mobile-ui-automation-tests",
        "buildOrder": 3,
        "buildName": "自动化代码仓库",
        "buildUrl": "https://gitlab.shorttv.live/shorttv/tools/mobile-ui-automation-tests",
        "reportUrl": "https://gitlab.shorttv.live/shorttv/tools/mobile-ui-automation-tests",
        "reportName": f"{get_test_plan_name()} {get_app_version()} 版本自动化测试报告",
    }
    allure_executor_file = os.path.join(f"{report_path}/allure-results/", "executor.json")

    # 写入执行人信息
    with open(allure_executor_file, "w", encoding="utf-8") as f:
        f.write(json.dumps(allure_executor, ensure_ascii=False, indent=4))


def get_test_plan_name():
    result = mysql_execute(f"SELECT name FROM test_plan WHERE id = %s", [args.task_id])
    if result:
        return result[0]["name"]
    else:
        return "ShortTv"


def escape_unicode(s):
    """
    将字符串转换为 Unicode 转义格式并解码为 ASCII
    java标准文件格式处理方式: .encode('unicode_escape').decode('ascii')
    """
    if not isinstance(s, str):
        s = str(s)
    return s.encode("unicode_escape").decode("ascii")


def get_apk():
    if args.apk:
        path = args.apk.replace("/var/ftp/pub/short_tv_apk/", "")
        name = path.split("/")
        if len(name) == 2:
            return f"文件夹: {name[0]}, 包体: {name[1]}"
        else:
            return f"包体路径未找到, 完整路径: {path}"
    else:
        return "未指定包体"


def set_report_env_on_results(report_path, module_error, testing_module):
    """
    在allure-results报告的目录下生成一个写入了环境信息的文件：environment.properties
    注意：确保文件编码为 UTF-8 以支持中文显示
    """
    # 需要写入的环境信息
    allure_env = {
        escape_unicode("测试设备名称"): get_device_names(),
        escape_unicode("测试设备id"): args.device,
        escape_unicode("执行模式"): escape_unicode(testing_module),
        escape_unicode("执行模块"): escape_unicode(get_modules_name()),
        escape_unicode("app语言"): escape_unicode(language_name()[args.language]),
        escape_unicode("测试设备安卓系统版本"): get_device_version(),
        escape_unicode("APK版本"): get_app_version(),
        escape_unicode("APK包体"): escape_unicode(get_apk()),

        # escape_unicode("主机IP"): get_local_ip(),
        # escape_unicode("主机平台"): escape_unicode(platform.platform()),
        # escape_unicode("主机名称"): escape_unicode(platform.node()),
        escape_unicode("执行代码位置"): escape_unicode(args.modules),
        # escape_unicode("Python版本"): escape_unicode(platform.python_version()),
        # escape_unicode("Pytest版本"): escape_unicode(pytest.__version__),
    }

    m_e = ",".join(module_error)
    new_element = {escape_unicode("警告"): escape_unicode(f"输入模块有误, {m_e} 暂不支持{get_app_version()}版本")}
    if module_error:
        allure_env = {**new_element, **allure_env}

    allure_env_file = os.path.join(f"{report_path}/allure-results/", "environment.properties")
    # 写入环境信息
    with open(allure_env_file, "w", encoding="utf-8") as f:
        for key, value in allure_env.items():
            f.write(f"{key}={value}\n")


def deal_video():
    video_path = os.path.join(android.report_output_dir, str(args.output_report), "allure-results")
    # video_files = []
    log_file_path = f"{android.report_output_dir}/{args.output_report}/log/日志_ffmpeg.log"
    # 遍历目录中的所有文件
    for filename in os.listdir(video_path):
        # 检查是否为文件且扩展名为 .mp4
        file = os.path.join(video_path, filename)
        if os.path.isfile(file) and filename.endswith('.mp4') and "_out" not in filename:
            # video_files.append(os.path.join(video_path, filename))
            file_output = file.replace(".mp4", "_out.mp4")
            # 获取原始文件大小
            original_size = os.path.getsize(file)
            try:
                """
                -crf 设置恒定速率因子。CRF值越低，输出质量越高，文件大小也越大
                -r fps参数可以降低帧率(例如，-r 24将帧率设置为24帧每秒)
                """
                # 记录开始时间
                start_time = time.time()
                subprocess.run(
                    ["ffmpeg", "-i", file, "-vcodec", "libx264", "-crf", "28", "-r", "30", file_output],
                    # check=True,
                    text=True,
                    stdout=open(log_file_path, "w"),
                )
                os.remove(file)
                # 获取转换后文件大小
                converted_size = os.path.getsize(file_output)
                # 计算文件大小变化
                size_change = converted_size - original_size
                # 记录结束时间
                end_time = time.time()
                # 计算并打印运行时间
                elapsed_time = end_time - start_time
                print(f"代码运行时间为: {elapsed_time} 秒")
                Log.logger.info(f"成功转换视频文件: {file} -> {file_output}")
                Log.logger.info(
                    f"文件大小变化: 原始大小 {original_size} 字节, 转换后大小 {converted_size} 字节, 变化 {size_change} 字节, 耗时: {elapsed_time}秒")
            except subprocess.CalledProcessError as e:
                Log.logger.error(f"转换视频文件失败: {file}\n错误信息: {e}")


def rename_video():
    video_path = os.path.join(android.report_output_dir, str(args.output_report), "allure-results")
    for filename in os.listdir(video_path):
        file = os.path.join(video_path, filename)
        if os.path.isfile(file) and filename.endswith('_out.mp4'):
            os.rename(file, file.replace("_out.mp4", ".mp4"))


def generate_report(module_error, testing_module):
    path = os.path.join(android.report_output_dir, str(args.output_report))
    # 生成报告中的环境信息
    set_report_env_on_results(path, module_error, testing_module)
    set_report_executor_on_results(path)
    rename_video()
    try:
        # 生成Allure报告 --single-file
        cmd = f"allure generate {path}/allure-results -o {path}/reports --clean"
        # os.popen(cmd)
        os.system(cmd)

    except subprocess.CalledProcessError as e:
        Log.logger.info(f"生成allure报告失败, 请检查{path}数据源\n", str(e))


def allure_server(ip, port):
    path = os.path.join(android.report_output_dir, str(args.output_report))
    try:
        # 生成Allure报告
        cmd = f"allure open {path}/ -h {ip} -p {port}"
        Log.logger.info(f"allure报告地址  http://{ip}:{port}")

        subprocess.run(cmd, shell=True, check=True, text=True)

    except subprocess.CalledProcessError as e:
        Log.logger.info("生成allure服务失败, 请检查本机环境")


def get_pass_rate():
    json_file = f"{android.report_output_dir}/{args.output_report}/reports/widgets/summary.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        total_tests = data['statistic']['total']
        passed_tests = data['statistic']['passed']
        pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        return round(pass_rate)


def get_cases_num():
    json_file = f"{android.report_output_dir}/{args.output_report}/reports/widgets/summary.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        total_tests = data['statistic']['total']

        return total_tests


def get_run_time():
    json_file = f"{android.report_output_dir}/{args.output_report}/reports/widgets/summary.json"
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        start_timestamp = data['time']['start']
        end_timestamp = data['time']['stop']
        start_timestamp /= 1000
        end_timestamp /= 1000
        # 将时间戳转换为datetime对象
        start_time = datetime.datetime.fromtimestamp(start_timestamp)
        end_time = datetime.datetime.fromtimestamp(end_timestamp)

        # 计算时间差
        time_difference = end_time - start_time

        # 获取时间差的秒数、分钟数和小时数
        seconds = int(time_difference.total_seconds())
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # 格式化输出
        formatted_time = f"{hours}时{minutes}分{seconds}秒"

        return formatted_time


def get_modules_name():
    client = MySQLClient()
    client.connect()
    cases = []
    try:
        for i in args.modules:
            if args.root_path:
                case = i.replace(args.root_path, "")
            else:
                case = i.replace("sys_android/test_cases/new/", "")
            result = client.execute_query(f"SELECT module_name_zh FROM cases WHERE class_name = %s", [case])
            if result:
                cases.append(result[0]["module_name_zh"])
            else:
                cases.append(i)

        client.connection.commit()
        client.close()
    except Exception as e:
        Log.logger.info(f"获取模块名称失败, 请检查{args.modules}数据源\n", str(e))
    return ", ".join(cases)


if __name__ == "__main__":
    # set_report_env_on_results()
    # set_report_executer_on_results()
    print(get_pass_rate())
