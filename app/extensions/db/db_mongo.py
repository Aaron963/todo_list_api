from pymongo import MongoClient
from flask import current_app

def init_mongo(app):
    """初始化MongoDB连接"""
    client = MongoClient(app.config["MONGODB_URI"])
    app.mongo_client = client
    app.mongo_db = client.get_database()  # 获取数据库实例

def get_mongo_collection(collection_name: str):
    """获取MongoDB集合（依赖注入）"""
    return current_app.mongo_db[collection_name]