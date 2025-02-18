import time

import allure

from common.utils.arg_parse_func import args
from common.utils.decorator import Decorate
from common.utils.report import get_app_version, compare_versions
from sys_android.page_objects.common_page import CommonPage


class ResolutionPage(CommonPage):

    @Decorate.collect_test("查看1080p限免字样")
    def versio_limit_free(self):
        if compare_versions():
            self.click(self.element.subscribe_page.new_resolution, "查看1080p限免字样")
        else:
            self.click(self.element.subscribe_page.resolution, "查看1080p限免字样")

    @Decorate.collect_test("选择1080分辨率播放")
    def version_1080p_play(self):
        if compare_versions():
            self.click(self.element.subscribe_page.new_resolution, "点击分辨率按钮")
        else:
            self.click(self.element.subscribe_page.resolution, "点击分辨率按钮")
        self.click(self.element.immersion_page.resolution_b, "选择1080分辨率播放")

