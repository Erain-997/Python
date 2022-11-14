# _*_coding:utf-8_*_
# Author：Erain
# Time：2022/11/08
import os
import re
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

rows = 1


class DevicesInit(object):

    def get_devices(self):
        """
        获取设备序列号
        :return:
        """
        str_init = ' '
        all_info = os.popen('adb devices').readlines()
        for i in range(len(all_info)):
            str_init += all_info[i]
        devices_name = re.findall('\n(.+?)\t', str_init, re.S)
        return devices_name

    def device_connect(self, device_id):
        self.connect_dev = connect_device(
            "Android://127.0.0.1:5037/" + device_id + "?cap_method=JAVACAP&touch_method=adb")
        self.ui = AndroidUiautomationPoco(device=self.connect_dev, use_airtest_input=True,
                                          screenshot_each_action=False)
        return self.connect_dev, self.ui

    @classmethod
    def rows(cls):
        global rows
        rows += 1
        return rows

    @classmethod
    def get_resolution(cls):
        # 获取当前设备分辨率
        w, h = device().get_current_resolution()
        return (w, h)
