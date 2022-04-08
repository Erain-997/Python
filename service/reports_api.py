#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/10 10:59
# @Author  : 张晓平

from flask import render_template, request, redirect, url_for
from flask import Blueprint

# 注册蓝图对象，
app_reply = Blueprint("reply", __name__)


@app_reply.route("/<name>")
def html_info(name):
    return render_template(f'/{name}.html')


@app_reply.route('/img_push', methods=['Get'])
def img_push():
    try:
        # img 文件名称
        img_name = request.args.get("img_name")
    except Exception as e:

        return {"code": 1, "info": str(e)}

    return redirect(url_for('static', filename=img_name))
