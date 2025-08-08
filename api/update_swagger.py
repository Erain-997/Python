# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Author : Z Erain
# Date : 2025-07-21
# Description : 校验接口文件的接口和实际客户端使用的接口
#               生成 matched_urls.txt 用于后续接口校验。
# ------------------------------------------------------------
import json
import os
from pathlib import Path


def load_matched_urls(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def mark_deprecated_apis(swagger_path, used_urls_path, output_path):
    with open(swagger_path, "r", encoding="utf-8") as f:
        swagger = json.load(f)

    matched_urls = load_matched_urls(used_urls_path)
    print(f"✅ 已匹配接口路径数：{len(matched_urls)}")

    paths = swagger.get("paths", {})
    for path_url, methods in paths.items():
        print(f"处理接口路径：{path_url}")
        normalized_path = path_url.replace("/ffff", "")
        if normalized_path not in matched_urls:
            for method, method_data in methods.items():
                if isinstance(method_data, dict):
                    summary = method_data.get("summary", "")
                    # 剔除一个h5接口
                    if "非客户端" not in summary and "/ffff/clickAd/lpReport" not in path_url:
                        method_data["summary"] = summary + "（非客户端）"

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(swagger, f, ensure_ascii=False, indent=2)

    print(f"✅ 处理完成，已保存至：{output_path}")


if __name__ == "__main__":
    # 获取当前脚本文件所在目录
    base_dir = Path(__file__).resolve().parent

    # 构造文件路径
    swagger_json_path = base_dir / "swaggerApi.json"
    matched_urls_path = base_dir / "matched_urls.txt"
    output_path = base_dir / "swagger_updated.json"

    # 执行函数
    if swagger_json_path.exists() and matched_urls_path.exists():
        mark_deprecated_apis(swagger_json_path, matched_urls_path, output_path)
    else:
        print("❌ 找不到必要的文件，请确认 swaggerApi.json 和 matched_urls.txt 存在于当前脚本目录下。")
