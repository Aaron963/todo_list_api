# 导出用户相关模型，简化外部导入（如 from app.models.users import User, Permission）
from .user import User, UserRole
from .permission import Permission, PermType