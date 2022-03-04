#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @author: zxp
# @date: 2021/08/10


from api.scene.common.common import *
from internal.file import img_path, parent_path
from internal.tools import except_output

# 清帝
Qing_Emperor_List = ["努尔哈赤", "康熙", "道光", "皇太极", "嘉庆", "雍正", "顺治", "咸丰"]
# 女将招募
natalie_list = ["司徒羽", "慕容英", "穆兰", "南宫玉"]


@except_output()
def imperial_academy(language, minister_name):
    """
    翰林院
    :return:
    # """
    resolution = get_resolution()
    imperial_academy_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\imperial_academy_img/"
    # 一级翰林院
    touch(Template(imperial_academy_path + r"一级翰林院.png", record_pos=(0.293, 0.069),
                   resolution=resolution))
    # 二级翰林院
    touch(Template(imperial_academy_path + r"二级翰林院.png", record_pos=(-0.129, -0.033),
                   resolution=resolution))
    # 品质页签
    if exists(Template(imperial_academy_path + r"品质.png", record_pos=(-0.46, -0.082), resolution=resolution)):
        touch(
            Template(imperial_academy_path + r"品质.png", record_pos=(-0.46, -0.082), resolution=resolution))
    # 滑动且选择大臣
    swipe_func(imperial_academy_path, "大臣列表下拉(农)", (-0.253, 0.225), [-0.0016, -0.3512], minister_name, (-0.176, -0.034))

    time.sleep(1)
    snapshot(filename=img_path() + r"大臣详情页.png", msg="大臣详情页", quality=99)
    # 皮肤
    touch(Template(imperial_academy_path + r"皮肤按钮.png", record_pos=(0.452, -0.106), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"皮肤页签.png", msg="大臣详情页", quality=99)
    # 进入皮肤故事
    touch(Template(imperial_academy_path + r"故事按钮.png", record_pos=(-0.448, 0.166), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"皮肤故事详情页.png", msg="大臣详情页", quality=99)
    # 关闭故事
    square_off(language)
    max_return_kay(language)
    # 大臣简介
    touch(Template(imperial_academy_path + r"详情按钮.png", record_pos=(0.471, -0.037),
                   resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"大臣简介头像.png", msg="大臣详情页", quality=99)
    touch(Template(imperial_academy_path + r"列表.png", record_pos=(-0.478, -0.036),
                   resolution=resolution))
    # 退出二级翰林院
    min_return_kay(language)

    if minister_name == "皇太子":
        max_return_kay(language)
        return

    # 进入天禄琳酿
    touch(Template(imperial_academy_path + r"天禄琳酿.png", record_pos=(-0.408, -0.036), resolution=resolution))
    # 品质页签
    if exists(Template(imperial_academy_path + r"品质.png", record_pos=(-0.46, -0.082), resolution=resolution)):
        touch(
            Template(imperial_academy_path + r"品质.png", record_pos=(-0.465, -0.081), resolution=resolution))
    # 选择大臣
    swipe_func(imperial_academy_path, "大臣列表下拉(木头)", (-0.239, 0.214), [-0.0016, -0.3512], minister_name,
               (-0.176, -0.034))

    time.sleep(1)
    snapshot(filename=img_path() + r"天禄琳琅-大臣展示.png", msg="翰林院天禄琳琅", quality=99)
    # 查看详情
    touch(Template(imperial_academy_path + r"详情.png", record_pos=(0.454, -0.037), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"天禄琳琅-大臣头像.png", msg="翰林院天禄琳琅", quality=99)
    # 大臣简介
    touch(Template(imperial_academy_path + r"大臣简介.png", record_pos=(0.085, -0.159), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"天禄琳琅-大臣简介.png", msg="翰林院天禄琳琅", quality=99)
    square_off(language)
    # 悟性顿悟
    touch(Template(imperial_academy_path + r"悟性.png", record_pos=(0.451, -0.078), resolution=resolution))
    # touch(Template(imperial_academy_path + r"顿悟.png", record_pos=(0.229, -0.038),resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"天禄琳琅-顿悟.png", msg="翰林院天禄琳琅", quality=99)

    # 退出天禄琳酿
    min_return_kay(language)

    # TODO 英文版本的字体大小不一样，导致无法识别
    # 进入军机处
    touch(Template(imperial_academy_path + r"军机处.png", record_pos=(0.456, -0.033), resolution=resolution))
    touch(Template(imperial_academy_path + r"点击开始选择.png", record_pos=(-0.373, 0.099), resolution=resolution))
    swipe_func(imperial_academy_path, "大臣列表左滑", (0.343, 0.143), [-0.2969, -0.0069], minister_name, (-0.176, -0.034))
    time.sleep(1)
    snapshot(filename=img_path() + r"派遣大臣卡牌.png", msg="翰林院-军机处", quality=99)

    # 退出军机处
    min_return_kay(language)
    min_return_kay(language)

    # 退出翰林院
    max_return_kay(language)


@except_output()
def enter_mansion(language):
    """
    进入府邸
    :return:
    """
    resolution = get_resolution()
    mansion_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\mansion_img/"
    swipe(Template(mansion_path + r"swipe_mansion.png", record_pos=(-0.029, -0.022), resolution=resolution),
          vector=[-0.1744, -0.0058])
    touch(Template(mansion_path + r"enter_mansion.png", record_pos=(0.477, -0.03), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"府邸气泡(中间).png", msg="大臣详情页", quality=99)
    # if minister_name == "上官璃":
    #     # 府邸内部
    #     touch(Template(mansion_path + r"mansion_internal.png", record_pos=(-0.192, -0.008), resolution=resolution))
    # elif minister_name == "康熙":
    #     touch(Template(mansion_path + r"康熙府邸.png", record_pos=(-0.416, 0.071), resolution=resolution))
    # elif minister_name == "努尔哈赤":
    #     touch(Template(mansion_path + r"努尔哈赤府邸.png", record_pos=(0.295, -0.222), resolution=resolution))
    # elif minister_name == "道光":
    #     touch(Template(mansion_path + r"道光府邸.png", record_pos=(-0.221, 0.174), resolution=resolution))
    # time.sleep(1)
    # snapshot(filename=img_path() + r"府主头像.png", msg="大臣详情页", quality=99)
    # max_return_kay(language)

    # 查看府邸左边的大臣
    swipe(Template(mansion_path + r"府邸左滑.png", record_pos=(0.158, 0.074), resolution=resolution),
          vector=[0.2372, -0.5683])
    time.sleep(1)
    snapshot(filename=img_path() + r"府邸气泡(左下).png", msg="大臣详情页", quality=99)
    max_return_kay(language)
    # 查看府邸右边的大臣
    touch(Template(mansion_path + r"enter_mansion.png", record_pos=(0.477, -0.03), resolution=resolution))
    time.sleep(1)
    swipe(Template(mansion_path + r"府邸右滑.png", record_pos=(0.384, -0.24), resolution=resolution),
          vector=[-0.831, 0.3444])
    time.sleep(1)
    snapshot(filename=img_path() + r"府邸气泡(右上).png", msg="大臣详情页", quality=99)

    max_return_kay(language)


@except_output()
def enter_checkpoint(language, minister_name):
    """
    关卡
    :return:
    """
    resolution = get_resolution()
    checkpoint_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\checkpoint_img/"
    out_palace(language)
    touch(Template(checkpoint_path + r"enter_checkpoint.png", record_pos=(0.26, 0.121), resolution=resolution))
    # 23章回京风波头目
    touch(Template(checkpoint_path + r"boss.png", record_pos=(0.396, -0.153),
                   resolution=resolution),
          timeout=200)
    time.sleep(1)
    # 更换大臣

    touch(Template(checkpoint_path + r"checkpoint_replace.png", record_pos=(0.262, 0.205),
                   resolution=resolution))
    swipe_func(checkpoint_path, "大臣列表下拉", (-0.308, 0.175), [-0.0031, -0.4097], minister_name, (-0.245, -0.136))

    time.sleep(1)
    snapshot(filename=img_path() + r"关卡更换大臣.png", msg="关卡更换大臣", quality=99)
    touch(Template(checkpoint_path + r"checkpoint_dispatch.png", record_pos=(0.323, 0.165),
                   resolution=resolution))
    time.sleep(0.5)
    snapshot(filename=img_path() + r"boss大臣.png", msg="boss大臣", quality=99)
    # 返回界面
    max_return_kay(language)
    min_return_kay(language)
    return_palace(language)


@except_output()
def arena(language, minister_name):
    """
    竞技场
    :return:
    """
    resolution = get_resolution()
    arena_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\arena_img/"
    out_palace(language)
    # 进入校场
    touch(Template(arena_path + r"enter_arena.png", record_pos=(-0.058, 0.115),
                   resolution=resolution))
    if exists(Template(arena_path + r"关闭窗口.png", record_pos=(0.426, -0.172), resolution=resolution)):
        touch(Template(arena_path + r"关闭窗口.png", record_pos=(0.426, -0.172), resolution=resolution))
    # 抓捕叛军
    touch(Template(arena_path + r"抓捕叛军.png", record_pos=(-0.271, 0.033), resolution=resolution))
    touch(Template(arena_path + r"抓捕.png", record_pos=(-0.22, 0.131), resolution=resolution))
    # 找到大臣
    swipe_func(arena_path, "大臣列表下拉(公爵)", (-0.207, 0.105), [-0.0008, -0.2616], minister_name, (-0.176, -0.034))

    sleep(1)
    snapshot(filename=img_path() + r"叛军抓捕派遣.png", msg="叛军抓捕派遣", quality=99)
    # 关闭派遣窗口
    touch(Template(arena_path + r"关闭派遣窗口.png", record_pos=(0.426, -0.172), resolution=resolution))
    max_return_kay(language)
    # 免战
    touch(Template(arena_path + r"进入免战.png", record_pos=(0.433, 0.012), resolution=resolution))
    # 点击免战
    touch(Template(arena_path + r"点击免战.png", record_pos=(-0.331, 0.207), resolution=resolution))
    # 降序
    touch(Template(arena_path + r"点击降序.png", record_pos=(-0.453, -0.188), resolution=resolution))
    # 找到大臣
    swipe_func(arena_path, "大臣列表下拉(公爵)", (-0.207, 0.105), [-0.0008, -0.2616], minister_name, (-0.245, -0.136))
    sleep(1)
    snapshot(filename=img_path() + r"免战派遣界面.png", msg="免战派遣", quality=99)
    # 免战派遣
    touch(Template(arena_path + r"点击免战.png", record_pos=(-0.32, 0.206), resolution=resolution))
    time.sleep(1.5)
    snapshot(filename=img_path() + r"免战界面.png", msg="免战界面", quality=99)
    # 召回
    touch(Template(arena_path + r"召回.png", record_pos=(-0.323, 0.209), resolution=resolution))
    touch(Template(arena_path + r"确认.png", record_pos=(0.11, 0.044), resolution=resolution))

    max_return_kay(language)
    max_return_kay(language)
    return_palace(language)


@except_output()
def treasury(language, minister_name):
    """
    国库
    :return:
    """
    resolution = get_resolution()
    treasury_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\treasury_img/"
    sleep(1)
    touch(Template(treasury_path + r"国库.png", record_pos=(-0.025, 0.236), resolution=resolution))
    touch(Template(treasury_path + r"百家丛书赏赐.png", record_pos=(0.27, 0.164), resolution=resolution))
    # 找到大臣
    swipe_func(treasury_path, "大臣列表下拉(公爵)", (-0.207, 0.105), [-0.0008, -0.2616], minister_name, (-0.353, -0.129))
    snapshot(filename=img_path() + r"国库赏赐.png", msg="国库赏赐", quality=99)
    close_hero(language)
    # 资质果
    touch(Template(treasury_path + r"资质果.png", record_pos=(-0.37, 0.148), resolution=resolution))
    use_button(language)
    # 找到大臣
    swipe_func(treasury_path, "大臣列表下拉(公爵)", (-0.207, 0.105), [-0.0008, -0.2616], minister_name, (-0.353, -0.129))
    snapshot(filename=img_path() + r"资质使用.png", msg="资质使用", quality=99)

    close_hero(language)
    min_return_kay(language)


@except_output()
def lingyan_pavilion(language):
    """
    凌烟阁
    :return:
    """
    resolution = get_resolution()
    lingyan_pavilion_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\lingyan_pavilion_img/"
    swipe(Template(lingyan_pavilion_path + r"主界面左移.png", record_pos=(0.028, 0.122), resolution=resolution),
          vector=[0.2822, -0.0046])
    # 图鉴
    touch(Template(lingyan_pavilion_path + r"凌烟阁.png", record_pos=(-0.075, -0.121), resolution=resolution))
    touch(Template(lingyan_pavilion_path + r"已拥有.png", record_pos=(0.026, 0.205), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"/图鉴.png", msg="凌烟阁", quality=99)

    max_return_kay(language)


@except_output()
def recruitment(language, minister_name):
    if minister_name not in natalie_list:
        return
    """
    招募活动-女将/清帝
    :return:
    """
    recruitment_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\recruitment_img/"
    resolution = get_resolution()
    # 女将
    if minister_name in natalie_list:
        # 进入招募活动
        if exists(Template(recruitment_path + r"招募活动.png", record_pos=(0.271, -0.012), resolution=resolution)):
            touch(Template(recruitment_path + r"招募活动.png", record_pos=(0.271, -0.012), resolution=resolution))
        else:
            open_activity(language)
            touch(Template(recruitment_path + r"招募活动.png", record_pos=(0.271, -0.012), resolution=resolution))
        touch(Template(recruitment_path + r"巾帼女将.png", record_pos=(-0.209, 0.102), resolution=resolution))
        time.sleep(1)
        snapshot(filename=img_path() + r"招募界面.png", msg="招募活动-女将", quality=99)
        # 女将界面
        touch(
            Template(recruitment_path + fr"{minister_name}.png", record_pos=(-0.404, -0.079), resolution=resolution))
        time.sleep(1)
        snapshot(filename=img_path() + r"女将界面.png", msg="招募活动-女将", quality=99)
        # 强化界面
        touch(Template(recruitment_path + r"强化.png", record_pos=(0.249, 0.197), resolution=resolution))
        time.sleep(1)
        snapshot(filename=img_path() + r"女将界面.png", msg="招募活动-女将", quality=99)

        max_return_kay(language)
        max_return_kay(language)
        max_return_kay(language)
        max_return_kay(language)
        close_activity(language)
    # 清帝
    elif minister_name in Qing_Emperor_List:
        if exists(Template(recruitment_path + r"招募活动.png", record_pos=(0.271, -0.012), resolution=resolution)):
            touch(Template(recruitment_path + r"招募活动.png", record_pos=(0.271, -0.012), resolution=resolution))
        else:
            open_activity(language)
            touch(Template(recruitment_path + r"招募活动.png", record_pos=(0.271, -0.012), resolution=resolution))
        touch(Template(recruitment_path + r"清帝.png", record_pos=(-0.003, 0.102), resolution=resolution))
        # 清帝界面
        touch(
            Template(recruitment_path + fr"{minister_name}.png", record_pos=(-0.404, -0.079), resolution=resolution))
        time.sleep(1)
        snapshot(filename=img_path() + r"清帝招募界面.png", msg="招募活动-清帝", quality=99)

        touch(Template(recruitment_path + r"前往强化.png", record_pos=(0.268, 0.218), resolution=resolution))
        time.sleep(1)
        snapshot(filename=img_path() + r"清帝强化界面.png", msg="招募活动-清帝", quality=99)
        max_return_kay(language)
        max_return_kay(language)
        max_return_kay(language)
        close_activity(language)
    else:
        return


@except_output()
def nadam_fair(language, minister_name):
    """
    那达慕
    :return:
    """
    resolution = get_resolution()
    nadam_fair_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\nadam_fair_img/"
    # 打开跨服活动列表
    open_cross_activity(language)
    # 进入招募活动
    count = 1
    while not exists(Template(nadam_fair_path + r"那达慕.png", record_pos=(0.056, -0.146), resolution=resolution)):
        left_cross_activity(language)
        count += 1
        if count == 5:
            # 找不着，返回主界面
            max_return_kay(language)
            return

    touch(Template(nadam_fair_path + r"那达慕.png", record_pos=(0.056, -0.146), resolution=resolution))
    # 首次进入有动画
    if not exists(Template(nadam_fair_path + r"参加大会.png", record_pos=(-0.003, -0.027), resolution=resolution)):
        for i in range(5):
            touch(Template(nadam_fair_path + r"蓝天.png", record_pos=(-0.029, -0.277), resolution=resolution))
    # 秘宝商铺
    if minister_name in Qing_Emperor_List:
        # 秘宝商铺
        touch(Template(nadam_fair_path + r"秘宝商铺.png", record_pos=(0.056, -0.146), resolution=resolution))
        if exists(Template(nadam_fair_path + r"加号.png", record_pos=(-0.253, -0.043), resolution=resolution)):
            touch(Template(nadam_fair_path + r"加号.png", record_pos=(-0.253, -0.043), resolution=resolution))
            time.sleep(1)
            snapshot(filename=img_path() + r"秘宝商铺--选择奖励.png", msg="那达慕", quality=99)
        # 选择大臣
        if exists(
                Template(nadam_fair_path + fr"{minister_name}.png", record_pos=(-0.084, 0.011), resolution=resolution)):
            touch(
                Template(nadam_fair_path + fr"{minister_name}.png", record_pos=(-0.084, 0.011), resolution=resolution))
            touch(Template(nadam_fair_path + r"选择.png", record_pos=(0.18, 0.193), resolution=resolution))
            touch(Template(nadam_fair_path + r"关闭窗口.png", record_pos=(0.426, -0.172), resolution=resolution))
        time.sleep(1)
        snapshot(filename=img_path() + r"秘宝商铺.png", msg="那达慕", quality=99)
        max_return_kay(language)
    # 进入大会
    touch(Template(nadam_fair_path + r"参加大会.png", record_pos=(-0.003, -0.027), resolution=resolution))
    if exists(Template(nadam_fair_path + r"加号.png", record_pos=(-0.253, -0.043), resolution=resolution)):
        touch(Template(nadam_fair_path + r"加号.png", record_pos=(-0.253, -0.043), resolution=resolution))
    else:
        touch(Template(nadam_fair_path + r"更换大臣.png", record_pos=(-0.249, 0.159), resolution=resolution))

    # 找到大臣
    swipe_func(nadam_fair_path, "大臣列表下拉(公爵)", (-0.209, 0.171), [0.0008, -0.4954], minister_name, (-0.176, -0.034))
    time.sleep(1)
    snapshot(filename=img_path() + r"派遣大臣界面.png", msg="那达慕大会", quality=99)
    # 委派大臣
    touch(Template(nadam_fair_path + fr"{minister_name}.png", record_pos=(-0.139, -0.136), resolution=resolution))
    if exists(Template(nadam_fair_path + r"委派.png", record_pos=(0.313, 0.175), resolution=resolution)):
        touch(Template(nadam_fair_path + r"委派.png", record_pos=(0.313, 0.175), resolution=resolution))
    else:
        touch(Template(nadam_fair_path + r"关闭窗口.png", record_pos=(0.426, -0.172), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"搜索界面.png", msg="那达慕大会", quality=99)
    # 寻宝
    touch(Template(nadam_fair_path + r"寻宝.png", record_pos=(0.277, 0.241), resolution=resolution))
    if exists(Template(nadam_fair_path + r"关闭窗口.png", record_pos=(0.426, -0.172), resolution=resolution)):
        touch(Template(nadam_fair_path + r"关闭窗口.png", record_pos=(0.426, -0.172), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"寻宝.png", msg="那达慕大会", quality=99)
    max_return_kay(language)

    max_return_kay(language)
    max_return_kay(language)
    max_return_kay(language)


@except_output()
def thousands_of_machines(language, minister_name):
    """
    千机迷云
    :return:
    """
    resolution = get_resolution()

    thousands_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\thousandsOfMachines_img/"
    open_cross_activity(language)
    sleep(1)
    if not exists(Template(thousands_path + r"千机迷云文字.png", record_pos=(0.091, -0.224), resolution=resolution)):
        left_cross_activity(language)
    touch(Template(thousands_path + r"千机迷云文字.png", record_pos=(0.091, -0.224), resolution=resolution))
    while not exists(Template(thousands_path + r"千机机关阵弩车.png", record_pos=(-0.381, -0.264), resolution=resolution)):
        touch(Template(thousands_path + r"千机山顶的树.png", record_pos=(-0.381, -0.264), resolution=resolution))
        if exists(Template(thousands_path + r"千机联盟弹窗.png", record_pos=(-0.381, -0.264), resolution=resolution)):
            touch(Template(thousands_path + r"千机联盟弹窗.png", record_pos=(-0.381, -0.264), resolution=resolution))
        if exists(Template(thousands_path + r"千机特殊奖励提示.png", record_pos=(0.316, -0.16), resolution=resolution)):
            touch(Template(thousands_path + r"千机特殊奖励提示.png", record_pos=(0.316, -0.16), resolution=resolution))

    touch(Template(thousands_path + r"千机机关阵弩车.png", record_pos=(0.091, -0.224), resolution=resolution))

    if exists(Template(thousands_path + r"千机确认按钮.png", record_pos=(-0.203, 0.106), resolution=resolution)):
        touch(Template(thousands_path + r"千机体力提示.png", record_pos=(-0.203, 0.106), resolution=resolution))
        touch(Template(thousands_path + r"千机确认按钮.png", record_pos=(-0.203, 0.106), resolution=resolution))

    if exists(Template(thousands_path + r"千机更换大臣按钮.png", record_pos=(0.091, -0.224), resolution=resolution)):
        # 到此处应进入消消乐界面
        touch(Template(thousands_path + r"千机更换大臣按钮.png", record_pos=(0.091, -0.224), resolution=resolution))

    time.sleep(1)
    touch(Template(thousands_path + r"千机英雄列表升序按钮.png", record_pos=(0.313, 0.179), resolution=resolution))

    swipe_func(thousands_path, "千机悟性", (-0.257, 0.181), [0.0039, -0.3118], minister_name, (-0.243, 0.145))

    snapshot(filename=img_path() + r"千机迷云-选大臣界面.png", msg="千机迷云-选人", quality=99)
    time.sleep(1)

    touch(Template(thousands_path + r"千机派遣按钮.png", record_pos=(0.313, 0.179), resolution=resolution))
    time.sleep(1)
    if exists(Template(thousands_path + r"千机消消乐提示.png", record_pos=(0.091, -0.224), resolution=resolution)):
        # 如果这个提示存在, 则需要过新手引导, 新手引导这边未经验证, 不一定好使
        swipe(Template(thousands_path + r"千机锁头.png", record_pos=(0.007, -0.219), resolution=resolution),
              vector=[0.0008, 0.1395])
        time.sleep(6)
        max_return_kay(language)
        time.sleep(1)
        max_return_kay(language)
        time.sleep(1)
        max_return_kay(language)
        swipe(Template(thousands_path + r"千机白玉球.png", record_pos=(0.124, -0.158), resolution=resolution),
              vector=[0.1101, 0.0012])
        time.sleep(7)
        swipe(Template(thousands_path + r"千机白玉球.png", record_pos=(0.124, -0.158), resolution=resolution),
              vector=[0.1101, 0.0012])
        time.sleep(7)
        swipe(Template(thousands_path + r"千机鲁班锁.png", record_pos=(-0.05, 0.072), resolution=resolution),
              vector=[0.1186, 0.0047])
        time.sleep(7)
        swipe(Template(thousands_path + r"千机白玉球.png", record_pos=(0.124, -0.158), resolution=resolution),
              vector=[0.1101, 0.0012])
        time.sleep(7)
        swipe(Template(thousands_path + r"千机鲁班锁.png", record_pos=(-0.169, 0.013), resolution=resolution),
              vector=[0.1186, 0.0047])
        max_return_kay(language)

    snapshot(filename=img_path() + r"千机迷云-消消乐界面.png", msg="千机迷云-消消乐界面", quality=99)
    max_return_kay(language)
    touch(Template(thousands_path + r"千机活跃奖励按钮.png", record_pos=(0.313, 0.179), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"千机迷云-活跃奖励界面.png", msg="千机迷云-活跃奖励界面", quality=99)
    # 返回到主场景
    max_return_kay(language)
    max_return_kay(language)
    max_return_kay(language)


@except_output()
def ruins(language, minister_name):
    """
    遗迹
    :return:
    """
    resolution = get_resolution()
    ruins_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\ruins_img/"
    # 打开跨服活动列表
    open_cross_activity(language)
    # 进入招募活动
    count = 1
    while not exists(Template(ruins_path + r"遗迹.png", record_pos=(0.084, -0.145), resolution=resolution)):
        left_cross_activity(language)
        count += 1
        if count == 5:
            # 找不着，返回主界面
            max_return_kay(language)
            return
    touch(Template(ruins_path + r"遗迹.png", record_pos=(0.084, -0.145), resolution=resolution))
    touch(Template(ruins_path + r"前往遗迹.png", record_pos=(-0.003, 0.012), resolution=resolution))
    # 首次进入派遣名臣
    if exists(Template(ruins_path + r"问号.png", record_pos=(-0.41, -0.208), resolution=resolution)):
        touch(Template(ruins_path + r"问号.png", record_pos=(-0.41, -0.208), resolution=resolution))
        swipe_func(ruins_path, "大臣列表下拉(公爵)", (-0.209, 0.171), [0.0008, -0.4954], minister_name, (-0.139, -0.136))
        time.sleep(1)
        snapshot(filename=img_path() + r"派遣名臣.png", msg="跨服/本服遗迹", quality=99)
        # 派遣大臣头像-搜索界面
        touch(Template(ruins_path + r"派遣按钮.png", record_pos=(0.322, 0.17), resolution=resolution))
        time.sleep(1)
        snapshot(filename=img_path() + r"派遣大臣头像.png", msg="跨服/本服遗迹", quality=99)
        # 派遣大臣头像-地图界面
        max_return_kay(language)
    time.sleep(1)
    snapshot(filename=img_path() + r"派遣大臣头像(地图).png", msg="跨服/本服遗迹", quality=99)
    # 派遣大臣头像-搜索界面
    touch(Template(ruins_path + r"头像.png", record_pos=(0.199, -0.081), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"派遣大臣头像.png", msg="跨服/本服遗迹", quality=99)

    max_return_kay(language)
    max_return_kay(language)
    max_return_kay(language)
    max_return_kay(language)


@except_output()
def rush_minister(language):
    """
    名臣冲榜
    :return:
    """
    resolution = get_resolution()
    rush_minister_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\rush_minister_img/"
    # 进入活动
    open_rush_activity(language)
    touch(Template(rush_minister_path + r"名臣冲榜.png", record_pos=(-0.391, -0.149), resolution=resolution))
    touch(Template(rush_minister_path + r"进入活动.png", record_pos=(0.369, 0.161), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"指定名臣冲榜.png", msg="名臣冲榜", quality=99)
    # 查看排行
    touch(Template(rush_minister_path + r"排行奖励.png", record_pos=(0.446, 0.24), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"排行榜界面.png", msg="名臣冲榜", quality=99)

    touch(Template(rush_minister_path + r"关闭窗口.png", record_pos=(0.426, -0.172), resolution=resolution))
    max_return_kay(language)
    close_rush_activity(language)


@except_output()
def prince(language, minister_name):
    """
    太子府
    :return:
    """
    if minister_name == "皇太子":
        resolution = get_resolution()
        prince_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\prince_img/"
        touch(Template(prince_path + r"进入上书房.png", record_pos=(0.209, -0.063), resolution=resolution))
        touch(Template(prince_path + r"进入太子府.png", record_pos=(0.16, -0.083), resolution=resolution))
        time.sleep(1)
        snapshot(filename=img_path() + r"太子府界面.png", msg="太子府-太子皮肤", quality=99)
        max_return_kay(language)
        max_return_kay(language)


@except_output()
def allied_nations(language, minister_name):
    """
    同盟国(盟国副本)
    :return:
    """
    resolution = get_resolution()
    allied_nations_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\allied_nations_img/"
    # 进入同盟国
    out_palace(language)
    touch(Template(allied_nations_path + r"同盟国.png", record_pos=(0.132, -0.051), resolution=resolution))
    touch(Template(allied_nations_path + r"盟国副本.png", record_pos=(0.429, -0.047), resolution=resolution))
    if exists(Template(allied_nations_path + r"前往.png", record_pos=(0.098, 0.143), resolution=resolution)):
        touch(Template(allied_nations_path + r"前往.png", record_pos=(0.098, 0.143), resolution=resolution))
    else:
        return
    # 更换大臣
    if exists(Template(allied_nations_path + r"我的大臣.png", record_pos=(-0.265, 0.144), resolution=resolution)):
        touch(Template(allied_nations_path + r"我的大臣.png", record_pos=(-0.265, 0.144), resolution=resolution))
        swipe_func(allied_nations_path, "大臣列表左滑", (0.343, 0.143), [-0.2969, -0.0069], minister_name, (-0.176, -0.034))
        time.sleep(1)
        snapshot(filename=img_path() + r"盟国副本-替换大臣.png", msg="同盟国", quality=99)
        time.sleep(1)
        max_return_kay(language)
        time.sleep(1)
        touch(Template(allied_nations_path + r"关闭窗口(红白).png", record_pos=(0.452, -0.245), resolution=resolution))
        # 组队详情
        touch(Template(allied_nations_path + r"组队详情.png", record_pos=(-0.446, 0.236), resolution=resolution))
        time.sleep(1)
        snapshot(filename=img_path() + r"盟国副本-组队详情.png", msg="同盟国", quality=99)
        touch(Template(allied_nations_path + r"关闭窗口.png", record_pos=(0.426, -0.172), resolution=resolution))
    else:
        # 首次进入，创建队伍，选择大臣
        touch(Template(allied_nations_path + r"创建队伍.png", record_pos=(0.348, 0.236), resolution=resolution))
        touch(Template(allied_nations_path + r"确定.png", record_pos=(0.11, 0.064), resolution=resolution))
        touch(Template(allied_nations_path + r"加号.png", record_pos=(-0.268, 0.022), resolution=resolution))
        touch(Template(allied_nations_path + r"上官璃.png", record_pos=(0.343, 0.143), resolution=resolution))
        touch(Template(allied_nations_path + r"派遣.png", record_pos=(0.419, 0.19), resolution=resolution))
        touch(Template(allied_nations_path + r"确定.png", record_pos=(0.11, 0.064), resolution=resolution))
        touch(Template(allied_nations_path + r"真正创建队伍.png", record_pos=(-0.004, 0.139), resolution=resolution))
        sleep(3)
        touch(Template(allied_nations_path + r"关闭窗口(红白).png", record_pos=(0.426, -0.172), resolution=resolution))
    # 组队
    swipe(Template(allied_nations_path + "同盟副本左滑.png", record_pos=(0.102, -0.225), resolution=resolution),
          vector=[-0.5713, -0.0278])
    touch(Template(allied_nations_path + r"前往.png", record_pos=(0.098, 0.143), resolution=resolution))
    if exists(Template(allied_nations_path + r"创建队伍.png", record_pos=(0.348, 0.236), resolution=resolution)):
        # 创建队伍，选择大臣
        touch(Template(allied_nations_path + r"创建队伍.png", record_pos=(0.348, 0.236), resolution=resolution))
        touch(Template(allied_nations_path + r"确定.png", record_pos=(0.11, 0.064), resolution=resolution))
        touch(Template(allied_nations_path + r"加号.png", record_pos=(-0.268, 0.022), resolution=resolution))
        swipe_func(allied_nations_path, "大臣列表左滑", (0.343, 0.143), [-0.2969, -0.0069], minister_name, (-0.176, -0.034))
        time.sleep(1)
        snapshot(filename=img_path() + r"盟国副本-创队.png", msg="同盟国", quality=99)

        max_return_kay(language)
        time.sleep(0.5)
        touch(Template(allied_nations_path + r"关闭窗口(红白).png", record_pos=(0.426, -0.172), resolution=resolution))
        time.sleep(0.5)
        touch(Template(allied_nations_path + r"关闭窗口(红白).png", record_pos=(0.426, -0.172), resolution=resolution))
        max_return_kay(language)
        max_return_kay(language)
        return_palace(language)
    else:
        max_return_kay(language)
        max_return_kay(language)
        return_palace(language)


@except_output()
def health_sharp_play_soldiers(language, minister_name):
    """
    健锐演兵
    :return:
    """
    resolution = get_resolution()
    health_sharp_play_soldiers_path = parent_path(
        __file__) + f"\\language\\{language}\\minister" + r"\health_sharp_play_soldiers_img/"

    # 打开跨服活动列表
    open_cross_activity(language)
    # 进入招募活动
    count = 1
    while not exists(
            Template(health_sharp_play_soldiers_path + r"健锐演兵.png", record_pos=(0.161, -0.147), resolution=resolution)):
        left_cross_activity(language)
        count += 1
        if count == 5:
            # 找不着，返回主界面
            max_return_kay(language)
            return
    # 进入健锐演兵
    touch(Template(health_sharp_play_soldiers_path + r"健锐演兵.png", record_pos=(0.161, -0.147), resolution=resolution))
    time.sleep(1)
    if exists(
            Template(health_sharp_play_soldiers_path + r"关闭弹窗.png", record_pos=(0.295, -0.184), resolution=resolution)):
        touch(
            Template(health_sharp_play_soldiers_path + r"关闭弹窗.png", record_pos=(0.295, -0.184), resolution=resolution))

    if exists(Template(health_sharp_play_soldiers_path + r"进入活动.png", record_pos=(-0.007, -0.027),
                       resolution=resolution)):
        touch(
            Template(health_sharp_play_soldiers_path + r"进入活动.png", record_pos=(-0.007, -0.027), resolution=resolution))

    if exists(
            Template(health_sharp_play_soldiers_path + r"新手引导.png", record_pos=(0.366, -0.224), resolution=resolution)):
        touch(
            Template(health_sharp_play_soldiers_path + r"新手引导.png", record_pos=(0.366, -0.224), resolution=resolution))

    if exists(Template(health_sharp_play_soldiers_path + r"更换大臣.png", record_pos=(-0.454, -0.219),
                       resolution=resolution)):
        touch(
            Template(health_sharp_play_soldiers_path + r"更换大臣.png", record_pos=(-0.454, -0.219), resolution=resolution))
    time.sleep(1)
    # # 找到大臣
    swipe_func(health_sharp_play_soldiers_path, "滑动大臣列表", (-0.266, 0.167), [0.0039, -0.1921], minister_name,
               (-0.353, -0.129))
    time.sleep(1)
    snapshot(filename=img_path() + r"健锐演兵-派遣大臣界面.png", msg="派遣大臣", quality=99)
    touch(Template(health_sharp_play_soldiers_path + r"委派大臣.png", record_pos=(0.31, 0.174), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"健锐演兵-大臣头像.png", msg="大臣头像", quality=99)
    touch(Template(health_sharp_play_soldiers_path + r"活跃奖励.png", record_pos=(0.45, 0.237), resolution=resolution))
    time.sleep(1)
    snapshot(filename=img_path() + r"健锐演兵-活跃奖励.png", msg="活跃奖励", quality=99)

    max_return_kay(language)
    max_return_kay(language)
    max_return_kay(language)
    max_return_kay(language)


@except_output()
def twist_egg(language, minister_name):
    """
    扭蛋活动
    这玩意是针对皇太子的
    :return:
    """
    if "太子" not in minister_name:
        return
    resolution = get_resolution()
    twist_egg_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\twist_egg_img/"

    open_activity(language)
    touch(Template(twist_egg_path + r"扭蛋春节活动.png", record_pos=(0.255, 0.088), resolution=resolution))
    touch(Template(twist_egg_path + r"扭蛋万岁庆典入口.png", record_pos=(-0.058, -0.092), resolution=resolution))
    touch(Template(twist_egg_path + r"扭蛋进入活动按钮.png", record_pos=(-0.023, -0.011), resolution=resolution))
    snapshot(filename=img_path() + r"扭蛋活动-太子形象.png", msg="扭蛋活动", quality=99)
    max_return_kay(language)
    max_return_kay(language)
    max_return_kay(language)


@except_output()
def quarrel(language, minister_name):
    # 舌战群儒
    resolution = get_resolution()

    quarrel_path = parent_path(__file__) + f"\\language\\{language}\\minister" + r"\quarrel_img/"

    open_cross_activity(language)
    if not exists(Template(quarrel_path + r"舌战群儒文字.png", record_pos=(0.239, -0.139), resolution=resolution)):
        left_cross_activity(language)
    touch(Template(quarrel_path + r"舌战群儒文字.png", record_pos=(0.239, -0.139), resolution=resolution))
    for i in range(8):
        if not exists(Template(quarrel_path + r"舌战群儒进入活动按钮.png", record_pos=(-0.005, -0.022), resolution=resolution)):
            touch(Template(quarrel_path + r"舌战群儒山顶.png", record_pos=(0.035, -0.199), resolution=resolution))
        else:
            touch(Template(quarrel_path + r"舌战群儒进入活动按钮.png", record_pos=(0.239, -0.139), resolution=resolution))
            break
    touch(Template(quarrel_path + r"舌战群儒随便一个书院.png", record_pos=(0.192, 0.071), resolution=resolution))
    touch(Template(quarrel_path + r"舌战群儒驻学按钮.png", record_pos=(0.115, 0.099), resolution=resolution))
    # 横向英雄列表滑动找到指定英雄且点击

    count_num = 0
    while not exists_imperial(quarrel_path, fr"{minister_name}.png", resolution):
        swipe(Template(quarrel_path + r"舌战群儒大臣列表滑动.png", record_pos=(0.347, 0.128), resolution=(1290, 853)),
              vector=[-0.4868, -0.0035])
        count_num += 1
        if count_num == 15:
            break
    touch(Template(quarrel_path + fr"{minister_name}.png", record_pos=(0.115, 0.099), resolution=resolution))
    snapshot(filename=img_path() + r"舌战群儒-驻学队列.png", msg="舌战群儒", quality=99)

    # 且保证选择了5个英雄
    # 下方是保证选择一共选择5个英雄, 达到五个就点击开始驻学-> 后边的流程涉及向作弊器中输入且执行命令, 有丢丢困难
    # # 滑到列表起点
    # while not exists_imperial(quarrel_path, r"独孤梦.png", resolution):
    #     swipe(Template(quarrel_path + r"舌战群儒大臣列表滑动.png", record_pos=(-0.488, 0.129), resolution=(1290, 853)),
    #     vector=[0.8318, -0.0023])
    #     count_num += 1
    #     if count_num == 15:
    #         break
    # name_list = ["独孤梦", "芈鸢", "司空影", "皇甫缨", "上官璃", "殷无双", "顾丹阳"]
    # for Name in name_list:
    #     if not exists_imperial(quarrel_path, fr"{Name}.png", resolution) or Name == minister_name:
    #         continue
    #     touch(Template(quarrel_path + fr"{Name}.png", record_pos=(0.35, 0.025), resolution=resolution))
    #     if not exists_imperial(quarrel_path, r"舌战群儒暂未部署.png", resolution):
    #         break
    # snapshot(filename=img_path() + r"舌战群儒-驻学队列.png", msg="舌战群儒", quality=99)
    #
    # touch(Template(quarrel_path + r"舌战群儒确认部署按钮.png", record_pos=(0.192, 0.071), resolution=resolution))
    max_return_kay(language)
    max_return_kay(language)
    max_return_kay(language)
    max_return_kay(language)
