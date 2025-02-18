import socket
import sys

from apscheduler.schedulers.background import BackgroundScheduler
from flask import (
    Flask,
    render_template,
    jsonify,
    send_from_directory,
    redirect,
    render_template_string,
    request,
)
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from ansi2html import Ansi2HTMLConverter

from backup import backup_mysql_data
from common.data import allure_servers
from func.app import *
from func.common import *
from func.device import *
from func.report import *
from func.test_case import *
from func.test_plan import *

app = Flask(__name__)
scheduler = BackgroundScheduler()
# 配置 CORS，允许所有来源的跨域请求
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
# CORS(app, origins=["http://localhost:4000","http://192.168.120.150:4000"])
# 启用跨域支持，允许所有域名
CORS(app)
socketio = SocketIO(app)


def daily_backup():
    backup_mysql_data()
    Log.logger.info("每日任务执行于: %s", datetime.datetime.now())


# 添加每日任务，每天午夜执行一次
scheduler.add_job(daily_backup, 'cron', hour=0, minute=0)
scheduler.start()

# todo
"""
统一找时间, 打点用户数据, 如果有必要的话
目前需求:
 - 各个模块的翻页
 - 页面停留情况
"""


# @app.before_request
# def before_request_func():
#     # 打印请求方法（GET, POST, PUT, DELETE 等）
#     print(f"Request Method: {request.method}")
#     # 打印请求的 URL（不包括查询字符串）
#     print(f"Request URL: {request.url}")
#     # 打印完整的请求路径（包括查询字符串）
#     print(f"Path with Query String: {request.path}")
#     # 打印查询字符串参数
#     print("Query String Parameters:")
#     for key, value in request.args.items():
#         print(f"  {key}: {value}")
#     # 如果请求是 POST, PUT 等，打印表单数据或 JSON 数据
#     if request.method in ['POST', 'PUT']:
#         if request.is_json:
#             # 打印 JSON 数据
#             print("JSON Data:")
#             print(request.get_json())
#         else:
#             # 打印表单数据
#             print("Form Data:")
#             for key, value in request.form.items():
#                 print(f"  {key}: {value}")
#     # 打印远程用户地址（注意：这可能是代理后的地址，不一定准确）
#     print(f"Remote Address: {request.remote_addr}")


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@app.route("/")
@app.route("/files", defaults={"req_path": ""})
@app.route("/files/<path:req_path>")
def files(req_path=""):
    abs_path = os.path.join(BASE_DIR, "report_output", req_path)

    if not os.path.exists(abs_path):
        return "Path does not exist", 404

    if os.path.isfile(abs_path):
        if abs_path.endswith(".html"):
            return send_from_directory(
                os.path.dirname(abs_path), os.path.basename(abs_path)
            )
        else:
            return send_from_directory(
                os.path.dirname(abs_path),
                os.path.basename(abs_path),
                as_attachment=True,
            )

    files = os.listdir(abs_path)
    return render_template("index.html", files=files, current_path=req_path)


@app.route("/allure/<path:req_path>")
def allure(req_path):
    abs_path = os.path.join(BASE_DIR, "report_output", req_path)
    if os.path.isdir(abs_path) and os.path.basename(abs_path) == "allure-results":
        if req_path not in allure_servers:
            port = find_free_port()
            subprocess.Popen(["allure", "serve", abs_path, "--port", str(port)])
            allure_servers[req_path] = port
        else:
            port = allure_servers[req_path]
        return redirect(f"http://localhost:{port}")
    return "Not an Allure results directory", 404


@app.route('/files/<path:req_path>/log/<filename>')
def show_log_file(req_path: str, filename: str):
    log_dir = os.path.join(BASE_DIR, "report_output", req_path, 'log')
    file_path = os.path.join(log_dir, filename)
    if not os.path.isfile(file_path):
        return "File not found", 404
    return render_template("log.html", req_path=req_path, filename=filename)


