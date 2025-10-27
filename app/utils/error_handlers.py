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
            return {
                "code": 400,
                "message": "Invalid request data",
                "errors": e.errors()
            }, 400
        except ResourceNotFoundError as e:
            return {
                "code": 404,
                "message": str(e)
            }, 404
        except DuplicateResourceError as e:
            return {
                "code": 409,
                "message": str(e)
            }, 409
        except AuthenticationError as e:
            return {
                "code": 401,
                "message": str(e)
            }, 401
        except ForbiddenError as e:
            return {
                "code": 403,
                "message": str(e)
            }, 403
        except Exception as e:
            print('Internal server error', str(e))
            return {
                "code": 500,
                "message": "Internal server error"
            }, 501

    wrapper.__name__ = func.__name__
    return wrapper
