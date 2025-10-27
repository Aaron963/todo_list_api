class BusinessError(Exception):
    """所有业务异常的基类，统一返回格式"""
    code: int = 400  # 默认HTTP状态码
    message: str = "业务处理失败"

    def __init__(self, message: str = None):
        if message:
            self.message = message
        super().__init__(self.message)

class DuplicateResourceError(BusinessError):
    """资源重复异常"""
    code = 401
    message = "DuplicateResourceError"

class AuthenticationError(BusinessError):
    """认证失败异常"""
    code = 401
    message = "AuthenticationError"

class ForbiddenError(BusinessError):
    """权限不足异常"""
    code = 401
    message = "ForbiddenError"

class DuplicateEmailError(BusinessError):
    """邮箱已被注册异常"""
    code = 401
    message = "该邮箱已被注册，请使用其他邮箱"


class InvalidCredentialsError(BusinessError):
    """认证失败异常（邮箱或密码错误）"""
    code = 401
    message = "邮箱或密码错误，请重新输入"


class PermissionDeniedError(BusinessError):
    """权限不足异常（无操作权限）"""
    code = 403
    message = "您没有权限执行此操作"


class ResourceNotFoundError(BusinessError):
    """资源不存在异常（查询的对象不存在）"""
    code = 404
    message = "请求的资源不存在"