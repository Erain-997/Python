# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/11/20
import os
from dataclasses import dataclass, asdict

# BASE_DIR = os.path.abspath("../short_tv")

# 获取当前脚本所在目录的绝对路径
current_script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 获取当前脚本所在目录的父级目录的绝对路径
BASE_DIR = os.path.join(os.path.dirname(current_script_dir), "short_tv")
APK_DIR = "/var/ftp/pub"

allure_servers = {}


@dataclass
class Device:
    name: str
    model: str
    ip: str
    udid: str
    android_version: str
    resolution: str
    status: str
    device: str


@dataclass
class DeviceInfo:
    udid: str  # 唯一
    device_system: str = None  # 不变
    system_version: str = None  # 不变
    name: str = None  # 不变
    name_zh: str = None
    model: str = None  # 不变
    ip: str = None
    tcpip_port: str = None
    resolution: str = None  # 不变
    testing_status: str = None
    connect_status: str = None
    owner: str = None
    remarks: str = None

    def to_dict(self):
        return asdict(self)


@dataclass
class CaseInfo:
    id: int = None
    module_name: str = None
    module_name_zh: str = None
    class_name: str = None
    title_name: str = None
    case_id: str = None
    case_setup: str = None
    case_steps: str = None
    data_resource: str = None
    expect_result: str = None
    pytest_mark: str = None
    allure_mark: str = None
    case_type: str = None
    user_name: str = None
    executor: str = None
    development_status: str = None
    runtime: str = None
    actual_result: str = None
    passed: bool = None
    remarks: str = None

    def to_dict(self):
        return asdict(self)


@dataclass
class TestPlan:
    id: int = None
    name: str = None
    device: str = None
    language: str = None
    root_path: str = None
    modules: str = None
    proxy: bool = None
    feishu: bool = None
    record: bool = None
    apk: bool = None
    apk_select_version: str = None
    apk_select_package: str = None
    k: str = None
    m: str = None
    status: str = None
    allure_features: str = None
    allure_stories: str = None
    version: str = None
    creat_time: str = None
    update_time: str = None
    user: str = None
    remarks: str = None

    def to_dict(self):
        return asdict(self)


@dataclass
class ReportInfo:
    plan_id: str = None  # 对应测试计划id
    name: str = None  # 测试计划名称
    case_num: int = None  # 用例总数
    test_cases: str = None  # 测试模块
    apk_version: str = None  # apk版本
    pass_rate: str = None  # 通过率
    run_time: str = None  # 运行时间
    device: str = None  # 设备

    def to_dict(self):
        return asdict(self)


# todo 之后规范下res和req, 统一
@dataclass
class ResponseData:
    code: int = None
    result: str = None
    data: dict = None

    def to_dict(self):
        return asdict(self)
