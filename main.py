# -*- encoding=utf8 -*-
# Time：'2022/9/30'
# __author__ = "Erain"
import base64
import os
import urllib
import numpy as np
import requests, time, json, threading, random


class Presstest(object):
    def __init__(self, press_url):
        self.press_url = press_url
        self.press_thread_num = 0

    def test_single(self):
        """压测接口"""
        global INDEX
        INDEX += 1

        global ERROR_NUM
        global TIME_LENS
        try:
            start = time.time()
            self.request(self.press_url)
            end = time.time()
            TIME_LENS.append(end - start)
            print('end')
        except Exception as e:
            print(e)
            ERROR_NUM += 1
            print(e)

    def test_task(self):
        """一次并发处理单个任务"""
        i = 0
        while i < ONE_WORKER_NUM:
            i += 1
            self.test_interface()
        time.sleep(LOOP_SLEEP)

    def request(self, url):

        count = 0

        start_time = time.time()
        requests.DEFAULT_RETRIES = 5  # 增加重试连接次数
        s = requests.session()
        s.keep_alive = False
        r = requests.post(url, headers={'Content-Type': 'application/json'}, timeout=200)
        text = json.loads(r.text)

        print("text",start_time,text,text["Time"])

    def run(self):
        """使用多线程进程并发测试"""
        t1 = time.time()
        Threads = []

        for i in range(THREAD_NUM):
            t = threading.Thread(target=self.test_onework, name="T" + str(i))
            t.setDaemon(True)
            Threads.append(t)

        for t in Threads:
            t.start()
        for t in Threads:
            t.join()
        t2 = time.time()
        print("===============压测结果===================")
        print("URL:", self.press_url)
        print("任务数量:", THREAD_NUM, "*", ONE_WORKER_NUM, "=", THREAD_NUM * ONE_WORKER_NUM)
        print("总耗时(秒):", t2 - t1)
        print("每次请求耗时(秒):", (t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM))
        print("每秒承载请求数:", 1 / ((t2 - t1) / (THREAD_NUM * ONE_WORKER_NUM)))
        print("错误数量:", ERROR_NUM)
        print(INDEX)


if __name__ == '__main__':
    press_url = "http://localhost:6060/test"
    TIME_LENS = []
    INDEX = 0
    THREAD_NUM = 50  # 并发线程总数
    ONE_WORKER_NUM = 50  # 每个线程的循环次数
    LOOP_SLEEP = 0  # 每次请求时间间隔(秒)
    ERROR_NUM = 0  # 出错数
    Presstest(press_url).test_single()
    print(TIME_LENS)
