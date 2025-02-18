import datetime
import os

# 获取当前日期和时间
now = datetime.datetime.now()
formatted_time = now.strftime("%Y%m%d_%H%M")

# 生成文件名
output_name = f"AutoTest-Win-{formatted_time}.exe"

# 构建 PyInstaller 命令
command = f"pyinstaller --onefile --windowed --icon=ic_launcher.ico --name={output_name} run_gui.py"

# 执行命令
os.system(command)
