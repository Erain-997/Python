import re
import time

from common.utils.decorator import Decorate
from sys_android.page_objects.common_page import CommonPage


class ShortsPage(CommonPage):

    @Decorate.collect_test("寻找feeds流预告片")
    def search_shorts_trailer(self, into=False):
        self.click(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[1]}"]'),
            "切换tab到短剧"
        )
        for i in range(10):
            if not self.wait_element(self.element.shorts_page.trailer_tv, "等待观看全局按钮出现,即预告片"):
                self.swipe_by_percent(0.28, 0.6, 0.28, 0.1, 200, "观看下一集")
            else:
                if into:
                    self.click(self.element.shorts_page.trailer_tv, "点击观看 预告片")
                break

    @Decorate.collect_test("下滑查看第一集")
    def swipe_to_first_episode(self):
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)

    def deal_with_episode_num(self, text):
        numbers = re.findall(r'\d+', text)
        if len(numbers) == 0:
            return -1
        numbers = list(map(int, numbers))

        # 返回最小值
        return min(numbers), max(numbers)

    @Decorate.collect_test("寻找feed流短剧")
    def search_shorts_drama(self, into=False):
        self.click(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[1]}"]'),
            "切换tab到短剧"
        )
        # self.swipe_by_percent(0.28, 0.6, 0.28, 0.1, 200)
        for i in range(6):
            if not self.wait_element(self.element.common_page.shorts_headshot, "等待头像出现,即短剧"):
                self.swipe_by_percent(0.28, 0.6, 0.28, 0.1, 200)
            else:
                show_name = self.get_element_text(self.element.immersion_page.shorts_name, f"获取短剧名称")
                episode_num = self.get_element_text(self.element.drama_page.episode_num, f"获取短剧集数")
                episode_now, episode_sum = self.deal_with_episode_num(episode_num)
                if into:
                    self.click(self.element.shorts_page.trailer_tv, "等待观看全局按钮出现,即预告片")
                return show_name, episode_now, episode_sum

    @Decorate.collect_test("点击集数进入正片播放")
    def into_shorts_drama(self, episode_now, episode_sum):
        self.click(self.element.drama_page.episode_num, "点击进入正片播放")
        # 默认进去选集
        if episode_now < 25:
            text = f"1-{episode_sum}"
        else:
            text = "1-25"
        self.assert_element_exists(
            ('xpath',
             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{text}"]'),
            f"断言-25集分页,当前总集数{episode_sum}"
        )
        self.press_back_button(case_name="关闭选集列表")

    @Decorate.collect_test("快速播完当前剧集, 到下一集")
    def to_next_drama(self):
        seekbar_pos = self.wait_element(self.element.immersion_page.shorts_seekbar_line,
                                        "等待进度条出现, 准备拉到底").location
        width, height = self.get_window_size()
        self.swipe(100, seekbar_pos["y"], int(width) - 50, seekbar_pos["y"], 450,
                   "拉动进度条到末尾")
        # 播放完自动进入下一集
        time.sleep(3)
        self.resolution_tap(0.5, 0.5, "点击视频中央暂停播放")

    @Decorate.collect_test("滑动查看剧集并记录名称进度")
    def shorts_name_progress(self):
        # 下滑查看第一集
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400, "下滑查看第一集")
        # 下滑查看第二集
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400, "下滑查看第二集")
        # 下滑查看第三集
        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400, "下滑查看第三集")
        # 观看6秒
        time.sleep(6)
        show_name = self.get_element_text(self.element.immersion_page.shorts_name, f"获取短剧名称")
        episode_num = self.get_element_text(self.element.drama_page.episode_num, f"获取短剧集数")

        return show_name, episode_num

    @Decorate.collect_test("退出沉浸页，进入追剧页面")
    def exit_immersion_page(self):
        time.sleep(4)
        self.press_back_button("退出沉浸页")
        self.click(self.element.common_page.later, "点击later按钮")
        # self.click(self.element.common_page.back, "返回首页")
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[2]}"]',
            ),
            "进入追剧页面",
        )
        self.click(self.element.common_page.recently_played, "点击最近播放按钮")

    @Decorate.collect_test("在shorts界面看完预告片")
    def watch_trailer_in_shorts(self):
        show_name = self.get_element_text(self.element.immersion_page.shorts_name, f"获取短剧名称")
        # 快速播完
        seekbar_pos = self.wait_element(self.element.immersion_page.new_seekbar_line, "等待进度条出现").location
        self.swipe(seekbar_pos["x"] + 500, seekbar_pos["y"], seekbar_pos["x"], seekbar_pos["y"], 150,
                   "拖动进度条到末尾")
        # 播放完自动进入第一集
        time.sleep(6)

        return show_name

    @Decorate.collect_test("sleep等待播放完当前剧集")
    def sleep_and_wait(self):
        self.resolution_tap(0.5, 0.5, "点击视频中央继续播放")
        time.sleep(5)

    @Decorate.collect_test("首页查看资源位短剧")
    def search_shorts_in_home(self):
        self.click(self.element.common_page.act_bottom_float_resource_iv, "点击首页资源位剧")
        self.swipe_by_percent(0.28, 0.6, 0.28, 0.1, 200, "观看下一集,即第二集")
        # 播放超过5s
        time.sleep(6)
        show_name = self.get_element_text(self.element.immersion_page.shorts_name, f"获取短剧名称")
        episode_num = self.get_element_text(self.element.drama_page.episode_num, f"获取当前短剧集数")
        episode, _ = self.deal_with_episode_num(episode_num)
        return show_name, episode

    @Decorate.collect_test("退出沉浸页,进入短剧")
    def exit_immersion_page_into_shorts(self):
        self.press_back_button("退出沉浸页")
        self.click(self.element.common_page.later, "点击later按钮")
        self.click(
            (
                "xpath",
                f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[1]}"]',
            ),
            "进入短剧页面",
        )
