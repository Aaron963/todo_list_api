from pymongo import MongoClient
from flask import current_app
import urllib.parse

def init_mongo(app):
    # aware: username and password encode with URL
    username = app.config["MONGO_USER"]
    password = app.config["MONGO_PASSWORD"]
    encoded_username = urllib.parse.quote_plus(username)
    encoded_password = urllib.parse.quote_plus(password)
    mongodb_uri = (
        f"mongodb://{encoded_username}:{encoded_password}@"
        f"{app.config['MONGO_HOST']}:{app.config['MONGO_PORT']}/"
        f"{app.config['MONGO_DB']}?authSource={app.config['MONGO_AUTH_DB']}"
    )
    client = MongoClient(mongodb_uri)
    app.mongo_client = client
    app.mongo_db = client.get_database()  # 获取数据库实例

def get_mongo_collection(collection_name: str):
    """获取MongoDB集合（依赖注入）"""
    return current_app.mongo_db[collection_name]