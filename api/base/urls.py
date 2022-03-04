# 接口地址
# 拆分为目的接口和接口后缀


class URL(object):
    @classmethod
    def base_url(cls):
        url = "http://10.6.28.88:3888"
        return url

    @classmethod
    def reg_url(cls):
        suffix = "/Register"
        return cls.base_url() + suffix
