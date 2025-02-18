# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/12/9

import csv
import sys
from datetime import datetime
from io import StringIO

import pymysql

from common.mysql import MySQLClient


def backup_mysql_data():
    """
    备份MySQL数据库数据到CSV文件
    :return: 无
    """
    # 初始化数据库客户端
    client = MySQLClient()
    try:
        client.connect()

        # 查询数据库
        query = "SELECT * FROM cases"
        with client.connection.cursor() as cursor:
            cursor.execute(query)

            # 获取列名（表头）
            columns = [desc[0] for desc in cursor.description]

            # 获取所有数据行
            rows = cursor.fetchall()

            # 检查是否有数据返回
            if not rows:
                print("没有数据可备份！")
                return

            # 将查询结果写入到内存中的CSV文件
            csv_data = StringIO()
            writer = csv.writer(csv_data)
            writer.writerow(columns)  # 写入表头

            # 写入数据行，确保从字典中提取值
            for row in rows:
                # 如果 row 是字典类型，获取字典中的值
                if isinstance(row, dict):
                    writer.writerow([row[col] for col in columns])  # 按列名顺序写入值
                else:
                    writer.writerow(row)  # 直接写入元组或列表

            # 获取CSV文件内容
            csv_file_content = csv_data.getvalue()

            # 使用当前时间生成唯一的文件名 todo 暂时这样, 手动维护一下
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if sys.platform == "linux":
                csv_filename = f"/var/ftp/pub/Case/backup_{timestamp}.csv"
            else:
                csv_filename = f"backup_{timestamp}.csv"

            # 将CSV文件内容写入本地文件
            with open(csv_filename, 'w', encoding='utf-8', newline='') as f:
                f.write(csv_file_content)

            print(f"备份成功，文件名为：{csv_filename}")

    except pymysql.MySQLError as e:
        print(f"数据库操作失败: {e}")
    finally:
        # 确保数据库连接关闭
        client.close()


if __name__ == '__main__':
    backup_mysql_data()
