#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @author: zxp
# @date: 2019/09/19


import time, os, xlwt, xlrd
from xlutils.copy import copy
from xlwt import *

workpath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '\\'


def now_time():
    '''
    获取当前时间
    '''
    return time.strftime("%m_%d_%H_%M_%S", time.localtime())


def report_file(data):
    """执行日记"""
    log_file = workpath + "result\\" + now_time() + ".log"
    try:
        with open(log_file, 'a')as f:
            f.write(str(data).encode('utf-8'))
    except Exception:
        with open(log_file, 'ab')as f:
            f.write(str(data).encode('utf-8'))


def create_excel():
    """excel 初始化"""
    # 为样式创建字体
    font = xlwt.Font()
    # 字体大小，11为字号，20为衡量单位
    # font.height = 20 * 11
    font.name = u'微软雅黑'
    # 字体加粗
    font.bold = True
    # # 下划线
    # font.underline = True
    # # 斜体字
    # font.italic = True
    # 初始化样式
    style = xlwt.XFStyle()
    # 字体设置
    style.font = font
    alignment = xlwt.Alignment()
    # 0x01(左端对齐)、0x02(水平方向上居中对齐)、0x03(右端对齐)
    alignment.horz = 0x01
    # 0x00(上端对齐)、 0x01(垂直方向上居中对齐)、0x02(底端对齐)
    alignment.vert = 0x01
    style.alignment = alignment
    # 自动换行
    style.alignment.wrap = 1
    # 背景色
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    # https://blog.csdn.net/apollo_miracle/article/details/105087548 色值
    pattern.pattern_fore_colour = 42
    style.pattern = pattern
    # 边框设置
    # 设置边框
    borders = xlwt.Borders()
    # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
    # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style.borders = borders
    file_name = xlwt.Workbook(encoding='utf-8')
    sheet = file_name.add_sheet("vk0.73", cell_overwrite_ok=True)
    sheet.write_merge(0, 0, 1, 3, '1.测试终端电量均大于30%；\n2.后台清理无关程序；\n3.测试机器与竞品机连接同一个无线网络;'
                                  '\n4.默认已登录帐号状态,且帐号等级道具保持一致; \n5.最终数据采取10次测试数据中间值', style)
    font = xlwt.Font()
    font.blod = True
    # 设置宽度
    sheet.col(0).width = 300 * 20
    sheet.col(1).width = 300 * 20
    sheet.col(2).width = 300 * 20
    sheet.col(3).width = 300 * 20
    sheet.col(4).width = 300 * 20
    # 设置高度
    sheet.row(0).height_mismatch = True
    sheet.row(0).height = 40 * 40
    sheet.write(0, 0, '预置条件', style)
    sheet.write(1, 0, '游戏', style)
    sheet.write(1, 1, '测试机型', style)
    sheet.write(1, 2, '冷启动耗时(s)', style)
    sheet.write(1, 3, '登录耗时(s)', style)
    return file_name, sheet


def form_style():
    style = xlwt.XFStyle()
    borders = xlwt.Borders()
    # 细实线:1，小粗实线:2，细虚线:3，中细虚线:4，大粗实线:5，双线:6，细点虚线:7
    # 大粗虚线:8，细点划线:9，粗点划线:10，细双点划线:11，粗双点划线:12，斜点划线:13
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style.borders = borders
    return style


if __name__ == '__main__':
    filename, sheet = create_excel()
    filename.save(workpath + 'result\\report' + time.strftime("%m_%d_%H_%M_%S", time.localtime()) + '.xls')
