#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/8/03
# @Author  : zxp
import time
import os
from .create_parameters import GetTestParams
from .allure_method import AllureMethod
from .case_method import CaseMethod

"""
*****************注意事项***********************
做为接口测试公共包,在修改已经实现方法时,要慎重,玩不得以不建议
进行修改,修改时应该考虑旧方法的兼容问题, 不然会导致旧方法的用
例产生报错信息,修改公共包前应与张晓平进行确认!
2020/08/03 挖的坑 o(╥﹏╥)o 
"""


class SmallTools(GetTestParams, AllureMethod, CaseMethod):
    """
    常规方法,添加时应注意该方法是否已经存在
    """

    @classmethod
    def get_date(cls):
        return time.strftime("%Y-%m-%d_%H:%M:%S")

    @classmethod
    def compare_dict(cls, original, reference, key_list, result):
        """
        字典比较
        :param original:
        :param reference:
        :param key_list:
        :param result:
        :return:
        """
        original_keys = []
        reference_keys = []
        original_keys = cls.get_dict_key(original, original_keys)
        reference_keys = cls.get_dict_key(reference, reference_keys)
        if len(key_list) != 0:
            for key in key_list:
                if key in original_keys and key in reference_keys:
                    if cls.get_dict_value(original, key) == cls.get_dict_value(reference, key):
                        if result is None:
                            assert True
                        else:
                            return True
                    else:
                        if result is None:
                            assert False, "%s 预期：%s，实际%s" % (
                                key, cls.get_dict_value(original, key), cls.get_dict_value(reference, key))
                        else:
                            return "%s 预期：%s，实际%s" % (
                                key, cls.get_dict_value(original, key), cls.get_dict_value(reference, key))
                else:
                    raise Exception('列表存在错误key', key, "\n", key_list)
        else:
            raise Exception('空列表')

    @classmethod
    def compare_dict_result(cls, original, reference, ignore=None, retain=None, result=None):
        """
        字典比对
        :param retain: 该参数为列表,只对比某些字段
        :param original:原始数据
        :param reference:预期数据
        :param ignore: 该参数为列表,忽略某些字段进行比较
        :param result: 是否在方法列断言
        """
        key_list = []
        key_list = cls.get_dict_key(original, key_list)
        if ignore is not None:
            for i in ignore:
                key_list.remove(i)
        if retain is not None:
            key_list = retain
        return cls.compare_dict(original, reference, key_list, result)

    @classmethod
    def get_dict_value(cls, dict_data, key_id):
        """
        提取字典值
        :param dict_data:被提取字典
        :param key_id: 键值
        :return:
        """
        for key in dict_data.keys():
            if key == key_id:
                return dict_data[key]
            if isinstance(dict_data[key], dict):
                value = cls.get_dict_value(dict_data[key], key_id)
                # 之前挖的坑,不判断 is not None 会导致 直接 return 会导致
                # 字典嵌套后的value 拿不到,考虑到兼容问题故只能以这种方式解决
                if value is not None:
                    return value
            if isinstance(dict_data[key], list):
                for i in dict_data[key]:
                    if isinstance(i, dict):
                        value = cls.get_dict_value(i, key_id)
                        if value is not None:
                            return value

    @classmethod
    def except_output(cls, finally_func=None):
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
                    if finally_func is not None:
                        finally_func()

            return wrapper

        return except_func

    @classmethod
    def get_dict_key(cls, dict_data, key_list):
        """
        提取字典key
        :param dict_data:被提取字典
        :param key_list: 键值
        :return:
        """
        for key in dict_data.keys():
            key_list.append(key)
            if isinstance(cls.get_dict_value(dict_data, key), dict):
                cls.get_dict_key(cls.get_dict_value(dict_data, key), key_list)
            if isinstance(cls.get_dict_value(dict_data, key), list):
                for i in cls.get_dict_value(dict_data, key):
                    if isinstance(i, dict):
                        cls.get_dict_key(i, key_list)

        return key_list

    @classmethod
    def project_directory(cls, path_file=__file__, split_path_list=None):
        """
        项目路径
        :param split_path_list: type list
        :param path_file:
        :return:
        """
        cur_path = os.path.abspath(os.path.dirname(path_file))
        if split_path_list is not None and type(split_path_list) is list:
            for i in split_path_list:
                path = cur_path.split(i)[0]
            return path
        return cur_path

    @classmethod
    def root_path(cls, path):
        """
        拼接项目路径
        :param path: os.path.dirname(__file__)
        :return:
        """
        cur_path = os.path.abspath(path)
        root_path = os.path.join(os.path.split(cur_path)[0],
                                 os.path.split(cur_path)[1]
                                 )
        return root_path
