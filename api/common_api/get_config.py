# _*_coding:utf-8_*_
# Author：Erain
# Time：2022/11/08
import configparser


def get_cfg_data(file_path, key=None, section='config'):
    config = configparser.ConfigParser()
    config.read(file_path)
    if key is None:
        return config.options(section)
    elif key in config.options(section):
        return config.get(section, key)
    return "key not found"