@socketio.on('get_log_file')
def handle_get_log_file(data):
    log_dir = os.path.join(BASE_DIR, "report_output", data['req_path'], 'log')
    file_path = os.path.join(log_dir, data['filename'])

    if not os.path.isfile(file_path):
        emit('log_update', {'content': f'<span style="color: red;">File not found: {file_path}</span>'})
        return

    conv = Ansi2HTMLConverter()  # 创建 ANSI 转 HTML 转换器

    def read_log_file():
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                while True:
                    line = file.readline()
                    if not line:
                        time.sleep(0.5)  # 等待新数据
                        continue
                    yield conv.convert(line, full=False)  # 转换为 HTML 格式
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='gbk') as file:
                    while True:
                        line = file.readline()
                        if not line:
                            time.sleep(0.5)  # 等待新数据
                            continue
                        yield conv.convert(line, full=False)  # 转换为 HTML 格式
            except Exception as e:
                yield f'<span style="color: red;">Failed to read file: {str(e)}</span>'

    for line in read_log_file():
        emit('log_update', {'content': line})


@app.route("/get_device_list", methods=['GET'])
def get_device_list():
    try:
        response = func_get_device_list()
        return jsonify(response), 200

    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_device_status", methods=['POST'])
def get_device_status():
    try:
        req_data = request.json
        Log.logger.info("%s", req_data)
        udid = req_data.get('udid')
        device = req_data.get('device')
        if not device:
            return jsonify({"error": "device 参数缺失"}), 400
        response = func_get_device_status(device, udid)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/add_device", methods=['POST'])
def add_device():
    try:
        req_data = request.json
        Log.logger.info("%s", req_data)
        device = req_data.get('device')
        if not device:
            return jsonify({"error": "device 参数缺失"}), 400
        response = func_add_device(device)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/delete_device", methods=['POST'])
def delete_device():
    try:
        req_data = request.json
        Log.logger.info("%s", req_data)
        udid = req_data.get('udid')
        device = req_data.get('device')
        response = func_delete_device(udid, device)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/set_device", methods=['POST'])
def set_device():
    try:
        req_data = request.json
        Log.logger.info("%s", req_data)
        udid = req_data.get('udid')
        device = req_data.get('device')
        name_zh = req_data.get('name_zh')
        owner = req_data.get('owner')
        remarks = req_data.get('remarks')
        connect = req_data.get('connect', True)
        if not udid:
            return jsonify({"error": "udid 参数缺失"}), 400
        response = func_set_device(udid, name_zh, owner, remarks, connect, device)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_case_list", methods=['POST'])
def get_case_list():
    try:
        req_data = request.json
        Log.logger.info("%s", req_data)
        page = req_data.get('page')
        size = req_data.get('size')
        if page:
            del req_data['page']
        if size:
            del req_data['size']
        response = func_get_case_list(req_data, page, size)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_report_list", methods=['POST'])
def get_report_list():
    try:
        req_data = request.json
        Log.logger.info("%s", req_data)
        page = req_data.get('page')
        size = req_data.get('size')
        if page:
            del req_data['page']
        if size:
            del req_data['size']
        response = func_get_report_list(req_data, page, size)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/update_report", methods=['POST'])
def update_report():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        old_name = req_data.get('old_name')
        new_name = req_data.get('new_name')
        if not old_name:
            return jsonify({"error": "old_name 参数缺失"}), 400
        response = func_update_report(old_name, new_name)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_version_list", methods=['GET'])
def get_version_list():
    try:
        response = func_get_version_list()
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_apk_list", methods=['GET'])
def get_apk_list():
    try:
        version = request.args.get('version')
        if not version:
            return jsonify({"error": "version 参数缺失"}), 400
        response = func_get_apk_list(version)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/run_cases", methods=['POST'])
async def run_cases():
    try:
        req_data = request.json
        Log.logger.info("%s", req_data)
        plan_id = req_data.get('plan_id')

        if not plan_id:
            return jsonify({"error": "plan_id 参数缺失"}), 400

        response = await func_run_cases(plan_id)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/update_app", methods=['POST'])
def update_app():
    try:
        req_data = request.json
        Log.logger.info("%s", req_data)
        device = req_data.get('device')
        app_path = req_data.get('app_path')
        if not device or not isinstance(device, list):
            return jsonify({"error": "device 参数缺失"}), 400
        if not app_path:
            return jsonify({"error": "app_path 参数缺失"}), 400

        response = func_update_app(device, app_path)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/set_device_proxy", methods=['POST'])
def set_device_proxy():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        device = req_data.get('device')
        value = req_data.get('value')
        Log.logger.info("isinstance(device, list): %s", isinstance(device, list))
        Log.logger.info("device: %s", device)
        if not device or not isinstance(device, list):
            return jsonify({"error": "device 参数缺失或不是一个列表"}), 400
        if not value:
            return jsonify({"error": "value 参数缺失"}), 400

        response = func_set_device_proxy(device, value)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/git_pull", methods=['POST'])
