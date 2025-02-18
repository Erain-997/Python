class RewardPage:
    def __init__(self):
        # 短剧模块按钮
        self.short_play_button = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="Shorts"]',
        ]
        # 右上角奖励图标按钮
        self.reward_icon_button = ["id", "com.startshorts.androidplayer:id/box_iv"]
        # 奖励预期
        self.reward_expect = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[1]",
        ]
        # 现在看广告
        self.look_button = ["id", "com.startshorts.androidplayer:id/watch_ad_button"]
        # 我的/奖励模块按钮
        self.reward_button = [
            "xpath",
            '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.startshorts.androidplayer:id/recycler_view"]/android.view.ViewGroup[1]',
        ]
        # 奖励模块/立即观看按钮
        self.watch_now_button = ["id", "com.startshorts.androidplayer:id/watch_ad_button"]
        # 双倍奖励按钮
        self.double_reward_button = ["id", "com.startshorts.androidplayer:id/check_in_tv"]
        # 双倍奖励断言
        self.double_reward_expect = ["id", "com.startshorts.androidplayer:id/bonus_value_tv"]
        # 关闭Watch Now
        self.cancel_button = [
            "id",
            "com.startshorts.androidplayer:id/close_iv",
        ]
        # 退出奖励模块
        self.back_reward = [
            "xpath",
            '//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/navigation_iv"]',
        ]
        # Bonus Record断言
        self.bonus_record = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/title_tv" and @text="Double Check-In"]',
        ]
        # 奖励币日期
        self.reward_coins_date = [
            "xpath",
            '(//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/time_tv"])[1]',
        ]
        # 观看按钮倒计时
        self.watch_time = ["id", "com.startshorts.androidplayer:id/check_in_tv"]


class MyPage:
    def __init__(self):
        # 跳过
        self.skip = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView",
        ]
        self.test_ad = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.TextView",
        ]
        # 我的
        self.my = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup[5]/android.widget.TextView",
        ]
        # 我的-我的钱包
        self.wallet = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[3]",
        ]
        # 我的-我的钱包-优惠
        self.discount = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView",
        ]
        # 我的-我的钱包-金币记录
        self.gold_records = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView",
        ]
        # 我的-我的钱包-奖励币记录
        self.reward_records = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView",
        ]
        # 我的-登录
        self.login_in = ["id", "com.startshorts.androidplayer:id/login_button"]
        # 我的-现在订阅
        self.subscribe_now = ["id", "com.startshorts.androidplayer:id/subscription_button_tv"]
        # 我的-充值
        self.top_up = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[8]",
        ]
        # 我的-奖励
        self.reward = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]",
        ]
        # 我的-奖励-签到提醒开关
        self.sign_switch = ["id", "com.startshorts.androidplayer:id/notification_switch_iv"]
        # 我的-反馈
        self.feedback = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView",
        ]
        # 我的-反馈弹窗
        self.feedback_text = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.TextView",
        ]
        # 我的-语言
        self.language = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView",
        ]
        # 我的-语言-英语
        self.english = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[1]",
        ]
        # 我的-设置
        self.setting = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[4]/android.widget.TextView",
        ]
        # 我的-钱包、充值、订阅、语言、设置-返回
        self.navigation_back = ["id", "com.startshorts.androidplayer:id/navigation_iv"]


class FoundPage:
    def __init__(self):
        # 发现
        self.found = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup[1]/android.widget.TextView",
        ]
        # 发现-搜索框
        self.search_box = ["id", "com.startshorts.androidplayer:id/search_label_tv"]
        # 返回
        self.back = ["id", "com.startshorts.androidplayer:id/back_iv"]
        # 发现-搜索框-输入
        self.input_search = ["id", "com.startshorts.androidplayer:id/search_label_edt"]
        # 发现-礼盒
        self.gift_box = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.view.ViewGroup[2]/android.view.ViewGroup/android.widget.ImageView",
        ]
        # 发现->
        self.more = ["id", "com.startshorts.androidplayer:id/more_iv"]
        # 发现->-返回   礼盒返回
        self.navigation_back = ["id", "com.startshorts.androidplayer:id/navigation_iv"]


class ShortsPage:
    def __init__(self):
        # 短剧
        self.shorts = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup[2]/android.widget.TextView",
        ]
        # 短剧-头像
        self.headshot = ["id", "com.startshorts.androidplayer:id/cover_iv"]
        # 短剧-沉浸页-头像
        self.shorts_headshot_stub = ["id", "com.startshorts.androidplayer:id/cover_viewstub"]
        # 短剧-收藏
        self.collect = ["id", "com.startshorts.androidplayer:id/collect_iv"]
        # 短剧-选集
        self.episodes = ["id", "com.startshorts.androidplayer:id/list_iv"]
        # 短剧-分享
        self.share = ["id", "com.startshorts.androidplayer:id/share_iv"]
        # 短剧-更多
        self.more = ["id", "com.startshorts.androidplayer:id/expand_viewstub"]
        # 短剧-观看全集
        self.trailer_tv = ["id", "com.startshorts.androidplayer:id/trailer_tv"]


class ChasingPage:
    def __init__(self):
        # 追剧
        self.chasing_dramas = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup[4]/android.widget.TextView",
        ]
        # 追剧-我的追剧
        self.my_followers = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView",
        ]
        # 追剧-最近播放
        self.recently_played = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView",
        ]
        # 追剧-编辑
        self.chasing_edit = ["id", "com.startshorts.androidplayer:id/edit_click_tv"]


