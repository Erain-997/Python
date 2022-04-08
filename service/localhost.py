#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/8 14:30
# @Author  : 张晓平

import logging
import traceback
import _thread
from api.role.role import *
from flask import Flask, request, jsonify, json
from api.suitcase.minister_case import run_cases
from internal.file import html_path, auto_path
from internal.report import report_output
from service.reports_api import app_reply
from internal.tools import except_retry
from internal.es_log import es, es_data
from func_timeout import func_set_timeout, FunctionTimedOut
from internal.ding import ding_exception_api

state = bool
app = Flask(__name__)
# 调用app_reply 对象创建路径
app.register_blueprint(app_reply)
err_resp = {
    "info": "parameters error",
    "code": 1
}
succeed = {
    "info": "succeed",
    "code": 0
}


def state_change():
    global state
    state = False


@except_retry(state_change)  # 重试3次
@func_set_timeout(1200)  # 每次执行限时20分钟
def cmd(version, server_id, minister_id, minister_skin_id, wive_id, wive_skin_id, fashion_id, mode):
    os.popen(auto_path() + r"//auto.sh " + version)
    sleep(40)
    os.system("python " + auto_path() + r"//ggg.py")
    sleep(5)
    global state
    try:
        logging.getLogger("airtest").setLevel(logging.ERROR)
        auto_setup(__file__, logdir=True, devices=["Windows:///?title_re=version -.*", ], project_root=html_path())
        run_cases(server_id, minister_id, minister_skin_id, wive_id, wive_skin_id, fashion_id, mode)
    except FunctionTimedOut as e:
        print("超时了")
        ding_exception_api("执行超时" + str(e), e.__traceback__.tb_frame)
        state = False
    report_output(minister_id, minister_skin_id, wive_id, wive_skin_id, fashion_id, version)
    state = False
    os.popen(auto_path() + r"//end.sh")


@app.route('/start_up', methods=["POST"])
def start_up():
    params = json.loads(request.get_data())
    global state
    if state is True:
        return {
            "info": "执行中",
            "code": 1
        }
    try:
        state = True
        # 大臣ID
        minister_id = params.get("minister_id")
        # 大臣皮肤ID
        minister_skin_id = params.get("minister_skin_id")
        # 妃子ID
        wive_id = params.get("wive_id")
        # 玩家时装
        fashion_id = params.get("fashion_id")
        # 妃子皮肤ID
        wive_skin_id = params.get("wive_skin_id")
        # 苏丹客户端版本例如 3.701
        version = params.get("version")
        # 测试的区服ID
        server_id = params.get("server_id")
        # 模式->0为全都跑,1为大臣,2为妃子,3为时装
        mode = params.get("mode")
        if minister_id is None and wive_id is None and fashion_id is None:
            return err_resp
        elif minister_skin_id is None and wive_skin_id is None and fashion_id is None:
            return err_resp
        elif version is None or mode is None or server_id is None:
            return err_resp
        elif minister_id is None and mode == 1:
            return err_resp
        # 妃子为空,则mode 不能为2
        elif wive_id is None and mode == 2:
            return err_resp
        elif fashion_id is None and mode == 3:
            return err_resp
        elif minister_id is None and minister_skin_id is None:
            minister_id = 0
            minister_skin_id = 0
        elif wive_id is None and wive_skin_id is None:
            wive_id = 0
            wive_skin_id = 0
        elif fashion_id is None:
            fashion_id = 0

        _thread.start_new_thread(cmd, (
            version, server_id, minister_id, minister_skin_id, wive_id, wive_skin_id, fashion_id, mode))
        es.es_info(es_data(start_up.__name__, params, "success", "success"))

    except Exception as e:
        es.es_error(es_data(start_up.__name__, params, str(e), traceback.format_exc()))
        state = False
        return {
            "info": e,
            "code": 1
        }
    return {
        "info": "succeed",
        "code": 0
    }
