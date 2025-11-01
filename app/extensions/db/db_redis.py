from flask_caching import Cache

cache = Cache()


def init_redis(app):
    # init redis cache
    cache.init_app(app, config={
        "CACHE_TYPE": app.config["CACHE_TYPE"],
        "REDIS_HOST": app.config["REDIS_HOST"],
        "REDIS_PORT": app.config["REDIS_PORT"],
        "CACHE_REDIS_DB": app.config["CACHE_REDIS_DB"],
        "REDIS_PASSWORD": app.config["REDIS_PASSWORD"],
        "CACHE_KEY_PREFIX": app.config["CACHE_KEY_PREFIX"],
        "CACHE_DEFAULT_TIMEOUT": app.config["CACHE_DEFAULT_TIMEOUT"]
    })
