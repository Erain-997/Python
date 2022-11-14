# _*_coding:utf-8_*_
# Author：Erain
# Time：2022/11/08
from api.execute_api.execute_api import ExecuteApi
import os

"""  
多设备执行时部分机型可能无法正常运行,需要单独执行例如华为荣耀V8
"""
if __name__ == '__main__':
    ExecuteApi().run_api(os.path.dirname(__file__))