class CommonPage:
    def __init__(self):
        # ended
        self.ended = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.app.Dialog",
        ]
        # 换位置弹窗确定
        self.ok = ["id", "com.startshorts.androidplayer:id/confirm_tv"]
        self.notify_logo = ["id", "com.startshorts.androidplayer:id/notify_logo_iv"]
        # 首页logo
        self.logo = ["id", "com.startshorts.androidplayer:id/logo_iv"]
        self.new_logo = ["id", "com.startshorts.androidplayer:id/logo_viewstub"]
        # 剧库
        self.drama_library = ["id", "com.startshorts.androidplayer:id/drama_library_iv"]
        # 首页文本
        self.home_test = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="Discover"]',
        ]
        # 广告
        self.act_resource = ["id", "com.startshorts.androidplayer:id/act_resource_iv"]
        # 系统通知-返回
        self.navigate_up = ["xpath", '//android.widget.ImageButton[@content-desc="Navigate up"]']
        self.later = ["id", "com.startshorts.androidplayer:id/later_tv"]
        # “画中画功能已上线”、“欢迎来到ShortMax”弹窗-关闭按钮
        self.close_iv = ["id", "com.startshorts.androidplayer:id/close_iv"]
        # 小窗播放按钮
        self.window = ("id", "com.startshorts.androidplayer:id/mini_window_viewstub")
        # 允许ShortMax向您发送通知？-图标
        self.allow_img = ["id", "com.android.permissioncontroller:id/permission_icon"]
        # 允许ShortMax向您发送通知？-允许
        self.allow = ["id", "com.android.permissioncontroller:id/permission_allow_button"]
        # 允许ShortMax向您发送通知？-不允许
        self.no_allow = ["id", "com.android.permissioncontroller:id/permission_deny_button"]
        # 获取大量奖金-取消
        self.cancel = ["id", "com.startshorts.androidplayer:id/later_button"]
        # 跳过
        self.skip = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/android.widget.TextView",
        ]
        self.test_ad = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.TextView",
        ]
        self.close_test_ad = [
            "xpath",
            "//android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.view.View/android.widget.Button",
        ]
        self.close_google_ad = [
            "xpath",
            "//android.webkit.WebView/android.view.View/android.view.View/android.view.View/android.view.View/android.view.View[2]/android.view.View/android.widget.Button",
        ]
        # 我的-我的钱包
        self.wallet = ["id", "com.startshorts.androidplayer:id/wallet_bg_view"]
        # 我的-我的钱包-优惠
        self.discount = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView",
        ]
        # 我的-我的钱包-金币记录
        self.gold_records = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView",
        ]
        # 我的-我的钱包-奖励币记录
        self.reward_records = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView",
        ]
        # 我的-登录
        self.login_in = ["id", "com.startshorts.androidplayer:id/login_button"]
        # 我的-现在订阅
        self.subscribe_now = ["id", "com.startshorts.androidplayer:id/subscription_button_tv"]
        # 标题：
        self.title = ["id", "com.startshorts.androidplayer:id/title_tv"]
        # 我的-充值-确认充值/我的-现在订阅-周卡-确定订阅
        self.cocnfirm_button = ["id", "com.startshorts.androidplayer:id/positive_button"]
        # 我的-金币数
        self.coins = ["id", "com.startshorts.androidplayer:id/coin_value_tv"]
        # 我的-奖励币数
        self.bonus = ["id", "com.startshorts.androidplayer:id/bonus_value_tv"]
        # 我的-充值
        self.top_up = [
            "xpath",
            "//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/android.widget.TextView[8]",
        ]
        # 我的-奖励
        self.reward = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]",
        ]
        # 我的-奖励-签到提醒开关
        self.sign_switch = ["id", "com.startshorts.androidplayer:id/notification_switch_iv"]
        # 我的-奖励-双倍奖励
        self.double_rewards = ["id", "com.startshorts.androidplayer:id/check_in_button_viewstub"]
        # 我的-反馈
        self.feedback = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView",
        ]
        # 我的-反馈弹窗
        self.feedback_text = ["id", "com.google.android.gm:id/welcome_tour_title"]
        # 我的-语言
        self.language = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView",
        ]
        # 我的-语言-英语
        self.english = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[1]",
        ]
        # 我的-语言-中文简体
        self.chinese_easy = [
            "xpath",
            "//android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView[1]",
        ]
        # 我的-设置
        self.settings = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.ScrollView/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[4]/android.widget.TextView",
        ]
        # 返回键
        self.navigation_back = ["id", "com.startshorts.androidplayer:id/navigation_iv"]
        # 取消Play Now按钮
        self.cancel_play_now = [
            "xpath",
            '//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/close_iv"]',
        ]

        # 设置-任务中心入口优化
        self.task_entry = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[13]",
        ]
        # 设置-任务中心入口优化-0:关闭
        self.shut_down = ["xpath", '//android.widget.TextView[@text="0:关闭"]']
        # 设置-批量解锁
        self.unlock_in_bulk = [
            "xpath",
            '//android.widget.TextView[contains(@text, "批量解锁")]',
        ]
        # 设置-批量解锁-实验值1
        self.unlock_inlet_one = ["xpath", '//android.widget.TextView[@text="1:实验值"]']
        # 设置-批量解锁-实验值2
        self.unlock_inlet_two = ["xpath", '//android.widget.TextView[@text="2:实验值"]']
        # 新人tab栏是否展示
        self.and_newuser = [
            "xpath",
            '//android.widget.TextView[contains(@text, "新人tab栏是否展示")]',
        ]
        # 1:展示
        self.show = ["xpath", '//android.widget.TextView[contains(@text, "1:展示")]']
        # 沉浸页支持小窗播放
        self.and_pip = [
            "xpath",
            '//android.widget.TextView[contains(@text, "沉浸页支持小窗播放")]',
        ]
        # 支持
        self.support = ["xpath", '//android.widget.TextView[contains(@text, "1:支持")]']
        # 解锁弹窗无广告解锁
        self.and_without = [
            "xpath",
            '//android.widget.TextView[contains(@text, "解锁弹窗无广告解锁")]',
        ]
        # 设置-解锁弹窗无广告解锁-实验值2
        self.and_without_one = ["xpath", '//android.widget.TextView[@text="1:纯付费+膨胀+广告挽留。"]']
        # 发现
        self.found = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup[1]/android.widget.TextView",
        ]
        # 发现-搜索框
        self.search_box = ["id", "com.startshorts.androidplayer:id/search_label_tv"]
        self.search_box_ar = ["id", "com.startshorts.androidplayer:id/view_pager_container"]
        # 分辨率
        self.resolution = ["id", "com.startshorts.androidplayer:id/play_resolution_tv"]
        # 返回
        self.back = ["id", "com.startshorts.androidplayer:id/back_iv"]
        # 发现-搜索框-输入
        self.input_search = ["id", "com.startshorts.androidplayer:id/search_label_edt"]
        # 发现-礼盒
        self.gift_box = [
            "id",
            "com.startshorts.androidplayer:id/box_iv",
        ]
        # 发现->
        self.more = ["id", "com.startshorts.androidplayer:id/more_iv"]

        # 短剧
        self.sketch = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup[2]/android.widget.TextView",
        ]
        # 短剧-广告关闭
        self.pop_ups = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View/android.view.View[1]/android.view.View/android.view.View[2]/android.view.View/android.widget.Button",
        ]
        # 沉浸页-头像
        self.headshot = ["id", "com.startshorts.androidplayer:id/cover_iv"]
        self.new_headshot = ["id", 'com.startshorts.androidplayer:id/cover_viewstub']
        # 沉浸页-收藏
        self.collect = ["id", "com.startshorts.androidplayer:id/collect_iv"]
        # 沉浸页-收藏-2.0.9
        self.new_collect = ["xpath",
                            '(//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/icon_iv"])[1]']
        # 沉浸页-选集
        # 沉浸页-选集
        self.episodes = [
            "id",
            "com.startshorts.androidplayer:id/list_iv",
        ]
        self.new_episodes = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[3]/android.widget.ImageView",
        ]
        # shorts-收藏
        self.shorts_collect = ["id", "com.startshorts.androidplayer:id/icon_iv"]
        # 添加到我的列表观看
        self.collect_tips = ("id", "com.startshorts.androidplayer:id/collect_tips_tv")
        # 收藏滑动条
        self.collect_progress = [
            "id",
            "com.startshorts.androidplayer:id/collect_tips_iv"
            ]
        # shorts-list
        self.shorts_list = [
            "xpath",
            "//android.view.ViewGroup[1]/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup[2]/android.widget.ImageView",
        ]
        # shorts-头像
        self.shorts_headshot = ["id", "com.startshorts.androidplayer:id/cover_view"]

        # 解锁所有剧集
        self.coins_unlock_all = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.view.View",
        ]
        # 短剧-分享
        self.share = ["id", "com.startshorts.androidplayer:id/share_iv"]

        # 追剧
        self.chasing_dramas = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="My List"]',
        ]
        # 追剧-我的追剧
        self.my_followers = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView",
        ]
        # 追剧-最近播放
        self.recently_played = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView",
        ]
        # 追剧-编辑
        self.chasing_edit = ["id", "com.startshorts.androidplayer:id/edit_click_tv"]
        # 全选
        self.select_all = ["id", "com.startshorts.androidplayer:id/select_all_tv"]
        # 拒绝通知权限/三星 13
        self.deny_notification_button = ["id", "com.android.permissioncontroller:id/permission_deny_button"]
        # 允许通知权限/三星 13
        self.notification_button = ["id", "com.android.permissioncontroller:id/permission_allow_button"]
        # 取消新人奖励按钮
        self.cancel_button = [
            "id",
            "com.startshorts.androidplayer:id/close_iv",
        ]
        # 取消更新按钮
        self.cancel_update_button = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/later_button"]',
        ]
        # 取消提示按钮
        self.cancel_tip_button = [
            "xpath",
            '//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/close_iv"]',
        ]
        # 关闭新人专享
        self.cancel_buy_button = [
            "id",
            "com.startshorts.androidplayer:id/navigation_iv",
        ]
        # 奖励模块/开启通知权限按钮
        self.open_notification_button = ["id", "com.startshorts.androidplayer:id/turn_on_button"]
        # 确定按钮
        self.confirm = ["id", "com.startshorts.androidplayer:id/confirm_button"]
        # 我的模块按钮
        self.my_button = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="Profile"]',
        ]
        # 我的模块按钮-多语言
        self.my_buttons = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv"]',
        ]
        # 我的文本
        self.my_button_text = [
            "xpath",
            "//android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.view.ViewGroup[4]/android.widget.TextView",
        ]
        # 新用户登录按钮
        self.login_button = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/app_name_tv"]',
        ]
        # 关闭开屏广告
        self.close_start_advertisements = ["xpath", '//android.view.View[@resource-id="close - button"]']
        # 关闭小窗播放
        self.close_small_window_button = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/start_tv"]',
        ]
        # 首页搜索
        self.index_search = [
            "xpath",
            '//android.widget.LinearLayout[@resource-id="com.startshorts.androidplayer:id/view_pager_container"]',
        ]
        # 搜索
        self.search = [
            "xpath",
            '//android.widget.EditText[@resource-id="com.startshorts.androidplayer:id/search_label_edt"]',
        ]

        # 设置模块
        # 任务中心入口优化按钮
        self.task_center_optimize_button = [
            "xpath",
            '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.startshorts.androidplayer:id/recycler_view"]/android.view.ViewGroup[11]',
        ]
        # 任务中心值 0
        self.task_center_optimize = [
            "xpath",
            '//android.widget.TextView[@resource-id="android:id/text1" and @text="0:关闭"]',
        ]
        # 任务中心补签模块
        self.task_center_supplementary_signature_button = [
            "xpath",
            '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.startshorts.androidplayer:id/recycler_view"]/android.view.ViewGroup[11]',
        ]
        # 任务中心补签模块/0关闭
        self.task_center_close_button = [
            "xpath",
            '//android.widget.TextView[@resource-id="android:id/text1" and @text="0:关闭"]',
        ]
        # 设置模块按钮
        self.settings_button = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv"]',
        ]
        # 设置模块按钮-多语言
        self.settings_buttons = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/name_tv"]',
        ]
        # 切换成新账号
        self.switch_new_button = ["xpath", '//android.widget.TextView[@text="切换成新账号"]']
        # 切换账号
        self.switch_button = ["xpath", '//android.widget.TextView[@resource-id="android:id/text1" and @text="切换:"]']
        # 卡顿必降档逻辑按钮
        self.stump_logic = [
            "xpath",
            '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.startshorts.androidplayer:id/recycler_view"]/android.view.ViewGroup[7]',
        ]
        # 开启降档
        self.open_stump = [
            "xpath",
            '//android.widget.TextView[@resource-id="android:id/text1" and @text="开启:触发卡顿后即使继续播放,也会走降档逻辑"]',
        ]
        # 首页模块按钮
        self.home_module_button = [
            "xpath",
            '(//android.view.View[@resource-id="com.startshorts.androidplayer:id/high_light_view"])[1]',
        ]
        # 首页模块文字
        self.home_module_text = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="Discover"]',
        ]
        # 视频加载等待提示
        self.video_loadings = [
            "xpath",
            '//android.widget.Toast[@text="The network is slow, the best quality has been selected for you."]',
        ]

        # 订阅模块按钮
        self.subscribe_button = [
            "id",
            "com.startshorts.androidplayer:id/subscription_button_tv",
        ]
        # 选择订阅
        self.subscribe_select = [
            "xpath",
            '(//android.view.View[@resource-id="com.startshorts.androidplayer:id/button_bg_view"])[1]',
        ]
        # 确定订阅按钮
        self.subscribe_confirm = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/positive_button"]',
        ]
        # 退出订阅模块按钮
        self.back_subscribe = [
            "id",
            "com.startshorts.androidplayer:id/navigation_iv",
        ]

        # 金币数量
        self.coin_number = ["id", "com.startshorts.androidplayer:id/coin_value_tv"]
        # 充值按钮
        self.recharge_button = ["xpath", '//android.widget.TextView[@text="Top Up"]']
        # 充值金币按钮
        self.recharge_coins_button = [
            "xpath",
            '(//android.view.View[@resource-id="com.startshorts.androidplayer:id/bg_view"])[3]',
        ]
        # 确认支付按钮
        self.confirm_payment = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/positive_button"]',
        ]
        # 充值页面/取消登录按钮
        self.cancel_login = [
            "id",
            "com.startshorts.androidplayer:id/close_iv",
        ]
        # 退出充值页面按钮
        self.cancel_recharge = [
            "xpath",
            '//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/navigation_iv"]',
        ]
        # AutomationTest 文本
        self.automation_test_text = ["id", "com.startshorts.androidplayer:id/title_tv"]
        # gmail的logo
        self.gmail_logo = ["id", "com.google.android.gm:id/gmail_logo"]

        # 谷歌广告 >
        self.google_back = ["xpath", "//android.widget.Button"]

        # Watch Ads, Earn bonus文本
        self.watch_ads_text = ["id", "com.startshorts.androidplayer:id/watch_ad_title_tv"]

        # 首页Search History文本
        self.search_history_text = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/title_tv" and @text="Search History"]',
        ]
        # 用户Uid
        self.user_uid = ["id", "com.startshorts.androidplayer:id/id_tv"]
        # 剧集简介
        self.introduction = ["id", "com.startshorts.androidplayer:id/top_tv"]
        # 剧集列表 tab
        self.tab = ["id", "com.startshorts.androidplayer:id/tab_view"]
        # 充值挽留弹窗标题
        self.retain_title = ["id", "com.startshorts.androidplayer:id/title_tv"]
        self.week_pro = ["id", "com.startshorts.androidplayer:id/first_recharge_tv"]
        # 奖励页面-获取奖励通知
        self.reward_notifications = [
            "xpath",
            "//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]",
        ]
        # 授权按钮
        self.authorize = ["id", "com.startshorts.androidplayer:id/turn_on_button"]
        # 奖励页面-绑定邮箱
        self.bind_email = [
            "xpath",
            "//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]",
        ]
        # 邮箱地址输入框
        self.email_address_edt = ["id", "com.startshorts.androidplayer:id/email_address_edt"]
        # 获取验证码
        self.get_code = ["id", "com.startshorts.androidplayer:id/get_code_button"]
        # 验证码输入框
        self.verify_otp_edt = ["id", "com.startshorts.androidplayer:id/verify_otp_edt"]
        # 奖励页面-绑定手机号
        self.bind_phone_number = [
            "xpath",
            "//androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[4]",
        ]
        # 区号
        self.phone_country_code = ["id", "com.startshorts.androidplayer:id/phone_country_code_tv"]
        # 手机号输入框
        self.phone_number_edt = ["id", "com.startshorts.androidplayer:id/phone_number_edt"]
        # 描述
        self.desc = ["id", "com.startshorts.androidplayer:id/desc_title_tv"]
        # 立即解锁
        self.unlock = ["id", "com.startshorts.androidplayer:id/unlock_tv"]
        # 看广告弹窗
        self.Ad_header = ["id", "com.startshorts.androidplayer:id/header_iv"]
        # 账户信息
        self.account_info = [
            "xpath",
            "//android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]",
        ]
        # 清空搜索框按钮
        self.clear_search_box = ["id", "com.startshorts.androidplayer:id/clear_iv"]
        # 折扣 93% Off
        self.discount = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/discount_content_tv" and contains(@text, "92")]',
        ]
        # 预约剧
        self.remind_me = ["id", "com.startshorts.androidplayer:id/coming_soon_cp"]
        # 订阅模块/图标
        self.subscribe_icon = [
            "id",
            "com.startshorts.androidplayer:id/flag_iv",
        ]
        # 尊享弹窗图标
        self.gift = ["id", "com.startshorts.androidplayer:id/gift_iv"]
        # 新人充值h5页面-第一个
        self.h5_1 = [
            "xpath",
            "//androidx.viewpager.widget.ViewPager/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.webkit.WebView/android.webkit.WebView/android.view.View[1]/android.view.View[1]",
        ]
        self.min_window = [
            "id",
            'com.google.android.googlequicksearchbox:id/googleapp_search_widget_ghost_google_logo',
        ]
        # 1.5倍播放元素
        self.play_x5 = [
            "id",
            'com.startshorts.androidplayer:id/speed_tips_tv',
        ]
        # 选集按钮文本元素
        self.episode_button = (
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/text_tv"]',
        )
        self.play_x5 = ["id", 'com.startshorts.androidplayer:id/speed_tips_tv']
        self.retry_button = ["id", 'com.startshorts.androidplayer:id/retry_button']
        self.look_advertisement = ["id", 'com.startshorts.androidplayer:id/content_tv']
        # 唤起连续观看广告挽留弹窗
        self.look_advertisement_pop = ["id", 'com.startshorts.androidplayer:id/title2_tv']
        # 首页资源位弹窗剧
        self.act_bottom_float_resource_iv = ["id", 'com.startshorts.androidplayer:id/act_bottom_float_resource_iv']


