from flask import Flask
import logging
from app.config.config import Config
from app.extensions import init_postgres, init_mongo, init_jwt
from app.controllers import auth_api, todo_list_api, todo_item_api
from flask_caching import Cache

# init redis cache
cache = Cache(config={
    "CACHE_TYPE": "RedisCache",
    "CACHE_REDIS_HOST": "localhost",
    "CACHE_REDIS_PORT": 6379,
    "CACHE_REDIS_DB": 1,
    "CACHE_REDIS_PASSWORD": "",
    "CACHE_KEY_PREFIX": "todo_app:",
    "CACHE_DEFAULT_TIMEOUT": 7200
})

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.logger.setLevel(logging.DEBUG)

    # 禁用 Flask-RESTful 的默认错误处理，避免循环
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # init caching for flask
    cache.init_app(app)

    # initialize extensions
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
