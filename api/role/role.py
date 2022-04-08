# -*- encoding=utf8 -*-
# Time：'2021/11/3'
# __author__ = "2021099"
import json

from api.common.common import *
from internal.file import current_path
import requests
from PIL import Image
from internal.es_log import es, es_data
from api.common.cheat_api import CheatApi
from api.common.areas import ImgFactory


class GetResource(CheatApi, ImgFactory):
    def get_photo(self, path, minister_id, skin_id, wive_id, wive_skin_id):
        """
        作用是获取到待测大臣原始形象和穿上皮肤后的形象图片
        待用客户端资源路径
        head_path = client_path + "\\assets\\unpack\\character\\servant\\head\\"
        half_path = client_path + "\\assets\\unpack\\character\\servant\\half\\"
        spine_path = client_path + "\\assets\\spine\\"

        :param path:客户端代码地址
        :param minister_id:大臣id
        :param skin_id:大臣皮肤id
        :param wive_id:妃子id
        :param wive_skin_id:妃子皮肤id
        # files = os.listdir(photo_path)//所有图片
        # files.sort(key=lambda x: int(x[:-4]))//图片排序
        :return:
        """
        photo_path = path + "\\assets\\unpack\\character\\servant\\head\\"
        half_photo_path = path + "\\assets\\unpack\\character\\servant\\half\\"
        wives_photo_path = path + "\\assets\\unpack\\character\\wives\\girl\\head\\"
        wives_photo_half_path = path + "\\assets\\unpack\\character\\wives\\girl\\role\\"
        wives_man_photo_path = path + "\\assets\\unpack\\character\\wives\\boy\\head\\"
        wives_man_half_path = path + "\\assets\\unpack\\character\\wives\\boy\\role\\"
        if str(minister_id) != "" and str(skin_id) != "" and int(minister_id) > 0:
            # 大臣图片
            servant_img_init = Image.open(photo_path + fr"{minister_id}.png")
            servant_img_init.crop((40, 20, 80, 100)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + fr"{minister_id}.png")
            # 大臣原图去头
            servant_img_init = Image.open(half_photo_path + fr"{minister_id}.png")
            servant_img_init.crop((15, 190, 200, 240)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + str(minister_id) + "body.png")
            # 大臣皮肤头像
            servant_img_skin = Image.open(photo_path + fr"{skin_id}.png")
            servant_img_skin.crop((20, 25, 75, 78)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + fr"{skin_id}.png")
            servant_img_skin.crop((40, 25, 75, 74)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + fr"{skin_id}_1.png")
            servant_img_skin.crop((30, 25, 70, 75)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + fr"{skin_id}_2.png")
            # 大臣皮肤图片
            servant_img_skin = Image.open(half_photo_path + fr"{skin_id}.png")
            servant_img_skin.crop((90, 190, 180, 260)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + str(skin_id) + "body.png")

        if str(wive_id) != "" and str(wive_skin_id) != "" and wive_skin_id is not None and int(wive_id) > 0:
            # 妃子图片
            wives_img_init = Image.open(wives_photo_path + "\\" + fr"{wive_id}.png")
            wives_img_init.crop((40, 20, 80, 100)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + fr"{wive_id}.png")

            # 妃子皮肤头像
            wives_img_init = Image.open(wives_photo_path + "\\" + fr"{wive_skin_id}.png")
            wives_img_init.crop((35, 25, 85, 78)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + fr"{wive_skin_id}.png")
            # 妃子皮肤图片去头
            wives_img_init = Image.open(wives_photo_half_path + "\\" + fr"{wive_skin_id}.png")
            wives_img_init.crop((165, 240, 400, 450)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + str(wive_skin_id) + "body.png")

            wives_img_init = Image.open(wives_man_photo_path + "\\" + fr"{wive_skin_id}.png")
            wives_img_init.crop((40, 20, 80, 100)).save(
                parent_path(__file__) + r"\\to_be_test_img\\" + str(wive_skin_id) + "man.png")
            # # 男妃子皮肤图片去头去头
            # wives_img_init = Image.open(wives_man_half_path + "\\" + fr"{wive_skin_id}.png")
            # wives_img_init.crop((165, 240, 400, 450)).save(
            #     parent_path(__file__) + r"\\to_be_test_img\\" + str(wive_skin_id) + "manBody.png")

    def role_register(self, server_id, name, minister_id, minister_skin_id, wive_id, wive_skin_id, fashion_id):
        """
        创建新的账号且登录
        :param server_id:区服id
        :param name:指定帐号名称,用于拼接生成角色
        :param minister_id:获取大臣
        :return:
        """
        # 重启
        text("^r")
        url = "http://192.168.5.196:31496/basic_role"
        payload = {
            "server_id": server_id,
            "name": name,
            "counsellor_id": [minister_id]
        }
        for i in range(3):
            response = requests.post(url, json=payload)
            if response.json().get("10000")["Code"] == 0:
                # 记录id
                sess = response.json().get("sess")
                showid = response.json()['10000']['Data']['RoleBase']['ShowId']
                device_id = response.json().get("device_id")
                # resp_10000 = response.json().get("10000")
                # print(resp_10000)
                print(device_id)
                es.es_info(es_data("role_register", payload, str(response), "success"))
                sleep(3)
                self.cheat_item(minister_skin_id, sess, server_id)  # 大臣皮肤道具
                self.cheat_item(wive_skin_id, sess, server_id)  # 妃子皮肤道具
                self.cheat_item(fashion_id, sess, server_id)  # 玩家时装道具
                self.cheat_item(600, sess, server_id)  # 战区喇叭道具
                self.cheat_wive_score(wive_id, sess, server_id)  # 妃子好感度作弊
                if int(minister_id) > 0 and int(minister_skin_id) > 0:
                    self.cheat_union(sess, server_id)  # 创建一个联盟且调整到出战阶段

                if fashion_id is not None and int(fashion_id) > 0:
                    self.cheat_item(525, sess, server_id)  # 宴会道具
                    self.cheat_item(526, sess, server_id)  # 宴会道具
                    self.cheat_item(554, sess, server_id)  # 宴会道具
                    for j in range(5):
                        success = self.cheat_federation(sess, server_id)  # 创建一个联邦
                        if success:
                            break
                        sleep(3)
                # 登录
                path = current_path(__file__) + r"\\"
                double_click(Template(path + r"作弊器.png", record_pos=(-0.472, 0.398)))
                sleep(2)
                touch((736, 348))
                sleep(1)
                self.img_location_click(path, "空白条", central_section())

                text(device_id)
                # text("zxp_dXVHT0IN41k") # 指定登录
                self.img_location_click(path, "设备号登录", big_tail())
                sleep(6)
                touch((500, 500))  # 开始游戏
                sleep(3)

                return sess, showid
        es.es_error(es_data("role_register", payload, str("注册失败"), ""))
        return "err"


if __name__ == '__main__':
    import logging

    logging.getLogger("airtest").setLevel(logging.ERROR)
    auto_setup(__file__, logdir=True, devices=["Windows:///?title_re=version -.*", ], project_root=html_path())

    screen = G.DEVICE.snapshot()

    # 局部截图，（0，160）是局部截图左上角的绝对坐标，（1067，551）是右下角的绝对坐标
    screen = aircv.crop_image(screen, [0, 0, 810, 551])
    aircv.imwrite("./test.png", screen, 99)
    # GetResource().role_register(2, "zx", 71, 1648, 0, 0)
    GetResource().role_register(2, "zx", 71, 1646, 0, 0)
