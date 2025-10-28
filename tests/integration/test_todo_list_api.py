import time

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


def create_test_user(user_key: str, email: str, password: str, full_name: str):
    """创建测试用户并返回认证头"""
    # 注册用户
    register_response = requests.post(url=f"{BASE_URL}/auth/register",
                                      json={
                                          "email": email,
                                          "password": password,
                                          "full_name": full_name
                                      })
    assert register_response.status_code == 201, f"用户注册失败: {user_key}"

    login_response = requests.post(url=f"{BASE_URL}/auth/login",
                                   json={
                                       "email": email,
                                       "password": password
                                   })
    login_data = login_response.json()

    # 保存重要数据
    test_data_manager.save_token(user_key, login_data["data"]["access_token"])
    test_data_manager.save_user_id(user_key, str(login_data["data"]["user"]["id"]))

    return test_data_manager.get_auth_headers(user_key)


def test_todo_list_create_success():
    """用例LIST-CRE-001：已认证用户创建列表"""
    auth_headers = create_test_user("test_create@list.com",
                                    "test_create@list.com",
                                    "Test1232!",
                                    "Test Create User")

    data = {
        "title": "Work List",
        "description": "Daily work tasks"
    }
    response = requests.post(url=f"{BASE_URL}/lists",
                             headers=auth_headers,
                             json=data)
    result = response.json()
    # # 验证响应
    assert response.status_code == 201
    assert result["code"] == 200
    assert result["message"] == "List created"
    assert result["data"]["title"] == "Work List"
    assert result["data"]["description"] == "Daily work tasks"
    assert "list_id" in result["data"]
    assert "owner_id" in result["data"]
    #
    test_data_manager.save_list_id("work_list", result["data"]["list_id"])


def test_todo_list_create_unauthorized():
    """用例LIST-CRE-002：未认证用户创建列表"""
    data = {
        "title": "Unauth List",
        "description": "Should fail"
    }
    response = requests.post(url=f"{BASE_URL}/lists",
                             json=data)
    result = response.json()

    # 验证响应
    assert response.status_code == 401
    assert result["code"] == 401
    assert "Authentication token is required" in result["message"]


def test_todo_list_create_missing_title():
    """用例LIST-CRE-003：创建列表缺少title字段"""
    auth_headers = create_test_user("test_user",
                                    "test_missing@example.com",
                                    "Test123!",
                                    "Test Missing User")
    response = requests.post(f"{BASE_URL}/lists",
                             headers=auth_headers,
                             json={
                                 "description": "No Title List"  # missing title
                             })
    result = response.json()
    assert response.status_code == 400
    assert result["code"] == 400
    assert "invalid request data" in result["message"].lower()


def test_todo_list_get_all():
    """用例LIST-GET-001：查询当前用户所有列表"""
    auth_headers = create_test_user("test_user", "test_get_all@example.com", "Test123!", "Test Get All User")

    # 先创建2个列表
    list1_response = requests.post(f"{BASE_URL}/lists", headers=auth_headers, json={
        "title": "List 1", "description": "First list"
    })
    assert list1_response.status_code == 201
    test_data_manager.save_list_id("list1", list1_response.json()["data"]["list_id"])

    list2_response = requests.post(f"{BASE_URL}/lists", headers=auth_headers, json={
        "title": "List 2", "description": "Second list"
    })
    assert list2_response.status_code == 201
    test_data_manager.save_list_id("list2", list2_response.json()["data"]["list_id"])

    # 查询所有列表
    response = requests.get(f"{BASE_URL}/lists", headers=auth_headers)
    result = response.json()

    # 验证响应
    assert response.status_code == 200
    assert result["code"] == 200
    assert len(result["data"]) == 2  # 应返回2个列表


def test_todo_list_get_single_success():
    """用例LIST-GET-002：查询指定存在的列表（本人创建）"""
    auth_headers = create_test_user("test_user",
                                    "test_get_single@example.com",
                                    "Test123!",
                                    "Test Get Single User")

    # 先创建列表
    create_res = requests.post(url=f"{BASE_URL}/lists",
                               headers=auth_headers,
                               json={
                                   "title": "Single List",
                                   "description": "Get single test"
                               })
    assert create_res.status_code == 201
    list_id = create_res.json()["data"]["list_id"]
    test_data_manager.save_list_id("single_list", list_id)

    # query that list
    response = requests.get(f"{BASE_URL}/lists/{list_id}", headers=auth_headers)
    result = response.json()
    assert response.status_code == 200
    assert result["code"] == 200
    assert result["data"]["list_id"] == list_id
    assert result["data"]["title"] == "Single List"
    assert result["data"]["description"] == "Get single test"


