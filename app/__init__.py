from flask import Flask
import logging
from app.config.config import Config
from app.extensions import init_postgres, init_mongo, init_jwt, init_redis
from app.controllers import auth_api, todo_list_api, todo_item_api


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.logger.setLevel(logging.DEBUG)

    # 禁用 Flask-RESTful 的默认错误处理，避免循环
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # initialize extensions
    init_redis(app)
    init_postgres(app)
    init_mongo(app)
    init_jwt(app)

    # register controller, route
    auth_api.init_app(app)
    todo_list_api.init_app(app)
    todo_item_api.init_app(app)

    # app.logger.debug("debug mode...")
    # app.logger.info("Flask app info...")
    return app
