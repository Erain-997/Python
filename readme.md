# [苏丹外显自动化脚本]()

# [概况]()
收集各个场景中的大臣外显，截图记录。其原理是：通过像素点识别，逐步点击到要测试的场景，截图记录

ps：故图片质量很重要，要大小且形状一致才可识别


# [项目结构]()
        * api                   脚本
            * scene             测试场景
                * common        公共方法
            * suitcase          测试用例
            * language*         各个语言版本需要的图片
                * common        模块通用图片
                * minister      大臣模块
                    * minister  所有大臣的名字截图
                    * modules*  大臣模块场景
                * rank          排行榜模块
                * role_info     角色模块
        * img                   结果截图
        * internal              框架文件
        * log                   日志
        * report                结果报告     
        * main.py               运行入口  
   
   
# [基础环境]()
| 环境                         | 版本      |
| ------------------------------ | --------- |
| python                         | 3.7       |
| airtest                        | 1.2.1     |
| test-components                | 1.3.22    |
| AirtestIDE版本：AirtestIDE     | 1.2.8     |
| Cornor版本：Solar 2D Simulator | 2020.3635 |

# [使用]()
## 注意事项
1. 运行前将语言调整至简体中文
1. 运行前mock掉弹窗

        客户端代码索引：return tGuideAndPop1,tGuideAndPop2,tGuideAndPop3
        修改代码为：return nil,nil,nil
1. 有些场景没办法短时间循环的，会影响结果。例：测中文时，派遣哥伦布学习，学习时间3h，切换到英文继续测试时，就没办法再测试了

## 使用
1、打开游戏，corona分辨率大小：800*1280

2、运行脚本

## 截图规范
1. 尽量截图局部，不受特效、语言的影响
1. 大臣不同场景可能由于背景不一样而导致识别不到，这种情况要重新截图