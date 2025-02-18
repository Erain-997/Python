import base64
import os
import shutil
import subprocess
import threading
import time
import traceback
import zipfile

import allure
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common import InvalidSessionIdException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from common.utils.arg_parse_func import args
from common.utils.cmd_tools import get_locale_language
from common.utils.log_utils import Log
from common.utils.report import deal_video
from sys_android.caps.android_capabilities import device2_capabilities
from sys_android.test_datas.short_tv_elements import ShortTvElements


class TestBase:
    """测试基类，初始化驱动对象并加载页面元素"""

    def __init__(self, boolean=True):
        self.capabilities = device2_capabilities.copy()

        # self.update_language(capabilities)
        self.update_locale_language()
        self.update_intent_arguments(boolean)
        options = UiAutomator2Options().load_capabilities(self.capabilities)
        # 设置 newCommandTimeout
        # 设置超时时间为 120 秒，可以根据需要调整
        options.set_capability("newCommandTimeout", 300)

        """初始化驱动对象"""
        self.driver = webdriver.Remote(f"http://localhost:{args.port}", options=options)

        # 通过self.__class__.__name__获取当前类的名称，作为yaml文件中的键
        # with open(f"{android.test_datas_dir}/top_up_modules.yaml", encoding="utf-8") as f:
        #     data = yaml.load(f, Loader=yaml.FullLoader)
        #     for key, value in data.items():
        #         if isinstance(value, dict):
        #             for sub_key, sub_value in value.items():
        #                 self.__setattr__(sub_key, sub_value)
        #         else:
        #             self.__setattr__(key, value)
        self.element = ShortTvElements()

    def allure_attach_fail(self, loc, e, case_name):
        img = self.driver.get_screenshot_as_png()
        allure.attach(img, name=case_name, attachment_type=allure.attachment_type.PNG)
        # 使用 allure.attach 附加异常信息和定位器信息
        allure.attach(str(loc), name="定位器信息", attachment_type=allure.attachment_type.TEXT)
        # 附加更详细的异常信息，包括堆栈跟踪
        allure.attach(traceback.format_exc(), name="异常堆栈跟踪", attachment_type=allure.attachment_type.TEXT)
        # 如果只想附加异常消息，可以使用 str(e)
        allure.attach(str(e), name="异常信息", attachment_type=allure.attachment_type.TEXT)
        # 标记用例为失败
        pytest.fail(f" {case_name} 失败")

    # 代码兼容, 允许不存在
    def allure_attach(self, loc, e, case_name):
        img = self.driver.get_screenshot_as_png()
        allure.attach(img, name=case_name, attachment_type=allure.attachment_type.PNG)
        # 使用 allure.attach 附加异常信息和定位器信息
        allure.attach(str(loc), name="定位器信息", attachment_type=allure.attachment_type.TEXT)
        # 附加更详细的异常信息，包括堆栈跟踪
        allure.attach(traceback.format_exc(), name="异常堆栈跟踪", attachment_type=allure.attachment_type.TEXT)
        # 如果只想附加异常消息，可以使用 str(e)
        allure.attach(str(e), name="异常信息", attachment_type=allure.attachment_type.TEXT)

    def wait_element(self, loc, case_name="默认等待", timeout=6):
        with allure.step(case_name):
            try:
                return WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*loc))
            except Exception as e:
                self.allure_attach(loc, e, case_name)
                return None

    def get_element_text(self, loc, case_name="默认获取元素文本", timeout=6):
        time.sleep(2)
        with allure.step(case_name):
            try:
                ele = WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*loc))
                try:
                    text = ele.text
                    allure.attach(text, name=case_name)
                    return text
                except Exception as e:
                    allure.attach(f"元素 {loc} 找到，但获取文本时发生异常: {str(e)}", name="异常信息",
                                  attachment_type=allure.attachment_type.TEXT)
                    pytest.fail(str(e))
            except Exception as e:
                allure.attach(f"元素 {loc} 未找到: {str(e)}", name="异常信息",
                              attachment_type=allure.attachment_type.TEXT)
                pytest.fail(str(e))

    def click(self, loc, case_name="默认等待并点击", timeout=10):
        with allure.step(case_name):
            try:
                WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*loc)).click()
            except Exception as e:
                self.allure_attach_fail(loc, e, case_name)
                raise e

    def long_press_element(self, element_id, duration, case_name):
        """对指定元素执行长按操作, 并发用这个"""
        with allure.step(case_name):
            element = self.wait_element(element_id)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click_and_hold().perform()  # 先移动到元素
            time.sleep(duration)  # 长按持续 duration 秒
            actions.move_to_element(element).release().perform()

    def long_press_coordinate(self, x, y, duration, case_name):
        screen_size = self.driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']
        # 计算点击坐标
        x = int(screen_width * x / 100)
        y = int(screen_height * y / 100)
        try:
            with allure.step(case_name):
                # 将秒转换为毫秒，adb 的 duration 单位为毫秒
                duration_ms = int(duration * 1000)
                # 构造 ADB 命令
                command = [
                    "adb", "-s", args.device, "shell", "input", "swipe",
                    str(x), str(y), str(x), str(y), str(duration_ms)
                ]
                # 执行命令
                result = subprocess.run(command, text=True)
                if result.returncode == 0:
                    print(f"成功长按坐标: ({str(x)}, {str(y)}) 持续 {str(duration_ms)} 秒")
                else:
                    print(f"长按失败，错误信息: {result.stderr}")
        except Exception as e:
            print(f"长按坐标 ({str(x)}, {str(y)}) 时发生错误: {e}")

    def click_and_hold(self, loc, case_name="点击并按下", timeout=10):
        with allure.step(case_name):
            try:
                element = WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(*loc))
                actions = ActionChains(self.driver)
                actions.click_and_hold(element).pause(3).release().perform()
            except Exception as e:
                self.allure_attach_fail(loc, e, case_name)
                raise e

    def drag_and_drop(self, source_id, target_id, case_name="默认等待并点击"):
        """对指定元素执行长按操作, 并发用这个"""
        with allure.step(case_name):
            source = self.wait_element(source_id)
            target = self.wait_element(target_id)
            actions = ActionChains(self.driver)
            actions.drag_and_drop(source, target).release().perform()  # 先移动到元素
            # time.sleep(duration)  # 长按持续 duration 秒
            # actions.move_to_element(element).release().perform()

    def click_screenshot(self, loc, case_name="默认等待并点击", page_name="", screenshot_path="", timeout=1):
        with allure.step(case_name):
            try:
                WebDriverWait(self.driver, 10).until(lambda d: d.find_element(*loc)).click()
                time.sleep(timeout)
            except Exception as e:
                self.allure_attach_fail(loc, e, case_name)
                raise e
        img = self.driver.get_screenshot_as_png()
        with open(screenshot_path + "/" + page_name + ".png", "wb") as f:
            f.write(img)
        # allure.attach(img, name=page_name, attachment_type=allure.attachment_type.PNG)

    def get_find_elements(self, loc, timeout=6):
        # TODO 后期需优化
        # case_name = "查找元素集合"
        # with allure.step(case_name):
        try:
            elements = WebDriverWait(self.driver, timeout).until(lambda d: d.find_elements(*loc))
            if elements:
                return [element.text for element in elements]
            else:
                return []
        except Exception as e:
            self.allure_attach_fail(loc, e, '查找元素')
            # raise e

    @allure.step("开始录制视频")
    def start_recording(self):
        try:
            self.driver.start_recording_screen(timeLimit=300)
        except Exception as e:
            allure.attach(str(e), name="该手机不支持录屏", attachment_type=allure.attachment_type.TEXT)

    # TODO 脚本视频待优化
    @allure.step("停止录制视频并保存")
    def stop_and_save_recording(self, test_status, case_name="用例执行录屏"):
        try:
            if not args.record and test_status:
                # TODO 超过400M处理不了, 会直接被丢弃, 目前最长两分半
                self.driver.stop_recording_screen()
            else:
                video_data = base64.b64decode(self.driver.stop_recording_screen())
                allure.attach(video_data, name=case_name, attachment_type=allure.attachment_type.MP4)
        except Exception as e:
            allure.attach(str(e), name="该设备机型, 不支持录屏", attachment_type=allure.attachment_type.TEXT)

        if args.compress:
            thread = threading.Thread(target=deal_video)
            thread.start()
            thread.join()

    def get_window_size(self):
        """获取屏幕的宽度和高度"""
        window_size = self.driver.get_window_size()
        return window_size["width"], window_size["height"]

    def swipe_by_percent(self, start_x_rel, start_y_rel, end_x_rel, end_y_rel, duration, case_name=None):
        """根据屏幕百分比坐标执行滑动操作"""
        screen_width, screen_height = self.get_window_size()

        # 将百分比坐标转换为绝对坐标
        start_x_abs = int(start_x_rel * screen_width)
        start_y_abs = int(start_y_rel * screen_height)
        end_x_abs = int(end_x_rel * screen_width)
        end_y_abs = int(end_y_rel * screen_height)

        # 确定滑动方向
        if start_x_abs < end_x_abs and abs(start_x_abs - end_x_abs) > abs(start_y_abs - end_y_abs):
            direction = "左滑"
        elif start_x_abs > end_x_abs and abs(start_x_abs - end_x_abs) > abs(start_y_abs - end_y_abs):
            direction = "右滑"
        elif start_y_abs < end_y_abs and abs(start_y_abs - end_y_abs) > abs(start_x_abs - end_x_abs):
            direction = "上滑"
        elif start_y_abs > end_y_abs and abs(start_y_abs - end_y_abs) > abs(start_x_abs - end_x_abs):
            direction = "下滑"
        else:
            direction = "未知方向"
        if case_name:
            step_name = f"{direction}, {case_name}"
        else:
            step_name = f"{direction}: ({start_x_abs}, {start_y_abs}) -> ({end_x_abs}, {end_y_abs})"
        # 使用allure记录滑动步骤
        with allure.step(step_name):
            self.driver.swipe(start_x_abs, start_y_abs, end_x_abs, end_y_abs, duration)

        # 滑动完默认等一秒稳定
        time.sleep(1)

    def swipe(self, start_x, start_y, end_x, end_y, duration, case_name=None):
        """
        param: start_x, start_y, end_x, end_y
        param: duration # 该字段过小时, 会变成点击操作
        """
        if start_x < end_x and abs(start_x - end_x) > abs(start_y - end_y):
            direction = "左滑"
        elif start_x > end_x and abs(start_x - end_x) > abs(start_y - end_y):
            direction = "右滑"
        elif start_y < end_y and abs(start_y - end_y) > abs(start_x - end_x):
            direction = "上滑"
        elif start_y > end_y and abs(start_y - end_y) > abs(start_x - end_x):
            direction = "下滑"
        else:
            direction = "未知方向"
        if case_name:
            step_name = f"{direction}, {case_name}"
        else:
            step_name = f"{direction}: ({start_x}, {start_y}) -> ({end_x}, {end_y})"
        with allure.step(step_name):
            self.driver.swipe(start_x, start_y, end_x, end_y, duration)

    @allure.step("退出App")
    def quit(self):
        # 当视频处理超过一分钟时, 默认自动关闭
        try:
            self.driver.quit()
        except InvalidSessionIdException as e:
            Log.logger.info(f"AppiumDriver已断开:{str(e)}")

    @allure.step("截图")
    def screenshot(self, file):
        allure.attach(
            self.driver.get_screenshot_as_base64(),
            name="language_error.png",
            attachment_type=allure.attachment_type.PNG,
        )
        self.driver.save_screenshot(file)

    def tap(self, x, y, case_name, duration=None):
        time.sleep(1)
        with allure.step(f"{case_name}: x:{x},y:{y}"):
            self.driver.tap([(x, y)], duration)

    def resolution_tap(self, x_percent, y_percent, case_name, duration=None):
        # 获取屏幕的宽度和高度
        screen_size = self.driver.get_window_size()
        screen_width = screen_size['width']
        screen_height = screen_size['height']
        # 计算点击坐标
        x = int(screen_width * x_percent)
        y = int(screen_height * y_percent)
        with allure.step(f"{case_name}: x:{x},y:{y}"):
            self.driver.tap([(x, y)], duration)

    # 系统返回按键
    def press_back_button(self, case_name="系统按键-返回", number=4):
        with allure.step(case_name):
            try:
                self.driver.press_keycode(number)
            except Exception as e:
                self.allure_attach_fail("按键", e, case_name)
                raise e

    def update_locale_language(self):
        lang, locale = get_locale_language()
        self.capabilities["language"] = lang
        self.capabilities["locale"] = locale

    def update_intent_arguments(self, boolean, pure_paying_user=None):
        """
        更新 capabilities 字典，将 new_env 合并到 capabilities 中
        """
        if boolean:
            self.capabilities.update(
                {
                    "optionalIntentArguments": "--es is_auto_test_running true "  # 自动化测试标识 (不要改)
                                               "--es disable_home_pop_dialogs true "  # 禁用首页弹窗
                                               "--es disable_campaign_parse true "  # 禁用归隐剧
                                               f"--es app_language {args.language} "  # 语言设置 
                    # "--es campaign_shorts_id 7321904 "  #

                }
            )
        else:
            self.capabilities.update(
                {
                    "optionalIntentArguments": "--es is_auto_test_running true "  # 自动化测试标识 (不要改)
                                               "--es disable_home_pop_dialogs false "  # 启用首页弹窗
                                               f"--es is_pure_paying_user {pure_paying_user}"  # 归因剧解锁类型（true：金币+广告）
                                               "--es disable_campaign_parse false"  # 启用归隐剧
                                               f" --es app_language {args.language}"  # 语言设置
                }
            )

    def attach_folder_as_zip(self, folder_path, zip_name):
        """
        将指定文件夹压缩成zip，并附加到Allure报告中。

        :param folder_path: 要压缩的文件夹路径
        :param zip_name: 压缩后的zip文件名
        """
        # 创建一个临时文件夹用于存放压缩文件
        temp_dir = os.path.join(os.getcwd(), "temp_zip_dir")
        os.makedirs(temp_dir, exist_ok=True)

        # 创建zip文件路径
        zip_path = os.path.join(temp_dir, zip_name)

        # 将文件夹压缩成zip
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 写入文件到zip，并保持文件夹结构
                    zipf.write(file_path, os.path.relpath(file_path, folder_path))

        # 将zip文件附加到Allure报告中
        allure.attach.file(zip_path, name=zip_name, attachment_type="application/zip")

        # 清理临时文件夹
        shutil.rmtree(temp_dir)

    def remove_folder(self, path):
        if not os.path.isdir(path):
            return
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(path)