class AdvertisementPage:
    def __init__(self):
        # 取消新页面
        self.cancel_new_page = [
            "xpath",
            '//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/close_iv"]',
        ]
        # 我的模块按钮
        self.my_button = [
            "xpath",
            '(//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/tab_iv"])[5]',
        ]
        # 设置模块按钮
        self.settings_button = [
            "xpath",
            '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.startshorts.androidplayer:id/recycler_view"]/android.view.ViewGroup[4]',
        ]
        # 影视详情 AutomationTest
        self.video_detail = [
            "xpath",
            '//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/cover_iv"]',
        ]

        # 首页开屏广告
        self.advertisement = ["xpath", '//android.widget.TextView[@text="Test Ad"]']
        # 原生广告元素
        self.native_advertisement = ["id", "com.startshorts.androidplayer:id/cta_tv"]
        # 拒绝通知权限/三星 13
        self.deny_notification_button = ["id", "com.android.permissioncontroller:id/permission_deny_button"]
        # 允许通知权限/三星 13
        self.notification_button = ["id", "com.android.permissioncontroller:id/permission_allow_button"]
        # 取消新人奖励按钮
        self.cancel_button = ["id", "com.startshorts.androidplayer:id/close_iv"]
        # 取消更新按钮
        self.cancel_update_button = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/later_button"]',
        ]
        # 关闭开屏广告按钮
        self.close_start_advertisement = ["xpath", '//android.view.View[@class="android.view.View"]']
        # expect
        self.video_message = ["xpath", '//android.widget.Toast[@text="Swipe to switch"]']
        # 首页模块按钮
        self.home_module_button = [
            "xpath",
            '(//android.view.View[@resource-id="com.startshorts.androidplayer:id/high_light_view"])[1]',
        ]
        # Shorts
        self.shorts = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/tab_tv" and @text="Shorts"]',
        ]
        # 右上角礼包
        self.gift_button = ["id", "com.startshorts.androidplayer:id/box_iv"]
        # 关闭折扣页面
        self.close_discount = ["id", "com.startshorts.androidplayer:id/close_iv"]
        # 剧集list列表文本
        self.drama_list_text = ["id", "com.startshorts.androidplayer:id/list_tv"]
        # 谷歌广告Skip
        self.skip_google = ["xpath", '//android.widget.TextView[@text="Skip video"]']
        # 谷歌广告Close
        self.close_google = ["xpath", '//android.widget.TextView[@text="Close and continue to app"]']
        # 观看激励视频1
        self.watch_reward_video_1 = ["id", "com.startshorts.androidplayer:id/watch_button"]
        # 观看激励视频2
        self.watch_reward_video_2 = ["id", "com.startshorts.androidplayer:id/watch_button"]
        # Coins Store文本
        self.coins_store_text = ["id", "com.startshorts.androidplayer:id/coin_store_tv"]
        # Privileges not activated?
        self.privileges_text = ["id", "com.startshorts.androidplayer:id/restore_tip_tv"]

        # 插屏广告元素
        self.interstitial_advertisement = ["id", "com.startshorts.androidplayer:id/content_layout"]
        # 获取奖励币元素_test_advertisement_14
        self.a = ["xpath", '(//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/amount_tv"])[1]']
        self.b = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/amount_tv" and @text="+10"]',
        ]
        self.c = [
            "xpath",
            '(//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/amount_tv"])[3]',
        ]
        self.d = [
            "xpath",
            '(//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/amount_tv"])[4]',
        ]
        self.e = [
            "xpath",
            '(//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/amount_tv"])[5]',
        ]
        self.f = [
            "xpath",
            '(//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/amount_tv"])[6]',
        ]
        self.g = [
            "xpath",
            '(//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/amount_tv"])[7]',
        ]


