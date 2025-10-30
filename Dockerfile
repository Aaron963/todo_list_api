# This Dockerfile is used to build the python image
FROM python:3.11-slim

# 替换默认源为阿里云（解决网络问题）
RUN echo "deb http://mirrors.aliyun.com/debian/ bullseye main non-free contrib" > /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ bullseye main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian-security/ bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian-security/ bullseye-security main" >> /etc/apt/sources.list && \
    echo "deb http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list && \
    echo "deb-src http://mirrors.aliyun.com/debian/ bullseye-updates main non-free contrib" >> /etc/apt/sources.list

# 设置工作目录
WORKDIR /app

# 安装系统依赖并清理缓存
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# 安装 pipenv
RUN pip install --no-cache-dir pipenv

# 复制依赖文件并安装
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system

# 复制应用代码
COPY app/ ./app/

# 设置timezone
ENV TZ=Asia/Shanghai

# 创建非root用户并切换
RUN useradd -m appuser
USER appuser

# Flask API 默认端口
EXPOSE 5000