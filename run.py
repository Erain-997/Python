#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2019/9/23
# @Author  : zxp
import os

from test_components.toolkit.processing_data import Output
from test_components.toolkit.tools import SmallTools

if __name__ == '__main__':
    Output.run_case(SmallTools.root_path(os.path.dirname(__file__)), "4")
