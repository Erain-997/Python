# -*- encoding=utf8 -*-
# Time：2021/08/13
__author__ = "admin"

from api.scene.minister_api import *


def minister_case(language, minister_name):
    # 翰林院
    imperial_academy(language, minister_name)
    # 府邸
    enter_mansion(language, minister_name)
    # 关卡（需要作弊到230601）
    enter_checkpoint(language, minister_name)
    # 校场(需要手动解锁一个位置)
    arena(language, minister_name)
    # 仓库（需要作弊资质果、百家丛书）
    treasury(language, minister_name)
    # 凌烟阁
    lingyan_pavilion(language)
    # 同盟国
    allied_nations(language, minister_name)
    # 太子府（需要作弊到明君6级，仅限皇太子）
    prince(language, minister_name)

    # 活动
    # 招募女将/清帝(测什么大臣活动就开什么大臣)
    recruitment(language, minister_name)
    # 扭蛋活动(仅限皇太子)
    twist_egg(language, minister_name)

    # 跨服活动
    # 那达慕
    nadam_fair(language, minister_name)
    # 健锐演兵
    health_sharp_play_soldiers(language, minister_name)
    # 千机迷云(可手动过掉引导)
    thousands_of_machines(language, minister_name)
    # 遗迹(前提能参加)
    ruins(language, minister_name)
    # 舌战群儒(要手动过掉引导)
    quarrel(language, minister_name)

    # 冲榜活动
    # 名臣冲榜
    rush_minister(language)
