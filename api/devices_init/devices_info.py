# _*_coding:utf-8_*_
# Author：Erain
# Time：2022/11/08
import os


class DevicesInfo(object):
    """
    todo 临时处理 后续看是走数据库还是配置
    """

    @classmethod
    def get_game_name(cls, package):
        if "vikingard" in package:
            return "维京"
        else:
            return "未知"

    @classmethod
    def get_device_info(cls, devices):
        if devices == "N5XVB20602000897":
            return "华为畅享Z(RAM_6GB)"
        elif devices == "69DDU16512002034":
            return "华为荣耀V8(6GB)"
        elif devices == "a1537257":
            return "红米Note8(RAM_4GB)"
        elif devices == "55858a25":
            return "oppo-A57((RAM_3GB))"
        elif devices == "MQM9X18B26G01803":
            return "华为畅玩7A((RAM_3GB))"
        elif devices == "acd9903f":
            return "vivo-Y85A(RAM_4GB)"
        elif devices == "0123456789ABCDEF":
            return "乐视手乐2((RAM_3GB))"
        elif devices == "5ENDU19A18001403":
            return "荣耀v20((RAM_6GB))"
        elif devices == "988a1b37534958595a":
            return "三星Galaxy8((RAM_3GB))"
        else:
            return "未知设备"
