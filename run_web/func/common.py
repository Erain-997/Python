# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/12/30
import subprocess

from common.data import BASE_DIR


def func_git_pull():
    try:
        out = subprocess.check_output(["git", "reset", "--hard", "HEAD"], cwd=f"{BASE_DIR}")
        out = subprocess.check_output(["git", "pull"], cwd=f"{BASE_DIR}")
        return {
            "data": {},
            "code": 0,
            "result": "success"
        }
    except subprocess.CalledProcessError as e:
        return {
            "data": str(e),
            "code": 1,
            "result": "error"
        }


def func_get_root_path():
    return {
        "data": {
            "report_path": "/reports/index.html",
            "report_log_path": "/log",
            "report_root_path": "/files",
            "android_case_path": "sys_android/test_cases/new/",
            "ftp_server": "ftp://192.168.120.150/pub/"
        },
        "code": 0
    }


def func_get_language():
    return {
        "data": [
            {"code": "en", "name": "英文"},
            {"code": "zh_cn", "name": "简体中文"},
            {"code": "zh", "name": "繁体中文"},
            {"code": "fil", "name": "菲律宾语"},
            {"code": "ar", "name": "阿拉伯语"},
            {"code": "hi", "name": "印地语"},
            {"code": "in", "name": "印尼语"},
            {"code": "vi", "name": "越南语"},
            {"code": "pt", "name": "葡萄牙语"},
            {"code": "es", "name": "西班牙语"},
            {"code": "ja", "name": "日语"},
            {"code": "de", "name": "德语"},
            {"code": "ko", "name": "韩语"},
            {"code": "th", "name": "泰语"},
            {"code": "ms", "name": "马来西亚"},
            {"code": "it", "name": "意大利"},
            {"code": "ru", "name": "俄语"},
            {"code": "fr", "name": "法语"}
        ],
        "code": 0
    }
