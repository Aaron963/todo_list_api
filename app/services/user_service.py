from sqlalchemy.orm import Session
from typing import Optional
from app.models.users import User, UserRole, Permission, PermType
from app.dto.user_dto import UserCreateDTO, UserLoginDTO
from app.utils.errors import (
    ResourceNotFoundError,
    DuplicateResourceError,
    AuthenticationError,
    ForbiddenError
)


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_create: UserCreateDTO) -> User:
        # check email address is exist
        if self.db.query(User).filter(User.email == user_create.email).first():
            print('check email address is exist， raise')
            raise DuplicateResourceError(f"Email {user_create.email} already registered")

        # creating new user
        user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            role=UserRole.USER
        )
        user.set_password(user_create.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def login_user(self, user_login: UserLoginDTO) -> User:
        user = self.db.query(User).filter(User.email == user_login.email).first()
        if not user or not user.verify_password(user_login.password):
            raise AuthenticationError("Invalid email or password")
        return user

    def get_user_by_id(self, user_id: int) -> User:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResourceNotFoundError(f"User {user_id} not found")
        return user

    def check_list_permission(self, user_id: int, list_id: str, required_perm: PermType):
        perm = self.db.query(Permission).filter(
            Permission.user_id == user_id,
            Permission.list_id == list_id,
            Permission.perm_type == required_perm
        ).first()
        if not perm:
            raise ForbiddenError(f"User {user_id} has no {required_perm} permission for list {list_id}")

    def grant_list_permission(self, user_id: int, list_id: str, perm_type: PermType) -> Permission:
        # 检查用户是否存在
        self.get_user_by_id(user_id)

        # 检查权限是否已存在
        existing = self.db.query(Permission).filter(
            Permission.user_id == user_id,
            Permission.list_id == list_id
        ).first()
        if existing:
            existing.perm_type = perm_type
            self.db.commit()
            return existing

        # 创建新权限
        perm = Permission(
            user_id=user_id,
            list_id=list_id,
            perm_type=perm_type
        )
        self.db.add(perm)
        self.db.commit()
        self.db.refresh(perm)
        return perm