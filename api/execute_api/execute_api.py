# _*_coding:utf-8_*_
# Author：Erain
# Time：2022/11/08
import time
from api.devices_init.devices_init import DevicesInit
from api.devices_init.devices_info import DevicesInfo
from api.result_api.case_report import create_excel, form_style
from api.common_api.project_path import report_path, img_path, config_path
from api.common_api.get_config import get_cfg_data
from multiprocessing import Process, Queue, Lock
from airtest.core.api import *
from airtest.core.android.recorder import *
from airtest.core.android.adb import *
from api.common_api.ding_api import ding_push

form_style = form_style()
sheet_list = []
q = Queue()


class ExecuteApi(DevicesInit, DevicesInfo):
    def run_case(self, devices_id, path, rows_list, q):
        package = get_cfg_data(config_path(path), "package")
        self.device_connect(devices_id)
        for i in range(int(get_cfg_data(config_path(path), "rounds"))):
            rows = rows_list[i]
            try:
                adb = ADB(serialno=devices_id)
                recorder = Recorder(adb)
                # 开启录屏
                recorder.start_recording()
                time.sleep(1)
                resolution = self.get_resolution()
                # 冷启动
                start_app_time = time.time()
                start_app(package)
                # sdk 确认提醒
                # wait(Template(img_path(path) + r"sdk_warn.png", record_pos=(-0.025, 0.926), resolution=(720, 1440)),
                #      interval=0.001, timeout=180)
                # # 点击确认
                # sdk_time = time.time()
                # touch(Template(img_path(path) + r"sdk_verify.png", record_pos=(0.001, 0.928), resolution=(720, 1440)),
                #       times=10)
                # sdk_end_time = time.time() - sdk_time + 1

                wait(Template(img_path(path) + r"start_app.png", record_pos=(-0.203, 0.646),
                              resolution=resolution),
                     interval=0.001,
                     timeout=120)
                # end_time = time.time() - start_app_time - sdk_end_time
                end_time = time.time() - start_app_time
                # 确保资源全部加载
                time.sleep(2)
                # 登录耗時
                start_login = time.time()
                if type(touch(
                        Template(img_path(path) + r"start_login.png", record_pos=(-0.079, 0.65),
                                 resolution=resolution),
                        times=10)) is tuple:
                    start_login = time.time()

                wait(Template(img_path(path) + r"login_complete.png", record_pos=(-0.075, 0.774),
                              resolution=resolution), timeout=180,
                     interval=0.001)
                login_end_time = time.time() - start_login
                recorder.stop_recording(
                    output=report_path(path) + "/" + self.get_device_info(devices_id) + time.strftime("%m_%d_%H_%M_%S",
                                                                                                      time.localtime()) + ".mp4")
                stop_app(package)
                # clear_app(package)
                # 记录
                sheet_list.append([rows, 0, self.get_game_name(package)])
                sheet_list.append([rows, 1, self.get_device_info(devices_id)])
                sheet_list.append([rows, 2, float(format(end_time, '.2f'))])
                sheet_list.append([rows, 3, float(format(login_end_time, '.2f'))])
            except Exception as e:
                print(e)
                recorder.stop_recording(
                    output=report_path(path) + "/" + self.get_device_info(devices_id) + time.strftime("%m_%d_%H_%M_%S",
                                                                                                      time.localtime()) + ".mp4")
                if devices_id:
                    print("退出程序")
                    stop_app(package)
                sheet_list.append([rows, 0, self.get_game_name(package)])
                sheet_list.append([rows, 1, self.get_device_info(devices_id)])
                sheet_list.append([rows, 2, "执行失败"])
                sheet_list.append([rows, 3, "执行失败"])
                # q.put(sheet_list)
        q.put(sheet_list)

    def run_api(self, path):
        filename, sheet = create_excel()
        p_lst = []
        for id in self.get_devices():
            rows_list = []
            for i in range(int(get_cfg_data(config_path(path), "rounds"))):
                rows_list.append(self.rows())
            time.sleep(1)  # 需要sleep 避免端口冲突
            p = Process(target=self.run_case, args=(id, path, rows_list, q,))
            p.start()
            p_lst.append(p)
        [p.join() for p in p_lst]
        # 获取结果list
        dicts = [q.get() for d in p_lst]
        for de_rows in range(len(dicts)):
            for i in range(len(dicts[de_rows])):
                sheet.write(dicts[de_rows][i][0], dicts[de_rows][i][1], dicts[de_rows][i][2], form_style)

        filename.save(report_path(path) + "/report" + time.strftime("%m_%d_%H_%M_%S", time.localtime()) + '.xls')
