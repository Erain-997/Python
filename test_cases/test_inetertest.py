#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/3/29
# @Author  : Erain

import pytest
import copy
import allure

from api.behavier.register_api import RegisterApi


@allure.feature("测试接口")
class TestRegister(RegisterApi):

    # @allure.story("测试登录接口")
    def test_demo_register_api(self):
        self.register_api(False)

    @allure.story("反向用例")
    @allure.title("{case_name}")
    # 对应api的请求数据和断言的列表放进来，就可以循环了
    # 测试数据生成，列表中每四个数据为一组，顺序为：头部参数，请求参数，预期结果，测试用例描述
    @pytest.mark.parametrize("header,request_data,expected,case_name", RegisterApi().data_generation())
    def test_register(self, header, request_data, expected, case_name):
        test_request_data = copy.deepcopy(request_data)
        # import json #调试用，查看具体包体
        # print(json.dumps(test_post_data))
        # 一定是headers=,不指定会报错
        resp_data = self.post(self.reg_url(), test_request_data, headers=header)
        self.save_data(url=self.reg_url(), request_data=test_request_data, response_data=resp_data.json(),
                       headers_data=header, name=("预期值：%s" % expected))

        # 断言结果
        self.compare_dict_result(expected, resp_data.json(), ignore=["data"])

    @pytest.mark.parametrize('exception_data', RegisterApi().exception_create_data())
    @allure.story("注册参数异常测试")
    def test_register_error(self, exception_data):
        """
        异常测试
        """
        # 数据处理，提高正确率和容错
        info_data = exception_data.pop(self.info)
        test_post_data = copy.deepcopy(exception_data)
        with self.post(self.reg_url(), test_post_data, headers={"Test": "123"}) as resp:
            self.save_data(url=self.reg_url(), request_data=test_post_data, response_data=resp.json(),
                           headers_data=self.register_header())
            # 先分类，再校验，模块化代码，提升可读性
            # 测试结果分类，已封装好的关键字
            code_0 = ["参数值随机: ['user']", "参数值随机: ['password']", "参数值为null: ['device_id']",
                      "参数值随机: ['device_id']", "参数缺失: ['device_type']", "参数值为空: ['device_type']",
                      "参数值为null: ['device_type']", "参数值随机: ['device_type']", "参数类型异常1: ['device_type']",
                      "参数类型异常2: ['device_type']", "参数类型异常3: ['device_type']"]
            code_501 = ["参数值为null: ['password']", "参数缺失: ['user']", "参数值为null: ['user']",
                        "参数类型异常1: ['user']", "参数类型异常2: ['user']", "参数类型异常3: ['user']",
                        "参数缺失: ['device_id']", "参数缺失: ['password']", "参数值为空: ['device_id']"]
            code_502 = ["参数值为空: ['user']"]
            code_504 = ["参数值为空: ['password']"]
            code_507 = ["参数类型异常1: ['password']",
                        "参数类型异常2: ['password']", "参数类型异常3: ['password']", "参数类型异常1: ['device_id']",
                        "参数类型异常2: ['device_id']", "参数类型异常3: ['device_id']"]
            # 若请求参数在result_1里就返回正确结果code_0,由于期望结果中有uid等多余参数，在返回结果时对比会出现错误
            # 此时可以使用ignore忽略掉某些字段(info："data"),进行对比，就会出现正常结果
            if info_data in code_0:
                self.compare_dict_result(self.code_0(), resp.json(), ignore=["data"])
            elif info_data in code_501:
                self.compare_dict_result(self.code_501(), resp.json(), ignore=["data"])
            elif info_data in code_502:
                self.compare_dict_result(self.code_502(), resp.json(), ignore=["data"])
            elif info_data in code_504:
                self.compare_dict_result(self.code_504(), resp.json(), ignore=["data"])
            elif info_data in code_507:
                self.compare_dict_result(self.code_507(), resp.json(), ignore=["data"])
            else:
                assert False, '使用异常的测试用例，请求【包同步】接口，断言失败，异常用例说明：%s，接口响应结果为：%s' % (info_data, resp.json())

    @pytest.mark.parametrize('exception_data', RegisterApi().data_0331())
    @allure.story("注册参数异常测试")
    def test_addproductmap_error(self, exception_data):
        info_data = exception_data.pop(self.info)
        post_data = copy.deepcopy(exception_data)
        with self.post("http://192.168.5.202:31928//backend/AddProductMap", post_data) as resp:
            self.save_data(url="http://192.168.5.202:31928//backend/AddProductMap", request_data=post_data,
                           response_data=resp.json())
            code_120_zh = ["参数缺失: ['app_key']", "参数值为空: ['app_key']", "参数值为null: ['app_key']", "参数缺失: ['products']",
                           "参数值为空: ['products']", "参数值为null: ['products']", "参数缺失: ['products'][0]",
                           "参数值为空: ['products'][0]", "参数缺失: ['products'][0]['cp_product_id']",
                           "参数值为空: ['products'][0]['cp_product_id']", "参数值为null: ['products'][0]['cp_product_id']",
                           "参数缺失: ['products'][0]['sp_product_id']", "参数值为空: ['products'][0]['sp_product_id']",
                           "参数值为null: ['products'][0]['sp_product_id']", "参数缺失: ['products'][0]['sp_currency']",
                           "参数值为空: ['products'][0]['sp_currency']", "参数值为null: ['products'][0]['sp_currency']",
                           "参数缺失: ['app_key']", "参数值为空: ['app_key']", "参数值为null: ['app_key']", "参数缺失: ['products']",
                           "参数值为空: ['products']", "参数值为null: ['products']", "参数缺失: ['products'][0]",
                           "参数值为空: ['products'][0]", "参数缺失: ['products'][0]['cp_product_id']",
                           "参数值为空: ['products'][0]['cp_product_id']", "参数值为null: ['products'][0]['cp_product_id']",
                           "参数缺失: ['products'][0]['sp_product_id']", "参数值为空: ['products'][0]['sp_product_id']",
                           "参数值为null: ['products'][0]['sp_product_id']", "参数缺失: ['products'][0]['sp_currency']",
                           "参数值为空: ['products'][0]['sp_currency']", "参数值为null: ['products'][0]['sp_currency']"]
            code_0 = ["参数值随机: ['app_key']", "参数值随机: ['products'][0]['cp_product_id']",
                      "参数值随机: ['products'][0]['sp_product_id']", "参数缺失: ['products'][0]['sp_amount']",
                      "参数值为null: ['products'][0]['sp_amount']", "参数值随机: ['products'][0]['sp_amount']",
                      "参数值随机: ['products'][0]['sp_currency']", "参数值随机: ['app_key']",
                      "参数值随机: ['products'][0]['cp_product_id']", "参数值随机: ['products'][0]['sp_product_id']",
                      "参数缺失: ['products'][0]['sp_amount']", "参数值为null: ['products'][0]['sp_amount']",
                      "参数值随机: ['products'][0]['sp_amount']", "参数值随机: ['products'][0]['sp_currency']"]
            code_120_en = ["参数类型异常1: ['app_key']", "参数类型异常2: ['app_key']", "参数类型异常3: ['app_key']",
                           "参数类型异常1: ['products']",
                           "参数类型异常2: ['products']", "参数类型异常3: ['products']", "参数类型异常1: ['products'][0]",
                           "参数类型异常2: ['products'][0]", "参数类型异常3: ['products'][0]",
                           "参数类型异常1: ['products'][0]['cp_product_id']", "参数类型异常2: ['products'][0]['cp_product_id']",
                           "参数类型异常3: ['products'][0]['cp_product_id']", "参数类型异常1: ['products'][0]['sp_product_id']",
                           "参数类型异常2: ['products'][0]['sp_product_id']", "参数类型异常3: ['products'][0]['sp_product_id']",
                           "参数类型异常1: ['products'][0]['sp_amount']", "参数类型异常2: ['products'][0]['sp_amount']",
                           "参数类型异常3: ['products'][0]['sp_amount']", "参数类型异常1: ['products'][0]['sp_currency']",
                           "参数类型异常2: ['products'][0]['sp_currency']", "参数类型异常3: ['products'][0]['sp_currency']",
                           "参数类型异常1: ['app_key']", "参数类型异常2: ['app_key']", "参数类型异常3: ['app_key']",
                           "参数类型异常1: ['products']",
                           "参数类型异常2: ['products']", "参数类型异常3: ['products']", "参数类型异常1: ['products'][0]",
                           "参数类型异常2: ['products'][0]", "参数类型异常3: ['products'][0]",
                           "参数类型异常1: ['products'][0]['cp_product_id']", "参数类型异常2: ['products'][0]['cp_product_id']",
                           "参数类型异常3: ['products'][0]['cp_product_id']", "参数类型异常1: ['products'][0]['sp_product_id']",
                           "参数类型异常2: ['products'][0]['sp_product_id']", "参数类型异常3: ['products'][0]['sp_product_id']",
                           "参数类型异常1: ['products'][0]['sp_amount']", "参数类型异常2: ['products'][0]['sp_amount']",
                           "参数类型异常3: ['products'][0]['sp_amount']", "参数类型异常1: ['products'][0]['sp_currency']",
                           "参数类型异常2: ['products'][0]['sp_currency']", "参数类型异常3: ['products'][0]['sp_currency']"]
            code_110 = ["参数值为null: ['products'][0]", "参数值为null: ['products'][0]"]
            if info_data in code_120_zh:
                assert_data = {"code": 120, "info": "\u53c2\u6570\u9519\u8bef"}
                assert resp.json() == assert_data, '断言失败！异常用例说明：%s，期望结果%s，实际接口响应结果为：%s' % (
                    info_data, assert_data, resp.json())
            elif info_data in code_0:
                assert_data = {"code": 0, "info": ""}
                assert resp.json() == assert_data, '断言失败！异常用例说明：%s，期望结果%s，实际接口响应结果为：%s' % (
                    info_data, assert_data, resp.json())
            elif info_data in code_120_en:
                assert_data = {"code": 120, "info": "Decode Fail"}
                assert resp.json() == assert_data, '断言失败！异常用例说明：%s，期望结果%s，实际接口响应结果为：%s' % (
                    info_data, assert_data, resp.json())
            elif info_data in code_110:
                assert_data = {"code": 110, "info": "Unknown Error"}
                assert resp.json() == assert_data, '断言失败！异常用例说明：%s，期望结果%s，实际接口响应结果为：%s' % (
                    info_data, assert_data, resp.json())
            else:
                assert False, '使用异常的测试用例，请求【包同步】接口，断言失败，异常用例说明：%s，接口响应结果为：%s' % (info_data, resp.json())
