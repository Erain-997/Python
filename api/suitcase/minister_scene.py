#!/usr/bin/evn python
# -*- coding:utf-8 -*-
# @author: zxp
# @date: 2021/08/10

from api.role.role import GetResource
from api.common.common import *
from internal.file import img_path, parent_path
from internal.tools import except_output
from api.common.areas import *
from api.common.cheat_api import CheatApi


class Scene(GetResource):
    def __init__(self, server_id, minister_id, skin_id, wive_id, wive_skin_id, fashion_id):
        super(Scene, self).__init__()
        self.server_id = server_id
        self.minister_id = minister_id
        self.skin_id = skin_id
        self.wive_id = wive_id
        self.wive_skin_id = wive_skin_id
        self.fashion_id = fashion_id
        self.sess, self.showId = self.role_register(server_id, "ui", minister_id, skin_id, wive_id, wive_skin_id,
                                                    fashion_id)  # 注册与作弊与登录

        self.client = r"G:\\server\\version\\"  # 客户端地址->资源机
        # self.client = r"D:\\code\\version1\\"  # 客户端地址->伟松
        self.Minister_Path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\minister_img/"
        self.cut_img_Path = parent_path(__file__) + "\\to_be_test_img\\"
        self.resolution = get_resolutiond()
        self.head_path = self.client + "\\assets\\unpack\\character\\servant\\head\\"
        # 大臣皮肤截图保存路径
        if not os.path.exists(img_path() + rf"\\{self.skin_id}") and str(
                self.skin_id) != "" and self.skin_id is not None and int(self.skin_id) > 0:
            os.makedirs(img_path() + rf"\\{self.skin_id}")
        self.img_path = img_path() + rf"\\{self.skin_id}\\"
        # 妃子皮肤截图保存路径
        if not os.path.exists(img_path() + rf"\\{self.wive_skin_id}") and str(
                self.wive_skin_id) != "" and self.wive_skin_id is not None and int(
            self.wive_skin_id) > 0:
            os.makedirs(img_path() + rf"\\{self.wive_skin_id}")
        self.wive_img_path = img_path() + rf"\\{self.wive_skin_id}\\"
        # 玩家时装截图保存路径
        if not os.path.exists(img_path() + rf"\\{self.fashion_id}") and str(
                self.fashion_id) != "" and self.fashion_id is not None and int(fashion_id > 0):
            os.makedirs(img_path() + rf"\\{self.fashion_id}")
        self.fashion_img_path = img_path() + rf"\\{self.fashion_id}\\"
        if fashion_id is None or str(fashion_id) == "" or int(fashion_id) == 0:
            self.common_img_path = img_path() + r"\\common\\"
            self.get_photo(self.client, minister_id, skin_id, wive_id, wive_skin_id)  # 获取大臣以及皮肤图片

    @except_output()
    def minister(self):
        # 给大臣换待测皮肤
        self.img_location_click(self.Minister_Path, "大臣", tail())
        self.img_location_click(self.Minister_Path, "战力", head())
        sleep(0.5)
        c = 0
        while not exists_imperial(self.cut_img_Path + str(self.minister_id) + "body.png"):
            swipe((678, 782), (678, 382))
            if c > 30:
                print("没找到大臣")
                break
        self.img_location_click(self.cut_img_Path, str(self.minister_id) + "body", big_central_section())

        self.img_location_click(self.Minister_Path, "右边弹窗2", central_section())
        touch((678, 582))  # 直接切到下一个皮肤
        c = 0

        while not exists_imperial(self.Minister_Path + fr"穿戴.png"):
            touch((678, 582))  # 直接切到下一个皮肤
            if c > 15:
                print("没找到皮肤")
                break
        self.img_location_click(self.Minister_Path, "穿戴", tail())
        time.sleep(0.5)
        snapshot(filename=self.img_path + rf"{self.skin_id}大臣刚穿新皮肤.png", msg="大臣", quality=99)
        return_kay()
        return_kay()
        snapshot(filename=self.img_path + rf"{self.skin_id}大臣列表.png", msg="大臣", quality=99)
        return_kay()

    @except_output()
    def share(self):
        """
        分享大臣信息
        :return:
        # """
        share_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\share_img/"
        a = exists_imperial(share_path + fr"主场景道具入口.png")
        touch((a[0], a[1] - 90))
        self.img_location_click(share_path, "分享", tail())
        self.img_location_click(share_path, "分享", tail())
        time.sleep(1)
        pos = find_in_area_and_swipe(to_be_find(self.skin_id, [1, 2]), share_area, [(652, 612), (150, 612)])
        touch(pos)
        time.sleep(1)
        snapshot(filename=self.img_path + rf"{self.skin_id}分享大臣横向列表.png", msg="聊天", quality=99)
        self.img_location_click(share_path, "分享按钮", big_tail())
        time.sleep(1)
        a = exists_imperial(share_path + fr"分享.png")
        touch((a[0] - 20, a[1] - 130))
        time.sleep(2)
        snapshot(filename=self.img_path + rf"{self.skin_id}分享大臣详情.png", msg="聊天", quality=99)
        # todo 有可能有显示问题,所以把分享搞到最后一步执行,之后就不退回主场景了
        # cheat_share_cd(self.sess)
        # off_kay()
        # return_kay()

    @except_output()
    def imperial_academy(self):
        """
        帝国书院
        :return:
        """
        # 属于是一次性的,一个账号只能搞一次
        imperial_academy_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\imperial_academy_img/"
        if not exists_imperial(imperial_academy_path + r"帝国书院.png"):
            for i in range(5):
                main_scene_right()

        self.img_location_click(imperial_academy_path, "帝国书院", central_section())
        self.img_location_click(imperial_academy_path, "帝国书院座位", head())

        pos = find_in_area_and_swipe([self.cut_img_Path + str(self.skin_id) + "body.png"], imperial_academy_area,
                                     [(503, 639), (503, 258)])

        snapshot(filename=self.img_path + rf"{self.skin_id}帝国书院大臣列表.png", msg="大臣", quality=99)
        touch(pos)
        self.img_location_click(imperial_academy_path, "确定", tail())
        sleep(2)
        snapshot(filename=self.img_path + rf"{self.skin_id}帝国书院书桌视角.png", msg="大臣", quality=99)
        return_kay()

    @except_output()
    def government(self):
        """
        这玩意一个号只能跑一次, 会作弊成为城主
        天下政令
        :return:
        """
        government_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\government_img/"
        self.cheat_sky(self.sess, self.server_id)
        if not exists_imperial(government_path + r"天下政令.png"):
            main_scene_left()
            main_scene_left()
            main_scene_left()

        self.img_location_click(government_path, "天下政令", head())
        for i in range(5):
            touch((500, 500))
            sleep(1)
        self.img_location_click(government_path, "前往城池按钮", tail())
        self.img_location_click(government_path, "时装按钮", tail(), sleep_time=1)
        sleep(1)
        if self.minister_id > 0 and self.skin_id > 0:
            pos = find_in_area([government_path + r"大臣形象按钮.png", government_path + r"大臣形象按钮2.png"],
                               [130, 200, 850, 400])
            touch(pos)
            pos = find_in_area_and_swipe([self.cut_img_Path + str(self.skin_id) + "body.png"], government_area,
                                         [(684, 959)])
            touch(pos)
            self.img_location_click(government_path, "穿戴按钮", tail())
            snapshot(filename=self.img_path + rf"{self.skin_id}天下政令大臣形象穿戴完.png", msg="天下政令", quality=99)
            off_kay()
            snapshot(filename=self.img_path + rf"{self.skin_id}天下政令大臣形象1级场景.png", msg="天下政令", quality=99)

        if self.wive_id > 0 and self.wive_skin_id > 0:
            self.img_location_click(government_path, "时装按钮", tail())
            self.img_location_click(government_path, "伴侣形象按钮", head())
            pos = find_in_area_and_swipe([self.cut_img_Path + fr"{self.wive_skin_id}body.png"], government_area,
                                         [(684, 959)])
            touch(pos)
            self.img_location_click(government_path, "穿戴按钮", tail())
            snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}天下政令妃子形象.png", msg="天下政令", quality=99)
            off_kay()
            snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}天下政令妃子形象1级场景.png", msg="天下政令", quality=99)

        back_to_main()

    @except_output()
    def guard_trial(self):
        """
        近卫军试炼
        :return:
        """
        guard_trial_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\guard_trial_img/"
        # 来到主场景最左边
        sleep(2)
        main_scene_left()
        main_scene_left()
        main_scene_left()

        self.img_location_click(guard_trial_path, "近卫军试炼入口", central_section())

        self.img_location_click(guard_trial_path, "出战阵容", big_central_section())
        self.img_location_click(guard_trial_path, "出战加号", head())
        sleep(0.5)
        pos = find_in_area_and_swipe([self.cut_img_Path + str(self.skin_id) + "body.png"], imperial_academy_area,
                                     [(503, 680), (503, 358)])
        touch(pos)
        snapshot(filename=self.img_path + rf"{self.skin_id}近卫军出战列表.png", msg="近卫军试炼", quality=99)
        self.img_location_click(guard_trial_path, "确定按钮", tail())
        snapshot(filename=self.img_path + rf"{self.skin_id}近卫帐篷视角.png", msg="近卫军试炼", quality=99)
        back_to_main()

    @except_output()
    def outskirts(self):
        """
        郊区
        :return:
        """

        outskirts_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\outskirts_img/"
        count = 0
        while not exists_imperial(outskirts_path + r"郊区.png"):
            count += 1
            main_scene_right()
            if count > 5:
                break
        self.img_location_click(outskirts_path, "郊区", head())
        self.img_location_click(outskirts_path, "猎场", central_section())
        time.sleep(2)
        touch_up100(exists_imperial(outskirts_path + r"自动攻击选择框.png"))  # 点击选择框上方100像素选择英雄
        time.sleep(1)
        touch((439, 1100))
        pos = find_in_area_and_swipe([self.cut_img_Path + str(self.skin_id) + "body.png"], imperial_academy_area,
                                     [(503, 680), (503, 358)])

        snapshot(filename=self.img_path + rf"{self.skin_id}郊区猎场大臣列表.png", msg="郊区", quality=99)
        touch((pos[0], pos[1] + 55))

        off_kay()
        snapshot(filename=self.img_path + rf"{self.skin_id}郊区猎场选择大臣后.png", msg="郊区", quality=99)

        touch((104, 1190))  # 白旗退出图标总点不到,直接用坐标代替,按钮位置是固定的

        self.img_location_click(outskirts_path, "海神岛", tail())
        touch((500, 500))
        sleep(2)
        touch_up100(exists_imperial(outskirts_path + r"自动攻击选择框.png"))  # 点击选择框上方100像素选择英雄
        sleep(0.5)

        pos = find_in_area_and_swipe([self.cut_img_Path + str(self.skin_id) + "body.png"], imperial_academy_area,
                                     [(503, 680), (503, 358)])

        snapshot(filename=self.img_path + rf"{self.skin_id}郊区猎场海神岛大臣列表.png", msg="郊区", quality=99)
        touch((pos[0], pos[1] + 55))
        off_kay()
        time.sleep(2)
        snapshot(filename=self.img_path + rf"{self.skin_id}郊区猎场海神岛选择大臣后.png", msg="郊区", quality=99)
        time.sleep(1)
        touch((104, 1190))  # 白旗退出图标总点不到,直接用坐标代替,按钮位置是固定的

        time.sleep(1)
        return_kay()

    @except_output()
    def arena(self):
        """
        竞技场,需要有60级以上英雄才行
        需要追杀令
        因为上一个场景已经在主场景最左边,这里就不滑动了
        :return:
        """
        arena_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\arena_img/"
        show_id = self.assist_account_register(self.server_id)
        self.img_location_click(arena_path, "竞技场", big_central_section())
        sleep(1)
        self.img_location_click(arena_path, "竞技场消息按钮", central_section())
        sleep(1)
        self.img_location_click(arena_path, "竞技场追杀列表按钮", head())
        pos = find_in_area([arena_path + r"竞技场追杀查询按钮.png"], [138, 235, 850, 358])
        touch_left150(pos)
        text(str(show_id))
        self.img_location_click(arena_path, "竞技场追杀查询按钮", head())
        sleep(1)
        self.img_location_click(arena_path, "竞技场追杀按钮", tail())
        sleep(1)
        pos = find_in_area_and_swipe([self.cut_img_Path + str(self.skin_id) + "body.png"], imperial_academy_area,
                                     [(503, 680), (503, 358)])
        snapshot(filename=self.img_path + rf"{self.skin_id}竞技场出战列表.png", msg="竞技场", quality=99)
        touch((pos[0] + 400, pos[1] + 20))
        self.img_location_click(arena_path, "竞技场确认追杀", big_central_section())

        sleep(3)
        snapshot(filename=self.img_path + rf"{self.skin_id}竞技场出战后.png", msg="竞技场", quality=99)
        back_to_main()

    @except_output()
    def stage(self):
        """
        关卡
        :return:
        """
        stage_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\stage_img/"
        count = 0
        while not exists_imperial(stage_path + r"关卡.png"):
            count += 1
            main_scene_right()
            if count > 3:
                break
        self.img_location_click(stage_path, "关卡", tail())
        self.img_location_click(stage_path, "boss关卡", head())
        # 跳过剧情
        for i in range(10):
            touch((500, 400))
            sleep(0.1)
        sleep(1)
        touch_up100(exists_imperial(stage_path + r"关卡实力标志.png"))
        pos = find_in_area_and_swipe([self.cut_img_Path + str(self.skin_id) + "body.png"], imperial_academy_area,
                                     [(503, 639), (503, 458)])
        snapshot(filename=self.img_path + rf"{self.skin_id}关卡出战前.png", msg="关卡出战前", quality=99)
        for i in [30, 40, 50]:  # 大臣下方选择坐标
            touch((pos[0], pos[1] + i))  # 点击到选择英雄按钮
        off_kay()
        sleep(2)
        snapshot(filename=self.img_path + rf"{self.skin_id}关卡出战后.png", msg="关卡出战后", quality=99)

        self.img_location_click(stage_path, "撤退", tail())

        back_to_main()

    @except_output()
    def harem(self):
        """
        后宫换皮肤
        需要亲密度作弊,如果能作弊可以免去滑动找妃子的时间
        :return:
        """
        harem_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\harem_img/"
        main_scene_left()
        main_scene_left()

        self.img_location_click(harem_path, "主场景后宫入口", big_central_section())
        time.sleep(1)
        if exists_imperial(harem_path + r"后宫引导1.png"):
            self.img_location_click(harem_path, "后宫引导", central_section())
            for i in range(4):
                touch((500, 500))
            return_kay()

        self.img_location_click(harem_path, "伴侣", big_tail())
        self.img_location_click(harem_path, "排序选择按钮", tail())
        self.img_location_click(harem_path, "亲密度排序", tail())

        touch((458, 450))
        sleep(2)
        pos = self.exists_imperial_list(harem_path, "取消确认弹窗", central_section())
        if pos:
            touch(pos)
        sleep(3)
        self.img_location_click(harem_path, "右边弹窗", central_section())
        c = 0
        while not self.exists_imperial_list(harem_path, "穿戴按钮", tail()):
            touch((678, 682))  # 直接切到下一个皮肤
            if c > 15:
                print("没找到妃子皮肤")
                break

        else:
            touch(self.exists_imperial_list(harem_path, "穿戴按钮", tail()))
        # 至此穿好了新皮肤
        sleep(1)
        touch((500, 500))
        snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}拜访妃子前.png", msg="后宫", quality=99)
        touch((500, 500))

        self.img_location_click(harem_path, "拜访按钮", tail())
        self.img_location_click(harem_path, "确认拜访按钮", central_section())
        sleep(8)
        snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}拜访妃子后.png", msg="后宫", quality=99)
        touch((500, 500))
        touch((500, 500))
        c = 0
        while not exists_imperial(harem_path + r"才艺学院.png"):
            return_kay()
            if c > 6:
                break
        self.img_location_click(harem_path, "才艺学院", central_section())
        time.sleep(3)
        pos = self.exists_imperial_list(harem_path, "跳过剧情按钮", head())
        if pos:
            touch(pos)  # 跳过剧情
        self.img_location_click(harem_path, "开启教学室", tail())
        touch((500, 500))  # 为了容错,已经弹出的选择会挡住背景

        a = exists_imperial(harem_path + r"宫廷画室背景.png")

        touch((a[0] - 500, a[1] + 150))  # 点击切换妃子
        sleep(2)
        snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}教学室选择妃子.png", msg="后宫", quality=99)

        touch_down150(a)  # 花费钥匙进入画室
        time.sleep(3)
        snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}教学室内.png", msg="后宫", quality=99)
        return_kay()
        # 到宫位院去
        self.img_location_click(harem_path, "宫位院", head())
        sleep(2)
        snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}升宫位前.png", msg="伴侣-后宫", quality=99)
        a = exists_imperial(harem_path + r"问号按钮.png")
        touch((a[0] - 50, a[1] + 350))
        sleep(2)
        snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}升宫位时.png", msg="伴侣-后宫", quality=99)
        off_kay()
        return_kay()

        back_to_main()

    @except_output()
    def union_fight(self):
        """
        跨服戰鬥
        跨服盟战
        :return:
        """
        union_fight_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\union_fight_img/"
        count = 0
        while not exists_imperial(union_fight_path + "主场景联盟入口.png"):
            count += 1
            main_scene_right()
            if count > 3:
                break
        self.img_location_click(union_fight_path, "主场景联盟入口", central_section())

        off_kay()
        # # 关掉弹窗
        touch((400, 100))
        self.img_location_click(union_fight_path, "跨服盟战入口", central_section())
        self.img_location_click(union_fight_path, "盟战派遣部队按钮", tail())
        # 跳过引导,且点击加号
        for i in range(1):
            touch((500, 500))
            sleep(0.3)
            touch((500, 500))
            sleep(0.3)
        # 找到想要的大臣
        touch((112, 744))  # 点击防守阵容第一个位置,再点击待测大臣,把他搞到防守位置第一个
        sleep(1)
        a = find_in_area(to_be_find(self.skin_id, [1, 2]), union_fight_area)
        if not a:
            # 防止想要的英雄在最右边
            swipe((600, 550), (10, 550), duration=0.1, steps=5)
            swipe((600, 750), (10, 750), duration=0.1, steps=5)
            sleep(1)
            a = find_in_area(to_be_find(self.skin_id, [1, 2]), union_fight_area)

        snapshot(filename=self.img_path + rf"{self.skin_id}盟战派遣界面.png", msg="盟战派遣界面", quality=99)
        touch(a)
        sleep(2)
        # 卷轴
        self.img_location_click(union_fight_path, "卷轴按钮", big_tail())
        snapshot(filename=self.img_path + rf"{self.skin_id}卷轴界面.png", msg="盟战派遣界面", quality=99)
        off_kay()
        back_to_main()

    @except_output()
    def use_item(self):
        """
        需要随选手册
        """
        item_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\item_img/"
        self.img_location_click(item_path, "主场景道具入口", tail())
        self.img_location_click(item_path, "培养道具", head())
        self.img_location_click(item_path, "随机手册", head())
        sleep(1)
        pos = find_in_area_and_swipe(to_be_find(self.skin_id, [1, 2]), [68, 283, 728, 950], [(650, 600), (200, 600)])
        touch(pos)
        snapshot(filename=self.img_path + rf"{self.skin_id}大臣物品使用界面.png", msg="物品使用界面", quality=99)
        back_to_main()

    @except_output()
    def share_wive(self):
        """
        分享妃子信息
        :return:
        """
        share_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\share_img/"
        a = exists_imperial(share_path + fr"主场景道具入口.png")
        touch((a[0], a[1] - 90))
        sleep(1)
        self.img_location_click(share_path, "分享", tail())
        self.img_location_click(share_path, "分享", tail())
        self.img_location_click(share_path, "分享内伴侣按钮", central_section())
        c = 0
        ad = exists_imperial(self.cut_img_Path + fr"{self.wive_skin_id}.png")
        while not ad:
            swipe((652, 612), (150, 612), duration=0.01, steps=2)
            ad = exists_imperial(self.cut_img_Path + fr"{self.wive_skin_id}.png")
            if c > 35:
                break
        touch(ad)
        time.sleep(1)
        snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}分享妃子横向列表.png", msg="聊天", quality=99)
        self.img_location_click(share_path, "分享按钮", big_tail())
        time.sleep(1)
        a = exists_imperial(share_path + fr"分享.png")
        touch((a[0] - 20, a[1] - 130))
        time.sleep(2)
        snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}分享妃子详情.png", msg="聊天", quality=99)
        self.cheat_share_cd(self.sess, self.server_id)
        off_kay()
        return_kay()

    @except_output()
    def use_item_wive(self):
        """
        需要祖母绿戒指
        """
        item_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\item_img/"

        if exists_imperial(item_path + "主场景道具入口.png"):
            self.img_location_click(item_path, "主场景道具入口", tail())
        self.img_location_click(item_path, "培养道具", head())
        self.img_location_click(item_path, "戒指", head())
        snapshot(filename=self.wive_img_path + rf"{self.wive_skin_id}妃子物品使用界面.png", msg="物品使用界面", quality=99)
        back_to_main()

    @except_output()
    def harem_man(self):
        """
        男的后宫
        需要亲密度作弊,如果能作弊可以免去滑动找妃子的时间
        :return:
        """
        harem_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\harem_img/"
        find_enter_path(harem_path + r"主场景后宫入口.png")

        self.img_location_click(harem_path, "主场景后宫入口", central_section())
        self.img_location_click(harem_path, "伴侣", big_tail())
        sleep(1)
        touch((435, 414))

        self.img_location_click(harem_path, "更换性别按钮", big_tail())
        sleep(4)
        for i in range(8):  # 鬼一样的引导, 比之前多出来一个提示
            touch((500, 100))
            sleep(0.4)
        self.img_location_click(harem_path, "免费切换按钮", big_tail())
        self.img_location_click(harem_path, "确定按钮", central_section())
        # 至此换好了性别
        sleep(2)
        snapshot(filename=self.wive_img_path + rf"man{self.wive_skin_id}拜访妃子前.png", msg="后宫", quality=99)
        self.img_location_click(harem_path, "拜访按钮", tail())
        self.img_location_click(harem_path, "确认拜访按钮", central_section())
        sleep(5)
        snapshot(filename=self.wive_img_path + rf"man{self.wive_skin_id}拜访妃子后.png", msg="后宫", quality=99)

        touch((500, 100))
        touch((500, 100))

        return_kay()
        snapshot(filename=self.wive_img_path + rf"man{self.wive_skin_id}妃子列表.png", msg="后宫", quality=99)
        return_kay()

        # 到才艺学院去
        self.img_location_click(harem_path, "才艺学院", central_section())
        sleep(2)
        snapshot(filename=self.wive_img_path + rf"man{self.wive_skin_id}教学室内.png", msg="后宫", quality=99)
        return_kay()
        # 到宫位院去
        self.img_location_click(harem_path, fr"宫位院", head())
        sleep(1)
        snapshot(filename=self.wive_img_path + rf"man{self.wive_skin_id}升宫位前.png", msg="伴侣-后宫", quality=99)
        a = exists_imperial(harem_path + r"问号按钮.png")
        touch((a[0] - 50, a[1] + 350))
        sleep(1)
        snapshot(filename=self.wive_img_path + rf"man{self.wive_skin_id}升宫位时.png", msg="伴侣-后宫", quality=99)
        off_kay()
        back_to_main()

    @except_output()
    def share_wive_man(self):
        """
        分享妃子信息
        :return:
        """
        text("^r")  # 重启使作弊生效
        sleep(7)
        touch((400, 100))  # 开始游戏
        touch((400, 300))  # 开始游戏
        sleep(3)

        share_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\share_img/"

        a = exists_imperial(share_path + fr"主场景道具入口.png")
        if a is False:
            print("主场景道具异常")

        touch((a[0], a[1] - 90))
        self.img_location_click(share_path, "分享", tail())
        self.img_location_click(share_path, "分享", tail())
        self.img_location_click(share_path, "分享内伴侣按钮", central_section())
        c = 0
        ad = exists_imperial(self.cut_img_Path + str(self.wive_skin_id) + "man.png")
        while not ad:
            swipe((652, 612), (150, 612), duration=0.01, steps=2)
            ad = exists_imperial(self.cut_img_Path + str(self.wive_skin_id) + "man.png")
            if c > 35:
                break
        touch(ad)
        time.sleep(1)
        snapshot(filename=self.wive_img_path + rf"man{self.wive_skin_id}分享妃子横向列表.png", msg="聊天", quality=99)
        self.img_location_click(share_path, "分享按钮", big_tail())
        time.sleep(1)
        a = exists_imperial(share_path + fr"分享.png")
        touch((a[0] - 20, a[1] - 130))
        time.sleep(2)
        snapshot(filename=self.wive_img_path + rf"man{self.wive_skin_id}分享妃子详情.png", msg="聊天", quality=99)
        off_kay()
        return_kay()

    @except_output()
    def use_item_wive_man(self):
        """
        需要祖母绿戒指
        """
        item_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\item_img/"
        if exists_imperial(item_path + "主场景道具入口.png"):
            self.img_location_click(item_path, "主场景道具入口", tail())
        self.img_location_click(item_path, "培养道具", head())
        self.img_location_click(item_path, "戒指", head())
        sleep(2)
        snapshot(filename=self.wive_img_path + rf"man{self.wive_skin_id}妃子物品使用界面.png", msg="物品使用界面", quality=99)
        back_to_main()

    @except_output()
    def government_man(self):
        """
        天下政令男妃子截图
        :return:
        """
        government_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\government_img/"
        main_scene_left()
        main_scene_left()
        main_scene_left()

        self.img_location_click(government_path, "天下政令", head())
        self.img_location_click(government_path, "帝陵城", head())

        sleep(2)
        snapshot(filename=self.wive_img_path + rf"man{self.skin_id}天下政令1级大臣形象.png", msg="天下政令", quality=99)
        self.img_location_click(government_path, "时装按钮", tail())
        self.img_location_click(government_path, "伴侣形象按钮", head(), sleep_time=1)
        snapshot(filename=self.wive_img_path + rf"man{self.skin_id}天下政令大臣形象.png", msg="天下政令", quality=99)

    @except_output()
    def fashion(self):
        """
        玩家穿戴测试用时装
        :return:
        """
        fashion_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        self.img_location_click(fashion_path, "玩家头像", head())
        self.img_location_click(fashion_path, "外观按钮", tail())
        self.img_location_click(fashion_path, "时装按钮", head())
        # 选择第二套时装的坐标
        touch((300, 800), times=1)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}玩家穿戴预览.png", msg="时装穿戴", quality=99)
        self.img_location_click(fashion_path, "穿戴按钮", tail())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}玩家穿戴.png", msg="时装穿戴", quality=99)
        self.img_location_click(fashion_path, "返回按钮", head())
        off_kay()
        return_kay()
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}玩家详情.png", msg="时装穿戴", quality=99)
        return_kay()

    @except_output()
    def fashion_federation(self):
        """
        玩家时装联邦界面截图
        :return:
         """
        fashion_federation_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        main_scene_right()
        main_scene_right()
        main_scene_right()

        self.img_location_click(fashion_federation_path, "联邦入口", big_central_section())
        self.img_location_click(fashion_federation_path, "前往按钮", tail())
        self.img_location_click(fashion_federation_path, "联邦大殿", central_section())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}联邦大殿玩家形象.png", msg="联邦大殿", quality=99)
        self.img_location_click(fashion_federation_path, "联邦大殿奖励领取按钮", tail())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}联邦奖励动画玩家形象.png", msg="联邦大殿", quality=99)
        touch((300, 800), times=1)  ##点击任意区域
        return_kay()
        self.fashion_chat_push()  # 联邦频道推送

    @except_output()
    def fashion_chat_push(self):
        """
        联邦界面推送截图
        :return:
         """
        fashion_chat_push_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        self.cheat_federation_chat_push(self.sess, self.server_id)
        self.img_location_click(fashion_chat_push_path, "联邦聊天入口", tail())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}联邦聊天推送.png", msg="联邦推送", quality=99)
        back_to_main()

    @except_output()
    def fashion_sky(self):
        """
        天下政令界面截图
        :return:
         """
        government_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\government_img/"
        fashion_sky_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        self.cheat_sky(self.sess, self.server_id)  # 作弊器入驻天下政令
        sleep(1)
        main_scene_left()  # 主场景左移
        main_scene_left()
        main_scene_left()
        self.img_location_click(government_path, "天下政令", head())
        for i in range(5):
            touch((500, 500))
            sleep(1)
        self.img_location_click(government_path, "前往城池按钮", tail())

        sleep(2)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}天下政令时装.png", msg="天下政令时装", quality=99)
        back_to_main()

    @except_output()
    def fashion_war(self):
        """
        无限征战界面和宝箱界面玩家形象截图
        :return:
         """
        self.cheat_infinite_battle(self.sess, self.server_id)
        fashion_war_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        main_scene_right()
        self.img_location_click(fashion_war_path, "无限征战入口", head())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}无限征战时装.png", msg="无限征战时装", quality=99)
        self.img_location_click(fashion_war_path, "pass", head())
        return_kay()
        # self.img_location_click(fashion_war_path,"本服频道",tail())
        # self.img_location_click(fashion_war_path,"无限征战宝箱",big_tail())
        # sleep(1)
        # snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}无限征战宝箱时装.png", msg="无限征战时装", quality=99)
        # self.img_location_click(fashion_war_path,"无限征战宝箱关闭",big_central_section())
        return_kay()

    @except_output()
    def fashion_campaign(self):
        """
        关卡界面玩家形象截图
        :return:
         """
        stage_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\stage_img/"

        self.img_location_click(stage_path, "关卡", big_tail())
        sleep(2)

        self.img_location_click(stage_path, "boss关卡", head())

        touch((500, 500), times=5)
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}关卡时装.png", msg="关卡时装", quality=99)
        touch((500, 500), times=5)

        sleep(2)
        touch((500, 500), times=5)

        self.img_location_click(stage_path, "撤退", tail())

        back_to_main()

    @except_output()
    def fashion_feast(self):
        """
        盛宴明君推送玩家形截图
        :return:
         """
        fashion_feast_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        self.img_location_click(fashion_feast_path, "宴会入口", tail())
        # 判断是否有旧的盛宴明君弹窗，有点击关闭
        if exists_imperial(fashion_feast_path + r"关闭按钮.png"):
            self.img_location_click(fashion_feast_path, "关闭按钮", big_central_section())

        if exists_imperial(fashion_feast_path + r"引导不用了按钮.png"):
            self.img_location_click(fashion_feast_path, "引导不用了按钮", big_central_section())
        touch((400, 300), times=5)
        sleep(1)
        touch((400, 300))

        self.img_location_click(fashion_feast_path, "开启家宴", central_section())
        sleep(1)
        self.img_location_click(fashion_feast_path, "确认按钮", central_section())
        # 作弊指令添加10个机器人
        self.cheat_feast_addrobot(self.sess, self.server_id, 10)
        sleep(1)
        return_kay()
        sleep(5)
        self.img_location_click(fashion_feast_path, "领奖按钮", big_tail())
        sleep(3)
        # 点击任意区域
        touch((500, 500))
        return_kay()
        # 作弊指令刷新盛宴明君榜单
        self.cheat_feast_refresh(self.sess, self.server_id)
        self.img_location_click(fashion_feast_path, "宴会入口", tail())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}盛宴明君推送.png", msg="盛宴明君推送", quality=99)
        self.img_location_click(fashion_feast_path, "关闭按钮", big_central_section())
        self.cheat_del_feast(self.sess, self.server_id)
        sleep(5)
        # 举办第二次宴会，为下面的宴会争夺做准备
        self.img_location_click(fashion_feast_path, "举办宴会", big_central_section())
        self.img_location_click(fashion_feast_path, "开启家宴", central_section())
        self.img_location_click(fashion_feast_path, "确认按钮", central_section())

        # 作弊指令添加10个机器人
        self.cheat_feast_addrobot(self.sess, self.server_id, 5)
        sleep(3)
        if exists_imperial(fashion_feast_path + r"确认按钮.png"):
            self.img_location_click(fashion_feast_path, "确认按钮", central_section())

        back_to_main()

    @except_output()
    def fashion_arena(self):
        """
        竞技场追杀玩家形象截图竞技场入口
        :return:
         """
        fashion_arena_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        showid = self.showId  ## 上一个穿了测试时装的玩家showid，用于搜索
        self.img_location_click(fashion_arena_path, "竞技场入口", big_tail())
        sleep(2)
        ##重启并创建新账号
        self.sess, self.showId = self.role_register(self.server_id, "ui", self.minister_id, self.skin_id, self.wive_id,
                                                    self.wive_skin_id, self.fashion_id)  # 注册与作弊与登录
        self.fashion()  ##给新账号穿戴测试的时装
        main_scene_left()
        main_scene_left()
        self.img_location_click(fashion_arena_path, "竞技场入口", big_tail())
        self.img_location_click(fashion_arena_path, "消息入口", big_tail())
        self.img_location_click(fashion_arena_path, "追杀入口", head())
        self.img_location_click(fashion_arena_path, "空白条", head())
        print(showid)
        text(str(showid))
        self.img_location_click(fashion_arena_path, "查询按钮", head())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}竞技场追杀玩家时装.png", msg="竞技场", quality=99)
        back_to_main()

    @except_output()
    def fashion_feast_PK(self):
        """
        宴会pk玩家形象截图
        :return:
         """
        fashion_feast_pk_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        main_scene_right()
        self.img_location_click(fashion_feast_pk_path, "宴会入口", tail())
        # 判断是否存在旧的盛宴明君推送，存在关闭推送
        if exists_imperial(fashion_feast_pk_path + r"关闭按钮.png"):
            self.img_location_click(fashion_feast_pk_path, "关闭按钮", big_central_section())
        self.img_location_click(fashion_feast_pk_path, "玩家宴会入口", big_tail())
        self.img_location_click(fashion_feast_pk_path, "争抢宴会席位", head())
        self.img_location_click(fashion_feast_pk_path, "开启家宴", central_section())  ##点击赴宴，由于按钮一样复用同一张图片
        sleep(0.5)
        snapshot(filename=self.fashion_img_path + rf"man{self.fashion_id}争抢宴会席位玩家形象.png", msg="宴会", quality=99)

    @except_output()
    def fashion_woman(self):
        """
        玩家性别切换，有男帝切换成女帝
        :return:
         """
        fashion_womam_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        self.sess, self.showId = self.role_register(self.server_id, "ui", self.minister_id, self.skin_id, self.wive_id,
                                                    self.wive_skin_id, self.fashion_id)  # 注册与作弊与登录

        self.img_location_click(fashion_womam_path, "道具列表按钮", tail())
        self.img_location_click(fashion_womam_path, "其他道具按钮", head())
        self.img_location_click(fashion_womam_path, "形象卡道具图标", big_central_section())
        self.img_location_click(fashion_womam_path, "使用按钮", big_tail())
        sleep(1)
        self.img_location_click(fashion_womam_path, "性别切换按钮", tail())
        sleep(1)
        self.img_location_click(fashion_womam_path, "使用形象卡按钮", big_tail())
        return_kay()
        self.img_location_click(fashion_womam_path, "玩家头像", head())
        self.img_location_click(fashion_womam_path, "外观按钮", tail())
        self.img_location_click(fashion_womam_path, "时装按钮", head())
        # 选择第二套时装的坐标
        touch((300, 800), times=1)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}玩家穿戴预览.png", msg="时装穿戴", quality=99)
        self.img_location_click(fashion_womam_path, "穿戴按钮", tail())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}玩家穿戴.png", msg="时装穿戴", quality=99)
        self.img_location_click(fashion_womam_path, "返回按钮", head())
        off_kay()
        return_kay()
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}玩家详情.png", msg="时装穿戴", quality=99)
        return_kay()

    @except_output()
    def fashion_woman_federation(self):
        """
        玩家时装联邦界面截图
        :return:
         """
        fashion_federation_woman_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        main_scene_right()
        main_scene_right()
        main_scene_right()
        self.img_location_click(fashion_federation_woman_path, "联邦入口", big_central_section())
        self.img_location_click(fashion_federation_woman_path, "前往按钮", big_tail())
        self.img_location_click(fashion_federation_woman_path, "联邦大殿", central_section())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}联邦大殿玩家形象.png", msg="联邦大殿", quality=99)
        self.img_location_click(fashion_federation_woman_path, "联邦大殿奖励领取按钮", big_tail())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}联邦奖励动画玩家形象.png", msg="联邦大殿", quality=99)
        touch((300, 800), times=1)  ##点击任意区域
        return_kay()
        self.fashion_woman_chat_push()  # 女苏丹联邦频道推送

    @except_output()
    def fashion_woman_chat_push(self):
        """
        联邦界面推送截图
        :return:
         """
        fashion_woman_chat_push_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        self.cheat_federation_chat_push(self.sess, self.server_id)
        self.img_location_click(fashion_woman_chat_push_path, "联邦聊天入口", tail())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}联邦聊天推送.png", msg="联邦推送", quality=99)
        back_to_main()

    @except_output()
    def fashion_woman_sky(self):
        """
        天下政令界面截图
        :return:
         """
        government_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\government_img/"
        fashion_woman_sky_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        self.cheat_sky(self.sess, self.server_id)  # 作弊器入驻天下政令
        main_scene_left()  # 主场景左移
        main_scene_left()
        main_scene_left()
        self.img_location_click(government_path, "天下政令", head())
        touch((500, 500))
        touch((500, 500))
        touch((500, 500))
        self.img_location_click(government_path, "前往城池按钮", big_tail())

        sleep(2)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}天下政令时装.png", msg="天下政令时装", quality=99)
        back_to_main()

    @except_output()
    def fashion_woman_war(self):
        """
        无限征战界面和宝箱界面玩家形象截图
        :return:
         """
        self.cheat_infinite_battle(self.sess, self.server_id)  ##作弊指令入驻无限征战
        fashion_woman_war_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        main_scene_right()
        self.img_location_click(fashion_woman_war_path, "无限征战入口", head())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}无限征战时装.png", msg="无限征战时装", quality=99)
        self.img_location_click(fashion_woman_war_path, "pass", head())
        return_kay()
        # self.img_location_click(fashion_woman_war_path,"本服频道",tail())
        # self.img_location_click(fashion_woman_war_path,"无限征战宝箱",big_tail())
        # sleep(1)
        # snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}无限征战宝箱时装.png", msg="无限征战时装", quality=99)
        # self.img_location_click(fashion_woman_war_path,"无限征战宝箱关闭",big_tail())
        return_kay()

    @except_output()
    def fashion_woman_campaign(self):
        """
        关卡界面玩家形象截图
        :return:
         """
        fashion_woman_campaign_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\stage_img/"
        main_scene_right()
        sleep(2)
        self.img_location_click(fashion_woman_campaign_path, "关卡", tail())
        self.img_location_click(fashion_woman_campaign_path, "boss关卡", head())
        touch((500, 500), times=5)
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}关卡时装.png", msg="关卡时装", quality=99)
        stage_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\stage_img/"
        touch((500, 500), times=5)

        sleep(2)
        touch((500, 500), times=5)
        self.img_location_click(stage_path, "撤退", tail())

        back_to_main()

    @except_output()
    def fashion_woman_feast(self):
        """
        盛宴明君推送玩家形截图
        :return:
         """
        fashion_woman_feast_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        sleep(5)
        self.img_location_click(fashion_woman_feast_path, "宴会入口", tail())
        # 判断是否有旧的盛宴明君弹窗，有点击关闭
        if exists_imperial(fashion_woman_feast_path + r"关闭按钮.png"):
            self.img_location_click(fashion_woman_feast_path, "关闭按钮", big_central_section())
        if exists_imperial(fashion_woman_feast_path + r"引导不用了按钮.png"):
            self.img_location_click(fashion_woman_feast_path, "引导不用了按钮", big_tail())
        touch((400, 300), times=5)
        sleep(1)
        touch((400, 300))

        self.img_location_click(fashion_woman_feast_path, "开启家宴", central_section())
        sleep(1)
        self.img_location_click(fashion_woman_feast_path, "确认按钮", big_central_section())
        # 作弊指令添加10个机器人
        self.cheat_feast_addrobot(self.sess, self.server_id, 10)
        sleep(1)
        return_kay()
        sleep(5)
        self.img_location_click(fashion_woman_feast_path, "领奖按钮", big_tail())
        sleep(3)
        # 点击任意区域
        touch((500, 500))

        return_kay()
        # 作弊指令刷新盛宴明君榜单
        self.cheat_feast_refresh(self.sess, self.server_id)
        self.img_location_click(fashion_woman_feast_path, "宴会入口", tail())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}盛宴明君推送.png", msg="盛宴明君推送", quality=99)
        self.img_location_click(fashion_woman_feast_path, "关闭按钮", big_central_section())
        # 举办第二次宴会，为下面的宴会争夺做准备
        self.img_location_click(fashion_woman_feast_path, "举办宴会", big_central_section())
        self.img_location_click(fashion_woman_feast_path, "开启家宴", big_central_section())
        self.img_location_click(fashion_woman_feast_path, "确认按钮", big_central_section())
        # 作弊指令添加10个机器人
        self.cheat_feast_addrobot(self.sess, self.server_id, 5)
        if exists_imperial(fashion_woman_feast_path + r"确认按钮.png"):
            self.img_location_click(fashion_woman_feast_path, "确认按钮", central_section())

        back_to_main()

    @except_output()
    def fashion_woman_arena(self):
        """
        竞技场追杀玩家形象截图
        :return:
         """
        fashion_woman_arena_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        showid = self.showId  # 上一个传了测试时装的玩家showid，用于搜索
        self.img_location_click(fashion_woman_arena_path, "竞技场入口", big_tail())
        sleep(2)
        # 重启并创建新账号
        self.fashion_woman()  # 给新账号穿戴测试的时装
        main_scene_left()
        main_scene_left()
        self.img_location_click(fashion_woman_arena_path, "竞技场入口", big_tail())
        self.img_location_click(fashion_woman_arena_path, "消息入口", tail())
        self.img_location_click(fashion_woman_arena_path, "追杀入口", head())
        self.img_location_click(fashion_woman_arena_path, "空白条", head())
        print(showid)
        text(str(showid))
        self.img_location_click(fashion_woman_arena_path, "查询按钮", head())
        sleep(1)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}竞技场追杀玩家时装.png", msg="竞技场", quality=99)
        back_to_main()

    @except_output()
    def fashion_woman_feast_PK(self):
        fashion_woman_feast_Pk_path = parent_path(__file__) + f"\\screen_shots\\minister" + r"\fashion_img/"
        main_scene_right()

        self.img_location_click(fashion_woman_feast_Pk_path, "宴会入口", tail())
        # 判断是否存在旧的盛宴明君推送，存在关闭推送
        if exists_imperial(fashion_woman_feast_Pk_path + r"关闭按钮.png"):
            self.img_location_click(fashion_woman_feast_Pk_path, "关闭按钮", big_central_section())
        self.img_location_click(fashion_woman_feast_Pk_path, "玩家宴会入口", big_tail())
        self.img_location_click(fashion_woman_feast_Pk_path, "争抢宴会席位", big_central_section())
        self.img_location_click(fashion_woman_feast_Pk_path, "开启家宴", big_central_section())  # 点击赴宴，由于按钮一样复用同一张图片
        sleep(0.5)
        snapshot(filename=self.fashion_img_path + rf"woman{self.fashion_id}争抢宴会席位玩家形象.png", msg="宴会", quality=99)


if __name__ == '__main__':
    import logging

    logging.getLogger("airtest").setLevel(logging.ERROR)
    auto_setup(__file__, logdir=True, devices=["Windows:///?title_re=version -.*", ], project_root=html_path())
    ST.RESIZE_METHOD = (810, 1344)
    # Scene(2, 71, 1646, 0, 0, "").arena()
    Scene(2, 0, 0, 6, 1755).government_man()
    # Scene(2, 71, 1646, 0, 0, "").government()
