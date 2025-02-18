from common.utils.arg_parse_func import args


class AndroidCapabilities:
    """存储Android设备的capabilities"""

    def __init__(
            self,
            platform_name="Android",
            automation_name="uiautomator2",
            device_name="Android",
            udid="Android",
            app_package="com.android.settings",
            app_activity=".Settings",
            language="en",
            locale="US",
            no_reset="true",
            auto_grant_permissions="false",
    ):
        self.platformName = platform_name
        self.automationName = automation_name
        self.deviceName = device_name
        self.appPackage = app_package
        self.appActivity = app_activity
        self.language = language
        self.locale = locale
        self.noReset = no_reset
        self.udid = udid
        self.autoGrantPermissions = auto_grant_permissions

    def to_dict(self):
        """将capabilities转换为字典"""
        return {
            "platformName": self.platformName,
            "automationName": self.automationName,
            "deviceName": self.deviceName,
            "udid": self.udid,
            "appPackage": self.appPackage,
            "appActivity": self.appActivity,
            "language": self.language,
            "locale": self.locale,
            "appium:noReset": self.noReset,
            "appium:autoGrantPermissions": self.autoGrantPermissions,
            "appium:env": {'IS_APPIUM_TEST': 'true'},
        }


# 创建多个设备的capabilities
device_emulator_5554_capabilities = AndroidCapabilities(
    platform_name="Android",
    automation_name="uiautomator2",
    device_name="RZ8R70WST8E",
    app_package="com.startshorts.androidplayer",
    app_activity="com.startshorts.androidplayer.ui.activity.RoutingActivity",
    language="en",
    locale="US",
    no_reset="true",
).to_dict()

device2_capabilities = AndroidCapabilities(
    platform_name="Android",
    automation_name="uiautomator2",
    device_name=args.device,
    udid=args.device,
    app_package="com.startshorts.androidplayer",
    app_activity="com.startshorts.androidplayer.ui.activity.RoutingActivity",
    language="zh-Hans",
    locale="CN",
    no_reset="false",
    # auto_grant_permissions="true",  # 添加 autoGrantPermissions 参数
).to_dict()

# 将多个设备的capabilities存储在一个列表中
capabilities_list = [device_emulator_5554_capabilities, device2_capabilities]
