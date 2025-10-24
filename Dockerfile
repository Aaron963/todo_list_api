# 使用官方的 Python 3.12 基础镜像
FROM python:3.12-slim

# 安装必要的系统依赖
RUN apt-get update && apt-get install -y libpq-dev build-essential

RUN apt-get update && apt-get install -y lsof

# 对于基于 Debian/Ubuntu 的镜像
RUN apt-get update && apt-get install -y curl

# 安装 pipenv
RUN pip install --no-cache-dir pipenv

# 设置工作目录
WORKDIR /app

# 复制 Pipfile 和 Pipfile.lock
COPY Pipfile Pipfile.lock ./

# 安装项目依赖
RUN pipenv install --system

RUN pip install redis

RUN pip install selenium
RUN pip install watchdog

# 安装 tzdata 包
RUN apt-get update && apt-get install -y tzdata

# 设置时区为主机时区（例如：Asia/Shanghai）
ENV TZ=Asia/Shanghai

# 重新配置时区数据
RUN dpkg-reconfigure -f noninteractive tzdata

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000