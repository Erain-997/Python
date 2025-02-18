import os


def workspace_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class PathConfig:
    def __init__(self, sys_path):
        # 获取项目的根目录
        self.base_dir = workspace_dir()
        print("\n项目根目录:", self.base_dir)

        # 公共模块
        self.common_dir = self.create_dir(os.path.join(self.base_dir, "common"))
        self.api_dir = self.create_dir(os.path.join(self.common_dir, "api"))
        self.mail_dir = self.create_dir(os.path.join(self.common_dir, "mail"))
        self.utils_dir = self.create_dir(os.path.join(self.common_dir, "utils"))
        self.language_dir = self.create_dir(os.path.join(self.common_dir, "language"))

        # 文档目录
        self.doc_dir = self.create_dir(os.path.join(self.base_dir, "doc"))

        # 系统相关目录
        self.sys_path = sys_path
        self.caps_dir = self.create_dir(os.path.join(self.sys_path, "caps"))
        self.install_packages_dir = self.create_dir(os.path.join(self.sys_path, "install_packages"))
        self.page_locators_dir = self.create_dir(os.path.join(self.sys_path, "page_locators"))
        self.page_objects_dir = self.create_dir(os.path.join(self.sys_path, "page_objects"))
        self.test_cases_dir = self.create_dir(os.path.join(self.sys_path, "test_cases"))
        self.test_cases_regression_dir = self.create_dir(os.path.join(self.test_cases_dir, "regression"))
        self.test_cases_v1_9_7_dir = self.create_dir(os.path.join(self.test_cases_dir, "v1_9_7"))
        self.test_cases_new_dir = self.create_dir(os.path.join(self.test_cases_dir, "new"))
        self.test_datas_dir = self.create_dir(os.path.join(self.sys_path, "test_datas"))
        self.report_output_dir = self.create_dir(os.path.join(self.base_dir, "report_output"))

        # 输出文件目录的子目录
        self.flow_data_dir = self.create_dir(os.path.join(self.report_output_dir, "flow_data"))
        self.mock_dir = self.create_dir(os.path.join(self.report_output_dir, "mock"))
        # self.screenshot_dir = self.create_dir(os.path.join(self.report_output_dir, "screenshot"))
        # self.recording_dir = self.create_dir(os.path.join(self.report_output_dir, "recording"))

    def create_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path


# 创建 Android 和 iOS 的路径配置
android = PathConfig(os.path.join(workspace_dir(), "sys_android"))
ios = PathConfig(os.path.join(workspace_dir(), "sys_ios"))

# 打印所有路径
if __name__ == "__main__":
    print("公共模块目录:", android.common_dir)
    print("API目录:", android.api_dir)
    print("邮件模块目录:", android.mail_dir)
    print("录制目录:", android.recording_dir)
    print("截图目录:", android.screenshot_dir)
    print("工具类目录:", android.utils_dir)
    print("文档目录:", android.doc_dir)
    print("报告输出文件目录:", android.report_output_dir)
    print("Android系统目录:", android.sys_path)
    print("Android配置文件目录:", android.caps_dir)
    print("Android安装包目录:", android.install_packages_dir)
    print("Android页面定位符目录:", android.page_locators_dir)
    print("Android页面对象目录:", android.page_objects_dir)
    print("Android测试用例目录:", android.test_cases_dir)
    print("Android回归测试用例目录:", android.test_cases_regression_dir)
    print("Android v1.9.7测试用例目录:", android.test_cases_v1_9_7_dir)
    print("Android测试数据目录:", android.test_datas_dir)
    print("Android HTML输出目录:", android.html_dir)
    print("Android日志目录:", android.logs_dir)
    print("Android视频目录:", android.recording_dir)
    print("iOS系统目录:", ios.sys_path)
    print("iOS配置文件目录:", ios.caps_dir)
    print("iOS安装包目录:", ios.install_packages_dir)
    print("iOS页面定位符目录:", ios.page_locators_dir)
    print("iOS页面对象目录:", ios.page_objects_dir)
    print("iOS测试用例目录:", ios.test_cases_dir)
    print("iOS回归测试用例目录:", ios.test_cases_regression_dir)
    print("iOS v1.9.7测试用例目录:", ios.test_cases_v1_9_7_dir)
    print("iOS测试数据目录:", ios.test_datas_dir)
    print("iOS HTML输出目录:", ios.html_dir)
    print("iOS日志目录:", ios.logs_dir)
    print("iOS截图输出目录:", ios.screenshot_dir)