class DramaPage:
    def __init__(self):
        # 影视详情
        self.video_detail = [
            "xpath",
            '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.startshorts.androidplayer:id/recycler_view"]/android.view.ViewGroup/android.widget.ImageView[3]',
        ]
        # 影视详情列表
        self.video_detail_list = [
            "xpath",
            '//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/list_iv" and @text="选集"]',
        ]
        # 影视详情列表 2.0.5
        self.video_detail_list_1 = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/text_tv" and @text="选集"]',
        ]
        # 剧情解锁
        self.unlock_dramas = [
            "xpath",
            '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.startshorts.androidplayer:id/recycler_view"]/android.view.ViewGroup[2]',
        ]
        # 广告解锁
        self.advertisement_unlock = [
            "id",
            "com.startshorts.androidplayer:id/title_tv",
        ]
        # 沉浸页/取消登录
        self.close_login = [
            "xpath",
            '//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/close_iv"]',
        ]
        # 广告解锁预期断言
        self.desc_tv = [
            "id",
            "com.startshorts.androidplayer:id/desc_tv",
        ]
        self.unlock_dramas_new = [
            "xpath",
            '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.startshorts.androidplayer:id/recycler_view"]/android.view.ViewGroup[1]',
        ]
        # 解锁剧情提示信息
        self.unlock_dramas_message = [
            "xpath",
            '//android.widget.Toast[@text="Please unlock the previous episode first"]',
        ]
        # 剧情解锁——4
        self.unlock_dramas_04 = [
            "xpath",
            '//android.widget.TextView[@text="4"]',
        ]
        # 重新进入付费卡点 剧情解锁——4
        self.unlock_drama_04 = [
            "id",
            "com.startshorts.androidplayer:id/unlock_tv",
        ]
        # 剧情解锁——5
        self.unlock_dramas_05 = [
            "xpath",
            '//android.widget.TextView[@text="5"]',
        ]
        # 跳过广告
        self.skip_advertisement = ["xpath", '//android.widget.TextView[@text="Skip"]']
        # 开屏广告
        self.advertisement_loading = ["xpath", '//android.widget.TextView[@text="Test Ad"]']
        self.advertisement_02 = ["xpath", '//android.widget.TextView[@text="Learn More"]']
        # play_video
        self.play_video = [
            "xpath",
            '//android.widget.FrameLayout[@resource-id="com.startshorts.androidplayer:id/play_layout"]',
        ]
        # Coins
        self.advertisement_unlock_number = [
            "xpath",
            '//android.widget.TextView[@text="Free Unlock"]',
        ]

        # 进度条文本
        self.progress_text = ["id", "com.startshorts.androidplayer:id/current_time_tv"]
        # 我的-充值-充值1
        self.top_up_one = [
            "xpath",
            "//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]",
        ]
        # 正在播放集数
        self.episode_num = ["id", "com.startshorts.androidplayer:id/episode_num_tv"]
        # 短剧-选集-第二集
        self.two_episodes = ["xpath", '//android.widget.TextView[@text="2"]']
        # 短剧-选集-第三集
        self.there_episodes = ["xpath", '//android.widget.TextView[@text="3"]']
        # 短剧-选集-第四集
        self.four_episodes = ["xpath", '//android.widget.TextView[@text="4"]']
        # 短剧-选集-第5集
        self.five_episodes = ["xpath", '//android.widget.TextView[@text="5"]']
        # 短剧-选集-第七集
        self.seven_episodes = ["xpath", '//android.widget.TextView[@text="7"]']
        # 短剧-选集-26-30
        self.twenty_six_thirty = ["xpath", '//android.widget.TextView[@text="26-30"]']
        # 短剧-选集-30
        self.thirty = ["xpath", '//android.widget.TextView[@text="30"]']
        # 短剧-选集-12
        self.twelve = ["xpath", '//android.widget.TextView[@text="12"]']
        # 广告AD文本
        self.advertisement_text = ["id", "com.startshorts.androidplayer:id/flag_view"]
        # 自动解锁按钮
        self.auto_unlock_episode = ["id", "com.startshorts.androidplayer:id/auto_unlock_episode_iv"]
        # Coins Store
        self.coin_store = [
            "id",
            "com.startshorts.androidplayer:id/coin_store_tv",
        ]
        # Store页面标题上方横线
        self.slide = ["id", "com.startshorts.androidplayer:id/slide_view"]
        # coins Store页面膨胀商品
        self.store_sku = ["id", "com.startshorts.androidplayer:id/body_view"]
        # 解锁第4集提示
        self.unlock_four_hint = ["xpath", '//android.widget.Toast[@text="We have unlocked episode 4 for you"]']
        # 批量解锁2集提示
        self.unlocks_two_hint = ["xpath", '//android.widget.Toast[@text="2 episodes have been unlocked in batches"]']
        # 批量解锁5集提示
        self.unlocks_five_hint = ["xpath", '//android.widget.Toast[@text="5 episodes have been unlocked in batches"]']
        # 批量解锁所有剧集提示ab-2
        self.unlocks_all_hint_two = [
            "xpath",
            '//android.widget.Toast[@text="27 episodes have been unlocked in batches"]',
        ]
        # 批量解锁所有剧集提示ab-1
        self.unlocks_all_hint_one = [
            "xpath",
            '//android.widget.Toast[@text="18 episodes have been unlocked in batches"]',
        ]
        # 批量解锁10集提示
        self.unlocks_ten_hint = ["xpath", '//android.widget.Toast[@text="10 episodes have been unlocked in batches"]']
        # 解锁到-5集
        self.unlock_five = [
            "xpath",
            "//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.TextView[4]",
        ]
        # 解锁到-8集
        self.unlock_eight = [
            "xpath",
            "//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.TextView[7]",
        ]
        # 解锁到-13集
        self.unlock_thirteen = [
            "xpath",
            "//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.widget.TextView[12]",
        ]
        # 播放最后一集集数
        self.last_episode = ["xpath", "//android.widget.TextView[@text='EP.30']"]


