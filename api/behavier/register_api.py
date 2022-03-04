import copy
import random
import string

from test_components.toolkit.create_parameters import GetTestParams
from test_components.toolkit.tools import SmallTools

from api.base.urls import URL
from api.request_data.request_data import RegData
from api.request_data.request_header import HeadParameter
from api.response_data.response_data import RegResp


# 封装各个函数，拥有最小的入参（测试字段）和出参（实际用于测试的包体）
# 类继承自：接口测试公共包，url、请求头部、请求包体、响应包体
class RegisterApi(SmallTools, URL, RegData, HeadParameter, RegResp):
    """正常注册"""

    def register_api(self, front, request_data=None):
        """正常注册"""
        front_case_name = None
        if request_data is not None:
            register_data = request_data
        else:
            register_data = copy.deepcopy(self.send_data())

        reps = self.post(self.reg_url(), register_data, self.register_header())  # 请求
        if front:
            front_case_name = self.register_api.__doc__
            # 保存数据，用于allure呈现
        self.save_data(self.reg_url(), register_data, front_case_name)  # 报告相关
        return self.reg_url(), register_data, reps

    @classmethod
    def normal_register(cls):
        """正常注册"""
        reg_data = copy.deepcopy(cls.send_data())
        return reg_data

    @classmethod
    def illegal_user_short(cls):
        """账户名长度非法，过短"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = random.choice(string.ascii_letters) + cls.generate_random_str(4)
        return reg_data

    @classmethod
    def illegal_user_long(cls):
        """账户名长度非法，过长"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = random.choice(string.ascii_letters) + cls.generate_random_str(21)
        return reg_data

    @classmethod
    def illegal_user_max(cls):
        """账户名长度非法，上边界相等"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = random.choice(string.ascii_letters) + cls.generate_random_str(19)
        return reg_data

    @classmethod
    def illegal_user_min(cls):
        """账户名长度非法，下边界相等"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = random.choice(string.ascii_letters) + cls.generate_random_str(5)
        return reg_data

    @classmethod
    def illegal_user_num(cls):
        """账户名格式非法，数字开头"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = "1" + cls.generate_random_str(14)
        return reg_data

    @classmethod
    def illegal_user_specialhead(cls):
        """账户名格式非法，特殊字符开头"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = "#+-" + random.choice(string.ascii_letters) + cls.generate_random_str(14)
        return reg_data

    @classmethod
    def illegal_user_special(cls):
        """账户名格式非法，带特殊符号"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = random.choice(string.ascii_letters) + cls.generate_random_str(14) + "#+-"
        return reg_data

    @classmethod
    def illegal_psw_short(cls):
        """密码长度非法，过短"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.Password] = GetTestParams.generate_random_str(5)
        return reg_data

    @classmethod
    def illegal_psw_long(cls):
        """密码长度非法，过长"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.Password] = GetTestParams.generate_random_str(21)
        return reg_data

    @classmethod
    def illegal_psw_max(cls):
        """密码长度非法，上边界相等"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.Password] = GetTestParams.generate_random_str(20)
        return reg_data

    @classmethod
    def illegal_psw_min(cls):
        """密码长度非法，下边界相等"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.Password] = GetTestParams.generate_random_str(6)
        return reg_data

    @classmethod
    def lack_of_user(cls):
        """缺失user参数"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data.pop(cls.user)
        return reg_data

    @classmethod
    def empty_user(cls):
        """user参数为空"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = ""
        return reg_data

    @classmethod
    def lack_of_psw(cls):
        """缺失Password参数"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data.pop(cls.Password)
        return reg_data

    @classmethod
    def empty_psw(cls):
        """Password参数为空"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.Password] = ""
        return reg_data

    @classmethod
    def lack_of_deviceid(cls):
        """缺失devidceId参数"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data.pop(cls.device_id)
        return reg_data

    @classmethod
    def empty_devicedid(cls):
        """devicedId参数为空"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.device_id] = ""
        return reg_data

    @classmethod
    def lack_of_devicedtype(cls):
        """缺失devicedtype参数"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data.pop(cls.device_type)
        return reg_data

    @classmethod
    def empty_devicedtype(cls):
        """devicedtype参数为空"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.device_type] = ""
        return reg_data

    @classmethod
    def lack_of_header(cls):
        """缺失Header参数"""
        reg_header = copy.deepcopy(cls.register_header())
        reg_header.pop('test')
        return reg_header

    @classmethod
    def empty_header(cls):
        """header参数为空"""
        reg_header = copy.deepcopy(cls.register_header())
        reg_header['test'] = ""
        return reg_header

    @classmethod
    def illegal_header(cls):
        """header参数为非法值"""
        reg_header = copy.deepcopy(cls.register_header())
        reg_header['test'] = "111"
        return reg_header

    @classmethod
    def existed_user(cls):
        """用户名冲突"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = "a123456"
        reg_data[cls.Password] = "a123456"
        reg_data[cls.device_id] = "a123456"
        reg_data[cls.device_type] = "phone"
        return reg_data

    @classmethod
    def illegal_user_not_string(cls):
        """用户名类型为纯数字"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.user] = 12345678
        return reg_data

    @classmethod
    def illegal_psw_not_string(cls):
        """密码类型为纯数字"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.Password] = 12345678
        return reg_data

    @classmethod
    def illegal_deviceid_not_string(cls):
        """deviceid类型为纯数字"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.device_id] = 12345678
        return reg_data

    @classmethod
    def illegal_devicetype_not_string(cls):
        """devicetype类型为纯数字"""
        reg_data = copy.deepcopy(cls.send_data())
        reg_data[cls.device_type] = 12345678
        return reg_data

    # 封装好各个请求和预期结果的对应情况，和@pytest.mark.parametrize配套使用（框架特性），从而实现循环遍历测试
    # 可理解为测试集合，所有的用例都会在这体现
    @classmethod
    def data_generation(cls):
        """
        测试数据生成，列表中每四个数据为一组，顺序为：头部参数，请求参数，预期结果，测试用例名
        :return:
        """
        data_generation_list = [
            # # 正常
            # (cls.register_header(), cls.normal_register(), cls.code_0(), cls.normal_register().__doc__),

            # 用户名
            (cls.register_header(), cls.illegal_user_short(), cls.code_502(), cls.illegal_user_short.__doc__),
            (cls.register_header(), cls.illegal_user_long(), cls.code_502(), cls.illegal_user_long.__doc__),
            (cls.register_header(), cls.illegal_user_max(), cls.code_502(), cls.illegal_user_max.__doc__),
            (cls.register_header(), cls.illegal_user_min(), cls.code_502(), cls.illegal_user_min.__doc__),
            (cls.register_header(), cls.illegal_user_num(), cls.code_505(), cls.illegal_user_num.__doc__),
            (cls.register_header(), cls.illegal_user_specialhead(), cls.code_503(),
             cls.illegal_user_specialhead.__doc__),
            (cls.register_header(), cls.illegal_user_special(), cls.code_503(), cls.illegal_user_special.__doc__),

            # 密码
            (cls.register_header(), cls.illegal_psw_short(), cls.code_504(), cls.illegal_psw_short.__doc__),
            (cls.register_header(), cls.illegal_psw_long(), cls.code_504(), cls.illegal_psw_long.__doc__),
            (cls.register_header(), cls.illegal_psw_max(), cls.code_504(), cls.illegal_psw_max.__doc__),
            (cls.register_header(), cls.illegal_psw_min(), cls.code_504(), cls.illegal_psw_min.__doc__),

            # 参数缺失、空值
            (cls.register_header(), cls.lack_of_user(), cls.code_501(), cls.lack_of_user.__doc__),
            (cls.register_header(), cls.lack_of_psw(), cls.code_501(), cls.lack_of_psw.__doc__),
            (cls.register_header(), cls.lack_of_deviceid(), cls.code_501(), cls.lack_of_deviceid.__doc__),
            (cls.register_header(), cls.lack_of_devicedtype(), cls.code_0(), cls.lack_of_devicedtype.__doc__),
            (cls.register_header(), cls.empty_user(), cls.code_505(), cls.empty_user.__doc__),
            (cls.register_header(), cls.empty_psw(), cls.code_504(), cls.empty_psw.__doc__),
            (cls.register_header(), cls.empty_devicedid(), cls.code_0(), cls.empty_devicedid.__doc__),
            (cls.register_header(), cls.empty_devicedtype(), cls.code_0(), cls.empty_devicedtype.__doc__),

            # 头部参数
            (cls.lack_of_header(), cls.normal_register(), cls.code_500(), cls.lack_of_header.__doc__),
            (cls.empty_header(), cls.normal_register(), cls.code_500(), cls.empty_header.__doc__),
            (cls.illegal_header(), cls.normal_register(), cls.code_500(), cls.illegal_header.__doc__),

            # 用户名冲突
            (cls.register_header(), cls.normal_register(), cls.code_500(), cls.existed_user.__doc__),

            # 参数类型
            (cls.register_header(), cls.normal_register(), cls.code_507(), cls.illegal_user_not_string.__doc__),
            (cls.register_header(), cls.normal_register(), cls.code_507(), cls.illegal_psw_not_string.__doc__),
            (cls.register_header(), cls.normal_register(), cls.code_507(), cls.illegal_deviceid_not_string.__doc__),
            (cls.register_header(), cls.normal_register(), cls.code_507(), cls.illegal_devicetype_not_string.__doc__),

        ]
        return data_generation_list

    # 生成异常数据列表
    def exception_create_data(self):
        """
        异常数据的生成
        """
        return self.get_all_exception_test_data(self.send_data())

    def data_0331(self):
        """
        异常数据的生成
        """
        return self.get_all_exception_test_data(self.addproductmap_data())


# 调试用
if __name__ == '__main__':
    a = RegisterApi().data_0331()  # 疑问点：为什么这样就可以不用传参，直接调用
    for i in a:
        print(i)
