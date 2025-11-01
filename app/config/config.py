import os
from dotenv import load_dotenv

if os.getenv("FLASK_ENV") == "development":
    load_dotenv(override=True)


class Config:
    # -------------------------- Database Configuration --------------------------
    # PostgreSQL：load from .env
    POSTGRES_USER: str = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_URI: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    # MongoDB：load from .env
    MONGO_USER: str = os.getenv("MONGO_USER")
    MONGO_PASSWORD: str = os.getenv("MONGO_PASSWORD")
    MONGO_HOST: str = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT: str = os.getenv("MONGO_PORT")
    MONGO_DB: str = os.getenv("MONGO_DB")
    MONGO_AUTH_DB: str = os.getenv("MONGO_AUTH_DB")

    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: str = os.getenv("REDIS_PORT")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD")

    # FLASK CACHING
    CACHE_TYPE: str = os.getenv("CACHE_TYPE")
    CACHE_REDIS_DB: str = os.getenv("CACHE_REDIS_DB")
    CACHE_KEY_PREFIX: str = os.getenv("CACHE_KEY_PREFIX")
    CACHE_DEFAULT_TIMEOUT: str = os.getenv("CACHE_DEFAULT_TIMEOUT")

    # FLASK
    FLASK_APP: str = os.getenv("FLASK_APP", "app/__init__.py")
    FLASK_ENV: str = os.getenv("FLASK_ENV", "development")
    API_PORT: int = int(os.getenv("API_PORT", "5000"))
    API_PREFIX: str = "/api"

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES: int = 36000  # expired by 1 days

    # -------------------------- 生产环境强制校验 --------------------------
    def __post_init__(self):
        """初始化后校验：生产环境必须有所有敏感配置，避免遗漏"""
        if self.FLASK_ENV == "production":
            required_configs = [
                self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_DB,
                self.JWT_SECRET_KEY
            ]
            # 检查是否有未传的配置
            missing = [name for name, val in zip(
                ["POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "JWT_SECRET_KEY"],
                required_configs
            ) if not val]
            if missing:
                raise ValueError(f"生产环境缺少必要配置：{', '.join(missing)}")


# 实例化配置（全局唯一）
config = Config()
# 调用校验方法（生产环境触发）
config.__post_init__()