class TopUpPage:
    def __init__(self):
        # Extra 20% Bonus offered
        self.extra = ["xpath", "//android.widget.TextView[@text='Extra 20% Bonus offered']"]
        # 我的-充值-充值1-7
        self.top_up_one = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="340 Coins"]',
        ]
        self.top_up_two = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and  @text="1500 Coins"]',
        ]
        self.top_up_three = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and  @text="500 Coins"]',
        ]
        self.top_up_four = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and  @text="5000 Coins"]',
        ]
        self.top_up_five = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="2500 Coins"]',
        ]
        self.top_up_six = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="4000 Coins"]',
        ]
        self.top_up_seven = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="12000 Coins"]',
        ]
        # 短剧-选集-解锁选项
        self.one_top_up = [
            "xpath",
            "//android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]",
        ]
        self.two_top_up = [
            "xpath",
            "//android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]",
        ]
        self.three_top_up = [
            "xpath",
            "//android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView[2]",
        ]
        self.four_top_up = [
            "xpath",
            "//android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[4]/android.widget.TextView[2]",
        ]
        self.five_top_up = [
            "xpath",
            "//android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[4]/android.widget.TextView[2]",
        ]
        self.a1 = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="70 Coins"]',
        ]

        self.bonus1 = [
            "id",
            "com.startshorts.androidplayer:id/bonus_tv",
        ]

        self.bonus_text = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/bonus_viewstub"]',
        ]

        self.bonus2 = [
            "xpath",
            '//android.widget.TextView[@text="+100 Bonus"]',
        ]
        self.bonus3 = [
            "xpath",
            '//android.widget.TextView[@text="+100 Bonus"]',
        ]
        self.bonus4 = [
            "xpath",
            '//android.widget.TextView[@text="+300 Bonus"]',
        ]
        self.bonus5 = [
            "xpath",
            '//android.widget.TextView[@text="+100 Bonus"]',
        ]
        self.bonus6 = [
            "xpath",
            '//android.widget.TextView[@text="+200 Bonus"]',
        ]
        self.bonus7 = [
            "xpath",
            '//android.widget.TextView[@text="+300 Bonus"]',
        ]
        self.bonus_sku = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/bonus_viewstub" and @text="+10000 Bonus"]',
        ]

        # 膨胀商品
        self.coin_store = [
            "xpath",
            '//android.widget.TextView[@text="7000 Coins"]',
        ]

        # 充值页面膨胀商品
        self.coin_store_one = [
            "xpath",
            '//android.widget.TextView[@text="$34.99"])',
        ]

        # 340 coins 选项
        self.three_hundred_forty = ["xpath", '//android.widget.TextView[@text="340 Coins"]']
        # 消费时间
        self.consume_time = ["id", "com.startshorts.androidplayer:id/time_tv"]
        # 记录第一条
        self.amount = ["id", "com.startshorts.androidplayer:id/amount_tv"]
        # 记录第一条
        self.amount_one = [
            "xpath",
            "//android.widget.FrameLayout/android.widget.RelativeLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[3]",
        ]
        # 记录第二条
        self.amount_two = [
            "xpath",
            "//android.widget.FrameLayout/android.widget.RelativeLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[3]",
        ]
        # 膨胀sku的百分比
        self.sku_ratio = [
            "xpath",
            "//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[1]",
        ]
        # 膨胀sku的金币值
        self.sku_coins = [
            "xpath",
            "//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[3]",
        ]
        # 膨胀sku的奖励币值
        self.sku_bonus = [
            "xpath",
            "//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[4]",
        ]
        # 膨胀sku的充值金额
        self.sku_price = [
            "xpath",
            "//android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[5]",
        ]
        # 【Refresh】
        self.refresh = ["id", "com.startshorts.androidplayer:id/restore_tv"]
        # 掉单测试
        self.negative_button = ["id", "com.startshorts.androidplayer:id/negative_button"]
        # 补单成功通知
        self.repair_order = ["xpath", "/hierarchy/android.widget.FrameLayout/android.view.ViewGroup"]
        # 恢复购买
        self.restore = [
            "xpath",
            "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.TextView[2]",
        ]
        # 充值挽留弹窗-【$34.99】按钮（购买按钮）
        self.purchase_button = ["id", "com.startshorts.androidplayer:id/purchase_button"]
        # 【Unlock now】按钮
        self.unlock_now = ["id", "com.startshorts.androidplayer:id/unlock_iv"]
        # 7000 coins
        self.seven_thousand = ["xpath", "//android.widget.TextView[@text='7000 Coins']"]
        # A1位置sku商品
        self.a1_sku = ["xpath", '(//android.view.View[@resource-id="com.startshorts.androidplayer:id/bg_view"])[1]']
        # B1位置sku商品
        self.b1_sku = ["xpath", '(//android.view.View[@resource-id="com.startshorts.androidplayer:id/bg_view"])[2]']
        # B2位置sku商品
        self.b2_sku = ["xpath", '(//android.view.View[@resource-id="com.startshorts.androidplayer:id/bg_view"])[3]']
        # B3位置sku商品
        self.b3_sku = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="5000 Coins"]',
        ]
        # B4位置sku商品
        self.b4_sku = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="2500 Coins"]',
        ]
        # B5位置sku商品
        self.b5_sku = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="4000 Coins"]',
        ]
        # B6位置sku商品
        self.b6_sku = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="12000 Coins"]',
        ]
        # 膨胀商品
        self.sku_inflation = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and @text="7000 Coins"]',
        ]
        # Coins store 340 coins
        self.store_one = [
            "xpath",
            "//android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.TextView[2]",
        ]
        self.top_up_one2 = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and contains(@text, "340")]',
        ]
        self.top_up_400 = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv" and contains(@text, "400")]',
        ]

        self.coins_text = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/coin_tv"]',
        ]

        self.top_up_sku = [
            "id",
            "com.startshorts.androidplayer:id/header_view",
        ]


