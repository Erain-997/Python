# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/13

from gevent import pywsgi
from service.localhost import *
from internal.server_api import process

# todo 该项目未整理
if __name__ == '__main__':
    process()
    server = pywsgi.WSGIServer(('0.0.0.0', 3888), app)
    server.serve_forever()
    # (version, server_id, minister_id, minister_skin_id, wive_id, wive_skin_id, fashion_id, mode)
    cmd("Branch_3.901_皮肤外观_0314", 2, 51, 1655, 0, 0, 0, 1)
