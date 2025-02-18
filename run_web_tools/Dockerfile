# 使用官方的 Python 镜像作为基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制当前目录的内容到容器的工作目录
COPY . /app

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Flask 默认端口
EXPOSE 5000

# 启动 Flask 应用
CMD ["python", "app.py"]