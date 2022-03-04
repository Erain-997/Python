#!usr/bin/python
# -*- coding: UTF-8 -*-
# @Time    : 2021/03/05
# @Author  : zxp

import pymysql
import os
import configparser


class MysqlDB(object):

    def __init__(self, file_path, port=3306, db_name=None):
        if os.path.exists(file_path):
            conf = configparser.ConfigParser()
            conf.read(file_path, encoding="utf-8")
            if db_name is not None:
                data_base = db_name
            else:
                data_base = conf.get("mysqlDB", "db")
        else:
            raise ValueError("配置路径不存在\n" + file_path)
        self.db = pymysql.connect(host=conf.get("mysqlDB", "host"),
                                  user=conf.get("mysqlDB", "user"),
                                  passwd=conf.get("mysqlDB", "pwd"),
                                  db=data_base,
                                  port=port,
                                  charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)

    def db_execute(self, sql_param, args=None):
        if sql_param[0].lower() == "s":
            self.cursor.execute(sql_param, args)
            data = self.cursor.fetchall()

            return data
        elif sql_param[0].lower() == "u" or \
                sql_param[0].lower() == "i" \
                or sql_param[0].lower() == "d":
            self.cursor.execute(sql_param, args)
            self.db.commit()
            self.db.rollback()



