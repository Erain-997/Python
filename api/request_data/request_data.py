
from test_components.toolkit.create_parameters import GetTestParams
import random
import string

# 用于生成各种各样的参数值
from api.request_data.request_index import RequestIndex


class RegData(RequestIndex):
    @classmethod
    def send_data(cls):
        return {
            cls.user: random.choice(string.ascii_letters) + GetTestParams.generate_random_str(14),
            cls.Password: GetTestParams.generate_random_str(15),
            cls.device_id: GetTestParams.generate_random_str(15),
            cls.device_type: GetTestParams.generate_random_str(15),
        }

    @classmethod
    def addproductmap_data(cls):
        appkey = "app_key"
        products = "products"
        cpproductid = "cp_product_id"
        spproductid = "sp_product_id"
        spamount = "sp_amount"
        spcurrency = "sp_currency"
        return {
                appkey: GetTestParams.generate_random_str(14),
                products: [
                    {
                        cpproductid: GetTestParams.generate_random_str(15),
                        spproductid: GetTestParams.generate_random_str(15),
                        spamount: GetTestParams.generate_random_int(3),
                        spcurrency: GetTestParams.generate_random_str(15),
                    }
                ]

        }





