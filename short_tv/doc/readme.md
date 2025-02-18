# 项目名称

SHORT_TV mobile-ui-automation-tests

## 库版本

python=3.11
pycharm=2024.2.1
java=17
Appium-windows=1.20.0
newAppium-Inspector-windows=2023.8.4

Appium-Python-Client=2.0.0
Appium-Python-Client==2.0.0
atomicwrites==1.4.1
attrs==24.2.0
BeautifulReport==0.1.3
certifi==2024.8.30
cffi==1.17.1
charset-normalizer==2.0.12
colorama==0.4.6
cryptography==43.0.1
execnet==2.1.1
h11==0.14.0
idna==3.8
iniconfig==2.0.0
outcome==1.3.0.post0
packaging==24.1
pluggy==1.5.0
py==1.11.0
pycparser==2.22
pyOpenSSL==24.2.1
PySocks==1.7.1
pytest==7.0.1
pytest-forked==1.6.0
pytest-html==3.1.1
pytest-metadata==3.1.1
pytest-xdist==2.5.0
PyYAML==6.0.2
requests==2.26.0
selenium==4.0.0
sniffio==1.3.1
sortedcontainers==2.4.0
tomli==2.0.1
trio==0.26.2
trio-websocket==0.11.1
typing_extensions==4.12.2
urllib3==1.26.20
urllib3-secure-extra==0.1.0
websocket-client==1.8.0
wsproto==1.2.0
yamail==1.0.2

## 目录结构

```
|-- common (公共模块)
    |-- api (API相关代码)
    |-- mail (邮件相关模块)
    |-- recording
    |-- screenshot
    |-- utils (实用工具类,例如path_utils.py 存放项目相关的路径)
|-- doc (项目文档)
|-- sys_android
    |-- caps (配置文件目录)
    |-- install_packages (apk or ipa 安装包目录)
    |-- outputs (输出文件目录)
        |-- html
        |-- log
        |-- screenshot
        |-- video
    |-- page_locators (页面定位符)
    |-- page_objects (页面对象)
    |-- test_cases (测试用例)
        |-- regression (回归测试用例 ps:依赖指定版本的测试用例)
        |-- v1_9_7 (指定版本的测试用例)
    |-- test_datas (测试数据)
|-- sys_ios
    |-- caps (配置文件目录)
    |-- install_packages (apk or ipa 安装包目录)
    |-- outputs (输出文件目录)
        |-- html
        |-- log
        |-- screenshot
        |-- video
    |-- page_locators (页面定位符)
    |-- page_objects (页面对象)
    |-- test_cases (测试用例)
        |-- regression (回归测试用例 ps:依赖指定版本的测试用例)
        |-- v1_9_7 (指定版本的测试用例)
    |-- test_datas (测试数据)
```