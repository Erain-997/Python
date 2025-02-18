import time
from time import sleep

import allure

from common.utils.cmd_tools import adb_shell
from common.utils.decorator import Decorate
from common.utils.device_tools import get_device_version, AndroidVersion_14
from common.utils.log_utils import Log
from sys_android.page_objects.common_page import CommonPage


class WindowPage(CommonPage):
    def switch_button(self, status):
        with allure.step(f"画中画开关—>{'开启' if status else '关闭'}"):
            """画中画功能开关"""
            self.click(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
                ),
                "进入我的模块",
            )
            sleep(1)
            try:
                if self.wait_element(self.element.common_page.logo, "等待登录弹窗出现", 3):
                    self.press_back_button()
            except Exception as e:
                Log.logger.error(f"An error: {e}")
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            self.click(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[3]}"]',
                ),
                "点击设置",
            )
            # 判断画中画功能按钮是否关闭
            if get_device_version() >= AndroidVersion_14:
                button_index = 3
                xpath = '(//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/status_iv"])[3]'
            else:
                button_index = 2
                xpath = '(//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/status_iv"])[2]'

            current_status = self.automatic_episode_button(button_index)

            if status == current_status:
                Log.logger.info(f'画中画功能按钮已经是所需状态: {status}')
            else:
                self.click(('xpath', xpath), "切换画中画功能")
                Log.logger.info(f'画中画功能按钮已切换到: {status}')

    @Decorate.collect_test("关闭系统悬浮窗权限")
    def close_suspended_window(self):
        adb_shell("appops set com.startshorts.androidplayer SYSTEM_ALERT_WINDOW deny")

    @Decorate.collect_test("开启系统悬浮窗权限")
    def start_suspended_window(self):
        adb_shell("appops set com.startshorts.androidplayer SYSTEM_ALERT_WINDOW allow")

    @Decorate.collect_test("点击小窗播放按钮")
    def click_mini_window(self):
        self.click(self.element.common_page.window, "点击小窗播放按钮")

    @Decorate.collect_test("回到主屏幕")
    # 回到主屏幕
    def back_home(self):
        self.driver.press_keycode(3)
        time.sleep(4)

    @Decorate.collect_test("轻敲小窗进入沉浸页")
    def tap_mini_window(self):
        self.resolution_tap(0.24, 0.78, "轻敲小窗")
        time.sleep(2)
        self.resolution_tap(0.24, 0.78, "轻敲小窗")
