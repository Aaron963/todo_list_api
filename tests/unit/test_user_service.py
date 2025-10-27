import pytest
from unittest.mock import Mock, patch
from app.services.user_service import UserService
from app.utils.errors import DuplicateEmailError, InvalidCredentialsError
from app.models.users.user import User

class TestUserService:
    # 测试用户注册：正常情况
    def test_register_success(self):
        # Mock数据库会话（避免真实数据库）
        mock_db_session = Mock()
        mock_db_session.add = Mock()
        mock_db_session.commit = Mock()

        # 调用注册方法
        user = UserService.register(
            db_session=mock_db_session,
            email="new@example.com",
            password="Pass123!",
            full_name="New User"
        )

        # 验证结果：用户对象正确创建，密码已加密
        assert user.email == "new@example.com"
        assert user.full_name == "New User"
        assert user.password_hash != "Pass123!"  # 密码已哈希
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()

    # 测试用户注册：邮箱已存在
    def test_register_duplicate_email(self):
        # Mock数据库查询：模拟邮箱已存在
        mock_db_session = Mock()
        mock_query = Mock()
        mock_query.filter_by.return_value.first.return_value = User(email="existing@example.com")
        mock_db_session.query.return_value = mock_query

        # 验证是否抛出预期异常
        with pytest.raises(DuplicateEmailError):
            UserService.register(
                db_session=mock_db_session,
                email="existing@example.com",
                password="Pass123!",
                full_name="Duplicate User"
            )

    # 测试用户登录：密码正确
    def test_login_success(self):
        # Mock用户对象和密码校验
        mock_user = Mock(spec=User)
        mock_user.email = "test@example.com"
        mock_user.verify_password.return_value = True  # 密码验证通过

        # Mock数据库查询
        mock_db_session = Mock()
        mock_query = Mock()
        mock_query.filter_by.return_value.first.return_value = mock_user
        mock_db_session.query.return_value = mock_query

        # 调用登录方法
        user = UserService.login(
            db_session=mock_db_session,
            email="test@example.com",
            password="correct_pass"
        )

        # 验证结果
        assert user == mock_user
        mock_user.verify_password.assert_called_with("correct_pass")

    # 测试用户登录：密码错误
    def test_login_invalid_password(self):
        # Mock用户对象（密码验证失败）
        mock_user = Mock(spec=User)
        mock_user.verify_password.return_value = False

        # Mock数据库查询
        mock_db_session = Mock()
        mock_query = Mock()
        mock_query.filter_by.return_value.first.return_value = mock_user
        mock_db_session.query.return_value = mock_query

        # 验证是否抛出预期异常
        with pytest.raises(InvalidCredentialsError):
            UserService.login(
                db_session=mock_db_session,
                email="test@example.com",
                password="wrong_pass"
            )