# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Author : Z Erain
# Date : 2025-07-21
# Description : 复制到客户端项目下, 提取 Dart 项目中的 HttpService().post 请求路径，
#               生成 swagger_update.json 用于生成python代码或者导入MeterSphere平台。
# ------------------------------------------------------------

import os
import re
import subprocess
from pathlib import Path

# 用于提取 HttpService().post("/xxx") 中的路径
pattern = re.compile(
    r'HttpService\(\)\s*\.\s*post\s*\(\s*["\'](.*?)["\']',
    re.DOTALL
)


def git_reset_and_pull(project_path):
    try:
        print(f"🔄 执行 git reset --hard")
        subprocess.run(["git", "reset", "--hard"], cwd=project_path, check=True)
        print(f"⬇️ 执行 git pull")
        subprocess.run(["git", "pull"], cwd=project_path, check=True)
        print("✅ Git 操作成功完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")


def find_http_calls(root_dir):
    urls = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".dart"):
                full_path = os.path.join(dirpath, file)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        urls += [m.group(1).strip() for m in pattern.finditer(content)]
                except Exception as e:
                    print(f"❌ 读取失败 {full_path}: {e}")
    return urls


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    project_root = base_dir  # 可替换为项目路径，如 Path("/Users/xxx/code/myproject")

    # 第一步：重置并拉取最新代码
    git_reset_and_pull(project_root)

    # 第二步：扫描 Dart 文件提取 URL
    result = find_http_calls(project_root)

    # 去重并保持顺序
    unique_urls = list(dict.fromkeys(result))
    unique_urls.append("/appReport/lpReport")  # H5调用的也加上

    # 第三步：保存结果
    output_path = base_dir / "matched_urls.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for url in unique_urls:
            f.write(url + "\n")

    print(f"✅ 共发现 URL（去重后）: {len(unique_urls)}")
    print(f"📄 结果已保存至: {output_path}")