def test_todo_list_get_other_user_list():
    """用例LIST-GET-003：查询其他用户创建的列表"""
    # 创建两个不同的用户
    user1_headers = create_test_user("user1",
                                     "user1@example.com",
                                     "Test123!",
                                     "User 1")
    user2_headers = create_test_user("user2",
                                     "user2@example.com",
                                     "Test123!",
                                     "User 2")

    # 用户2创建列表
    create_res = requests.post(f"{BASE_URL}/lists", headers=user2_headers, json={
        "title": "Other User List", "description": "Private list"
    })
    assert create_res.status_code == 201
    other_list_id = create_res.json()["data"]["list_id"]

    # 用户1尝试查询用户2的列表
    response = requests.get(f"{BASE_URL}/lists/{other_list_id}", headers=user1_headers)
    result = response.json()

    # 验证响应
    assert response.status_code == 403
    assert result["code"] == 403
    assert "permission" in result["message"].lower()


def test_todo_list_get_nonexistent():
    """用例LIST-GET-004：查询不存在的列表ID"""
    auth_headers = create_test_user("test_user",
                                    "test_nonexistent@example.com",
                                    "Test123!",
                                    "Test Nonexistent User")

    nonexistent_id = "list_nonexistent_12345"
    response = requests.get(url=f"{BASE_URL}/lists/{nonexistent_id}",
                            headers=auth_headers)
    result = response.json()
    print('result', result)

    # 验证响应
    assert response.status_code == 404
    assert result["code"] == 404
    assert "not found" in result["message"].lower()


def test_todo_list_update_success():
    """用例LIST-UPD-001：本人更新列表信息"""
    auth_headers = create_test_user("test_user",
                                    "test_update@example.com",
                                    "Test123!",
                                    "Test Update User")

    # 先创建列表
    create_res = requests.post(url=f"{BASE_URL}/lists",
                               headers=auth_headers,
                               json={
                                   "title": "Old Title",
                                   "description": "Old desc"
                               })
    assert create_res.status_code == 201
    list_id = create_res.json()["data"]["list_id"]

    # 更新列表
    update_data = {
        "title": "Updated Title",
        "description": "Updated desc"
    }
    response = requests.put(f"{BASE_URL}/lists/{list_id}", headers=auth_headers, json=update_data)
    result = response.json()

    # 验证响应
    assert response.status_code == 201
    assert result["code"] == 200
    assert result["message"] == "List updated"
    assert result["data"]["title"] == "Updated Title"
    assert result["data"]["description"] == "Updated desc"
    assert result["data"]["list_id"] == list_id


def test_todo_list_update_other_user():
    """用例LIST-UPD-002：更新其他用户的列表"""
    # 创建两个不同的用户
    user1_headers = create_test_user("user1",
                                     "user1_update@example.com",
                                     "Test123!",
                                     "User 1 Update")
    user2_headers = create_test_user("user2",
                                     "user2_update@example.com",
                                     "Test123!",
                                     "User 2 Update")

    # 用户2创建列表
    create_res = requests.post(url=f"{BASE_URL}/lists",
                               headers=user2_headers,
                               json={
                                   "title": "Other User List",
                                   "description": "Cannot update"
                               })
    assert create_res.status_code == 201
    other_list_id = create_res.json()["data"]["list_id"]

    # 用户1尝试更新
    update_data = {"title": "Hacked Title"}
    response = requests.put(f"{BASE_URL}/lists/{other_list_id}", headers=user1_headers, json=update_data)
    result = response.json()

    # 验证响应
    assert response.status_code == 403
    assert result["code"] == 403
    assert "permission" in result["message"].lower()


