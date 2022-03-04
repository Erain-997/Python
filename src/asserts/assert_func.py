#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/5/14
# @Author  : 2018248


# 对响应结果进行断言
from api.response_data.response_data import RegResp


class AssertMethod(RegResp):

    @classmethod
    def assert_demo(cls, resp):
        """
        断言正常获取验证码
        :param value:
        :param resp:
        :return:
        """
        assert resp[cls.code] == 0, "code预期：0，实际: %s" % resp[cls.code]
