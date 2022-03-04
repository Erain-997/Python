#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/04/28
# @Author  : zxp

import os
from multiprocessing import Process


def start_server():
    os.system("python -m http.server")


def process():
    z = Process(target=start_server, args=())
    z.start()


if __name__ == '__main__':
    process()

