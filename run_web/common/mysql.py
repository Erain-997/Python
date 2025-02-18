# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/11/18

import pymysql

from common.log_tools import Log


class MySQLClient:
    def __init__(self):
        self.host = "192.168.120.150"
        self.port = 3306
        self.user = "user"
        self.password = "password"
        self.database = "shorttv"
        self.connection = None

    def connect(self):
        """连接数据库"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            Log.logger.info("数据库连接成功")
        except pymysql.MySQLError as e:
            Log.logger.error(f"数据库连接失败: {e}")
            raise

    def execute_query(self, query, params=None):
        """执行查询并返回结果"""
        if not self.connection:
            raise Exception("数据库未连接")

        try:
            with self.connection.cursor() as cursor:
                Log.logger.info("数据库执行: %s,%s", query, params)
                cursor.execute(query, params)
                result = cursor.fetchall()
                # 将所有整数1/0转换为True/False
                for row in result:
                    for key, value in row.items():
                        # if isinstance(value, int) and value in (0, 1):
                        if key in ["pass", "proxy", "record", "feishu"]:
                            row[key] = bool(value)
                return result
        except pymysql.MySQLError as e:
            Log.logger.error(f"查询执行失败: {e}")
            raise

    def execute_non_query(self, query, params=None):
        """执行非查询语句（如插入、更新、删除）"""
        if not self.connection:
            raise Exception("数据库未连接")

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
        except pymysql.MySQLError as e:
            Log.logger.error(f"非查询语句执行失败: {e}")
            self.connection.rollback()
            raise

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            Log.logger.info("数据库连接已关闭")
