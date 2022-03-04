#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/8/13
# @Author  : zxp

import requests


class CaseMethod(object):
    """
    请求相关在此处定义
    """
    @classmethod
    def post(cls, url, request_data, data=None, **kwargs):
        if data is None:
            with requests.post(url, json=request_data, **kwargs) as resp:
                return resp
        else:
            with requests.post(url, data=data, **kwargs) as resp:
                return resp

    @classmethod
    def put(cls, url, data=None, **kwargs):
        with requests.put(url, data=data, **kwargs) as resp:
            return resp

    @classmethod
    def delete(cls, url, **kwargs):
        with requests.delete(url, **kwargs) as resp:
            return resp

    @classmethod
    def get(cls, url, params=None, **kwargs):
        with requests.get(url, params=params, **kwargs) as resp:
            return resp

    @classmethod
    def patch(cls, url, data=None, **kwargs):
        with requests.patch(url, data=data, **kwargs) as resp:
            return resp
