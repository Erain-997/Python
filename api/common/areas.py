from internal.es_log import es, es_data
from api.common.common import find_in_area
from airtest.core.api import *
from airtest.aircv import *

union_fight_area = [0, 400, 760, 900]
share_area = [68, 500, 728, 700]
imperial_academy_area = [68, 283, 728, 1060]
government_area = [80, 910, 733, 1060]


class ImgFactory(object):

    @classmethod
    def img_location_click(cls, img_ptah, img_name, position, sleep_time=0.1):
        time.sleep(sleep_time)
        img_list = []
        for _, _, files in os.walk(img_ptah):
            for file_name in files:
                if img_name in file_name:
                    img_list.append(img_ptah + file_name)
        pos = find_in_area(img_list, position)
        if pos:
            touch(pos)
            return
        else:
            # 全部区域找图
            for i in img_list:
                if exists(Template(i)):
                    touch(Template(i))
                    return
            # 用于失败后自己重新截识别
            # screen = G.DEVICE.snapshot()
            # # 局部截图，（0，160）是局部截图左上角的绝对坐标，（1067，551）是右下角的绝对坐标
            # screen = aircv.crop_image(screen, "这里要填你要识别的图的具体坐标")
            # retry_img = rf"{img_name + str(int(time.time()))}.png"
            # aircv.imwrite(img_ptah + retry_img, screen, 99)
            # touch(Template(img_ptah + retry_img))

        es.es_error(es_data("img_location", str(img_name), str(img_name), ""))
        return "图片未找到"

    @classmethod
    def exists_imperial_list(cls, img_ptah, img_name, area):
        img_list = []
        for _, _, files in os.walk(img_ptah):
            for file_name in files:
                if img_name in file_name:
                    img_list.append(img_ptah + file_name)
        pos = find_in_area(img_list, area)
        if pos:
            return pos
        else:
            return False
