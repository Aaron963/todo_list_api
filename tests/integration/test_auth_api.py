import requests
import pytest
from tests.utils import test_data_manager

# 基础配置
BASE_URL = "http://localhost:5000/api"


@pytest.fixture(autouse=True)
def setup_and_cleanup():
    """每个测试前后的设置和清理"""
    test_data_manager.clear_all()
    yield
    test_data_manager.clear_all()


def test_register_success():
    """用例AUTH-REG-001：正常注册"""
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "test_reg@example.com",
        "password": "Test123!",
        "full_name": "Test Register"
    })
    result = response.json()

    # 验证响应
    assert response.status_code == 201
    assert result["code"] == 200
    assert result["data"]["user"]["email"] == "test_reg@example.com"
    assert result["data"]["user"]["full_name"] == "Test Register"
    assert "access_token" in result["data"]

    # 保存重要数据
    test_data_manager.save_token("test_user", result["data"]["access_token"])
    test_data_manager.save_user_id("test_user", str(result["data"]["user"]["id"]))


def test_register_duplicate_email():
    """用例AUTH-REG-002：注册重复邮箱"""
    # 先注册一次
    requests.post(f"{BASE_URL}/auth/register", json={
        "email": "dup@example.com",
        "password": "Dup1234!",
        "full_name": "Dup User"
    })

    # 再次注册相同邮箱
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "dup@example.com",
        "password": "Dup1234!",
        "full_name": "Dup Again"
    })
    result = response.json()
    # 验证响应
    assert response.status_code == 409
    assert result["code"] == 409
    assert "already registered" in result["message"]


def test_register_missing_field():
    """用例AUTH-REG-003：注册缺少必填字段"""
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "miss@example.com",
        "password": "Miss123!"
        # 缺少full_name
    })
    result = response.json()

    # 验证响应
    assert response.status_code == 400
    assert result["code"] == 400
    assert "Invalid request data" in result["message"]


def test_register_weak_password():
    """用例AUTH-REG-004：注册密码强度不够"""
    # Condition 1
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "weak@example.com",
        "password": "123123456",  # 密码太弱
        "full_name": "Weak User"
    })
    result = response.json()
    assert response.status_code == 400
    assert result["code"] == 400
    assert "Invalid request data" in result["message"]

    #Condition 2
    response = requests.post(f"{BASE_URL}/auth/register", json={
        "email": "weak@example.com",
        "password": "qqwwwwww",  # 密码太弱
        "full_name": "Weak User"
    })
    result = response.json()
    assert response.status_code == 400
    assert result["code"] == 400
    assert "Invalid request data" in result["message"]


def test_login_success():
    """用例AUTH-LOGIN-001：正常登录"""
    # 先注册
    requests.post(f"{BASE_URL}/auth/register", json={
        "email": "test_login@example.com",
        "password": "Login123!",
        "full_name": "Test Login"
    })

    # 登录
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "test_login@example.com",
        "password": "Login123!"
    })
    result = response.json()

    # 验证响应
    assert response.status_code == 200
    assert result["code"] == 200
    assert "access_token" in result["data"]
    assert result["data"]["user"]["email"] == "test_login@example.com"

    # 保存重要数据
    test_data_manager.save_token("login_user", result["data"]["access_token"])
    test_data_manager.save_user_id("login_user", str(result["data"]["user"]["id"]))


def test_login_invalid_password():
    """用例AUTH-LOGIN-002：密码错误"""
    # 先注册
    requests.post(f"{BASE_URL}/auth/register", json={
        "email": "test_pwd@example.com",
        "password": "Correct123!",
        "full_name": "Test Password"
    })

    # 用错误密码登录
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "test_pwd@example.com",
        "password": "Wrong123!"
    })
    result = response.json()

    # 验证响应
    assert response.status_code == 401
    assert result["code"] == 401
    assert "Invalid email or password" in result["message"]


def test_login_nonexistent_user():
    """用例AUTH-LOGIN-003：不存在的用户"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "Any123!"
    })
    result = response.json()

    # 验证响应
    assert response.status_code == 401
    assert result["code"] == 401
    assert "Invalid email or password" in result["message"]


def test_login_missing_field():
    """用例AUTH-LOGIN-004：登录缺少必填字段"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "test@example.com"
        # 缺少password
    })
    result = response.json()

    # 验证响应
    assert response.status_code == 400
    assert result["code"] == 400
    assert "Invalid request data" in result["message"]


def test_token_validation():
    """用例AUTH-TOKEN-001：验证token有效性"""
    # 注册并登录
    requests.post(f"{BASE_URL}/auth/register", json={
        "email": "token_test@example.com",
        "password": "Token123!",
        "full_name": "Token Test"
    })

    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "token_test@example.com",
        "password": "Token123!"
    })
    token = login_response.json()["data"]["access_token"]
    test_data_manager.save_token("token_user", token)

    # 使用token访问受保护的端点
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/lists", headers=headers)

    # 验证响应
    assert response.status_code == 200
    assert response.json()["code"] == 200


def test_invalid_token():
    """用例AUTH-TOKEN-002：无效token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = requests.get(f"{BASE_URL}/lists", headers=headers)
    result = response.json()

    # 验证响应
    assert response.status_code == 200
    assert result["code"] == 401
    assert "Invalid token" in result["message"]


def test_no_token():
    """用例AUTH-TOKEN-003：没有token"""
    response = requests.get(f"{BASE_URL}/lists")
    result = response.json()

    # 验证响应
    assert response.status_code == 401
    assert result["code"] == 401
    assert "Authentication token is required" in result["message"]


def test_data_manager_functionality():
    """用例DM-001：测试数据管理器功能"""
    # 保存数据
    test_data_manager.save_token("test", "token_123")
    test_data_manager.save_user_id("test", "user_456")
    test_data_manager.save_list_id("test", "list_789")

    # 验证数据获取
    assert test_data_manager.get_token("test") == "token_123"
    assert test_data_manager.get_user_id("test") == "user_456"
    assert test_data_manager.get_list_id("test") == "list_789"

    # 验证认证头
    headers = test_data_manager.get_auth_headers("test")
    assert headers["Authorization"] == "Bearer token_123"

    # 验证摘要
    summary = test_data_manager.get_summary()
    assert summary["tokens"] == 1
    assert summary["user_ids"] == 1
    assert summary["list_ids"] == 1
    assert summary["total"] == 3