def test_todo_list_delete_success():
    """用例LIST-DEL-001：本人删除列表"""
    auth_headers = create_test_user("test_user",
                                    "test_delete@example.com",
                                    "Test123!",
                                    "Test Delete User")

    # 先创建列表
    create_res = requests.post(url=f"{BASE_URL}/lists",
                               headers=auth_headers,
                               json={
                                   "title": "To Delete List",
                                   "description": "Delete test"
                               })
    assert create_res.status_code == 201
    list_id = create_res.json()["data"]["list_id"]

    # 删除列表
    response = requests.delete(url=f"{BASE_URL}/lists/{list_id}",
                               headers=auth_headers)
    result = response.json()

    # 验证响应
    assert response.status_code == 200
    assert result["code"] == 200
    assert f"List {list_id} deleted successfully" in result["message"]
    assert "permissions revoked" in result["message"]

    # 验证列表已被删除
    get_response = requests.get(f"{BASE_URL}/lists/{list_id}", headers=auth_headers)
    assert get_response.status_code == 404


def test_todo_list_delete_other_user():
    """用例LIST-DEL-002：删除其他用户的列表"""
    # 创建两个不同的用户
    user1_headers = create_test_user("user1",
                                     "user1_delete@example.com",
                                     "Test123!",
                                     "User 1 Delete")
    user2_headers = create_test_user("user2",
                                     "user2_delete@example.com",
                                     "Test123!",
                                     "User 2 Delete")

    # 用户2创建列表
    create_res = requests.post(url=f"{BASE_URL}/lists",
                               headers=user2_headers,
                               json={
                                   "title": "Other User List",
                                   "description": "Cannot delete"
                               })
    assert create_res.status_code == 201
    other_list_id = create_res.json()["data"]["list_id"]

    # 用户1尝试删除
    response = requests.delete(url=f"{BASE_URL}/lists/{other_list_id}",
                               headers=user1_headers)
    result = response.json()

    # 验证响应
    assert response.status_code == 403
    assert result["code"] == 403
    assert "permission" in result["message"].lower()


def test_todo_list_delete_nonexistent():
    """用例LIST-DEL-003：删除不存在的列表"""
    auth_headers = create_test_user("test_user",
                                    "test_delete_nonexistent@example.com",
                                    "Test123!",
                                    "Test Delete Nonexistent User")

    nonexistent_id = "list_nonexistent_delete"
    response = requests.delete(url=f"{BASE_URL}/lists/{nonexistent_id}",
                               headers=auth_headers)
    result = response.json()
    assert response.status_code == 404
    assert result["code"] == 404
    assert "not found" in result["message"].lower()


def test_todo_list_create_empty_title():
    """用例LIST-CRE-004：创建列表时title为空"""
    auth_headers = create_test_user("test_user",
                                    "test_empty_title@example.com",
                                    "Test123!",
                                    "Test Empty Title User")

    response = requests.post(url=f"{BASE_URL}/lists",
                             headers=auth_headers, json={
            "title": "",  # 空标题
            "description": "Empty title test"
        })
    result = response.json()

    assert response.status_code == 400
    assert result["code"] == 400
    assert "Invalid request data" in result["message"]


def test_todo_list_create_title_too_long():
    """用例LIST-CRE-005：创建列表时title过长"""
    auth_headers = create_test_user("test_user",
                                    "test_long_title@example.com",
                                    "Test123!",
                                    "Test Long Title User")

    response = requests.post(url=f"{BASE_URL}/lists",
                             headers=auth_headers,
                             json={
                                 "title": "A" * 101,  # 超过100字符限制
                                 "description": "Long title test"
                             })
    result = response.json()
    assert response.status_code == 400
    assert result["code"] == 400
    assert "Invalid request data" in result["message"]


def test_todo_list_create_description_too_long():
    """用例LIST-CRE-006：创建列表时description过长"""
    auth_headers = create_test_user("test_user",
                                    "test_long_desc@example.com",
                                    "Test123!",
                                    "Test Long Desc User")

    response = requests.post(url=f"{BASE_URL}/lists",
                             headers=auth_headers,
                             json={
                                 "title": "Valid Title",
                                 "description": "A" * 501  # 超过500字符限制
                             })
    result = response.json()
    assert response.status_code == 400
    assert result["code"] == 400
    assert "Invalid request data" in result["message"]


