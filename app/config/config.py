import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """基础配置"""
    # PostgresSQL
    POSTGRES_URI = os.getenv(
        "POSTGRES_URI",
        "postgresql://todo_user:todo_pass@postgres:5432/todo_auth_db"
    )
    # MongoDB
    MONGODB_URI = os.getenv(
        "MONGODB_URI",
        "mongodb://mongo:27017/todo_db"
    )
    # JWT
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev_jwt_secret_123")  # 生产环境需更换
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时过期

    # Flask API
    DEBUG = os.getenv("FLASK_ENV", "development") == "development"
    PORT = int(os.getenv("PORT", os.getenv("API_PORT", 5000)))