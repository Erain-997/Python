from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
import subprocess
import threading

app = Flask(__name__)
lock = threading.Lock()
connected_device = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/connect", methods=["POST"])
def connect():
    global connected_device
    device_ip = request.json["device_ip"]
    with lock:
        if connected_device is not None:
            # Disconnect the currently connected device
            subprocess.run(["adb", "disconnect", connected_device], check=True)
            connected_device = None
        try:
            # Set the environment variable
            os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-dir"

            # Set up ADB connection
            subprocess.run(["adb", "tcpip", "9999"], check=True)
            subprocess.run(["adb", "connect", device_ip], check=True)

            # Start scrcpy-ws with the specified device IP
            subprocess.run(["npm", "start", "--", "--tcpip=" + device_ip], cwd="/tmp/scrcpy-ws", check=True)
            connected_device = device_ip
            return jsonify({"status": "success", "message": "scrcpy-ws started successfully", "url": "http://localhost:8080"})
        except subprocess.CalledProcessError as e:
            return jsonify({"status": "error", "message": str(e)})

@app.route("/device")
def device():
    global connected_device
    device_ip = request.args.get("ip")
    if device_ip:
        with lock:
            if connected_device is not None:
                # Disconnect the currently connected device
                subprocess.run(["adb", "disconnect", connected_device], check=True)
                connected_device = None
            try:
                # Set the environment variable
                os.environ["XDG_RUNTIME_DIR"] = "/tmp/runtime-dir"

                # Set up ADB connection
                subprocess.run(["adb", "tcpip", "9999"], check=True)
                subprocess.run(["adb", "connect", device_ip.replace('_', '.')], check=True)

                # Start scrcpy-ws with the specified device IP
                subprocess.run(["npm", "start", "--", "--tcpip=" + device_ip.replace('_', '.')], cwd="/tmp/scrcpy-ws", check=True)
                connected_device = device_ip.replace('_', '.')
                return redirect("http://localhost:8080")
            except subprocess.CalledProcessError as e:
                return jsonify({"status": "error", "message": str(e)})
    return render_template("device.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    # 新增页面页面, 页面路径是 device, 输入 ip, ?ip=172_16_9_10_9999 以及启动scrcpy-ws 并且当前页面重定向到scrcpy-ws 生成的页面
    #  docker exec -it mobile-ui-automation-tests_web_remote_debug_1 /bin/sh
    #  adb设置成系统
    #  docker run --network host -p 8002:5000 mobile-ui-automation-tests_web_remote_debug /bin/sh
    #  scrcpy --tcpip=172.16.9.10:9999
    #  scrcpy --tcpip=172.31.251.119:9999
    #  scrcpy --tcpip=172.31.251.119:9999 --no-audio
    #  Start scrcpy with the specified device IP