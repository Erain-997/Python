import logging
from datetime import datetime

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from common.utils.tools import language_name
from common.language.lang_mgr import lang_mgr
from common.mysql.mysql import MySQLClient2
from common.utils.cmd_tools import *
from common.utils.report import get_app_version
from sys_android.page_objects.common_page import CommonPage


class PagesScreenshotPage(CommonPage):
    client = MySQLClient2()

    def pages_screenshot_01(self, screenshot_path):
        with allure.step("跳过首页广告弹窗"):
            try:
                self.click_screenshot(
                    self.element.common_page.allow_img, "点击通知图标", "允许ShortMax向您发送通知弹窗", screenshot_path
                )
                self.click(self.element.common_page.no_allow, "点击Don’t allow按钮")
            except Exception as e:
                pass
            try:
                self.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
            except Exception as e:
                logging.error(f"An error：{e}")
            time.sleep(10)
            self.click(self.element.common_page.navigation_back, "退出归因剧")
            element = ('xpath', f'//android.widget.TextView[@text="{lang_mgr.common_later()}"]')
            if self.wait_element(element, "升级弹窗存在", 6) is not None:
                self.click_screenshot(
                    self.element.common_page.close_iv, "关闭升级弹窗", "升级弹窗", screenshot_path
                )
            self.click_screenshot(
                self.element.common_page.notify_logo, "点击礼物图标", "推荐授权通知并获得奖金弹窗", screenshot_path
            )
            # self.click_screenshot(self.element.common_page.close_pop_ups, "关闭推荐更新弹窗", "授权通知并获得奖金弹窗")
            self.click_screenshot(
                self.element.common_page.close_iv, "关闭授权通知并获得奖金弹窗", "新人专享", screenshot_path
            )
            self.click(self.element.common_page.navigation_back, "退出新人专享")

            if self.wait_element(self.element.common_page.close_iv, "合并账号弹窗存在", 6) is not None:
                self.driver.save_screenshot(screenshot_path + "/合并账号弹窗.png")
                self.click(self.element.common_page.close_iv, "关闭合并账号弹窗")
                time.sleep(1)
                self.driver.save_screenshot(screenshot_path + "/首页.png")
                self.click_screenshot(
                self.element.common_page.drama_library, "进入剧库页面", "剧库页面1", screenshot_path, 2
            )
                self.click_screenshot(self.element.found_page.more, "查看更多", "剧库页面2", screenshot_path)
                self.press_back_button("关闭Filter页面")
            else:
                self.driver.save_screenshot(screenshot_path + "/首页.png")
            # self.click_screenshot(
            #     self.element.common_page.navigation_back, "返回首页", "首页登录引导", screenshot_path, 2
            # )
            # self.click(self.element.common_page.close_iv, "关闭登录引导弹窗")
        with allure.step("切换账号"):
            self.click_screenshot(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
                ),
                "进入我的模块",
                "我的登录引导",
                screenshot_path,
            )
            time.sleep(1)
            self.press_back_button("退出登录引导")
            time.sleep(2)
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            self.click(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[3]}"]',
                ),
                "点击设置按钮",
            )
            self.click(self.element.common_page.switch_new_button, "切换成新账号")
            self.click(self.element.common_page.switch_button, "点击切换")
            for i in range(6):
                time.sleep(0.5)
                if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                    self.press_back_button()
                else:
                    break
        with allure.step("沉浸页相关"):
            try:
                self.click_screenshot(self.element.common_page.search_box, "点击搜索框", "搜索页面",
                                      screenshot_path)
            except:
                self.click_screenshot(self.element.common_page.search_box_ar, "点击搜索框", "搜索页面",
                                      screenshot_path)
            self.swipe_by_percent(0.8, 0.5, 0.2, 0.5, 300)
            self.driver.save_screenshot(screenshot_path + "/排行榜(搜索页).png")
            if language_name()[args.language] != "en":
                try:
                    self.click_screenshot(self.element.found_page.more, "查看更多", "排行榜", screenshot_path, 2)
                    self.click(self.element.common_page.navigation_back, "退出排行榜")
                except Exception as e:
                    logging.error(f"An error：{e}")
            for k, j in self.language_search().items():
                if k == args.language:
                    self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
            time.sleep(2)
            self.click_screenshot(self.element.redeem_codes_page.search_iv, "点击搜索", "搜索内容页面",
                                  screenshot_path)
            self.click_screenshot(
                self.element.drama_page.video_detail, "进入视频沉浸页", "沉浸页页面", screenshot_path, 2
            )

            self.click_screenshot(self.element.common_page.new_headshot, "点击短剧头像", "剧简介页面",
                                  screenshot_path)
            self.press_back_button()

            self.click_screenshot(
                self.element.subscribe_page.new_resolution, "点击分辨率按钮", "分辨率", screenshot_path
            )
            self.click_screenshot(
                self.element.immersion_page.resolution_a, "点击480p选项", "提示-正在切换至 480p", screenshot_path
            )

            self.click_screenshot(self.element.immersion_page.new_play_speed, "点击倍速按钮", "倍速",
                                  screenshot_path)
            self.click_screenshot(
                self.element.immersion_page.half_speed, "点击0.5X选项", "已切换至0.5倍播放", screenshot_path
            )

            self.click_screenshot(
                self.element.common_page.new_episodes, "点击选集按钮", "剧集列表页面", screenshot_path
            )
            self.click_screenshot(
                self.element.drama_page.five_episodes, "点击第5集", "提示-请解锁先前的剧", screenshot_path
            )
            self.click_screenshot(
                self.element.drama_page.four_episodes, "点击第4集", "付费卡点页面", screenshot_path, 5
            )
            # 付费卡点所有订阅选项截图
            self.driver.save_screenshot(screenshot_path + "/订阅(付费卡点)1.png")
            for i in range(2, 8):
                self.swipe_by_percent(0.8, 0.35, 0.3, 0.35, 300)
                time.sleep(1)
                self.driver.save_screenshot(screenshot_path + f"/订阅(付费卡点){i}.png")
            self.click_screenshot(
                self.element.automatic_unlock_page.coins_store,
                "点击【Coins Store】",
                "【Coins Store】页面1",
                screenshot_path,
                2,
            )
            time.sleep(1)
            self.press_back_button("退出付费卡点页面")
            self.click_screenshot(
                self.element.common_page.retain_title, "充值挽留弹窗", "充值挽留弹窗", screenshot_path, 2
            )
            self.click(self.element.common_page.close_iv, "关闭充值挽留弹窗")
            self.click_screenshot(
                self.element.common_page.unlock, "点击立即解锁按钮", "付费卡点页面(充值挽留商品)", screenshot_path, 2
            )
            self.click_screenshot(
                self.element.automatic_unlock_page.coins_store,
                "点击【Coins Store】",
                "【Coins Store】页面(充值挽留)",
                screenshot_path,
                2,
            )
            time.sleep(1)
            self.swipe_by_percent(0.8, 0.8, 0.29, 0.8, 300)
            self.swipe_by_percent(0.8, 0.8, 0.29, 0.8, 300)
            self.click_screenshot(
                self.element.drama_page.slide, "点击store标题上方横线", "【Coins Store】页面2", screenshot_path
            )
            self.swipe_by_percent(0.2, 0.8, 0.8, 0.8, 300)
            self.swipe_by_percent(0.2, 0.8, 0.8, 0.8, 300)
            self.click(self.element.drama_page.store_sku, "购买膨胀商品")
            self.click_screenshot(
                self.element.common_page.cocnfirm_button, "确认支付", "提示-充值成功、登录弹窗", screenshot_path, 2
            )
            self.click(self.element.common_page.close_iv, "关闭提示登录弹窗")
            # 定位到需要长按的元素
            element_to_long_press = self.wait_element(self.element.common_page.new_logo, "获取到logo元素")
            # 使用 ActionChains 执行长按操作
            actions = ActionChains(self.driver)
            actions.click_and_hold(element_to_long_press).pause(4)
            # 开始执行长按操作
            actions.perform()
            # 在长按的同时进行截图
            time.sleep(1)  # 等待1秒后截图，确保长按已经开始
            self.driver.save_screenshot(screenshot_path + "/长按倍速提示.png")
            # 完成长按操作
            actions.release(element_to_long_press).perform()

            self.click_screenshot(
                self.element.common_page.navigation_back, "退出沉浸页", "选择你想接收的通知类型弹窗",
                screenshot_path
            )
            self.click(self.element.common_page.close_iv, "关闭选择你想接收的通知类型弹窗")
        with allure.step("兑换码"):
            self.click(self.element.common_page.clear_search_box, "清空搜索内容")
            self.wait_element(self.element.common_page.search, "输入tvq8lgcby9").send_keys("tvq8lgcby9")
            self.click_screenshot(
                self.element.redeem_codes_page.search_iv, "点击搜索", "兑换成功弹窗", screenshot_path, 3
            )
            time.sleep(4)
            self.press_back_button("关闭兑换码弹窗")
            time.sleep(5)
            self.press_back_button("退出沉浸页")
            if self.wait_element(self.element.common_page.later, "判断Later按钮是否存在", 1) is not None:
                self.click(self.element.common_page.later, "点击Later按钮")
            # 重复搜索已兑换的兑换码
            self.wait_element(self.element.common_page.search, "输入兑换码：tvq8lgcby9").send_keys("tvq8lgcby9")
            self.click_screenshot(
                self.element.redeem_codes_page.search_iv, "点击搜索", "兑换成功弹窗(已领取)", screenshot_path, 2
            )
            time.sleep(4)
            self.press_back_button("关闭兑换码弹窗")
            time.sleep(4)
            self.press_back_button("退出沉浸页")
            if self.wait_element(self.element.common_page.later, "判断Later按钮是否存在", 1) is not None:
                self.click(self.element.common_page.later, "点击Later按钮")
            # 搜索已用完的兑换码
            self.wait_element(self.element.common_page.search, "输入兑换码：tvzpneu73").send_keys("tvzpneu73")
            self.click_screenshot(
                self.element.redeem_codes_page.search_iv, "点击搜索", "提示-来晚了，已领完", screenshot_path, 1.5
            )
            time.sleep(3)
            # self.click_screenshot(self.element.common_page.discount, "点击折扣剧", "沉浸页折扣ui")
            self.press_back_button("退出沉浸页")
            if self.wait_element(self.element.common_page.later, "判断Later按钮是否存在", 1) is not None:
                self.click(self.element.common_page.later, "点击Later按钮")
            time.sleep(6)
            if self.wait_element(self.element.common_page.cancel_login, 3):
                self.click(self.element.common_page.cancel_login, "关闭插屏广告")
            # 搜索已过期的兑换码
            self.wait_element(self.element.common_page.search, "输入兑换码：tvl5fb").send_keys("tvl5fb")
            self.click_screenshot(
                self.element.redeem_codes_page.search_iv, "点击搜索", "提示-兑换码已过期", screenshot_path, 2
            )
            time.sleep(5)
            self.press_back_button("退出沉浸页")
            if self.wait_element(self.element.common_page.later, "判断Later按钮是否存在", 1) is not None:
                self.click(self.element.common_page.later, "点击Later按钮")
            # 禁用的兑换码
            self.wait_element(self.element.common_page.search, "输入兑换码：tvbxq4jy").send_keys("tvbxq4jy")
            self.click_screenshot(
                self.element.redeem_codes_page.search_iv, "点击搜索", "提示兑换码不存在", screenshot_path, 2
            )
            self.click(self.element.common_page.back, "返回首页")
            for h in range(3):
                time.sleep(1)
                if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                    self.press_back_button()
                else:
                    break
        with allure.step("搜索历史相关"):
            self.click(self.element.common_page.index_search, "点击首页搜索框")
            self.wait_element(self.element.common_page.search, "输入：test").send_keys("test")
            self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
            time.sleep(3)
            self.press_back_button("返回")
            if lang_mgr.app_language_code == "in" or lang_mgr.app_language_code == "ar":
                self.click_screenshot(
                    self.element.common_page.search_box_ar, "点击搜索框", "搜索页面(有搜索记录)", screenshot_path, 1
                )
            else:
                self.click_screenshot(
                    self.element.common_page.search_box, "点击搜索框", "搜索页面(有搜索记录)", screenshot_path, 1
                )
            self.click_screenshot(
                self.element.redeem_codes_page.history_clear_iv, "点击删除搜索历史图标", "确认删除弹窗", screenshot_path
            )
            self.click_screenshot(
                self.element.common_page.cocnfirm_button, "确认删除", "搜索历史已删除页面", screenshot_path
            )
            self.click(self.element.common_page.back, "返回首页")
            for i in range(6):
                time.sleep(0.5)
                if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                    self.press_back_button()
                else:
                    break
        with allure.step("Shorts相关"):
            self.click_screenshot(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[1]}"]',
                ),
                "进入短剧页面",
                "短剧页面",
                screenshot_path,
                2,
            )
            time.sleep(1)

            self.click(self.element.common_page.shorts_collect, "点击收藏按钮")
            self.driver.save_screenshot(screenshot_path + "/Shorts页面(已收藏).png")
        with allure.step("My List相关"):
            self.click_screenshot(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[2]}"]',
                ),
                "进入追剧页面",
                "追剧页面",
                screenshot_path,
                2,
            )
            self.click_screenshot(self.element.common_page.chasing_edit, "点击编辑", "收藏页面-编辑", screenshot_path)
            self.click_screenshot(
                self.element.common_page.select_all, "点击全选", "收藏页面-编辑-全选", screenshot_path
            )
            self.click_screenshot(
                self.element.common_page.recently_played, "点击最近播放", "提示-请先取消选中的剧", screenshot_path
            )
            self.click_screenshot(
                self.element.immersion_page.delete, "点击删除按钮", "收藏页面-确认删除弹窗", screenshot_path
            )
            self.click_screenshot(
                self.element.common_page.cocnfirm_button, "点击确认按钮", "收藏页面(无剧)", screenshot_path
            )
            self.click_screenshot(
                self.element.common_page.recently_played, "点击最近播放", "最近播放页面(有剧)", screenshot_path, 2
            )
            self.click(self.element.common_page.chasing_edit, "点击编辑")
            self.click(self.element.common_page.select_all, "选择短剧")
            self.click(self.element.immersion_page.delete, "点击删除按钮")
            self.click_screenshot(
                self.element.common_page.cocnfirm_button, "点击确认按钮", "最近播放页面(无剧)", screenshot_path
            )
        with allure.step("设置相关"):
            self.click(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
                ),
                "进入我的模块",
            )
            time.sleep(1)
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            self.click(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[2]}"]',
                ),
                "进入语言页面",
            )
            self.driver.save_screenshot(screenshot_path + "/语言页面1.png")
            time.sleep(2)
            self.swipe_by_percent(0.28, 0.75, 0.28, 0.1, 400)
            self.click_screenshot(self.element.common_page.title, "点击语言设置(标题)", "语言页面2", screenshot_path)
            self.click(self.element.common_page.navigation_back, "退出语言设置页面")
            self.click_screenshot(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[3]}"]',
                ),
                "点击设置按钮",
                "设置页面1",
                screenshot_path,
            )
            self.click_screenshot(
                self.element.common_page.account_info, "点击账户信息", "账户信息页面", screenshot_path
            )
            self.click(self.element.common_page.navigation_back, "退出账户信息")
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            self.click(self.element.common_page.unlock_in_bulk, "点击批量解锁")
            self.click(self.element.common_page.unlock_inlet_two, "实验2")
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            self.click(self.element.common_page.and_newuser, "点击新人tab栏是否展示")
            self.click(self.element.common_page.show, "1:展示")
            # self.click(self.element.common_page.and_pip, "点击沉浸页支持小窗播放")
            # self.click(self.element.common_page.support, "1:支持")
            self.click(self.element.common_page.and_without, "点击解锁弹窗无广告解锁")
            self.click(self.element.common_page.and_without_one, "选择值1")
            time.sleep(1)
            self.swipe_by_percent(0.28, 0.2, 0.28, 0.6, 400)
            self.swipe_by_percent(0.28, 0.2, 0.28, 0.6, 400)
            self.click(self.element.common_page.switch_new_button, "切换成新账号")
            self.click_screenshot(
                self.element.common_page.switch_button, "切换", "提示-新账号创建完毕", screenshot_path, 1
            )
            for i in range(3):
                time.sleep(0.5)
                if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                    self.press_back_button()
                else:
                    break
        with allure.step("沉浸页相关"):
            try:
                self.click_screenshot(self.element.common_page.search_box, "点击搜索框", "搜索页面", screenshot_path)
            except:
                self.click_screenshot(self.element.common_page.search_box_ar, "点击搜索框", "搜索页面", screenshot_path)
            for k, j in self.language_search().items():
                if k == args.language:
                    self.wait_element(self.element.common_page.search, f"输入:{j}").send_keys(f"{j}")
            time.sleep(2)
            self.click(self.element.redeem_codes_page.search_iv, "点击搜索")
            self.click(self.element.drama_page.video_detail, "进入视频沉浸页")
            time.sleep(3)
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            self.click_screenshot(
                self.element.common_page.new_logo, "点击logo", "提示-添加到列表后观看", screenshot_path
            )
            time.sleep(2)
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            time.sleep(7)
            self.press_back_button("退出付费卡点")
            self.click_screenshot(
                self.element.common_page.Ad_header, "点击看广告弹窗标题", "看广告弹窗", screenshot_path, 2
            )
            self.click_screenshot(
                self.element.common_page.close_iv, "关闭看广告弹窗", "立即解锁按钮", screenshot_path
            )
            self.click_screenshot(
                self.element.common_page.unlock, "点击立即解锁按钮", "付费卡点页面(批量解锁)", screenshot_path, 2
            )
            self.click(self.element.top_up_page.three_top_up, "选择解锁全部剧集选项")
            self.click_screenshot(
                self.element.common_page.cocnfirm_button, "点击确认按钮", "提示-已批量解锁27集", screenshot_path, 2
            )
            time.sleep(2)

            self.click_screenshot(
                self.element.common_page.navigation_back, "退出沉浸页", "【画中画】功能上线了~弹窗", screenshot_path
            )
            try:
                self.wait_element(self.element.common_page.close_iv, "关闭【画中画】弹窗").click()
            except Exception as e:
                logging.error(f"An error：{e}")
            time.sleep(4)
            self.press_back_button("退出沉浸页")
            time.sleep(3)
            self.click(self.element.common_page.later, "点击Later按钮")
            time.sleep(8)
            if self.wait_element(self.element.reward_page.cancel_button, "等待广告出现"):
                self.click(self.element.reward_page.cancel_button, "关闭广告")
                time.sleep(1)
            self.click(self.element.common_page.back, "返回首页")
            time.sleep(1)

    def pages_screenshot_02(self, screenshot_path):
        with allure.step("我的页面相关"):
            self.android_version()
            self.switch_new_account()
            with allure.step("我的-登录"):
                self.click(
                    (
                        "xpath",
                        f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
                    ),
                    "进入我的模块",
                )
                time.sleep(2)
                self.driver.save_screenshot(screenshot_path + "/我的页面.png")
                self.click_screenshot(self.element.common_page.login_in, "点击登录按钮", "登录页面", screenshot_path, 1)
                self.click(self.element.common_page.navigation_back, "退出登录页面")
            with allure.step("订阅相关"):
                self.click_screenshot(
                    self.element.common_page.subscribe_now, "点击订阅按钮", "订阅页面", screenshot_path, 1
                )
                self.swipe_by_percent(0.28, 0.6, 0.28, 0.1, 300)
                self.click_screenshot(
                    self.element.common_page.desc, "点击关于订阅标题", "订阅页面-关于订阅", screenshot_path
                )
                self.click_screenshot(
                    self.element.top_up_page.refresh, "点击Restore", "提示-没有购买可以恢复(订阅)", screenshot_path
                )
                self.swipe_by_percent(0.28, 0.1, 0.28, 0.6, 300)
                # 所有订阅选项截图
                self.driver.save_screenshot(screenshot_path + "/订阅(订阅页面)1.png")
                for i in range(2, 9):
                    self.swipe_by_percent(0.6356, 0.38, 0.0347, 0.38, 500)
                    time.sleep(1)
                    self.driver.save_screenshot(screenshot_path + f"/订阅(订阅页面){i}.png")
                self.swipe_by_percent(0.2, 0.38, 0.7, 0.38, 500)
                time.sleep(1)
                self.swipe_by_percent(0.2, 0.38, 0.7, 0.38, 500)
                time.sleep(1)
                self.swipe_by_percent(0.2, 0.38, 0.7, 0.38, 500)
                for i in range(5):
                    if self.wait_element(self.element.common_page.week_pro, "等待pro卡出现", 1) is not None:
                        self.click(self.element.common_page.week_pro, "点击年卡pro")
                        break
                    else:
                        self.swipe_by_percent(0.2, 0.38, 0.7, 0.38, 500)
                self.click_screenshot(
                    self.element.common_page.cocnfirm_button, "确认订阅", "订阅页面(已订阅)", screenshot_path, 5
                )
                self.click_screenshot(
                    self.element.common_page.navigation_back, "退出订阅页面", "我的页面(已订阅)", screenshot_path
                )
                user_id = self.get_element_text(self.element.common_page.user_uid)[-6:]
                PagesScreenshotPage.client.connect()
                time.sleep(2)
                sql_result = f'UPDATE hi_subscription_user SET end_time = "0", end_time_real = "0" WHERE user_id = (SELECT id FROM hi_user WHERE user_code ={user_id})'
                PagesScreenshotPage.client.execute_non_query(sql_result)
                PagesScreenshotPage.client.close()
                allure.attach(sql_result, name="SQL", attachment_type=allure.attachment_type.TEXT)
                with allure.step("冷启动app"):
                    adb_shell("am force-stop com.startshorts.androidplayer")
                    time.sleep(2)
                    adb_shell(
                        "am start -n com.startshorts.androidplayer/.ui.activity.RoutingActivity --es is_auto_test_running true --es disable_home_pop_dialogs true --es disable_campaign_parse true"
                    )
                    time.sleep(2)
                    try:
                        self.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
                    except Exception as e:
                        logging.error(f"An error：{e}")
                    time.sleep(2)
                    for i in range(6):
                        time.sleep(0.5)
                        if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 3) is None:
                            self.press_back_button()
                        else:
                            self.swipe_by_percent(0.28, 0.5, 0.28, 0.35, 400)
                            break
                # 进入沉浸页
                self.click(self.element.immersion_page.shorts_name, "进入沉浸页")
                time.sleep(2)
                if self.wait_element(self.element.common_page.close_iv, "订阅到期弹窗关闭按钮") is not None:
                    self.driver.save_screenshot(screenshot_path + "/订阅到期弹窗.png")
                    self.click(self.element.common_page.close_iv, "关闭订阅到期弹窗")
                time.sleep(4)
                self.press_back_button("退出沉浸页")
                self.click(self.element.common_page.later, "点击Later按钮")
                for i in range(6):
                    time.sleep(0.5)
                    if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                        self.press_back_button()
                    else:
                        break
                self.click(
                    (
                        "xpath",
                        f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
                    ),
                    "进入我的模块",
                )
                self.click(self.element.common_page.subscribe_now, "点击订阅按钮")
                time.sleep(2)
                # self.swipe_by_percent(0.6356, 0.38, 0.0347, 0.38, 500)
                # 当前语言的订阅商品信息
                for i in range(8):
                    try:
                        if self.wait_element(self.element.subscribe_page.annual_pro, "等待pro卡出现", 1) is not None:
                            self.click(self.element.subscribe_page.annual_pro, "点击年卡pro")
                            break
                    except TimeoutException:
                        self.swipe_by_percent(0.5556, 0.3686, 0.0347, 0.3686, 500)

                self.click_screenshot(
                    self.element.top_up_page.negative_button,
                    "点击掉单测试按钮",
                    "掉点测试弹窗(订阅)",
                    screenshot_path,
                    2,
                )
                time.sleep(4)
                # self.click(self.element.common_page.close_pop_ups, "关闭【重试】弹窗")
                self.press_back_button("关闭【重试】弹窗")
                time.sleep(2)
                self.click(self.element.common_page.navigation_back, "退出订阅模块")
            with allure.step("充值页面相关"):
                self.click_screenshot(self.element.common_page.top_up, "点击充值按钮", "充值页面", screenshot_path, 2)
                self.click_screenshot(
                    self.element.top_up_page.restore, "点击【Refresh】", "提示-没有购买可以恢复(充值)", screenshot_path
                )
                coins_one = self.get_find_elements(self.element.top_up_page.coins_text)[0]
                self.click(
                    ("xpath", f'//android.widget.TextView[contains(@text, "{coins_one}")]'), f"点击充值{coins_one}"
                )
                time.sleep(1)
                self.click_screenshot(
                    self.element.top_up_page.negative_button, "点击掉单测试按钮", "掉点测试弹窗(充值)", screenshot_path
                )
                self.click(self.element.common_page.close_iv, "关闭【重试】弹窗")
                self.click_screenshot(
                    self.element.top_up_page.restore, "点击【Refresh】", "补单成功弹窗", screenshot_path
                )
                self.click(self.element.common_page.close_iv, "关闭补单通知")
                with allure.step("冷启动app"):
                    time.sleep(2)
                    adb_shell("am force-stop com.startshorts.androidplayer")
                    time.sleep(2)
                    adb_shell(
                        "am start -n com.startshorts.androidplayer/.ui.activity.RoutingActivity --es is_auto_test_running true --es disable_home_pop_dialogs true --es disable_campaign_parse true"
                    )
                    time.sleep(2)
                try:
                    self.wait_element(self.element.common_page.skip, "点击Skip按钮").click()
                except Exception as e:
                    logging.error(f"An error：{e}")
                for i in range(3):
                    time.sleep(0.5)
                    if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                        self.press_back_button()
                    else:
                        break
                self.click(
                    (
                        "xpath",
                        f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
                    ),
                    "进入我的模块",
                )
                self.click(self.element.common_page.top_up, "点击充值按钮")
                self.click(
                    ("xpath", f'//android.widget.TextView[contains(@text, "{coins_one}")]'), f"点击充值{coins_one}"
                )
                self.click(self.element.common_page.cocnfirm_button, "确认支付")
                try:
                    if self.wait_element(self.element.common_page.close_iv, "关闭弹窗"):
                        self.press_back_button("关闭弹窗")
                except Exception as e:
                    logging.error(f"An error：{e}")
                self.click(self.element.common_page.navigation_back, "退出充值页面")
                self.click_screenshot(
                    self.element.common_page.close_iv, "关闭好评弹窗", "好评弹窗", screenshot_path
                )
                self.click(self.element.common_page.top_up, "点击充值按钮")
                time.sleep(1)
                self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
                self.click_screenshot(self.element.common_page.title, "点击说明标题", "充值页面-说明", screenshot_path)
                self.click(self.element.common_page.navigation_back, "退出充值页面")
            with allure.step("我的钱包"):
                self.click_screenshot(
                    self.element.common_page.wallet, "点击我的钱包", "我的钱包页面", screenshot_path, 2
                )
                self.click_screenshot(
                    self.element.common_page.gold_records, "点击金币记录", "金币记录页面", screenshot_path, 2
                )
                self.click_screenshot(
                    self.element.common_page.reward_records, "点击奖励币记录", "奖励币记录页面", screenshot_path, 2
                )
                self.click(self.element.common_page.navigation_back, "退出我的钱包")
            with allure.step("任务中心页面相关"):
                time.sleep(1)
                self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
                self.click_screenshot(
                    (
                        "xpath",
                        f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[0]}"]',
                    ),
                    "点击奖励按钮",
                    "奖励页面-现在看弹窗",
                    screenshot_path,
                    2,
                )
                self.click_screenshot(
                    self.element.common_page.close_iv, "关闭广告弹窗", "任务中心页面", screenshot_path
                )
                self.click(
                    self.element.common_page.reward_notifications,
                    "点击获取奖励通知选项",
                )
                # self.click(self.element.common_page.allow, "点击允许按钮")
                self.click_screenshot(
                    self.element.common_page.reward_notifications,
                    "点击获取奖励通知选项",
                    "获取奖励通知提示",
                    screenshot_path,
                    2,
                )
                # 邮箱相关
                self.swipe_by_percent(0.28, 0.5, 0.28, 0.3, 400)
                self.click_screenshot(
                    self.element.common_page.bind_email, "点击绑定邮箱", "绑定邮箱页面", screenshot_path
                )
                self.wait_element(self.element.common_page.email_address_edt, "输入邮件地址：@").send_keys("@")
                self.click_screenshot(
                    self.element.common_page.get_code, "点击获取验证码", "提示-邮箱验证码发送失败", screenshot_path, 2
                )
                self.wait_element(self.element.common_page.verify_otp_edt, "输入验证码：1234").send_keys("1234")
                self.click_screenshot(
                    self.element.common_page.confirm, "点击确定", "提示-电子邮件验证码错误或过期", screenshot_path, 2
                )
                self.click(self.element.common_page.navigation_back, "退出绑定邮箱页面")
                # 手机号相关
                self.click_screenshot(
                    self.element.common_page.bind_phone_number, "点击绑定手机号", "绑定手机号页面", screenshot_path
                )
                self.click_screenshot(
                    self.element.common_page.phone_country_code, "选择区号", "区号页面", screenshot_path
                )
                self.click(self.element.common_page.navigation_back, "退出选择区号页面")
                self.wait_element(self.element.common_page.phone_number_edt, "输入手机号：123456").send_keys("123456")
                self.click_screenshot(
                    self.element.common_page.get_code, "点击获取验证码", "提示-手机号码格式不正确", screenshot_path
                )
                self.wait_element(self.element.common_page.verify_otp_edt, "输入验证码：1234").send_keys("1234")
                self.click_screenshot(
                    self.element.common_page.confirm, "点击确定", "提示-手机验证码错误或者已失效", screenshot_path, 2
                )
                self.click(self.element.common_page.navigation_back, "退出绑定手机号页面")
                self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
                self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
                self.click_screenshot(self.element.common_page.desc, "点击描述标题", "奖励页面-描述", screenshot_path)
                time.sleep(1)
                self.press_back_button("退出任务中心")

        # with allure.step("新人充值h5页面"):
        #     new_tab = self.get_find_elements(self.element.common_page.title)[2]
        #     print(
        #         new_tab,
        #         '---------------------'
        #     )
        #     self.click_screenshot(
        #         (
        #             "xpath",
        #             f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/title_tv" and @text="{new_tab}"]',
        #         ),
        #         "进入新人充值h5页面",
        #         "新人充值h5页面",
        #         screenshot_path,
        #         8,
        #     )
        #     self.click(self.element.common_page.h5_1, "点击订阅")
        #     self.click(self.element.common_page.cocnfirm_button, "点击确定订阅")
        #     time.sleep(3)
        #     for i in range(6):
        #         self.click(self.element.common_page.h5_1, "点击充值")
        #         self.click(self.element.common_page.cocnfirm_button, "点击确定充值")
        #         time.sleep(2.5)
        #     if self.wait_element(self.element.common_page.ended, "h5买完弹窗") is None:
        #         self.click(self.element.common_page.h5_1, "点击充值")
        #         self.click(self.element.common_page.cocnfirm_button, "点击确定充值")
        #     time.sleep(2)
        #     self.driver.save_screenshot(screenshot_path + "/h5页面全部充值完毕弹窗.png")

        # 点击我的获取uid修改分值
        with allure.step("冷启动app展示rfm低价值充值弹窗"):
            self.click(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
                ),
                "进入我的模块",
            )
            time.sleep(2)
            self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)
            self.click(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv" and @text="{self.get_my_button_text()[3]}"]',
                ),
                "点击设置按钮",
            )
            self.click(self.element.common_page.switch_new_button, "切换成新账号")
            self.click(self.element.common_page.switch_button, "点击切换")
            time.sleep(4)
            for i in range(6):
                time.sleep(0.5)
                if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                    self.press_back_button()
                else:
                    break
            self.click(
                (
                    "xpath",
                    f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[3]}"]',
                ),
                "进入我的模块",
            )
            user_id = self.get_element_text(self.element.common_page.user_uid)[-6:]
            time_str = datetime.now().strftime("%Y%m%d")
            PagesScreenshotPage.client.connect()
            time.sleep(2)
            sql_result = f"INSERT INTO ads_ever_user_rfm_tag_data_layer_max_1d (uid, country_code, max_login_cnt_score, max_pay_amount_score, dateid, ds) VALUES ((SELECT id FROM hi_user WHERE user_code ={user_id}),'US',2,1,{time_str},{time_str})"
            PagesScreenshotPage.client.execute_non_query(sql_result)
            PagesScreenshotPage.client.close()
            allure.attach(sql_result, name="SQL", attachment_type=allure.attachment_type.TEXT)
            adb_shell("am force-stop com.startshorts.androidplayer")
            time.sleep(2)
            adb_shell(
                "am start -n com.startshorts.androidplayer/.ui.activity.RoutingActivity --es is_auto_test_running true --es disable_home_pop_dialogs true --es disable_campaign_parse true"
            )
            time.sleep(2)
            try:
                self.wait_element(self.element.common_page.skip, "点击Skip按钮").click()
            except Exception as e:
                logging.error(f"An error：{e}")
            if self.wait_element(self.element.common_page.gift, "等待尊享图标出现", 6) is not None:
                self.driver.save_screenshot(screenshot_path + "/rfm低价值充值弹窗.png")

    def pages_screenshot_03(self, screenshot_path):
        with allure.step("剧解锁类型为金币"):
            time.sleep(4)
            adb_shell("am force-stop com.startshorts.androidplayer")
            time.sleep(4)
            adb_shell(
                "am start -n com.startshorts.androidplayer/.ui.activity.RoutingActivity --es is_auto_test_running true --es disable_home_pop_dialogs true --es disable_campaign_parse false --es is_pure_paying_user true"
            )
            try:
                self.wait_element(self.element.common_page.allow, "点击allow按钮", 4).click()
            except Exception as e:
                logging.error(f"An error：{e}")
            try:
                self.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
            except Exception as e:
                logging.error(f"An error：{e}")
            time.sleep(5)
            with allure.step("进入付费卡点"):
                for i in range(8):
                    element = ['xpath', f'//android.widget.TextView[@text="{lang_mgr.unlock_episode_dialog_fragment_coin_store()}"]']
                    if self.wait_element(element, "等待付费卡点出现", 2):
                        if self.get_element_text(element, 1.5) == lang_mgr.unlock_episode_dialog_fragment_coin_store():
                            time.sleep(4)
                            self.driver.save_screenshot(screenshot_path + "/付费卡点（剧解锁类型为金币）.png")
                            self.press_back_button("退出付费卡点")
                            time.sleep(2)
                            self.driver.save_screenshot(screenshot_path + "/广告挽留弹窗.png")
                            self.click_screenshot(self.element.common_page.title, "广告解锁", "广告请求失败，toast【请再试一次】",
                                                  screenshot_path, 2)
                            # if self.wait_element(("xpath", f"//android.widget.TextView[@text='请再试一次']"), "判断toast提示出现"):
                            #     self.driver.save_screenshot(screenshot_path + "广告请求失败，toast【请再试一次】.png")
                            self.click(self.element.common_page.cancel_button, "关闭广告挽留弹窗")
                            time.sleep(2)
                            self.driver.save_screenshot(screenshot_path + "/解锁选择弹窗.png")
                    else:
                        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)

        with allure.step("剧解锁类型为（广告+金币）"):
            time.sleep(4)
            adb_shell("am force-stop com.startshorts.androidplayer")
            time.sleep(4)
            adb_shell(
                "am start -n com.startshorts.androidplayer/.ui.activity.RoutingActivity --es is_auto_test_running true --es disable_home_pop_dialogs true --es disable_campaign_parse false --es is_pure_paying_user false"
            )
            try:
                self.wait_element(self.element.common_page.allow, "点击allow按钮", 4).click()
            except Exception as e:
                logging.error(f"An error：{e}")
            try:
                self.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
            except Exception as e:
                logging.error(f"An error：{e}")
            time.sleep(5)
            with allure.step("进入付费卡点"):
                for i in range(8):
                    element = ['xpath', f'//android.widget.TextView[@text="{lang_mgr.unlock_episode_dialog_fragment_coin_store()}"]']
                    if self.wait_element(element, "等待付费卡点出现", 2):
                        if self.get_element_text(element, 1.5) == lang_mgr.unlock_episode_dialog_fragment_coin_store():
                            time.sleep(4)
                            self.driver.save_screenshot(screenshot_path + "/付费卡点（广告+金币）.png")
                            self.press_back_button("退出付费卡点")
                            time.sleep(2)
                            self.driver.save_screenshot(screenshot_path + "/膨胀挽留弹窗.png")
                    else:
                        self.swipe_by_percent(0.28, 0.5, 0.28, 0.1, 400)

    def pages_screenshot_07(self, screenshot_path):
        try:
            self.wait_element(self.element.common_page.allow, "点击allow按钮", 4).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        try:
            self.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
        except Exception as e:
            logging.error(f"An error：{e}")
        self.driver.press_keycode(3)
        with allure.step(f"卸载{get_app_version()},安装2.0.7"):
            os.system(f"adb -s {args.device} uninstall com.startshorts.androidplayer")
            time.sleep(5)
            install_apk("/var/ftp/pub/short_tv_apk/android_QA/v2.0.7_20241223_1728.apk")
            time.sleep(5)
            adb_shell(f"am start com.startshorts.androidplayer/.ui.activity.RoutingActivity --es is_auto_test_running true --es app_language {args.language}")
        with allure.step("跳过首页广告弹窗"):
            self.click(self.element.common_page.no_allow, "点击Don’t allow按钮")
            try:
                self.wait_element(self.element.common_page.skip, "点击Skip按钮", 3).click()
            except Exception as e:
                logging.error(f"An error：{e}")
            time.sleep(10)
            self.press_back_button("退出归因剧")
            try:
                self.wait_element(self.element.common_page.later, "点击Later按钮").click()
            except Exception as e:
                logging.error(f"An error：{e}")
            element = ('xpath', f'//android.widget.TextView[@text="{lang_mgr.common_later()}"]')
            if self.wait_element(element, "升级弹窗存在", 6) is not None:
                self.click(self.element.common_page.close_iv, "关闭升级弹窗")
            self.click(self.element.common_page.notify_logo, "点击礼物图标")
            self.click(self.element.common_page.close_iv, "关闭授权通知并获得奖金弹窗")
            try:
                self.wait_element(self.element.common_page.navigation_back, "退出新人专享").click()
                self.wait_element(self.element.common_page.close_iv, "关闭合并账号弹窗").click()
            except Exception as e:
                logging.error(f"An error：{e}")
            self.click(
                self.element.common_page.drama_library,
                "进入剧库页面",
            )
            self.click_screenshot(
                self.element.common_page.navigation_back, "返回首页", "首页登录引导(保底)", screenshot_path, 2
            )
        with allure.step(f"覆盖{get_app_version()}安装新版本"):
            install_apk("/var/ftp/pub/short_tv_apk/android_QA/v2.0.10_支持自动化标识.apk")
            time.sleep(5)
            adb_shell("am start com.startshorts.androidplayer/.ui.activity.RoutingActivity")
            try:
                self.wait_element(self.element.common_page.skip, "点击Skip按钮").click()
            except Exception as e:
                logging.error(f"An error：{e}")
            for i in range(6):
                time.sleep(0.5)
                if self.wait_element(self.element.common_page.logo, "等待首页logo出现", 1) is None:
                    self.press_back_button()
                else:
                    break
            time.sleep(5)
            # 等待换位引导出现
            if self.wait_element(self.element.common_page.ok, "等待换位引导出现"):
                self.driver.save_screenshot(screenshot_path + "/reward换位置引导.png")
                self.click_screenshot(self.element.common_page.ok, "点击确定", "my list 换位置引导", screenshot_path, 2)
            else:
                # 切换tab的逻辑
                tab_elements = [
                    ('xpath',
                     f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[1]}"]'),
                    ('xpath',
                     f'//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="{self.get_tab_button()[0]}"]')
                ]

                for tab_element in tab_elements:
                    self.click(tab_element, "切换tab")
