# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08

import argparse


def get_arg_parse():
    """
    命令行解析
    :return:
    """
    parser = argparse.ArgumentParser(epilog="外部传入apk路径&包名&设备号,自动化运行测试脚本")
    parser.add_argument('devices', help='设备号')
    parser.add_argument('apk', help='apk路径')
    parser.add_argument('package', help='包名')
    parser.add_argument('module',help='执行模块')
    parser.add_argument('task_id', help='任务id')
    return parser.parse_args()