class SubscribePage:
    def __init__(self):
        self.week = ["xpath", "//android.widget.TextView[@text='Annual Pass']"]
        # 我的-现在订阅-订阅
        self.week_package = [
            "xpath",
            '(//android.view.View[@resource-id="com.startshorts.androidplayer:id/button_bg_view"])[2]',
        ]
        # 分辨率
        self.resolution = ["id", "com.startshorts.androidplayer:id/play_resolution_tv"]
        self.new_resolution = ["id", "com.startshorts.androidplayer:id/resolution_tv"]
        # 周卡pro名称
        self.weekly_pro = ["xpath", "//android.widget.TextView[@text='周卡Pro']"]
        # 月卡pro名称
        self.monthly_pro = ["xpath", "//android.widget.TextView[@text='Monthly Pass Pro']"]
        # 年卡pro名称
        self.annual_pro = ["xpath", "//android.widget.TextView[@text='Annual Pass Pro']"]
        # 订阅月卡
        self.monthly = ["xpath", '//android.widget.TextView[@text="Monthly Pass"]']
        # 订阅周卡
        self.weekly = ["xpath", '//android.widget.TextView[@text="Weekly Pass"]']
        # 订阅年卡
        self.annual = ["xpath", '//android.widget.TextView[@text="Annual Pass"]']
        # Subscribed文本
        self.subscribed_text = ["id", "com.startshorts.androidplayer:id/subscribed_tv"]
        # 查看bonus记录
        self.bonus_records = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/title_tv"]',
        ]
        self.subscribe_goods = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/card_name_tv"]',
        ]

        # Top Up 模块
        self.top_up = ["xpath", '//android.widget.TextView[@class="android.widget.TextView"]']
        # 订阅周卡Pro
        # self.weekly_pro = ["id", "com.startshorts.androidplayer:id/card_name_tv"]
        # # 订阅月卡Pro
        # self.monthly_pro = ["id", "com.startshorts.androidplayer:id/current_price_tv"]
        # 订阅年卡Pro
        self.annual_pro = ["id", "com.startshorts.androidplayer:id/current_price_tv"]


