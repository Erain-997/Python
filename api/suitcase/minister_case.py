# -*- encoding=utf8 -*-
# Time：2021/08/13
__author__ = "admin"

from api.suitcase.minister_scene import *


def run_cases(server_id, minister_id, minister_skin_id, wive_id, wive_skin_id, fashion_id, mode):
    test_run = Scene(server_id, minister_id, minister_skin_id, wive_id, wive_skin_id, fashion_id)

    if str(minister_id) != "" and str(minister_skin_id) != "" and mode == 1:
        # 大臣
        test_run.minister()
        # 郊外
        test_run.outskirts()
        # 关卡
        test_run.stage()
        # 跨服盟战
        test_run.union_fight()
        # 近卫军试炼
        test_run.guard_trial()
        # 竞技场
        test_run.arena()
        # 天下
        test_run.government()
        # 帝国书院
        test_run.imperial_academy()
        # 仓库
        test_run.use_item()
        # # 分享
        test_run.share()

    if str(wive_id) != "" and str(wive_skin_id) != "" and mode == 2:
        # # 妃子女
        test_run.harem()
        test_run.government()
        test_run.share_wive()
        test_run.use_item_wive()
        # # 妃子男
        test_run.harem_man()
        test_run.share_wive_man()
        test_run.use_item_wive_man()
        test_run.government_man()

    if str(fashion_id) != "" and mode == 3:
        # 玩家时装
        # 男苏丹形象
        test_run.fashion()  # 时装穿戴
        test_run.fashion_campaign()  # 关卡
        test_run.fashion_federation()  # 联邦大殿以及联邦奖励弹窗
        test_run.fashion_sky()  # 天下政令
        test_run.fashion_war()  # 无限征战
        test_run.fashion_feast()  # 盛宴明君推送
        test_run.fashion_arena()  # 竞技场追杀
        test_run.fashion_feast_PK()  # 宴会争抢席位

        # 女苏丹形象
        test_run.fashion_woman()  # 换成女性苏丹形象，并穿戴测试时装
        test_run.fashion_woman_campaign()  # 女苏丹关卡
        test_run.fashion_woman_federation()  # 女苏丹联邦大殿以及联邦奖励弹窗
        test_run.fashion_woman_sky()  # 女苏丹天下政令
        test_run.fashion_woman_war()  # 女苏丹无限征战

        test_run.fashion_woman_feast()  # 女苏丹宴会明君推送
        test_run.fashion_woman_arena()  # 女苏丹竞技场追杀

        test_run.fashion_woman_feast_PK()  # 女苏丹宴会争抢席位