def test_todo_list_update_partial():
    """用例LIST-UPD-003：部分更新列表信息"""
    auth_headers = create_test_user("test_user",
                                    "test_partial_update@example.com",
                                    "Test123!",
                                    "Test Partial Update User")

    # 先创建列表
    create_res = requests.post(url=f"{BASE_URL}/lists",
                               headers=auth_headers,
                               json={
                                   "title": "Original Title",
                                   "description": "Original desc"
                               })
    assert create_res.status_code == 201
    list_id = create_res.json()["data"]["list_id"]

    # 只更新title
    response = requests.put(url=f"{BASE_URL}/lists/{list_id}",
                            headers=auth_headers,
                            json={"title": "Updated Title Only"})
    result = response.json()

    # 验证响应
    assert response.status_code == 201
    assert result["code"] == 200
    assert result["data"]["title"] == "Updated Title Only"
    assert result["data"]["description"] == "Original desc"  # 应该保持不变


def test_todo_list_get_empty_list():
    """用例LIST-GET-005：查询空列表"""
    auth_headers = create_test_user("test_user",
                                    "test_empty_list@example.com",
                                    "Test123!",
                                    "Test Empty List User")

    response = requests.get(f"{BASE_URL}/lists", headers=auth_headers)
    result = response.json()
    assert response.status_code == 200
    assert result["code"] == 200
    assert result["data"] == []  # 应该返回空列表


def test_todo_list_create_without_description():
    """用例LIST-CRE-007：创建列表时不提供description"""
    auth_headers = create_test_user("test_user",
                                    "test_no_desc@example.com",
                                    "Test123!",
                                    "Test No Desc User")

    response = requests.post(url=f"{BASE_URL}/lists",
                             headers=auth_headers,
                             json={
                                 "title": "No Description List"
                                 # 不提供description字段
                             })
    result = response.json()

    # 验证响应
    assert response.status_code == 201
    assert result["code"] == 200
    assert result["data"]["title"] == "No Description List"
    assert result["data"]["description"] is None


def test_todo_list_update_nonexistent():
    """用例LIST-UPD-004：更新不存在的列表"""
    auth_headers = create_test_user("test_user",
                                    "test_update_nonexistent@example.com",
                                    "Test123!",
                                    "Test Update Nonexistent User")

    nonexistent_id = "list_nonexistent_update"
    response = requests.put(url=f"{BASE_URL}/lists/{nonexistent_id}",
                            headers=auth_headers,
                            json={"title": "Updated Title"})
    result = response.json()
    assert response.status_code == 404
    assert result["code"] == 404
    assert "not found" in result["message"].lower()


def test_cross_user_data_isolation():
    """用例CROSS-001：验证用户间数据隔离"""
    # 创建两个不同的用户
    user1_headers = create_test_user("user1",
                                     "isolation_user1@example.com",
                                     "Test123!",
                                     "Isolation User 1")
    user2_headers = create_test_user("user2",
                                     "isolation_user2@example.com",
                                     "Test123!",
                                     "Isolation User 2")

    # 用户1创建列表
    user1_list = requests.post(url=f"{BASE_URL}/lists",
                               headers=user1_headers,
                               json={
                                   "title": "User 1 List",
                                   "description": "Private to user 1"
                               })
    assert user1_list.status_code == 201
    user1_list_id = user1_list.json()["data"]["list_id"]

    # 用户2创建列表
    user2_list = requests.post(url=f"{BASE_URL}/lists",
                               headers=user2_headers,
                               json={
                                   "title": "User 2 List",
                                   "description": "Private to user 2"
                               })
    assert user2_list.status_code == 201
    user2_list_id = user2_list.json()["data"]["list_id"]

    # 用户1只能看到自己的列表
    user1_lists = requests.get(url=f"{BASE_URL}/lists",
                               headers=user1_headers)
    assert user1_lists.status_code == 200
    user1_lists_data = user1_lists.json()["data"]
    assert len(user1_lists_data) == 1
    assert user1_lists_data[0]["list_id"] == user1_list_id

    # 用户2只能看到自己的列表
    user2_lists = requests.get(url=f"{BASE_URL}/lists",
                               headers=user2_headers)
    assert user2_lists.status_code == 200
    user2_lists_data = user2_lists.json()["data"]
    assert len(user2_lists_data) == 1
    assert user2_lists_data[0]["list_id"] == user2_list_id