class ImmersionPage:
    def __init__(self):
        # 短剧名称
        self.shorts_name = ["id", "com.startshorts.androidplayer:id/shorts_name_tv"]
        # 分辨率480p
        self.resolution_a = ["xpath", "//android.widget.TextView[@text='480p']"]
        # 分辨率1080p
        self.resolution_b = ["xpath", "//android.widget.TextView[@text='1080p']"]
        # 播放速度
        self.play_speed = ["id", "com.startshorts.androidplayer:id/play_speed_tv"]
        self.new_play_speed = ["id", "com.startshorts.androidplayer:id/play_speed_viewstub"]
        # 0.5x   o.5倍速
        self.half_speed = ["xpath", "//android.widget.TextView[@text='0.5X']"]
        # 进度条
        self.seekbar_line = ["id", "com.startshorts.androidplayer:id/seekbar"]
        self.new_seekbar_line = ["id", "com.startshorts.androidplayer:id/seekbar_viewstub"]
        # shorts页面进度条
        self.shorts_seekbar_line = ["id", "com.startshorts.androidplayer:id/seek_bar_viewstub"]
        # 编辑
        self.edit = ["id", "com.startshorts.androidplayer:id/edit_iv"]
        # 删除
        self.delete = ["id", "com.startshorts.androidplayer:id/delete_tv"]
        # 返回首页按钮
        self.go_home_button = ["id", "com.startshorts.androidplayer:id/go_home_button"]
        # shorts页面下方剧集条
        self.episode_num_view = ["id", "com.startshorts.androidplayer:id/episode_num_view"]
        # 剧集状态
        self.episode_status = ["id", "com.startshorts.androidplayer:id/status_tv"]
        # 唤起选集列表
        self.slide = ["id", "com.startshorts.androidplayer:id/slide_view"]
        # 分级信息文本
        self.classification_text = ["id", "com.startshorts.androidplayer:id/content_desc_tv"]
        # 分级信息
        self.classification = ["id", "com.startshorts.androidplayer:id/short_rating_view"]


