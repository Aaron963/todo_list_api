from flask import Flask
from app.config.config import Config
from app.extensions import init_postgres, init_mongo, init_jwt
from app.controllers import auth_api, todo_list_api, todo_item_api

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 禁用 Flask-RESTful 的默认错误处理，避免循环
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # initialize extensions
    init_postgres(app)
    init_mongo(app)
    init_jwt(app)

    # 注册controller, route
    auth_api.init_app(app)
    todo_list_api.init_app(app)
    todo_item_api.init_app(app)

    return app
