#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/16 15:29
# @Author  : 张晓平

import uuid
import time
from test_components.toolkit.kibana_method import Es
from internal.file import log_path
import datetime
from datetime import timezone, timedelta

es = Es("test_sultan_ui_server", file_path=log_path() + "/ui.log")


def get_uuid():
    return str(uuid.uuid4()).replace("-", '')


def es_data(path, request, response, msg, trace_id=get_uuid(), level="Error"):
    if msg == "success":
        level = "Info"
    return {
        "trace_id": trace_id,
        'path': path,
        'request': request,
        'response': response,
        'level': level,
        'msg': msg,
        'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        '@timestamp': datetime.datetime.now(tz=timezone(timedelta(hours=8))).replace()

    }


if __name__ == '__main__':
    es.es_info(es_data("test", {}, "", "success"))
