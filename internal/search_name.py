#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/9 14:54
# @Author  : 张晓平
import pymysql


def get_search_nam(minister_id=None, minister_skin_id=None, wive_id=None, wive_skin_id=None, fashion_id=None):
    db = pymysql.connect(
        host="10.46.191.42", user="gos", passwd="123456",
        port=3306, charset='utf8', database="chuangxinsan_profile_dev"
    )
    cursor = db.cursor()
    if minister_id and minister_skin_id:
        cursor.execute(f"SELECT * FROM tcitem WHERE Id ={minister_skin_id}")
        minister_skin_name = cursor.fetchone()[1]
        cursor.execute(f"SELECT * FROM tccounsellor WHERE CounsellorId ={minister_id}")
        minister_name = cursor.fetchone()[1]
        db.close()
        return minister_name, minister_skin_name
    if wive_id and wive_skin_id:
        cursor.execute(f"SELECT * FROM tcbeauty WHERE BeautyId ={wive_id}")
        wive_name = cursor.fetchone()[2]
        cursor.execute(f"SELECT * FROM tcitem WHERE Id ={wive_skin_id}")
        wive_skin_name = cursor.fetchone()[1]
        db.close()
        return wive_name, wive_skin_name
    if fashion_id:
        cursor.execute(f"SELECT * FROM tcfashioncfg WHERE ItemId ={fashion_id}")
        fashion_name = cursor.fetchone()[1]
        db.close()
        return "时装", fashion_name


if __name__ == '__main__':
    # print(get_search_nam(24, 1642))
    print(get_search_nam(fashion_id=450))
