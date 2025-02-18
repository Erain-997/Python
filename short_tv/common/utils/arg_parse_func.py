# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/11/1


import argparse
import os

from common.utils.path_config import android
from common.utils.tools import get_available_port

modules_list = {
    "广告模块": "test_advertisement_module.py",
    "公共模块": "test_all.py",
    "反馈模块": "test_feedback.py",
    "沉浸页模块": "test_immersion_module.py",
    "页面截图模块": "test_pages_screenshot_module.py",
    "语言模块": "test_language.py",
    "奖励模块": "test_reward_module.py",
    "订阅模块": "test_subscribe_module.py",
    "充值金币模块": "test_top_up_module.py",
    "补单模块": "test_reissue_order_module.py",
    "解锁剧模块": "test_unlock_drama_module.py",
    "自动解锁模块": "test_automatic_unlock_module.py",
    "视频详情模块": "test_video_details_module.py",
    "兑换码模块": "test_redeem_codes_module.py",
    "测试": "test_demo.py",
    "分辨率1080p限免": "test_resolution.py",
    "子函数文件": "test_get_yaml.py",
    "小窗播放相关模块": "test_window_module.py",
    "沉浸页入口": "test_shorts_entrance.py"
}


def get_arg_parse():
    """
    命令行解析
    :return:
    """
    parser = argparse.ArgumentParser(
        description="自动化运行测试脚本参数",
        epilog="外部传入apk路径&包名&设备号,自动化运行测试脚本"
    )

    cases_path = f"{android.test_cases_new_dir}"
    files_list = [f for f in os.listdir(cases_path) if os.path.isfile(os.path.join(cases_path, f))]
    inverted_modules_list = {v: k for k, v in modules_list.items()}
    m = [inverted_modules_list[i] for i in files_list if i in inverted_modules_list and
         inverted_modules_list[i] != "测试" and inverted_modules_list[i] != '子函数文件']

    # 必填参数
    parser.add_argument("device", type=str, default="sys_android/test_cases/new/",
                        help="设备号, 格式: R58RC3CXAZX 或 172.16.9.3:5555")
    parser.add_argument("output_report", type=str, default="默认", help="报告路径")

    # 脚本
    parser.add_argument("-modules", type=str, nargs="+", help=f"执行模块, 不填则默认全模块, \n 目前支持: {m}")
    parser.add_argument("-apk", type=str, help="apk路径, 格式:D:\\Data\\1.9.11_输出日志_密钥写死_可以录屏.apk\n")
    parser.add_argument("-proxy", action="store_true", help="启用代理服务, 默认不使用代理")
    parser.add_argument("-record", action="store_true", help="启用保留所有录屏文件")
    parser.add_argument("-debug", action="store_true", help="启用debug, 会打印所有服务的日志")
    parser.add_argument("-port", default=get_available_port(), help="appium默认随机端口")
    parser.add_argument("-proxy_port", type=str, default=None, help="mitmproxy代理默认随机端口")
    parser.add_argument("-feishu", action="store_true", help="是否飞书通知群")
    parser.add_argument("-language", type=str, default="en", help="启用更换appium语言，默认值为 'en'")
    parser.add_argument("-compress", action="store_true", help="是否压缩处理视频")

    # 查询
    parser.add_argument("-get_cases", action="store_true", help="收集所有用例,不执行")

    # 执行
    parser.add_argument("-rerun", type=str, default="1", help="重试次数, 默认2次")
    parser.add_argument("-root_path", type=str, default=None, help="根目录")
    parser.add_argument("-k", type=str, nargs="+", help="执行匹配到的用例")
    parser.add_argument("-m", type=str, help="执行指定标签的用例")
    parser.add_argument("--allure_features", type=str, nargs="+", help="执行指定allure feature标签的用例")
    parser.add_argument("--allure_stories", type=str, nargs="+", help="执行指定allure story标签的用例")

    # 服务
    parser.add_argument("-task_id", type=str, default="默认", help="task_id")

    return parser.parse_args()


args = get_arg_parse()

# 示例调用
if __name__ == "__main__":
    args = get_arg_parse()
    print(f"设备号: {args.device}")
    print(f"APK 路径: {args.apk}")
    print(f"执行模块: {args.module}")
    print(f"任务 ID: {args.task_id}")
    print(f"appium默认随机端口: {args.port}")
    # print(f"调试模式: {"启用" if args.debug else "未启用"}")

    if args.apk:
        print(22222)
        print(args.apk)
    # cases_path = f"{android.test_cases_new_dir}"
    # files_list = [f for f in os.listdir(cases_path) if os.path.isfile(os.path.join(cases_path, f))]
    # m = [modules_list[i] for i in files_list]
    # print(files_list)
    # print(m)
