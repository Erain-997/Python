import time
from time import sleep

import allure
from selenium.webdriver.common.action_chains import ActionChains

from common.language.lang_mgr import lang_mgr
from common.utils.decorator import Decorate
from common.utils.report import get_app_version, compare_versions
from sys_android.page_objects.common_page import CommonPage


class ImmersionPage(CommonPage):

    @Decorate.collect_test("点击分辨率按钮")
    def click_resolution_button(self):
        if compare_versions():
            self.click(self.element.subscribe_page.new_resolution, "点击分辨率按钮")
        else:
            self.click(self.element.subscribe_page.resolution, "点击分辨率按钮")
        self.click(self.element.immersion_page.resolution_a, "选择480p播放")
        time.sleep(1)

    @Decorate.collect_test("切换至480p播放")
    def switch_4080p(self):
        self.click(self.element.immersion_page.resolution_a, "选择480p播放")

    @Decorate.collect_test("切换至0.5X倍速播放")
    def switch_half_speed(self):
        if compare_versions():
            self.click(self.element.immersion_page.new_play_speed, "点击倍速按钮")
        else:
            self.click(self.element.immersion_page.play_speed, "点击倍速按钮")
        self.click(self.element.immersion_page.half_speed, "选择0.5X倍速播放")

    @Decorate.collect_test("获取当前播放进度")
    def get_play_progress(self):
        if compare_versions():
            element_to_long_press = self.wait_element(self.element.immersion_page.new_seekbar_line, "获取进度条元素")
            actions = ActionChains(self.driver)
            actions.click_and_hold(element_to_long_press).pause(6)
            actions.perform()
        else:
            self.tap(400, 600, "唤起菜单栏", 200)

    @Decorate.collect_test("退出沉浸页，进入追剧页面")
    def exit_immersion_page(self):
        with allure.step("退出沉浸页"):
            time.sleep(4)
            self.press_back_button("退出沉浸页")
            self.click(self.element.common_page.later, "点击later按钮")
            self.click(self.element.common_page.back, "返回首页")
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[2]}"]',
            ),
            "进入追剧页面",
        )

    @Decorate.collect_test("点击短剧头像")
    def click_headshot(self):
        if compare_versions():
            self.click(self.element.common_page.new_headshot, "点击短剧头像")
        else:
            self.click(self.element.common_page.headshot, "点击短剧头像")

    @Decorate.collect_test("沉浸页-点击短剧头像")
    def click_immersion_headshot(self):
        self.click(self.element.common_page.shorts_headshot, "点击短剧头像")

    @Decorate.collect_test("点击收藏按钮")
    def click_collect(self):
        if compare_versions():
            self.click(self.element.common_page.new_collect, "点击收藏按钮")
        else:
            self.click(self.element.common_page.collect, "点击收藏按钮")

    @Decorate.collect_test("点击最近播放按钮")
    def click_play(self):
        self.click(self.element.common_page.recently_played, "点击最近播放按钮")

    @Decorate.collect_test("进入短剧页面")
    def enter_shorts(self):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[1]}"]',
            ),
            "进入短剧页面",
        )

    @Decorate.collect_test("进入追剧页面")
    def enter_chase_shorts(self):
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[1]}"]',
            ),
            "进入短剧页面",
        )

    @Decorate.collect_test("删除短剧记录")
    def delete_history(self):
        self.click(self.element.immersion_page.edit, "点击编辑按钮")
        self.click(self.element.immersion_page.shorts_name, "选择短剧")
        self.click(self.element.immersion_page.delete, "点击删除按钮")
        self.click(self.element.common_page.cocnfirm_button, "确认删除")

    @Decorate.collect_test("返回首页")
    def back_home(self):
        time.sleep(4)
        self.press_back_button("退出简介页面")
        time.sleep(4)
        self.press_back_button("退出沉浸页")
        self.click(self.element.common_page.later, "点击later按钮")
        self.click(self.element.common_page.back, "返回首页")

    @Decorate.collect_test("点击下方剧集条")
    def click_episode_num_view(self):
        self.click(self.element.immersion_page.episode_num_view, "点击下方剧集条")

    @Decorate.collect_test("点击右侧list")
    def click_shorts_list(self):
        self.click(self.element.common_page.shorts_list, "点击右侧list")

    @Decorate.collect_test("点击头像")
    def click_shorts_headshot(self):
        self.click(self.element.common_page.shorts_headshot, "点击头像")

    @Decorate.collect_test("获取短剧名称")
    def get_shorts_name(self):
        self.assert_element_exists(self.element.immersion_page.shorts_name, "获取短剧名称")

    @Decorate.collect_test("拖动进度条")
    def drag_progress_bar(self):
        progress_bar = self.wait_element(self.element.immersion_page.shorts_seekbar_line, "获取进度条元素")
        # 获取进度条的尺寸和位置
        progress_bar_size = progress_bar.size
        progress_bar_location = progress_bar.location
        # 计算要拖动到的位置
        start_x = progress_bar_location["x"] + progress_bar_size["width"] * 0.05
        start_y = progress_bar_location["y"] + progress_bar_size["height"] / 2
        end_x = progress_bar_location["x"] + progress_bar_size["width"]
        end_y = start_y
        actions = ActionChains(self.driver)
        actions.pause(1)
        actions.drag_and_drop_by_offset(progress_bar, end_x - start_x, end_y - start_y).perform()
        time.sleep(3)
        self.resolution_tap(0.5, 0.5, "点击视频中央暂停播放")

        if compare_versions():
            element_to_long_press = self.wait_element(self.element.immersion_page.new_seekbar_line, "获取进度条元素")
            actions = ActionChains(self.driver)
            actions.click_and_hold(element_to_long_press).pause(6)
            actions.perform()

    @Decorate.collect_test("连续播放两集")
    def play_two_episodes(self):
        sleep(2)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(2)
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
        sleep(2)

    @Decorate.collect_test("点击收藏滑动条")
    def click_collect_swipe(self):
        self.click(self.element.common_page.collect_progress, "点击收藏滑动条")

    def check_element_task(self):
        element = self.wait_element(self.element.common_page.play_x5)
        self.assert_text_equal(element, "1.5x Speed Playing", "断言-长按屏幕视频1.5倍速播放")

    @Decorate.collect_test("从沉浸页进入付费卡点")
    def immersion_page_into_pay_card(self):
        # 记录每一集的进度
        # time_now_01 = self.get_current_time_tv()
        self.swipe_by_percent(0.28, 0.7, 0.28, 0.3, 400)  # 上滑
        # 第二集播放4秒, 为了后面校验进度
        time.sleep(4)
        time_now_02 = self.get_current_time_tv()
        self.swipe_by_percent(0.28, 0.7, 0.28, 0.3, 400)  # 上滑
        # 第三集播放4秒, 为了后面校验进度
        time.sleep(4)
        time_now_03 = self.get_current_time_tv()
        self.swipe_by_percent(0.28, 0.7, 0.28, 0.3, 400)  # 上滑
        return time_now_02, time_now_03

    @Decorate.collect_test("观看广告解锁剧集")
    def unlock_by_advertisement(self):
        self.click(self.element.common_page.title, "观看视频解锁")
        time.sleep(6)
        self.click(self.element.common_page.cancel_login, "关闭激励视频")
        self.press_back_button()

    @Decorate.collect_test("沉浸页从第四集返回第三集, 检查第三/四集播放进度")
    def check_4_and_3_play(self, time_now_03_before):
        time.sleep(4)
        time_now = self.get_current_time_tv()
        self.assert_more_than("00:03", time_now, "断言-第四集播放4秒,进度不止3秒")
        self.swipe_by_percent(0.28, 0.3, 0.28, 0.7, 400)  # 上滑
        time_now_03 = self.get_current_time_tv()
        self.assert_more_than(time_now_03_before, time_now_03, "断言-第三集播放继续播放,进度不止3秒")

    @Decorate.collect_test("沉浸页从第四集跳转返回第二集, 检查第二/四集播放进度")
    def check_4_and_2_play(self, time_now_02_before):
        time.sleep(4)
        time_now = self.get_current_time_tv()
        self.assert_more_than("00:03", time_now, "断言-第四集播放4秒,进度不止3秒")
        self.click(('xpath', f'//android.widget.TextView[@text="{lang_mgr.shorts_fragment_list()}"]'),
                   "点击选集按钮")
        self.click(self.element.drama_page.two_episodes, "点击第2集")
        time_now_02 = self.get_current_time_tv()
        self.assert_more_than(time_now_02_before, time_now_02, "断言-第二集播放继续播放,进度不止3秒")

    @Decorate.collect_test("断言-等待10秒")
    def wait_10s(self):
        time.sleep(10)
