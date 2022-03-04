#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/08/09
# @Author  : zxp

from internal.ding import ding_exception_api


def except_output():
    def except_func(func):
        """
        异常处理装饰器
        :param func:
        :return:
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(e)
                print(e.__traceback__.tb_frame)
                # ding_exception_api(e,e.__traceback__.tb_frame)
        return wrapper
    return except_func
