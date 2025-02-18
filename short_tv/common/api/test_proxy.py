from mitmproxy import http

host = "test-api.shorttv.live"


# 本地调试代理
class MockProxy:
    def request(self, flow: http.HTTPFlow) -> None:
        """拦截并打印目标域名的请求"""
        if host in flow.request.host:
            print(f"\n=================== Request to {host} ===================")
            print(f"hhhhost: {flow.request.host}")
            print(f"mmmmmmethod: {flow.request.method}")
            print(f"uuuuuurl: {flow.request.url}")
            print("Headers:")
            for key, value in flow.request.headers.items():
                print(f" {key}: {value}")

            # 如果是 POST 请求，打印请求体
            if flow.request.method == "POST" and flow.request.content:
                print("\nRequest Body:")
                print(flow.request.text)

    def response(self, flow: http.HTTPFlow) -> None:
        if host in flow.request.host:
            print(f"\n =================== response from {host}  ===================")
            print(f"状态码: {flow.response.status_code}")
            print(f"地址: {flow.request.url}")
            # 打印响应体（仅文本类型）
            print("************************************\n",
                  flow.response.content,
                  "\n************************************\n")


# 注册为 mitmproxy 的 addon
addons = [MockProxy()]

if __name__ == '__main__':
    a = MockProxy()
    a.modify("/app/abtest/getAbtestParams", '"and_task_test":"0"', '"and_task_test":"1"')
