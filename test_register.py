#!/usr/bin/env python3
"""
测试脚本：验证注册API是否正常工作
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_register_success():
    """测试正常注册"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "test_reg@example.com",
        "password": "Test123!",
        "full_name": "Test Register"
    }
    
    try:
        response = requests.post(url, json=data)
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 注册成功!")
            print(f"用户ID: {result['data']['user']['id']}")
            print(f"邮箱: {result['data']['user']['email']}")
            print(f"访问令牌: {result['data']['access_token'][:20]}...")
            return True
        else:
            print("❌ 注册失败")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Flask应用正在运行")
        return False
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False

if __name__ == "__main__":
    test_register_success()

