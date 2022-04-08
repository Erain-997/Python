#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/08/09
# @Author  : zxp
import traceback
import datetime
from internal.es_log import es, es_data
from api.common.common import *
from internal.ding import ding_exception_api

retry = 0


def except_output(added_value=None):
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
                print(traceback.format_exc())
                t = datetime.datetime.now().strftime('%m%d%H%M%S')
                snapshot(filename=project_directory() + f"/err{t}.png", msg="异常", quality=99)
                es.es_error(es_data(func.__name__, {}, "", traceback.format_exc()))
                ding_exception_api(e, e.__traceback__.tb_frame)
                text("^r")
                # sleep(600000)
                touch((500, 500))  # 开始游戏
                sleep(3)
                if added_value is not None:
                    added_value()

        return wrapper

    return except_func


def except_retry(added_value=None):
    def except_retry_func(func):
        """
        异常处理装饰器
        :param func:
        :return:
        """

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                global retry
                retry += 1
                if retry > 2:
                    if added_value is not None:
                        added_value()
                    return
                else:
                    print("执行重试", e)
                    return wrapper(*args, **kwargs)

        return wrapper

    return except_retry_func
