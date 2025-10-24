from flask import Flask
from app.config.config import Config
from app.extensions import init_postgres, init_mongo, init_jwt
from app.controllers import auth_api, todo_list_api, todo_item_api

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 初始化扩展
    init_postgres(app)
    init_mongo(app)
    init_jwt(app)

    # 注册控制器路由
    auth_api.init_app(app)
    todo_list_api.init_app(app)
    todo_item_api.init_app(app)

    return app