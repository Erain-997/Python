#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2020/08/13
# @Author  : zxp

import json, time, os, pytest
import shutil


class Output(object):
    """
    调用run_case()类方法进行用例的执行已经报告的输出
    """

    @classmethod
    def file_path(cls, root_path):
        cls.file_json = os.path.join(root_path,
                                     "report",
                                     "allure-reports",
                                     "data",
                                     "categories.json"
                                     )
        return cls.file_json

    @classmethod
    def summary_file(cls, root_path):
        cls.summary_file = os.path.join(root_path,
                                        "report",
                                        "allure-reports",
                                        "widgets",
                                        "summary.json"
                                        )
        cls.create_time = time.strftime("%Y-%m-%d_%H:%M:%S")
        return cls.summary_file

    @classmethod
    def result_data(cls, root_path):
        """
        判断成功or失败
        :return:
        """
        exists = os.path.exists((os.path.join(root_path,
                                              "report",
                                              "allure-reports"
                                              )))
        if exists is True:
            json_file = open(cls.file_path(root_path), encoding='utf-8')
            setting = json.load(json_file)
            data = setting['children']
            summary_data = open(cls.summary_file(root_path), encoding='utf-8')
            setting = json.load(summary_data)
            run_time = str(setting['time']['start'])
            if data is []:
                with open(root_path + '//result.txt', 'w') as result:
                    result.write('Pass''\r\n''File creation time: ')
                    result.write(time.strftime("%Y-%m-%d_%H:%M:%S"))
                    result.write('\r\n')
                    result.write(run_time)
        else:
            raise ValueError('allure静态文件不存在')

    @classmethod
    def run_case(cls, root_path, cpu='auto', case_path=None, limited_time=30, report_path=None):
        """
         --dist=loadscope
        将按照同一个模块module下的函数和同一个测试类class下的方法来分组，然后将每个测试组发给可以执行的worker，确保同一个组的测试用例在同一个进程中执行
        目前无法自定义分组，按类class分组优先于按模块module分组
         --dist=loadfile
        按照同一个文件名来分组，然后将每个测试组发给可以执行的worker，确保同一个组的测试用例在同一个进程中执行
        :param case_path: 指定用例路径参数；
        例：Output.run_case(rootPath, cpu="4", case_path='/compatible_version/test_alter_523mail.py')
         或 Output.run_case(rootPath, cpu="4", case_path='/compatible_version）
        :param root_path:
        :param limited_time: 默认30秒超时
        :param report_path: 测试报告生成地址，示例："F:\\report"
        :param cpu: 核数
        :return:
        """
        if report_path is None:
            report_path = root_path + '/report'
        allure_path = report_path + '/allure-reports'
        report_path = report_path + '/report'
        try:
            shutil.rmtree(root_path + '/report/report')
        except Exception:
            pass
        file_path = '/test_cases'
        if case_path is not None:
            file_path += case_path
        pytest.main(
            ['-v', '-n', cpu, '--dist=loadfile', '-s', root_path + file_path, '--alluredir',
             report_path, '--clean-alluredir'])
        code = 1
        new = time.time()
        while code:
            try:
                exists = os.path.exists(report_path)
                if exists is True:
                    os.system(
                        'allure generate ' + report_path + ' -o ' + allure_path + '/ --clean')
                    break
                else:
                    pytest.main(['-v', '-s', root_path + file_path, '--alluredir', report_path,
                                 '--clean-alluredir'])
            except Exception as e:
                print('等待生成静态文件...', e)
            finally:
                time.sleep(1)
                if int(time.time()) - int(new) > limited_time:
                    code = 0
                    print('报告生成失败')
        # # 生成ci判断结果
        # code = 1
        # new = time.time()
        # while code:
        #     try:
        #         cls.result_data(root_path)
        #         break
        #     except Exception as e:
        #         print(e)
        #     finally:
        #         time.sleep(1)
        #         if int(time.time()) - int(new) > 8:
        #             code = 0
