class ResourceNotFoundError(Exception):
    """资源不存在异常"""
    pass

class DuplicateResourceError(Exception):
    """资源重复异常"""
    pass

class AuthenticationError(Exception):
    """认证失败异常"""
    pass

class ForbiddenError(Exception):
    """权限不足异常"""
    pass