import requests

# 基础配置（替换为你的服务地址和端口）
BASE_URL = "http://localhost:5000/api"


def test_register_success():
    """测试正常注册"""
    url = f"{BASE_URL}/auth/register"

    response = requests.post(url, json={
        "email": "test_reg@example.com",
        "password": "Test123!",
        "full_name": "Test Register"
    })
    result = response.json()
    assert response.status_code == 201, f"注册失败，状态码：{response.status_code}"
    assert result["code"] == 200, f"响应码错误：{result['code']}"
    assert result["data"]["user"]["email"] == "test_reg@example.com", "邮箱不匹配"

    requests.post(f"{BASE_URL}/auth/register", json={
        "email": "test_pwd@example.com",
        "password": "Correct123!",
        "full_name": "Test Password"
    })
    result = response.json()
    assert response.status_code == 201, f"注册失败，状态码：{response.status_code}"
    assert result["code"] == 200, f"响应码错误：{result['code']}"
    assert result["data"]["user"]["email"] == "test_reg@example.com", "邮箱不匹配"


def test_register_password_strength():
    """注册的密码强度不够"""
    url = f"{BASE_URL}/auth/register"
    response = requests.post(url, json={
        "email": "password_strength@example.com",
        "password": "d1234!",
        "full_name": "Dup User"
    })
    result = response.json()
    assert response.status_code == 400, "密码强度不够，返回400"
    assert "Invalid request data" in result["message"], "错误信息不正确"


def test_register_duplicate_email():
    """测试注册重复邮箱"""
    url = f"{BASE_URL}/auth/register"
    # 先注册一次
    requests.post(url, json={
        "email": "dup@example.com",
        "password": "Dup1234!",
        "full_name": "Dup User"
    })
    # 再次注册相同邮箱
    response = requests.post(url, json={
        "email": "dup@example.com",
        "password": "Dup1234!",
        "full_name": "Dup Again"
    })
    result = response.json()
    assert response.status_code == 409, "重复注册应返回409"
    assert "Email dup@example.com already registered" in result["message"], "错误信息不正确"


def test_login_success():
    """测试登录成功"""
    # 先注册
    requests.post(f"{BASE_URL}/auth/register", json={
        "email": "test_login@example.com",
        "password": "Login123!",
        "full_name": "Test Login"
    })
    # 登录请求
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": "test_login@example.com",
        "password": "Login123!"
    }
    response = requests.post(url, json=data)
    result = response.json()

    assert response.status_code == 200, "登录失败"
    assert "access_token" in result["data"], "未返回token"
    assert result["data"]["user"]["email"] == "test_login@example.com", "用户信息错误"


def test_login_invalid_password():
    """测试账号或密码错误"""
    # 先注册

    # 用错误密码登录
    url = f"{BASE_URL}/auth/login"
    data = {
        "email": "test_pwd@example.com",
        "password": "Wrong123!"
    }
    response = requests.post(url, json=data)
    result = response.json()

    assert response.status_code == 401, "密码错误应返回401"
    assert "Invalid email or password" in result["message"], "错误信息不正确"
