# **Py接口自动化框架**

## 框架介绍

- 框架分两大块,业务逻辑处理,以及公共方法([test_components](https://gitlab.dianchu.cc/testGroup/testInnerProjects/tools/testcomponentsproject/test_components))
- 业务模块:主要负责业务的处理(测试用例的编写),框架支持并发执行,故用例编写有特定要求
- 公共包:主要负责常用方法的封装,减少代码冗余,提高代码维护性


## 用例编写

- 用例之间是独立的，用例之间没有依赖关系，用例可以完全独立运行【独立运行】
- 用例执行没有顺序，随机顺序都能正常执行【随机执行】
- 每个用例都能重复运行,运行结果不会影响其他用例【不影响其他用例】
- 用例请求数据赋值&获取时,不采用"XX"等字符串索引,应使用声明变量
- 相关具体写法详见[邮件服务](https://gitlab.dianchu.cc/testGroup/basicServices/interfacescript/mailserviceproject/new_mail_service_test)

## 公共包主要结构

- allure 报告生成相关方法
- http请求相关方法
- 数据库驱动相关方法
- 测试数据构造,异常用例生成
- 脚本运行方式
- 数据提取,对比验证
- 具体方法详情[代码](https://gitlab.dianchu.cc/testGroup/testInnerProjects/tools/testcomponentsproject/test_components),ps:测试当中有需要其他方法需求可通过在测开组提TB单给张晓平

## 框架结构

```
├─api          		 		基础接口请求
│  │ 
│  ├─ automatic_demo_api    		接口基础Api,最小用例集封装(可根据项目模块建立多个模块)
│  │ 
│  ├─ base             			请求URl封装
│  │ 
│  ├─request_data			接口请求数据body
│  │ 
│  ├─response_data			接口返回相关数据
│ 
├─src          	    			公共方法
│  │ 
│  ├─ asserts             		断言相关
│ 
├─test_cases               		用例执行
│ 
│
├─Pipfile				依赖包内容解析
│
├─Pipfile.lock      			虚拟环境依赖的版本号以及哈希
│ 
└─run.py          			生成测试报告

```

# [使用]() 

##  一、环境准备

####  **1、 下载项目到本地** 

- git clone https://gitlab.dianchu.cc/testGroup/testInnerProjects/tools/frameproject/py_automatic_demo.git

####  2、安装python依赖模块**

- pipenv install 

- 选择虚拟环境解析器就可开始编写测试用例

#### 3、pipfile依赖包解析说明
- 此文件是环境说明
- *代表所有版本兼容
- 目的：在运行项目的时候可以自动创造运行环境

