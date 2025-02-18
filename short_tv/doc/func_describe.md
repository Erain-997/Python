# 公共功能说明

## Mock

### TODO

暂时对mock没做历史记录

### 文件

[mock_data.py](./../common/api/mock_data.py)

### 描述

对指定端口修改指定值, 入参绑定到结果报告的对应用例中, 并产出:

- [mock.yaml](./../common/api/mock.yaml)

### MockData对象

```python
class MockData:
    def __init__(self):
        # Mock行为记录, 产出文件路径
        self.file_path = f'{android.api_dir}/mock.yaml'
        # Mock域名
        self.host = "test-api.shorttv.live"

```

### 调用

```python
from common.api.mock_data import MockData


def setup_steps(self):
    self.mock_data = MockData(args.device.split(':')[0])
    # 用例名称, 接口, 要修改的值
    self.mock_data.mock_data("test_unlock_drama_01", "/app/abtest/getAbtestParams",
                             {"and_task_test": "1"})
```

## Proxy

### TODO

暂时对抓包没做历史记录

### 文件

[tv_proxy.py](./../tv_proxy.py)

### 描述

在执行用例前, 启动代理服务, 通过执行tv_proxy.py脚本, 对HTTP进行捕获和修改数据, 将经过代理的http包本地存储到文件:

- [flow_data.json](./../common/api/flow_data.json)

### MockProxy对象:

```python
from common.api.mock_data import MockData


class MockProxy:
    def __init__(self):
        # 打开并加载 mock.yaml 文件
        self.mock_data = MockData(args.device.split(':')[0])
        # HTTP流本地存储路径
        self.file_path = f'{android.api_dir}/flow_data.json'
        # 流本地编号
        self.trace_id = 0

```

### 调用

```python
from common.utils.cmd_tools import start_proxy, stop_proxy


def setup_steps(self):
    # 创建子线程, 启动代理
    self.proxy_process = start_proxy()


def teardown_steps(self):
    yield
    # kill子线程
    stop_proxy(self.proxy_process)
```

## Save User Data

### TODO

暂时没有用例需求需要用到这个解密, 封装了基础需求

- 数据可用来构造包体
- 可分离出数据用于下个接口入参

### 描述

对启用proxy时抓包的http数据, 进行数据处理

- 处理数据来源: [flow_data.json](./../common/api/flow_data.json)

### UserData对象:

```python
class UserData:
    def __init__(self):
        # 处理数据来源
        self.file_path = f'{android.api_dir}/flow_data.json'
```

### 调用

```python
from common.api.user_data import UserData

a = UserData()
decrypted = a.get_data("log_path", "http://test-api.shorttv.live/app/homeData/getHomeConfig")

print(decrypted)
'''
 {"data":{"facebookLoginType":"1","ggLoginBonus":"100","haveFacebookAccount":false,"metaLoginBonus":"100","notificationsBonus":"100","userAccountMergeBonus":"200"},"message":"成功","status":0} 
'''
```

## Api

### TODO

基础封装了, 暂时还没用, 后续迭代优化和使用

### 实现

封装了[开发api文档](https://yapi.shorttv.live/project/11/interface/api), 直接拉取所有接口信息到本地文件

- [api_data.json](./../common/api/api_data.json)

### ApiAll对象

```python
class ApiAll:
    # 登录
    def login_yapi_api(self):
    # 下载
    def download_yapi_api(self, cookies):
    # api请求
    def api_request(self, path, headers=None, payload=None):
```

### 调用

```python
from common.api.api_all import ApiAll
# 自定义请求包体, 如果为空, 则使用api文档中默认的参数
headers = {
    # 'gaid': 'dc9f3ed8-8d0c-43f6-9f24-420da32030b3',
    'Authorization': '1pkeeporqzC4ou7Jk1fWnuZOfTmmPzFXbRKqbYUFKCbaHJFVMkjd0nlWvoPxQjUXOP3tkiCXSNnXb6JYwd05IX3woU+Nz+Q8PAYMA8YSwEpim++x+Nvz0vC6KIQP/XaXfUByP/y/vxa+KRzk6+nZewj5x//W+EIkTHLQ3iFfkC9bkggmt8Rg5Z2+XmdPqDWhhL3RHX2AC7en5e5A6H1aJmOXebgiq3s6gfT0MexiL1qD4L5R8qLnBjZQP85pc7dBV+qzCcZ2c/h9+MjG8ZdfJDqtbYOb6Xk58X9KAXXkGXYnJzgt2+HaHzZ3JQC1s0rMerrJLoXfNPuKKE1MN0r6P65JEVUACtcOwsYVNFneDNshBSbsROFA+gJm4WD7K/Xl7Eq4gsy5MFwjG5+SqckNfk4W0KpNNJ/vl94Cs9WXzRfgUzY6wBycwJg7gTx34LM9TiUMUJfLg+i0v0DZGVceRIQJMieeWzwF7zxcthcStMx8Fh+HjPmXPU/G3ZZJsYWFHboyklqhvfJYPQi0Ux+cDwU3MO1gSPm4BWFTVA83X13MiR0B2WG75U6s1xrVI+8/SZxZBdNB8z0GaQ3yIhFrobKuxL1gG5si7qiIROyzw9d2BVNbl/+f1FiMTzkQm0bt01zeu2Ld/xvjd8wVc2wJPA==',
}
payload = {}

# 初始化
a = ApiAll()
# 更新api文档
cook = a.login_yapi_api()
a.download_yapi_api(cook)

# 构造请求
a.api_request("/app/login/v2/getUserInfo", headers=headers, payload=payload)
```