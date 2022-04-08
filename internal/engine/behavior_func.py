# -*- encoding=utf8 -*-
# Time：'2022/4/8'
# __author__ = "Erain"
# 复写poco的原方法


import uuid
from time import sleep

import allure
import pytest
from test_components.toolkit.tools import SmallTools

from devices_init.devices_init import GetClient
from devices_init.devices_init import args
from internal.engine.engine_part import exists_func, touch_func
from internal.tools.assist_func import *
from internal.tools.log import log
from internal.tools.tool import except_go_main, case_snapshot


class BehaviorFunc(GetClient, SmallTools):
    log = log(args.devices)
    client_type = "client_type"  # 客户端类型
    client = ""

    def client_func(self, data):
        """
        获取客户端操作类型对象
        :param data:
        :return:
        """
        if data == "android_poco":
            self.client = self.android_poco
        else:
            self.client = self.poco

    def node_path(self, data):
        """
        节点路径
        :param data:
        :return:
        """
        return eval("self.client" + data)

    def execute(self, case_name, data, case_type, note):
        with allure.step(str(case_name) + ":" + str(case_type)):
            # 提交文本
            if case_type == "set_text":
                if note is not None:
                    self.node_path(data).set_text(note)
                else:
                    self.node_path(data).set_text(str(uuid.uuid1()).replace("-", "")[:20])

            # 提交随机文本
            elif case_type == "set_rand":
                if note is not None:
                    note = str(uuid.uuid1()).replace("-", "")[:int(note)]
                else:
                    note = str(uuid.uuid1()).replace("-", "")[:20]
                self.node_path(data).set_text(note)

            # 点击
            elif case_type == "click":
                # 指定点击元素上的位置以及点击后间隔时间
                self.node_path(data).click()
            # 元素是否存在
            elif case_type == "exists":
                return self.node_path(data).exists()
            # 等待
            elif case_type == "wait":
                # 获取关键字执行对应程序
                pass
                # wait_func(case_name)
            # 图片是否存在
            # elif case_type == "img_exists":
            #     # 获取关键字执行对应程序
            #     return exists_func(case_name)

            # 断言元素文本值与预期相等
            elif case_type == "assert_text":
                result = self.node_path(data).exists()
                if result is False:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, data)
                    pytest.fail(case_name + "->断言文本失败,该元素不存在")
                else:
                    result_text = self.node_path(data).get_text()
                    # 实际与预期不一致则失败
                    if result_text != note:
                        except_go_main(self.client, self.node_path(data))
                        self.log.info("%s 失败:预期值%s--实际值%s", case_name, note,
                                      result_text)
                        pytest.fail(
                            case_name + "->断言文本失败,预期值:" + note + " 实际值:" + result_text)
            # 断言元素文本值与预期不相等
            elif case_type == "assert_text_not":
                result = self.node_path(data).exists()
                if result is False:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, data)
                    pytest.fail(case_name + "->断言文本失败,该元素不存在")
                else:
                    result_text = self.node_path(data).get_text()
                    # 实际与预期一致则失败
                    if result_text == note:
                        except_go_main(self.client, self.node_path(data))
                        self.log.info("%s 失败:预期值%s--实际值%s", case_name, note,
                                      result_text)
                        pytest.fail(
                            case_name + "->断言元素文本不是某值失败,预期值:" + note + " 实际值:" + result_text)
            # 断言元素不存在则失败
            elif case_type == "assert":
                result = self.node_path(data).exists()
                if result is False:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, data)
                    pytest.fail(case_name + "断言元素存在失败" + data)
            # 断言元素存在则失败
            elif case_type == "assert_exist_fail":
                result = self.node_path(data).exists()
                if result is True:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, data)
                    pytest.fail(case_name + "断言元素不存在失败" + data)
            # 图片断言
            elif case_type == "assert_img":
                result = exists_func(case_name)
                if result is False:
                    except_go_main(self.client, self.node_path(data))
                    pytest.fail(case_name + "断言图片存在失败")
            # 元素等待
            elif case_type == "poco_wait":
                if note is None:
                    self.node_path(data).wait(timeout=120)
                else:
                    self.node_path(data).wait(timeout=int(note))
            # 轮询等待元素 存在即点击,不存在则标记用例失败
            elif case_type == "wait_for_appearance":
                result = self.node_path(data).wait_for_appearance()
                if result is None:
                    self.node_path(data).click()
                    if note is not None:
                        sleep(float(note))
                else:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, data)
                    pytest.fail(case_name + "元素不存在" + data)
            # 滑动从父节点坐标 滑动到子节点坐标
            elif case_type == "swipe":
                data = data.replace("]", "").replace(" ", "").replace("[", "")
                list_pos = data.split(",")
                self.client.swipe([float(list_pos[0]), float(list_pos[1])], [float(list_pos[2]), float(list_pos[3])])
                if note is not None:
                    sleep(float(note))
            # 获取文本对比进行断言
            elif case_type == "get_text":
                return self.node_path(data).get_text()

            # 长按默认2秒
            elif case_type == "long_click":
                if note is not None:
                    self.node_path(data).long_click(duration=float(note))
                else:
                    self.node_path(data).long_click()
            # 拖动 第一元素对象拖到到第二元素对象
            elif case_type == "drag_to":
                if note is not None:
                    data.drag_to(note, duration=0.6)

            # 图片点击
            elif case_type == "touch":
                touch_func(case_name)
            # 双击
            elif case_type == "double_click":
                pos = self.node_path(data).get_position()
                self.client.agent.input.click(pos[0], pos[1])
                self.client.agent.input.click(pos[0], pos[1])
                if note is not None:
                    sleep(float(note))
            # 连续点击
            elif case_type == "continuous_click":
                for i in range(int(note)):
                    self.node_path(data).click()

            # 是否截图
            elif case_type == "snapshot":
                case_snapshot(case_name)