class AutomaticUnlockPage:
    def __init__(self):
        # 自动解锁开关
        self.auto_unlock_switch = ["xpath",
                                   '(//android.widget.ImageView[@resource-id="com.startshorts.androidplayer:id/status_iv"])[1]']
        # 自动解锁按钮
        self.auto_unlock_episode = ["id", "com.startshorts.androidplayer:id/auto_unlock_episode_iv"]
        # 充值挽留提示框按钮
        self.purchase_button = ["id", "com.startshorts.androidplayer:id/purchase_button"]
        # 【Coins Store】按钮
        self.coins_store = ["id", "com.startshorts.androidplayer:id/coin_store_tv"]
        # 广告解锁剧集
        self.free_unlock = [
            "xpath",
            "//android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.TextView",
        ]
        # 断言正在播放集数-4集
        self.four_episode = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/episode_num_tv" and contains(@text, "4")]',
        ]


class RedeemCodesPage:
    def __init__(self):
        # My List上的红点
        self.red_point = ["id", "com.startshorts.androidplayer:id/red_point_view"]
        # Play New上的红点
        self.red_point1 = ["id", "com.startshorts.androidplayer:id/red_circle_iv"]
        # 搜索图标
        self.search_iv = ["id", "com.startshorts.androidplayer:id/search_iv"]
        # 金币/奖励币记录为空图标
        self.empty_iv = ["id", "com.startshorts.androidplayer:id/empty_iv"]
        # 已领取按钮
        self.received = ["id", "com.startshorts.androidplayer:id/receive_tv"]
        # 搜索历史的删除图标
        self.history_clear_iv = ["id", "com.startshorts.androidplayer:id/history_clear_iv"]
        # Redemption code does not exist文本
        self.code_does_not_exist = [
            "xpath",
            '//android.widget.Toast[ @ text = "Redemption code does not exist"]',
        ]
        # No Record For Now文本
        self.no_record_for_now = [
            "xpath",
            '//android.widget.TextView[@text="No Record For Now"]',
        ]
        # toast 文本
        self.toast_text = [
            "xpath",
            '//android.widget.Toast[@class="android.widget.Toast"]',
        ]
        # toast1 文本
        self.toast1_text = [
            "xpath",
            '//android.widget.Toast[@text="The redemption code has expired"]',
        ]
        # 首页search 文本
        self.search_text = [
            "xpath",
            '//android.widget.TextView[@resource-id="com.startshorts.androidplayer:id/title_tv" and @text="vl5fb"]',
        ]
        # 搜索频繁 toast文本
        self.search_frequently_text = [
            "xpath",
            '//android.widget.Toast[@text="Search frequency is too high, please try again later"]',
        ]


class ResolutionPage:
    def __init__(self):
        # 1080p限免
        self.resolution_1080p = ["id", "com.startshorts.androidplayer:id/tip_tv"]
        # Switched文本
        self.resolution_switch_text = ["xpath", '//android.widget.Toast[@text="Switched to 1080p"]']
        # 1080p vip
        self.resolution_1080p_vip = [
            "xpath",
            '//androidx.recyclerview.widget.RecyclerView[@resource-id="com.startshorts.androidplayer:id/play_resolution_view"]',
        ]


class ShortTvElements:
    def __init__(self):
        self.drama_page = DramaPage()
        self.top_up_page = TopUpPage()
        self.subscribe_page = SubscribePage()
        self.common_page = CommonPage()
        self.advertisement_page = AdvertisementPage()
        self.chasing_page = ChasingPage()
        self.shorts_page = ShortsPage()
        self.found_page = FoundPage()
        self.my_page = MyPage()
        self.reward_page = RewardPage()
        self.immersion_page = ImmersionPage()
        self.automatic_unlock_page = AutomaticUnlockPage()
        self.redeem_codes_page = RedeemCodesPage()
        self.resolution_page = ResolutionPage()


if __name__ == "__main__":
    a = ShortTvElements()
    print(a.common_page.coins_unlock_all)
