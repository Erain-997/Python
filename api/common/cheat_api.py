#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/29 11:45
# @Author  : 张晓平
import requests
import time


class CheatApi(object):
    def __init__(self):
        self.url = "http://192.168.5.193:31392/frontend"

    def cheat_item(self, item_name, sess, server_id):
        if str(item_name) == "0" or item_name is None:
            return
        t = time.time()
        d = {"Sess": sess, "Num": 100, "appId": 1020, "ActId": 80007, "Ver": "3.901", "serverId": server_id,
             "actionid": 80007,
             "RetailId": 1, "T": int(t),
             "Lang": "zh-cn", "ItemId": str(item_name)}

        res = requests.post(url=self.url, json=d)
        if res.json()["Code"] != 0:
            print("作弊道具失败", item_name)

    def cheat_wive_score(self, wive_id, sess, server_id):
        d = {"Sess": sess, "IntimacyNum": 100, "CharmNum": 100, "appId": 1020, "ActId": 80006, "BeautyId": wive_id,
             "Ver": "3.901", "serverId": server_id, "actionid": 80006, "RetailId": 1, "T": 1638848666, "Lang": "zh-cn",
             }
        requests.post(url=self.url, json=d)

    def cheat_share_cd(self, sess, server_id):
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": 1638846420, "Conditions": "clearsharecd", "Lang": "zh-cn", "actionid": 19101}
        requests.post(url=self.url, json=d)

    def cheat_sky(self, sess, server_id):
        # 天下政令入驻城池
        t = time.time()
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": int(t), "Conditions": "order entry 1 2", "Lang": "zh-cn", "actionid": 19101}
        rep = requests.post(url=self.url, json=d)

    def chat_send(self, sess, server_id):
        # 聊天刷屏避免bug
        t = time.time()
        for i in range(8):
            d = {"Sess": sess, "RetailId": 1, "T": int(t), "appId": 1020, "ContainsCatEmoji": False, "ActId": 12301,
                 "Text": "123" + str(i), "DeviceId": "uibVeH265uk2", "Ver": "3.901", "serverId": server_id,
                 "Channel": "c", "actionid": 12301, "Time": "2021-12-28 11:18:59.642", "Lang": "zh-cn", "TeamId": ""}
            requests.post(url=self.url, json=d)

    def cheat_union(self, sess, server_id):
        t = time.time()
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": int(t), "Conditions": "crossWar stage startFight", "Lang": "zh-cn", "actionid": 19101}
        requests.post(url=self.url, json=d)
        time.sleep(2)
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": int(t), "Conditions": "crossWar stage next", "Lang": "zh-cn", "actionid": 19101}
        requests.post(url=self.url, json=d)
        time.sleep(2)
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": int(t), "Conditions": "crossWar join", "Lang": "zh-cn", "actionid": 19101}
        requests.post(url=self.url, json=d)

    def assist_account_register(self, server_id):
        # 用于复仇的账号
        url = "http://192.168.5.196:31496/basic_role"
        show_id = 0
        for i in range(3):
            response_assist = requests.post(url, json={
                "server_id": server_id,
                "name": "ass",
                "counsellor_id": [42]
            }, headers={
                'Content-Type': "application/json",
                'cache-control': "no-cache",
                'Postman-Token': "f42b0a9f-16a5-455d-88d5-5e873f29f2f0"
            })
            if response_assist.json().get("10000")["Code"] == 0:
                d = {"Sess": response_assist.json().get("sess"), "appId": 1020, "ActId": 10801, "Ver": "3.901",
                     "serverId": 2,
                     "RetailId": 1, "T": int(time.time()), "actionid": 10801, "Lang": "zh-cn", "ToCreate": 0}
                requests.post(url="http://192.168.5.193:31392/frontend", json=d)  # 进入竞技场场景,解锁竞技场
                show_id = response_assist.json().get("10000")["Data"]["RoleBase"]["ShowId"]
                break
        if show_id == 0:
            print("副账号注册不成功")
        return show_id

    def cheat_federation(self, sess, server_id):
        # 创建联邦以及设置上周贡献度3000
        t = time.time()
        d = {"Sess": sess, "appId": 1020, "ActId": 19103, "RetailId": 1, "Ver": "3.901", "serverId": server_id,
             "actionid": 19103, "T": int(t), "Lang": "zh-cn", "Conditions": "federation create", "isCross": True}
        url = 'http://10.6.29.84:8030/cross_server'  ##跨服作弊指令url
        requests.post(url=url, json=d)
        time.sleep(2)
        data = {"Sess": sess, "appId": 1020, "ActId": 19103, "RetailId": 1, "Ver": "3.901", "serverId": server_id,
                "actionid": 19103, "T": 1644220355,
                "Lang": "zh-cn", "Conditions": "federation setlastweekcontribution 3000", "isCross": True}
        res = requests.post(url=url, json=data)

        if res.json()["Code"] == 0:
            return True

    def cheat_federation_chat_push(self, sess, server_id):
        # 发送联邦聊天频道推送
        t = time.time()
        d = {"Sess": sess, "appId": 1020, "ActId": 19103, "RetailId": 1, "Ver": "3.901", "serverId": server_id,
             "actionid": 19103, "T": int(t), "Lang": "zh-cn", "Conditions": "federation addfederationlog",
             "isCross": True}
        url = 'http://10.6.29.84:8030/cross_server'  ##跨服作弊指令url
        req = requests.post(url=url, json=d)

    def cheat_infinite_battle(self, sess, server_id):
        # 无限征战玩家入驻
        t = time.time()
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": int(t), "Conditions": "infiniteBattle StarRole 2", "Lang": "zh-cn", "actionid": 19101}
        requests.post(url=self.url, json=d)
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": int(t), "Conditions": "infiniteBattle SpoilsLv 1 2 10", "Lang": "zh-cn",
             "actionid": 19101}
        requests.post(url=self.url, json=d)

    def cheat_feast_addrobot(self, sess, server_id, num):
        t = time.time()
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": int(t), "Conditions": "dinnerref addrobot 1 " + str(num), "Lang": "zh-cn",
             "actionid": 19101}
        requests.post(url=self.url, json=d)

    def cheat_feast_refresh(self, sess, server_id):
        t = time.time()
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": int(t), "Conditions": "dinnerref wisekingend", "Lang": "zh-cn",
             "actionid": 19101}
        requests.post(url=self.url, json=d)

    def cheat_del_feast(self, sess, server_id):
        t = time.time()
        d = {"Sess": sess, "appId": 1020, "ActId": 19101, "Ver": "3.901", "serverId": server_id,
             "RetailId": 1, "T": int(t), "Conditions": "dinnerref delalldata", "Lang": "zh-cn",
             "actionid": 19101}
        requests.post(url=self.url, json=d)
