# 头部参数封装
class HeadParameter(object):
    test = "test"

    @classmethod
    def register_header(cls):
        """
        头部参数
        :return:
        """
        return {
            cls.test: "123",
        }
