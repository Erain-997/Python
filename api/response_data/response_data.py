from api.response_data.response_index import RegRespDataIndex


# 响应包体索引，包含各种响应码

# 继承于请求索引
class RegResp(RegRespDataIndex):
    """
    存放各个响应码，用于assert校验
    """

    @classmethod
    def code_0(cls):
        return {
            cls.code: 0,
            cls.data: {},
            cls.info: ""
        }

    @classmethod
    def code_500(cls):
        return {
            cls.code: 500,
            cls.data: {},
            cls.info: "Header参数错误"
        }

    @classmethod
    def code_501(cls):
        return {
            cls.code: 501,
            cls.data: {},
            cls.info: "必填参数缺失"
        }

    @classmethod
    def code_502(cls):
        return {
            cls.code: 502,
            cls.data: {},
            cls.info: "用户名称长度错误"
        }

    @classmethod
    def code_503(cls):
        return {
            cls.code: 503,
            cls.data: {},
            cls.info: "用户名格式错误"
        }

    @classmethod
    def code_504(cls):
        return {
            cls.code: 504,
            cls.data: {},
            cls.info: "密码长度错误"
        }

    @classmethod
    def code_505(cls):
        return {
            cls.code: 505,
            cls.data: {},
            cls.info: "用户名必须是首字母开头"
        }

    @classmethod
    def code_506(cls):
        return {
            cls.code: 506,
            cls.data: {},
            cls.info: "账号已被注册"
        }

    @classmethod
    def code_507(cls):
        return {
            cls.code: 507,
            cls.data: {},
            cls.info: "参数类型错误"
        }

    @classmethod
    def code_00(cls):
        return {
            cls.code: 0,
            cls.info: ""
        }

    @classmethod
    def code_120(cls):
        return {
            cls.code: 120,
            cls.info: "Decode Fail"
        }
