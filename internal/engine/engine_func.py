# _*_coding:utf-8_*_
# Author：Erain
# Time：2021/04/08
"""设计原则:操作类型不涉及节点操作 例如input_text skip_tag 不用于节点排序规则,字段能少则少"""
import allure
import json
import pytest
import uuid
from devices_init.devices_init import GetClient, except_function
from test_components.toolkit.tools import SmallTools
from internal.engine.engine_part import wait_func, exists_func, touch_func
from internal.tools.assist_func import *
from internal.tools.tool import except_go_main, assert_report, case_snapshot
from internal.tools.log import log
from devices_init.devices_init import args

execution_decision = {}
drag_to_list = []
text_dict = {}


class EngineFunc(GetClient, SmallTools):
    log = log(args.devices)
    type = "type"  # 操作类型
    case_name = "case_name"  # 用例名称
    offspring = "offspring"
    skip_tag = "skip_tag"  # if 条件
    input_text = "input_text"
    function_name = "function_name"
    father = "father"
    client_type = "client_type"  # 客户端类型
    client = ""
    snapshot = "snapshot"  # 是否截图
    condition = False

    def client_func(self, data):
        """
        获取客户端操作类型对象
        :param data:
        :return:
        """
        if data.get(self.client_type) == "android_poco":
            self.client = self.android_poco
        else:
            self.client = self.poco

    def node_path(self, data):
        """
        节点路径
        :param data:
        :return:
        """
        return eval("self.client" + data.get(self.father))

    def engine(self, data):
        case_type = data.get(self.type)
        input_text = data.get(self.input_text)
        case_name = data.get(self.case_name)
        father = data.get(self.father)

        with allure.step(case_name + ":" + case_type):
            # 注释用例
            if case_type == "//":
                return
            # 提交文本
            elif case_type == "set_text":
                if input_text is not None:
                    if input_text in text_dict.keys():
                        text = text_dict.get(input_text)
                    else:
                        text = input_text
                else:
                    text = str(uuid.uuid1()).replace("-", "")[:20]
                self.node_path(data).set_text(text)
            # 提交随机文本
            elif case_type == "set_rand":
                if input_text is not None:
                    text = str(uuid.uuid1()).replace("-", "")[:int(input_text)]
                else:
                    text = str(uuid.uuid1()).replace("-", "")[:20]
                self.node_path(data).set_text(text)

            # 点击
            elif case_type == "click":
                # 每次点击前如果有弹窗就关闭
                for i in range(3):
                    if self.client(textMatches="Tap to c*").exists():
                        try:
                            pos_list = self.client(textMatches="Tap to c*").get_position()
                            if pos_list[0] > 1 or pos_list[1] > 1:
                                break
                            self.client(textMatches="Tap to c*").click()
                            sleep(1)  # 等待下一个弹窗出来
                        except Exception:
                            sleep(1)  # 等待下一个弹窗出来

                    else:
                        break
                # 指定点击元素上的位置以及点击后间隔时间
                if input_text is not None:
                    if "," in input_text:
                        # 兼容传两个数和三个数
                        pos_list = input_text.split(",")
                        if len(pos_list) == 3:
                            self.node_path(data).click((float(pos_list[0]), float(pos_list[1])))
                            sleep(float(pos_list[2]))
                        else:
                            self.node_path(data).click((float(pos_list[0]), float(pos_list[1])))
                    else:
                        self.node_path(data).click()
                        sleep(float(input_text))
                else:
                    self.node_path(data).click()
            # 元素是否存在
            elif case_type == "exists":
                result = self.node_path(data).exists()
                # 存在即存入字典进行标记
                execution_decision["result"] = result
                execution_decision["case_name"] = case_name
            # 等待
            elif case_type == "wait":
                # 获取关键字执行对应程序
                wait_func(case_name)
            # 图片是否存在
            elif case_type == "img_exists":
                # 获取关键字执行对应程序
                result = exists_func(case_name)
                execution_decision["result"] = result
                execution_decision["case_name"] = case_name
            # 断言元素文本值与预期相等
            elif case_type == "assert_text":
                result = self.node_path(data).exists()
                if result is False:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, father)
                    pytest.fail(case_name + "->断言文本失败,该元素不存在")
                else:
                    result_text = self.node_path(data).get_text()
                    # 实际与预期不一致则失败
                    if result_text != input_text:
                        except_go_main(self.client, self.node_path(data))
                        self.log.info("%s 失败:预期值%s--实际值%s", case_name, input_text,
                                      result_text)
                        pytest.fail(
                            case_name + "->断言文本失败,预期值:" + input_text + " 实际值:" + result_text)
            # 断言元素文本值与预期不相等
            elif case_type == "assert_text_not":
                result = self.node_path(data).exists()
                if result is False:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, father)
                    pytest.fail(case_name + "->断言文本失败,该元素不存在")
                else:
                    result_text = self.node_path(data).get_text()
                    # 实际与预期一致则失败
                    if result_text == input_text:
                        except_go_main(self.client, self.node_path(data))
                        self.log.info("%s 失败:预期值%s--实际值%s", case_name, input_text,
                                      result_text)
                        pytest.fail(
                            case_name + "->断言元素文本不是某值失败,预期值:" + input_text + " 实际值:" + result_text)
            # 断言元素不存在则失败
            elif case_type == "assert":
                result = self.node_path(data).exists()
                if result is False:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, father)
                    pytest.fail(case_name + "断言元素存在失败" + father)
            # 断言元素存在则失败
            elif case_type == "assert_exist_fail":
                result = self.node_path(data).exists()
                if result is True:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, father)
                    pytest.fail(case_name + "断言元素不存在失败" + father)
            # 图片断言
            elif case_type == "assert_img":
                result = exists_func(case_name)
                if result is False:
                    except_go_main(self.client, self.node_path(data))
                    pytest.fail(case_name + "断言图片存在失败")
            # 元素等待
            elif case_type == "poco_wait":
                if input_text is None:
                    self.node_path(data).wait(timeout=120)
                else:
                    self.node_path(data).wait(timeout=int(input_text))
            # 轮询等待元素 存在即点击,不存在则标记用例失败
            elif case_type == "wait_for_appearance":
                result = self.node_path(data).wait_for_appearance()
                if result is None:
                    self.node_path(data).click()
                    if input_text is not None:
                        sleep(float(input_text))
                else:
                    except_go_main(self.client, self.node_path(data))
                    self.log.info("%s 失败 元素:%s", case_name, father)
                    pytest.fail(case_name + "元素不存在" + father)
            # 滑动从父节点坐标 滑动到子节点坐标
            elif case_type == "swipe":
                father = father.replace("]", "").replace(" ", "").replace("[", "")
                list_pos = father.split(",")
                self.client.swipe([float(list_pos[0]), float(list_pos[1])], [float(list_pos[2]), float(list_pos[3])])
                if input_text is not None:
                    sleep(float(input_text))
            # 获取文本对比进行断言
            elif case_type == "get_text":
                get_text = self.node_path(data).get_text()
                # input_text 为空则存取文本
                if input_text is not None:
                    if "==" in input_text:
                        data[self.input_text] = re_sign(input_text)
                        self.condition = True
                    # 存在增减字符,进行数量对比
                    if "-" in input_text:
                        case_name, num = string_re(input_text, "-")
                        # 判断字典key 是否存在 存在对比字典值,不存在则直接对比文本
                        if case_name in text_dict.keys():
                            assert_report(self.condition, int(text_dict.get(case_name)) - num, int(get_text),
                                          self.client,
                                          self.node_path(data), case_name)

                        else:
                            assert_report(self.condition, input_text, get_text, self.client,
                                          self.node_path(data), case_name)

                    elif "+" in input_text:
                        case_name, num = string_re(input_text, "+")
                        # 判断字典key 是否存在 存在对比字典值,不存在则直接对比文本
                        if case_name in text_dict.keys():
                            # 增加对应数量进行数目对比
                            assert_report(self.condition, int(text_dict.get(case_name)) + num, int(get_text),
                                          self.client,
                                          self.node_path(data), case_name)

                        else:
                            assert_report(self.condition, input_text, get_text, self.client,
                                          self.node_path(data), case_name)

                    # 判断字典key 是否存在 存在对比字典值,不存在则直接对比文本
                    elif input_text in text_dict.keys():
                        # 比对文本
                        assert_report(self.condition, text_dict.get(input_text), get_text, self.client,
                                      self.node_path(data), case_name)
                    else:
                        assert_report(self.condition, input_text, get_text, self.client,
                                      self.node_path(data), case_name)

                else:
                    # 获取文本存取后续可根据用例名进行断言
                    text_dict.setdefault(case_name, get_text)
            # 长按默认2秒
            elif case_type == "long_click":
                if input_text is not None:
                    self.node_path(data).long_click(duration=float(input_text))
                else:
                    self.node_path(data).long_click()
            # 拖动 第一元素对象拖到到第二元素对象
            elif case_type == "drag_to":
                drag_to_list.append(self.node_path(data))
                if len(drag_to_list) == 2:
                    drag_to_list[0].drag_to(drag_to_list[1], duration=0.6)
                    drag_to_list.clear()
            # 图片点击
            elif case_type == "touch":
                touch_func(case_name)
            # 双击
            elif case_type == "double_click":
                pos = self.node_path(data).get_position()
                self.client.agent.input.click(pos[0], pos[1])
                self.client.agent.input.click(pos[0], pos[1])
                if input_text is not None:
                    sleep(float(input_text))
            # 连续点击
            elif case_type == "continuous_click":
                for i in range(int(input_text)):
                    self.node_path(data).click()

            # 是否截图
            if data.get(self.snapshot) is not None:
                case_snapshot(case_name)

    def type_func(self, data):
        # 获取操作类型
        self.client_func(data)
        function_name = data.get(self.function_name)
        # 不包括中文
        if is_chinese(function_name) is False:
            with allure.step(data.get(self.case_name)):
                eval(function_name)
        elif function_name is not None and "循环" in function_name:  # 循环3次循环(3) 循环[3]
            # 获取循环次数
            loop = re.findall(r"\d+\.?\d*", function_name)
            if loop:
                for i in range(loop[0]):
                    self.engine(data)
            else:
                self.log.error("循环函数未设置循环次数:%s ", function_name)
        else:
            # 判断用例是否是条件下上个用例的条件用例,满足执行,不满足则跳过
            if execution_decision and execution_decision.get(self.case_name) == data.get(self.skip_tag):
                # skip_tag 字段判断结果为true
                if execution_decision["result"] is True or function_name == "假":
                    self.engine(data)
                else:
                    pass
            else:
                self.engine(data)
