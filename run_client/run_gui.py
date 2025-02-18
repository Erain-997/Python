import sys

from adb_connect import ADBManager
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import subprocess
import paramiko
import re
from output_callback_manager import OutputCallbackManager  # 导入单例类
from check_appium_progress import list_appium_processes, terminate_appium_processes
from run_api import Api
from ssh_connect import (
    create_ssh_client,
    ssh_python_run,
    ssh_python_run_test_cases,
    ssh_execute_commands,
)
import webbrowser
from tkinter import ttk, simpledialog, scrolledtext

from tool_func import ToolFunc


def start_tkinter(api):
    root = tk.Tk()
    root.title("AutoTest-Win")
    # 设置窗口大小
    root.geometry("800x800")  # 宽度800像素，高度600像素

    # 配置主窗口的行和列，使其可伸缩
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # 工具模块
    tools_frame = ttk.LabelFrame(root, text="工具模块", padding="10")
    tools_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    button_list_device = ttk.Button(
        tools_frame,
        text="查看运行中的设备进程",
        command=lambda: api.run_adb_operations("list_device_processes"),
    )
    button_list_device.grid(row=0, column=0, padx=5, pady=5)
    ToolFunc(button_list_device, "查看所有在进行中设备进程, 可以看到残留的报告服务")

    def open_report_server():
        api.run_adb_operations("open_report")
        webbrowser.open("http://192.168.120.54:9988")

    open_report = ttk.Button(
        tools_frame,
        text="查看历史报告",
        command=open_report_server,
    )
    open_report.grid(row=0, column=3, padx=5, pady=5)
    ToolFunc(open_report, "查看历史报告, 根据设备ip和时间戳寻找")

    button_list_appium = ttk.Button(
        tools_frame,
        text="查看运行中的Appium进程",
        command=lambda: api.run_adb_operations("list_appium_processes"),
    )
    button_list_appium.grid(row=0, column=1, padx=5, pady=5)
    ToolFunc(button_list_appium, "查看目前正在进行的自动化进程")

    button_git_pull = ttk.Button(
        tools_frame,
        text="git pull",
        command=lambda: api.run_adb_operations("git_pull"),
    )
    button_git_pull.grid(row=0, column=2, padx=5, pady=5)
    ToolFunc(button_git_pull, "更新脚本代码")

    # 清理模块
    clear_frame = ttk.LabelFrame(root, text="环境清理模块", padding="10")
    clear_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=2)

    def terminate_appium_with_port():
        port = simpledialog.askstring("输入端口名", "请输入端口名 (可以为空):")
        terminate_appium_processes(port)

    button_kill_appium = ttk.Button(
        clear_frame,
        text="终止所有Appium进程",
        command=terminate_appium_with_port,
    )
    button_kill_appium.grid(row=0, column=0, padx=5, pady=2)
    ToolFunc(button_kill_appium, "会影响正在进行的测试")

    button_clear = ttk.Button(
        clear_frame,
        text="清理测试环境",
        command=lambda: api.run_adb_operations("clear_all"),
    )
    button_clear.grid(row=0, column=1, padx=5, pady=2, sticky=tk.E)
    ToolFunc(button_clear, "清除所有自动化进程, 请确认无人在运行测试, 否则会强制终止")

    # apk工具模块
    apk_frame = ttk.LabelFrame(root, text="apk工具模块", padding="10")
    apk_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # versions, apks, cases = api.start_app()

    def update_apk_version_now(event=None):
        api.get_apk_versions()

    label_version = ttk.Label(apk_frame, text="版本号:")
    label_version.pack(side=tk.LEFT, padx=5, pady=1)
    label_version.bind("<Button-1>", update_apk_version_now)
    ToolFunc(label_version, "此版本是包体版本, 若无版本请联系自动化人员更新脚本, 点击会更新版本")

    def update_apk_version(event=None):
        if not hasattr(update_apk_version, "cache"):
            update_apk_version.cache = {}

        version = entry_version.get()
        if version not in update_apk_version.cache:
            update_apk_version.cache[version] = api.get_apk_versions()

        entry_version.config(values=update_apk_version.cache[version])

    entry_version = ttk.Combobox(apk_frame, values=api.apk_version_list)
    entry_version.pack(side=tk.LEFT, padx=1, pady=1)
    entry_version.bind("<Button-1>", update_apk_version)
    entry_version.set(api.apk_version_list[-1])  # 设置默认值

    def update_apks(event=None):
        if not hasattr(update_apks, "cache"):
            update_apks.cache = {}

        version = entry_version.get()
        if version not in update_apks.cache:
            update_apks.cache[version] = api.get_apks(version)

        apk_name.config(values=update_apks.cache[version])

    apk_name = ttk.Combobox(apk_frame, values=api.apk_list, width=25)
    apk_name.pack(side=tk.LEFT, padx=1, pady=1)
    apk_name.bind("<Button-1>", update_apks)
    apk_name.set(api.apk_list[-1])

    check_apk_version_map = {True: "-apk", False: " "}
    check_apk_version_box = tk.BooleanVar(value=False)
    check_apk_version = ttk.Checkbutton(apk_frame, text="更新apk", variable=check_apk_version_box)
    check_apk_version.pack(side=tk.LEFT, padx=5, pady=1)
    ToolFunc(check_apk_version, "在启动测试后安装指定apk")

    # 脚本运行模块
    script_frame = ttk.LabelFrame(root, text="脚本运行模块", padding="10")
    script_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    label_case_name = ttk.Label(script_frame, text="模块:")
    label_case_name.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    ToolFunc(label_case_name,
             "支持单用例模式, 自定义输入用例名称, 详见测试用例"
             "\n格式如: test_advertisement_module.py::TestAdvertisementModule::test_advertisement_1")

    entry_case_name = ttk.Combobox(
        script_frame,
        width=30,  # 增加按钮宽度
        values=api.cases_list
    )
    entry_case_name.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
    entry_case_name.set(api.cases_list[-1])

    def update_modules(event=None):
        api.get_supported_modules()
        entry_case_name.config(values=api.cases_list)

    label_case_name.bind("<Button-1>", update_modules)

    # 勾选框，默认勾选
    check_proxy_map = {True: "-proxy", False: " "}
    check_var_proxy = tk.BooleanVar(value=True)
    check_proxy = ttk.Checkbutton(script_frame, text="代理", variable=check_var_proxy)
    check_proxy.grid(row=0, column=2, padx=5, pady=5)
    ToolFunc(check_proxy, "启用代理功能, 会将所有的ABtest的值置为0")

    # 勾选框，默认勾选
    check_feishu_map = {True: "-feishu", False: " "}
    check_var_feishu = tk.BooleanVar(value=True)
    check_feishu = ttk.Checkbutton(script_frame, text="飞书通知", variable=check_var_feishu)
    check_feishu.grid(row=0, column=3, padx=5, pady=5)
    ToolFunc(check_feishu, "启用飞书通知功能, 用例执行结束后会将报告发到飞书群里")

    # 勾选框，默认勾选
    check_record_map = {True: "-record", False: " "}
    check_var_record = tk.BooleanVar(value=True)
    check_record = ttk.Checkbutton(script_frame, text="录屏", variable=check_var_record)
    check_record.grid(row=0, column=4, padx=5, pady=5)
    ToolFunc(check_record, "启用录屏功能, 无论用例失败与否都保留录屏, 否则只记录失败录屏")

    def copy_to_clipboard(text):
        root.clipboard_clear()
        root.clipboard_append(text)
        root.update()

    def on_right_click(event, uid, ip):
        # 创建右键菜单
        menu = tk.Menu(root, tearoff=0)
        menu.add_command(label="复制设备 ID ", command=lambda: copy_to_clipboard(uid))
        menu.add_command(label="复制 IP 地址", command=lambda: copy_to_clipboard(ip))
        menu.post(event.x_root, event.y_root)

    def update_device_list():
        output_callback_in = OutputCallbackManager().get_callback()
        devices = api.get_device_list()
        if not devices:
            # 弹出错误提示框
            messagebox.showerror("错误", f"未检测到设备, 请接入设备")
            return
        res = api.set_device_ip(devices)
        if not res:
            messagebox.showerror("错误", f"获取不到设备ip, 请确认设备连接内网网络, 连接内网wifi")
            return
        for widget in script_frame.grid_slaves(row=2, column=1):
            widget.destroy()
        count = 0
        for device_id, device in res.items():
            count = count + 1
            radio = ttk.Radiobutton(
                script_frame,
                text=device["name"] + "" + device["uid"] + "\n" + device["ip"],
                variable=device_var,
                value=device["ip"],
            )
            radio.grid(row=2, column=count, padx=5, pady=5, sticky=tk.W)
            # 绑定右键事件
            radio.bind("<Button-3>", lambda event, uid=device["name"], ip=device["ip"]: on_right_click(event, uid, ip))

        output_callback_in(f"\n 设备检查结束 , 请选择设备 \n")

    # 创建按钮
    button_check_devices = ttk.Button(
        script_frame, text="检测手机",
        command=update_device_list
    )
    button_check_devices.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
    ToolFunc(button_check_devices, "请先连接手机, 多设备多耗时")

    device_var = tk.StringVar()

    update_apk = ttk.Button(
        apk_frame,
        text="立即安装app",
        command=lambda: api.update_app(device_var.get(), entry_version.get(), apk_name.get()),
    )
    update_apk.pack(side=tk.LEFT, padx=5, pady=1)
    ToolFunc(update_apk, "更新手机apk")

    label_remark = tk.Label(script_frame, text="启动测试追加参数:")
    label_remark.grid(row=4, column=0, padx=1, pady=1, sticky=tk.W)
    # Add the entry widget for additional parameters
    entry_additional_params = tk.Entry(script_frame)
    entry_additional_params.grid(row=4, column=1, padx=1, pady=1, sticky=tk.EW)
    entry_additional_params.insert(0, "")  # Set default value

    button_clear_proxy = ttk.Button(
        script_frame,
        text="清空手机代理",
        command=lambda: api.run_adb_operations("clear_proxy", device_var.get()),
    )
    button_clear_proxy.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
    ToolFunc(button_clear_proxy, "请勾选手机后执行")

    def run_script():
        if not device_var.get():
            # 弹出错误提示框
            messagebox.showerror("错误", f"未检测到设备, 请选择设备")
            return
        api.add_to_history(apk_name.get(), api.apk_list),
        apk_name.config(values=api.apk_list),
        api.add_to_history(entry_version.get(), api.apk_version_list),
        entry_version.config(values=api.apk_version_list),
        api.add_to_history(entry_case_name.get(), api.cases_list),
        entry_case_name.config(values=api.cases_list),
        api.run_python_script(
            version=entry_version.get(),
            module=entry_case_name.get(),
            device=device_var.get(),
            proxy=check_proxy_map[check_var_proxy.get()],
            feishu=check_feishu_map[check_var_feishu.get()],
            record=check_record_map[check_var_record.get()],
            apk=check_apk_version_map[check_apk_version_box.get()],
            apk_path=apk_name.get(),
            exif_params=entry_additional_params.get(),
        ),

    # 运行脚本 按钮
    button_run_script = ttk.Button(
        script_frame,
        text="启动测试",
        # width=20,  # 增加按钮宽度
        command=run_script
    )
    button_run_script.grid(row=5, column=0, columnspan=6, padx=5, pady=5, sticky=tk.EW)
    ToolFunc(button_run_script, "运行脚本前, 请先选择设备")

    button_list_appium = ttk.Button(
        script_frame,
        text="终止测试",
        command=lambda: api.run_adb_operations("kill_device_processes", device_var.get()),
    )
    button_list_appium.grid(row=5, column=7, padx=1, pady=1)
    ToolFunc(button_list_appium, "请勾选手机后执行")

    entry_commands = tk.Entry(script_frame)
    entry_commands.grid(row=6, column=1, padx=1, pady=1, sticky=tk.EW)
    label_remark = tk.Button(
        script_frame,
        text="单独执行脚本",
        command=lambda: api.run_single_script(entry_commands.get())
    )
    label_remark.grid(row=6, column=0, padx=10, pady=1, sticky=tk.W)
    ToolFunc(label_remark, "独立执行Linux命令, 可作为调试用")
    ToolFunc(entry_commands, "独立执行Linux命令, 可作为调试用")

    # 日志模块
    log_frame = ttk.LabelFrame(root, text="日志", padding="10")
    log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # 配置 log_frame 的行和列，使其可伸缩
    log_frame.columnconfigure(0, weight=1)
    log_frame.rowconfigure(0, weight=1)

    text_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
    text_area.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    def output_callback(line):
        try:
            text_area.insert(tk.END, line.decode("utf-8"))
        except AttributeError:
            text_area.insert(tk.END, line)
        text_area.see(tk.END)

    OutputCallbackManager().set_callback(output_callback)

    button_clear_log = ttk.Button(
        log_frame,
        text="清空日志",
        command=lambda: text_area.delete(1.0, tk.END),
    )
    button_clear_log.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    api = Api()
    start_tkinter(api)
