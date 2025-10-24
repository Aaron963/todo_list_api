from flask import jsonify
from pydantic import ValidationError
from app.utils.errors import (
    ResourceNotFoundError,
    DuplicateResourceError,
    AuthenticationError,
    ForbiddenError
)

def handle_exceptions(func):
    """统一异常处理装饰器"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValidationError as e:
            return jsonify({
                "code": 400,
                "message": "Invalid request data",
                "errors": e.errors()
            }), 400
        except ResourceNotFoundError as e:
            return jsonify({
                "code": 404,
                "message": str(e)
            }), 404
        except DuplicateResourceError as e:
            return jsonify({
                "code": 409,
                "message": str(e)
            }), 409
        except AuthenticationError as e:
            return jsonify({
                "code": 401,
                "message": str(e)
            }), 401
        except ForbiddenError as e:
            return jsonify({
                "code": 403,
                "message": str(e)
            }), 403
        except Exception as e:
            return jsonify({
                "code": 500,
                "message": "Internal server error"
            }), 500
    return wrapper