def git_pull():
    try:
        response = func_git_pull()
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/stop_testing", methods=['POST'])
def stop_testing():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        plan_id = req_data.get('plan_id')
        if not plan_id:
            return jsonify({"error": "plan_id 参数缺失"}), 400
        response = func_stop_testing(plan_id)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/delete_report", methods=['POST'])
def delete_report():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        report_name = req_data.get('report_name')
        if not report_name:
            return jsonify({"error": "report_name 参数缺失"}), 400
        response = func_delete_report(report_name)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/delete_case", methods=['POST'])
def delete_case():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        response = func_delete_case(req_data)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_case", methods=['POST'])
def get_case():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        title_name = req_data.get('title_name')
        if not title_name:
            return jsonify({"error": "title_name 参数缺失"}), 400
        response = func_get_case(title_name)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/update_case", methods=['POST'])
def update_case():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        title_name = req_data.get('title_name')
        if not title_name:
            return jsonify({"error": "title_name 参数缺失"}), 400
        response = func_update_case(title_name, req_data)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_enumeration", methods=['POST'])
def get_enumeration():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        field_name = req_data.get('field_name')
        if not field_name:
            return jsonify({"error": "field_name 参数缺失"}), 400
        response = func_get_list(field_name, "cases")
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_enumeration_test_plan", methods=['POST'])
def get_enumeration_test_plan():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        field_name = req_data.get('field_name')
        if not field_name:
            return jsonify({"error": "field_name 参数缺失"}), 400
        response = func_get_list_test_plan(field_name, "test_plan")
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_enumeration_report", methods=['POST'])
def get_enumeration_report():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        field_name = req_data.get('field_name')
        if not field_name:
            return jsonify({"error": "field_name 参数缺失"}), 400
        response = func_get_list_report(field_name)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/create_case", methods=['POST'])
def create_case():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        default_values = {
            "case_type": "功能",
            "development_status": "待编写"
        }
        case_info_dict = {key: req_data.get(key, default_values.get(key)) for key in CaseInfo.__annotations__.keys()}
        case_info = CaseInfo(**case_info_dict)
        if not case_info.title_name:
            return jsonify({"error": "title_name 参数缺失"}), 400
        response = func_create_case(case_info)

        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/create_test_plan", methods=['POST'])
def create_test_plan():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        default_values = {
            "creat_time": now,
            "update_time": now
        }
        plan_info_dict = {key: req_data.get(key, default_values.get(key)) for key in TestPlan.__annotations__.keys()}
        plan_info = TestPlan(**plan_info_dict)

        response = func_test_plan_add(plan_info)

        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/test_plan_list", methods=['POST'])
def get_test_plan_list():
    try:
        req_data = request.json
        Log.logger.info("%s", req_data)
        page = req_data.get('page')
        size = req_data.get('size')
        if page:
            del req_data['page']
        if size:
            del req_data['size']
        response = func_test_plan_list(req_data, page, size)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_test_plan", methods=['POST'])
def test_plan():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        plan_id = req_data.get('plan_id')
        if not plan_id:
            return jsonify({"error": "plan_id 参数缺失"}), 400
        response = func_get_test_plan(plan_id)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/delete_test_plan", methods=['POST'])
def delete_test_plan():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        plan_id = req_data.get('plan_id')
        if not plan_id:
            return jsonify({"error": "plan_id 参数缺失"}), 400
        response = func_delete_test_plan(plan_id)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/update_test_plan", methods=['POST'])
def update_test_plan():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        plan_id = req_data.get('plan_id')
        if not plan_id:
            return jsonify({"error": "plan_id 参数缺失"}), 400
        response = func_update_test_plan(plan_id, req_data)
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_root_path", methods=['POST'])
def get_root_path():
    try:
        req_data = request.json
        Log.logger.info("req_data: %s", req_data)
        response = func_get_root_path()
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/get_language", methods=['GET'])
def get_language():
    try:
        response = func_get_language()
        return jsonify(response), 200
    except Exception as e:
        Log.logger.info("崩溃: %s", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    sys.stdout = Log
    socketio.run(app, host="0.0.0.0", port=9988, debug=False, allow_unsafe_werkzeug=True)
    Log.logger.info("服务启动")
