from flask import Flask, request, render_template, send_file, jsonify, url_for
from flask_socketio import SocketIO, emit
from translate.translate import create_zip_file
from datetime import datetime
import os
import sys
from utils.log_handler import LogHandler

app = Flask(__name__)
socketio = SocketIO(app)

log_handler = LogHandler()


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/translate", methods=["GET", "POST"])
def translate():
    if request.method == "POST":
        log_handler.redirect_logs()

        # 现在所有的 print 语句都会通过 emit_log_message 函数发送到前端
        print("This will be sent to the front-end log.")
        # 获取上传的文件
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        if not file.filename.endswith(".xml"):
            return jsonify({"error": "Only .xml files are allowed"}), 400
        file_path = "xml_to_translate.xml"
        file.save(file_path)

        # 获取输入的 cookie 字符串
        cookie = request.form.get("cookie")
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        output_filename = f"translated_{current_time}.zip"
        if not cookie:
            gzip_file = create_zip_file(file_path)
        else:
            gzip_file = create_zip_file(file_path, cookie)
        # rename
        os.rename(gzip_file, output_filename)
        os.remove(file_path)
        file_url = url_for("download_file", filename=output_filename)

        # 恢复原始日志
        log_handler.restore_logs()
        # 获取日志内容
        logs = log_handler.get_logs()

        return jsonify({"logs": logs, "file_url": file_url})

    cookie_str = ""
    if os.path.exists("cache/cookies.txt"):
        with open("cache/cookies.txt", "r") as f:
            cookie_str = f.read()

    return render_template("translate.html", cookie_str=cookie_str, logs="")


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
