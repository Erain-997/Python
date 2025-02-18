import json
import threading

import pymysql
import yaml
from mitmproxy import http

from common.api.mock_data import MockData
from common.api.rc4_kt import RC4Kit
from common.utils.path_config import android


class MockProxy:
    def __init__(self):
        # 打开并加载 mock.yaml 文件
        self.mock_data = MockData()
        # HTTP流本地存储路径
        self.file_path = f"{android.flow_data_dir}/flow_data.json"
        # 流本地编号
        self.trace_id = 0
        self.data_written = False
        self.first_response_processed = False
        self.lock = threading.Lock()

    def request(self, flow: http.HTTPFlow) -> None:
        self.mock_data.file_path = f"{android.mock_dir}/mock_{flow.client_conn.peername[0]}.yaml"
        """拦截并打印目标域名的请求"""
        if self.mock_data.host in flow.request.host:
            print(f"\n=================== Request to {self.mock_data.host} ===================")
            print(f"hhhhost: {flow.request.host}")
            print(f"mmmmmmethod: {flow.request.method}")
            print(f"uuuuuurl: {flow.request.url}")
            print(f"Client IP: {flow.client_conn.peername[0]}")
            print("Headers:")
            for key, value in flow.request.headers.items():
                print(f" {key}: {value}")

            # 如果是 POST 请求，打印请求体
            if flow.request.method == "POST" and flow.request.content:
                print("\nRequest Body:")
                print(flow.request.text)

    def response(self, flow: http.HTTPFlow) -> None:
        if self.mock_data.host in flow.request.host:
            # TODO 待调试
            # original_content = flow.response.content
            # chunk_size = 512 * 1024 // 300  # 每 100ms 发送的字节数
            # flow.response.content = b""  # 清空内容
            #
            # # 分段发送数据
            # for i in range(0, len(original_content), chunk_size):
            #     time.sleep(0.1)  # 每次等待 100ms
            #     flow.response.content += original_content[i:i + chunk_size]
            # if flow.request.path in str(self.mock_data.config):
            #     threading.Thread(target=self.save_api_data, args=(copy.deepcopy(flow),)).start()

            print(f"\n =================== response from {self.mock_data.host}  ===================")
            print(f"状态码: {flow.response.status_code}")
            print(f"地址: {flow.request.url}")
            # 打印响应体（仅文本类型）
            print(
                "***************before:flow.response.content*********************\n",
                flow.response.content,
                "\n*******************************\n",
            )

            self.mock_home_data(flow)
            self._get_data(flow)
            # self.update_user_info(flow)

            # TODO 后续优化修改 data_tmp["data"]["keyValueMap"][k] = v
            for case_name, api_info in self.mock_data.get_config().items():
                if case_name != "TARGET_HOST" and case_name != "default":
                    for api_path, values in api_info.items():
                        expected_url = f"http://{self.mock_data.host}{api_path}"
                        if flow.request.url == expected_url:
                            if "/app/abtest/getAbtestParams" in api_path:
                                data_tmp = json.loads(flow.response.content.decode("utf-8"))
                                data_tmp["data"]["keyValueMap"] = {}
                                for k, v in values.items():
                                    data_tmp["data"]["keyValueMap"][k] = v
                                flow.response.content = json.dumps(data_tmp, ensure_ascii=False).encode("utf-8")

            print("***************after:flow.response.content*********************\n",
                  flow.response.content,
                  "\n************************************\n")

    def _get_data(self, flow2):
        """获取充值页面接口返回值"""
        if "getConisStoreListBySkuModelV2" in flow2.request.url or "getConisStoreListBySkuModelV3" in flow2.request.url:
            # TODO key目前apk写死
            key = "abcdefghijklmnopqrstuvwxyzABCDEF"

            try:
                # 检查 response content 是否为有效的 JSON
                response_content = json.loads(flow2.response.content.decode("utf-8"))

                if "result" in response_content and not self.first_response_processed:
                    encrypted_result = response_content["result"]

                    # 解密
                    decrypted = RC4Kit.decrypt(encrypted_result, key)

                    # 检查解密后的内容是否为有效的 JSON
                    decrypted_json = json.loads(decrypted)
                    print(
                        '--------------------',
                        decrypted_json
                    )
                    yaml_file_path = f"{android.test_datas_dir}/top_up_modules.yaml"
                    result = {}

                    # 从 retainSkuInfoResponses 中提取 coins
                    if "retainSkuInfoResponses" in decrypted_json["data"]:
                        coins = decrypted_json["data"]["retainSkuInfoResponses"]["coins"]
                        bonus = decrypted_json["data"]["retainSkuInfoResponses"]["keepGiveCoins"]
                        key = f"top_up_sku_coins"
                        result[key] = [f"{coins}"]
                        key = f"top_up_sku_bonus"
                        result[key] = [f"{bonus}"]

                    # 从 skuInfoResponses 中提取 coins
                    if "skuInfoResponses" in decrypted_json["data"]:
                        for i, item in enumerate(decrypted_json["data"]["skuInfoResponses"],
                                                 start=2):
                            coins = item["coins"]
                            coins_key = f"top_up_coins{i - 1}"
                            gpskuId = item["gpSkuId"]
                            sku_id_key = f"gp_skuId{i - 1}"
                            result[coins_key] = [f"+{coins}"]
                            result[sku_id_key] = [f"{gpskuId}"]

                    # 从 skuInfoResponses 中提取 bonus
                    if "skuInfoResponses" in decrypted_json["data"]:
                        for i, item in enumerate(decrypted_json["data"]["skuInfoResponses"],
                                                 start=2):
                            bonus = item["productGiveCoins"]
                            key = f"top_up_bonus{i - 1}"
                            result[key] = [f"+{bonus}"]

                    # 读取或创建 YAML 文件
                    try:
                        with open(yaml_file_path, "r") as file:
                            data = yaml.safe_load(file)
                    except FileNotFoundError:
                        print("文件不存在，不进行任何操作")
                        data = None

                    # 如果文件存在且 TopUpPage 存在
                    if data is not None:
                        # 确保 TopUpPage 存在
                        if "TopUpPage" not in data:
                            data["TopUpPage"] = {}

                        # 检查数据是否一致
                        existing_data = data.get("TopUpPage", {})
                        if not self.data_written and existing_data != result:
                            # 更新 TopUpPage 下的数据
                            data["TopUpPage"].update(result)
                            # 标记数据已被更新
                            self.data_written = True

                            # 写入 YAML 文件
                            with open(yaml_file_path, "w") as file:
                                yaml.dump(data, file, default_flow_style=False, sort_keys=False)
                            print("数据已写入文件")
                        else:
                            print("数据一致或已写入，无需更新")

                    # 打印结果
                    print(
                        "***************bbbbbbbbbbbbbbbb*********************\n",
                        result,
                        "\n*******************************\n",
                    )

            except json.JSONDecodeError:
                print("Invalid JSON in response content")
            except Exception as e:
                print(f"An error occurred: {e}")

    def mock_home_data(self, flow2):
        expected_url1 = f"http://{self.mock_data.host}/app/homeData/getHomeConfig"
        if expected_url1 == flow2.request.url:
            key = "abcdefghijklmnopqrstuvwxyzABCDEF"
            try:
                for case_name, api_info in self.mock_data.get_config().items():
                    if case_name != "TARGET_HOST" and case_name != "default":
                        for api_path, values in api_info.items():
                            if "/app/homeData/getHomeConfig" in api_path:
                                for k, v in values.items():
                                    # 检查 response content 是否为有效的 JSON
                                    response_content = json.loads(flow2.response.content.decode("utf-8"))
                                    if "result" in response_content:
                                        encrypted_result = response_content["result"]

                                        # 解密
                                        decrypted = RC4Kit.decrypt(encrypted_result, key)

                                        # 检查解密后的内容是否为有效的 JSON
                                        decrypted_json = json.loads(decrypted)
                                        # 修改 ggLoginBonus 的值
                                        decrypted_json["data"][k] = v  # 修改为你想要的值
                                        # 将修改后的内容重新加密并更新 response content
                                        new_encrypted_result = RC4Kit.encrypt(json.dumps(decrypted_json), key)

                                        response_content["result"] = new_encrypted_result
                                        flow2.response.content = json.dumps(
                                            response_content, ensure_ascii=False
                                        ).encode("utf-8")

                print("getSkuAndShorts JSON modified and re-encrypted")
            except json.JSONDecodeError:
                print("Invalid JSON in response content")
            except Exception as e:
                print(f"An error occurred: {e}")

    def update_user_info(self, flow2):
        if "login/v3/initLogin" in flow2.request.url:
            try:
                client = MySQLClientProxy()
                # 检查 response content 是否为有效的 JSON
                response_content = json.loads(flow2.response.content.decode("utf-8"))
                user_code = response_content['data']['userResponse']['userCode']
                sql_result = f'UPDATE hi_subscription_user SET end_time = "0", end_time_real = "0" WHERE user_id = (SELECT id FROM hi_user WHERE user_code ={user_code})'
                sql_update_coins = f'UPDATE hi_user SET coins = 0, bonus = 0 WHERE user_code = {user_code}'
                client.execute_non_query(sql_result)
                client.execute_non_query(sql_update_coins)
                client.close()
                print(
                    "***************sssss*********************\n",
                    "\n*******************************\n",
                )
            except Exception as e:
                print(f"An error occurred: {e}")

    def flow_to_dict(self, flow):
        # TODO 有并发问题
        self.trace_id += 1
        flow_dict = {
            self.trace_id: {
                "request": {
                    "method": flow.request.method,
                    "url": flow.request.url,
                    "headers": dict(flow.request.headers),  # 将 Headers 对象转换为字典
                    # 如果需要，你可以添加更多请求相关的属性
                    "body": flow.request.content.decode("utf-8"),  # 注意：这取决于你的需求和数据类型
                },
                "response": {
                    # 初始时响应可能为空，因此我们需要检查它是否存在
                    "status_code": flow.response.status_code if flow.response else None,
                    "headers": dict(flow.response.headers) if flow.response else {},
                    # 同样，你可以添加更多响应相关的属性
                    "body": flow.response.content.decode("utf-8"),  # 注意：这取决于你的需求和数据类型
                },
                # 你可以添加更多与 HTTPFlow 相关的属性，如时间戳、错误信息等
            }
        }
        return flow_dict

    def save_api_data(self, flow):
        with self.lock:
            flow_dict = self.flow_to_dict(flow)
            ip_str = flow.client_conn.peername[0]
            self.file_path = f"{android.flow_data_dir}/flow_data_{ip_str}.json"
            try:
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                data = {}

            data.update(flow_dict)

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)


# 注册为 mitmproxy 的 addon
addons = [MockProxy()]


class MySQLClientProxy:
    def __init__(self):
        self.host = "10.10.39.11"
        self.port = 3306
        self.user = "root"
        self.password = "hinow1@a"
        self.database = "shorttv"
        self.connection = None
        self.connect()

    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor,
            )
            print("数据库连接成功")
        except pymysql.MySQLError as e:
            print(f"数据库连接失败: {e}")
            raise

    def execute_query(self, query, params=None):
        """执行查询并返回结果"""
        if not self.connection:
            raise Exception("数据库未连接")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return result
        except pymysql.MySQLError as e:
            print(f"查询执行失败: {e}")
            raise

    def execute_non_query(self, query, params=None):
        """执行非查询语句（如插入、更新、删除）"""
        if not self.connection:
            raise Exception("数据库未连接")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
        except pymysql.MySQLError as e:
            print(f"非查询语句执行失败: {e}")
            self.connection.rollback()
            raise

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")
