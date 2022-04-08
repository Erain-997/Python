# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08
import time
import re


def sleep(seconds):
    time.sleep(seconds)


def string_re(data, sign=None):
    if sign is not None:
        return data[:data.find(sign)], int(data[data.rfind(sign):].replace(sign, ""))
    return data[:data.find("--")], int(data[data.rfind("--"):].replace("--", ""))


def is_chinese(string):
    """
    检查整个字符串是否包含中文
    :param string: 需要检查的字符串
    :return: bool
    """
    if string is None:
        return True
    for ch in string:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


def re_sign(data):
    item = re.findall(r'[^=]', data)
    item = ''.join(item)
    item = item.replace('[', '').replace(']', '')
    # 正则去除[]
    return item

