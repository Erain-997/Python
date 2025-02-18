import subprocess

from common.utils.arg_parse_func import args

AndroidVersion_14 = "14"
AndroidVersion_13 = "13"
AndroidVersion_12 = "12"
AndroidVersion_11 = "11"


def get_connected_device_info(start_port):
    """
    获取连接的 Android 设备信息
    """
    devices = []
    try:
        output = subprocess.check_output(["adb", "devices"]).decode("utf-8").strip().split("\n")[1:]
        for line in output:
            if line.strip():
                serial, status = line.split("\t")
                devices.append(serial)
    except Exception as e:
        print(f"Error getting connected devices: {e}")
    # 生成一个端口号列表
    device_port = {device: start_port + index for index, device in enumerate(devices)}

    if len(device_port) == 0:
        print("请连接设备: No connected devices found.")

    return device_port.items()


def get_device_names():
    """
    获取连接设备的名称
    """
    device_names = []
    try:
        output = (
            subprocess.check_output(
                ["adb", "-s", args.device, "shell", "getprop", "ro.product.brand"])
            .decode("utf-8")
            .strip()
        )
        device_names.append(output)
        output = (
            subprocess.check_output(["adb", "-s", args.device, "shell", "getprop", "ro.product.model"])
            .decode("utf-8")
            .strip()
        )
        device_names.append(output)
        return ", ".join(device_names)
    except Exception as e:
        return f"Error getting device name for {args.device}: {e}"


def get_device_version():
    """
    获取连接设备的系统版本: todo 暂定安卓
    """
    try:
        output = (
            subprocess.check_output(["adb", "-s", args.device, "shell", "getprop", "ro.build.version.release"])
            .decode("utf-8")
            .strip()
        )
        return output
    except Exception as e:
        return f"Error getting device version for {args.device}: {e}"


if __name__ == "__main__":
    print(get_device_version())
    # print(get_device_info())
