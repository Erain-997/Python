#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/8/13
# @Author  : zxp
import allure, json


class AllureMethod(object):
    """
    allure 相关方法封装
    """

    @classmethod
    def save_data(cls, url, request_data, response_data, name=None, headers_data=None, response_head=None):
        if name is not None:
            with allure.step("前置条件：%s" % name):
                pass
        if headers_data is not None:
            with allure.step("请求头参数：%s" % headers_data):
                pass
        with allure.step("请求地址：%s，请求参数：%s" % (url, request_data)):
            pass
        if response_head is not None:
            with allure.step("请求头返回值：%s" % response_head):
                pass
        with allure.step("返回值：%s" % response_data):
            pass

