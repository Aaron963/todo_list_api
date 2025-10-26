import os
from dotenv import load_dotenv

# 关键：只在开发环境加载 .env.prod 文件（生产环境不加载，避免意外读取本地文件）
if os.getenv("FLASK_ENV") == "development":
    # 开发环境：加载本地 .env.prod 文件（注入环境变量）
    load_dotenv(override=True)  # override=True：若系统已有环境变量，优先用 .env.prod 的值

class Config:
    # -------------------------- 数据库配置 --------------------------
    # PostgreSQL：从环境变量读取，生产环境必须传，开发环境无默认值（强迫用 .env.prod）
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")  # 开发本地默认 localhost
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    # 拼接 PostgreSQL 连接地址（统一格式）
    POSTGRES_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # MongoDB：从环境变量读取，格式同 PostgreSQL
    MONGODB_URI: str = os.getenv("MONGODB_URI")

    # -------------------------- 应用配置 --------------------------
    FLASK_APP: str = os.getenv("FLASK_APP", "app/__init__.py")
    FLASK_ENV: str = os.getenv("FLASK_ENV", "production")  # 默认生产环境（安全优先）
    API_PORT: int = int(os.getenv("API_PORT", "5000"))
    API_PREFIX: str = "/api"  # 通用配置，无需环境变量

    # JWT 配置：生产环境必须传，开发环境无默认值（强迫用 .env.prod）
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES: int = 3600  # 1小时过期

    # -------------------------- 生产环境强制校验 --------------------------
    def __post_init__(self):
        """初始化后校验：生产环境必须有所有敏感配置，避免遗漏"""
        if self.FLASK_ENV == "production":
            required_configs = [
                self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB,
                self.MONGODB_URI, self.JWT_SECRET_KEY
            ]
            # 检查是否有未传的配置
            missing = [name for name, val in zip(
                ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "MONGODB_URI", "JWT_SECRET_KEY"],
                required_configs
            ) if not val]
            if missing:
                raise ValueError(f"生产环境缺少必要配置：{', '.join(missing)}")

# 实例化配置（全局唯一）
config = Config()
# 调用校验方法（生产环境触发）
config.__post_init__()