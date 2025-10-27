from flask_jwt_extended import JWTManager


def init_jwt(app):
    """初始化JWT扩展"""
    jwt = JWTManager(app=app)

    # 令牌过期回调
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            "code": 401,
            "message": "Token has expired"
        }, 401

    # 无效令牌回调
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print('error', str(error))
        return {
            "code": 401,
            "message": "Invalid token"
        }

    # 未提供令牌回调
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "code": 401,
            "message": "Authentication token is required"
        }, 401