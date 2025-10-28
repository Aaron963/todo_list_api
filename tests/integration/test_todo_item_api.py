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


def create_test_list(auth_headers, list_key: str, title: str, description: str = None):
    """创建测试列表并返回列表ID"""
    data = {"title": title}
    if description:
        data["description"] = description

    response = requests.post(url=f"{BASE_URL}/lists",
                             headers=auth_headers,
                             json=data)
    assert response.status_code == 201
    list_id = response.json()["data"]["list_id"]
    test_data_manager.save_list_id(list_key, list_id)
    return list_id


def test_todo_item_create_success():
    """用例ITEM-CRE-001：已认证用户创建待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_create@example.com",
                                    "Test123!",
                                    "Test Create User")
    list_id = create_test_list(auth_headers, "test_list",
                               "Test List",
                               "Test Description")

    response = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                             headers=auth_headers,
                             json={
                                 "title": "Complete API Documentation",
                                 "description": "Write Postman import documentation",
                                 "due_date": "2024-12-31T23:59:59Z",
                                 "status": "In Progress",
                                 "priority": "High",
                                 "tags": ["docs", "urgent"]
                             })
    result = response.json()
    # 验证响应
    assert response.status_code == 201
    assert result["code"] == 200
    assert result["message"] == "Item created"
    assert result["data"]["title"] == "Complete API Documentation"
    assert result["data"]["description"] == "Write Postman import documentation"
    assert result["data"]["list_id"] == list_id
    assert "item_id" in result["data"]
    #
    test_data_manager.save_item_id("work_item", result["data"]["item_id"])


def test_todo_item_create_unauthorized():
    """用例ITEM-CRE-002：未认证用户创建待办事项"""
    list_id = "list_123"
    data = {
        "title": "Unauth Task",
        "description": "Should fail"
    }
    response = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                             json=data)
    result = response.json()
    assert response.status_code == 401
    assert result["code"] == 401
    assert "Authentication token is required" == result["message"]


def test_todo_item_create_missing_title():
    """用例ITEM-CRE-003：创建待办事项缺少title字段"""
    auth_headers = create_test_user("test_user",
                                    "test_missing@example.com",
                                    "Test123!",
                                    "Test Missing User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")
    response = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                             headers=auth_headers,
                             json={
                                 "description": "No Title Task"  # 缺少title
                             })
    result = response.json()
    assert response.status_code == 400
    assert result["code"] == 400
    assert "invalid request data" == result["message"]


def test_todo_item_create_invalid_list():
    """用例ITEM-CRE-004：在不存在的列表中创建待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_invalid_list@example.com",
                                    "Test123!",
                                    "Test Invalid List User")

    nonexistent_list_id = "list_nonexistent"
    response = requests.post(url=f"{BASE_URL}/lists/{nonexistent_list_id}/items",
                             headers=auth_headers,
                             json={
                                 "title": "Task in Invalid List",
                                 "description": "Should fail"
                             })
    result = response.json()
    assert response.status_code == 403
    assert result["code"] == 403
    assert "no permission" in result["message"]


def test_todo_item_get_all():
    """用例ITEM-GET-001：查询列表中的所有待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_get_all@example.com",
                                    "Test123!",
                                    "Test Get All User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    # 先创建2个待办事项
    item1_response = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                                   headers=auth_headers,
                                   json={
                                       "title": "Task 1",
                                       "description": "First task"
                                   })
    assert item1_response.status_code == 201
    test_data_manager.save_item_id("item1", item1_response.json()["data"]["item_id"])

    item2_response = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                                   headers=auth_headers,
                                   json={
                                       "title": "Task 2",
                                       "description": "Second task"
                                   })
    assert item2_response.status_code == 201
    test_data_manager.save_item_id("item2", item2_response.json()["data"]["item_id"])

    # 查询所有待办事项
    response = requests.get(f"{BASE_URL}/lists/{list_id}/items", headers=auth_headers)
    result = response.json()
    assert response.status_code == 200
    assert result["code"] == 200
    assert len(result["data"]) == 2  # 应返回2个待办事项


def test_todo_item_get_single_success():
    """用例ITEM-GET-002：查询指定存在的待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_get_single@example.com",
                                    "Test123!",
                                    "Test Get Single User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    # 先创建待办事项
    create_res = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                               headers=auth_headers,
                               json={
                                   "title": "Single Task",
                                   "description": "Get single test"
                               })
    assert create_res.status_code == 201
    item_id = create_res.json()["data"]["item_id"]
    test_data_manager.save_item_id("single_item", item_id)

    # 查询该待办事项
    response = requests.get(f"{BASE_URL}/lists/{list_id}/items/{item_id}", headers=auth_headers)
    result = response.json()

    assert response.status_code == 200
    assert result["code"] == 200
    assert result["data"]["item_id"] == item_id
    assert result["data"]["title"] == "Single Task"
    assert result["data"]["description"] == "Get single test"


def test_todo_item_get_other_user_list():
    """用例ITEM-GET-003：查询其他用户列表中的待办事项"""
    # 创建两个不同的用户
    user1_headers = create_test_user("user1",
                                     "user1@example.com",
                                     "Test123!",
                                     "User 1")
    user2_headers = create_test_user("user2",
                                     "user2@example.com",
                                     "Test123!",
                                     "User 2")

    # 用户2创建列表和待办事项
    list_id = create_test_list(user2_headers,
                               "other_list",
                               "Other User List")
    create_res = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                               headers=user2_headers,
                               json={
                                   "title": "Other User Task",
                                   "description": "Private task"
                               })
    assert create_res.status_code == 201
    item_id = create_res.json()["data"]["item_id"]

    # 用户1尝试查询用户2的待办事项
    response = requests.get(url=f"{BASE_URL}/lists/{list_id}/items/{item_id}",
                            headers=user1_headers)
    result = response.json()

    assert response.status_code == 403
    assert result["code"] == 403
    assert "permission" in result["message"].lower()


def test_todo_item_get_nonexistent():
    """用例ITEM-GET-004：查询不存在的待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_nonexistent@example.com",
                                    "Test123!",
                                    "Test Nonexistent User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    nonexistent_item_id = "item_nonexistent_12345"
    response = requests.get(url=f"{BASE_URL}/lists/{list_id}/items/{nonexistent_item_id}",
                            headers=auth_headers)
    result = response.json()
    assert response.status_code == 404
    assert result["code"] == 404
    assert "not found" in result["message"].lower()


def test_todo_item_update_success():
    """用例ITEM-UPD-001：本人更新待办事项信息"""
    auth_headers = create_test_user("test_user",
                                    "test_update@example.com",
                                    "Test123!",
                                    "Test Update User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    # 先创建待办事项
    create_res = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                               headers=auth_headers,
                               json={
                                   "title": "Old Task",
                                   "description": "Old desc"
                               })
    assert create_res.status_code == 201
    item_id = create_res.json()["data"]["item_id"]

    # 更新待办事项
    response = requests.put(url=f"{BASE_URL}/lists/{list_id}/items/{item_id}",
                            headers=auth_headers,
                            json={
                                "title": "Updated Task",
                                "description": "Updated desc",
                                "status": "IN_PROGRESS"
                            })
    result = response.json()
    assert response.status_code == 200
    assert result["code"] == 200
    assert result["message"] == "Item updated"
    assert result["data"]["title"] == "Updated Task"
    assert result["data"]["description"] == "Updated desc"
    assert result["data"]["item_id"] == item_id  # ID应该保持不变


def test_todo_item_update_other_user():
    """用例ITEM-UPD-002：更新其他用户的待办事项"""
    # 创建两个不同的用户
    user1_headers = create_test_user("user1",
                                     "user1_update@example.com",
                                     "Test123!",
                                     "User 1 Update")
    user2_headers = create_test_user("user2",
                                     "user2_update@example.com",
                                     "Test123!",
                                     "User 2 Update")

    # 用户2创建列表和待办事项
    list_id = create_test_list(user2_headers,
                               "other_list",
                               "Other User List")
    create_res = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                               headers=user2_headers,
                               json={
                                   "title": "Other User Task",
                                   "description": "Cannot update"
                               })
    assert create_res.status_code == 201
    item_id = create_res.json()["data"]["item_id"]

    # 用户1尝试更新
    update_data = {"title": "Hacked Task"}
    response = requests.put(url=f"{BASE_URL}/lists/{list_id}/items/{item_id}",
                            headers=user1_headers,
                            json=update_data)
    result = response.json()

    assert response.status_code == 403
    assert result["code"] == 403
    assert "no permission" in result["message"].lower()


def test_todo_item_delete_success():
    """用例ITEM-DEL-001：本人删除待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_delete@example.com",
                                    "Test123!",
                                    "Test Delete User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    # 先创建待办事项
    create_res = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                               headers=auth_headers,
                               json={
                                   "title": "To Delete Task",
                                   "description": "Delete test"
                               })
    assert create_res.status_code == 201
    item_id = create_res.json()["data"]["item_id"]

    # 删除待办事项
    response = requests.delete(url=f"{BASE_URL}/lists/{list_id}/items/{item_id}",
                               headers=auth_headers)
    result = response.json()
    assert response.status_code == 200
    assert result["code"] == 200
    assert f"Item {item_id} deleted successfully" in result["message"]

    # 验证待办事项已被删除
    get_response = requests.get(url=f"{BASE_URL}/lists/{list_id}/items/{item_id}",
                                headers=auth_headers)
    assert get_response.status_code == 404


def test_todo_item_delete_other_user():
    """用例ITEM-DEL-002：删除其他用户的待办事项"""
    # 创建两个不同的用户
    user1_headers = create_test_user("user1",
                                     "user1_delete@example.com",
                                     "Test123!",
                                     "User 1 Delete")
    user2_headers = create_test_user("user2",
                                     "user2_delete@example.com",
                                     "Test123!",
                                     "User 2 Delete")

    # 用户2创建列表和待办事项
    list_id = create_test_list(user2_headers,
                               "other_list",
                               "Other User List")
    create_res = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                               headers=user2_headers,
                               json={
                                   "title": "Other User Task",
                                   "description": "Cannot delete"
                               })
    assert create_res.status_code == 201
    item_id = create_res.json()["data"]["item_id"]

    # 用户1尝试删除
    response = requests.delete(url=f"{BASE_URL}/lists/{list_id}/items/{item_id}",
                               headers=user1_headers)
    result = response.json()
    assert response.status_code == 403
    assert result["code"] == 403
    assert "no permission" in result["message"].lower()


def test_todo_item_delete_nonexistent():
    """用例ITEM-DEL-003：删除不存在的待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_delete_nonexistent@example.com",
                                    "Test123!",
                                    "Test Delete Nonexistent User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    nonexistent_item_id = "item_nonexistent_delete"
    response = requests.delete(url=f"{BASE_URL}/lists/{list_id}/items/{nonexistent_item_id}",
                               headers=auth_headers)
    result = response.json()
    assert response.status_code == 404
    assert result["code"] == 404
    assert "not found" in result["message"].lower()


def test_todo_item_create_empty_title():
    """用例ITEM-CRE-005：创建待办事项时title为空"""
    auth_headers = create_test_user("test_user",
                                    "test_empty_title@example.com",
                                    "Test123!",
                                    "Test Empty Title User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    response = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                             headers=auth_headers,
                             json={
                                 "title": "",  # 空标题
                                 "description": "Empty title test"
                             })
    result = response.json()
    assert response.status_code == 400
    assert result["code"] == 400
    assert "Invalid request data" in result["message"]


def test_todo_item_create_without_description():
    """用例ITEM-CRE-006：创建待办事项时不提供description"""
    auth_headers = create_test_user("test_user",
                                    "test_no_desc@example.com",
                                    "Test123!",
                                    "Test No Desc User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    data = {
        "title": "No Description Task"
        # 不提供description字段
    }
    response = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                             headers=auth_headers,
                             json=data)
    result = response.json()
    assert response.status_code == 201
    assert result["code"] == 200
    assert result["data"]["title"] == "No Description Task"
    assert result["data"]["description"] is None


def test_todo_item_update_partial():
    """用例ITEM-UPD-003：部分更新待办事项信息"""
    auth_headers = create_test_user("test_user",
                                    "test_partial_update@example.com",
                                    "Test123!",
                                    "Test Partial Update User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    # 先创建待办事项
    create_res = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                               headers=auth_headers,
                               json={
                                   "title": "Original Task",
                                   "description": "Original desc"
                               })
    assert create_res.status_code == 201
    item_id = create_res.json()["data"]["item_id"]

    # 只更新title
    update_data = {"title": "Updated Task Only"}
    response = requests.put(url=f"{BASE_URL}/lists/{list_id}/items/{item_id}",
                            headers=auth_headers,
                            json=update_data)
    result = response.json()
    assert response.status_code == 200
    assert result["code"] == 200
    assert result["data"]["title"] == "Updated Task Only"
    assert result["data"]["description"] == "Original desc"  # 应该保持不变


def test_todo_item_get_empty_list():
    """用例ITEM-GET-005：查询空列表中的待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_empty_list@example.com",
                                    "Test123!",
                                    "Test Empty List User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    response = requests.get(url=f"{BASE_URL}/lists/{list_id}/items",
                            headers=auth_headers)
    result = response.json()
    assert response.status_code == 200
    assert result["code"] == 200
    assert result["data"] == []  # 应该返回空列表


def test_todo_item_update_nonexistent():
    """用例ITEM-UPD-004：更新不存在的待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_update_nonexistent@example.com",
                                    "Test123!",
                                    "Test Update Nonexistent User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    nonexistent_item_id = "item_nonexistent_update"
    response = requests.put(url=f"{BASE_URL}/lists/{list_id}/items/{nonexistent_item_id}",
                            headers=auth_headers,
                            json={"title": "Updated Task"})
    result = response.json()
    assert response.status_code == 404
    assert result["code"] == 404
    assert "not found" in result["message"]


def test_todo_item_filter_by_status():
    """用例ITEM-FILTER-001：按状态过滤待办事项"""
    auth_headers = create_test_user("test_user",
                                    "test_filter@example.com",
                                    "Test123!",
                                    "Test Filter User")
    list_id = create_test_list(auth_headers,
                               "test_list",
                               "Test List")

    # 创建不同状态的待办事项
    result = requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                  headers=auth_headers,
                  json={
                      "title": "Not Started Task",
                      "status": "NOT_STARTED"
                  })
    print('result', result)

    result= requests.post(url=f"{BASE_URL}/lists/{list_id}/items",
                  headers=auth_headers,
                  json={
                      "title": "In Progress Task",
                      "status": "IN_PROGRESS"
                  })
    print('result', result)

    # 按状态过滤
    response = requests.get(url=f"{BASE_URL}/lists/{list_id}/items?status=NOT_STARTED",
                            headers=auth_headers)
    result = response.json()
    print('result', result)
    # assert response.status_code == 200
    # assert result["code"] == 200
    # assert len(result["data"]) == 1
    # assert result["data"][0]["status"] == "NOT_STARTED"


def test_todo_item_sort_by_due_date():
    """用例ITEM-SORT-001：按截止日期排序待办事项"""
    auth_headers = create_test_user("test_user", "test_sort@example.com", "Test123!", "Test Sort User")
    list_id = create_test_list(auth_headers, "test_list", "Test List")

    # 创建不同截止日期的待办事项
    requests.post(f"{BASE_URL}/lists/{list_id}/items", headers=auth_headers, json={
        "title": "Later Task", "due_date": "2024-12-31"
    })
    requests.post(f"{BASE_URL}/lists/{list_id}/items", headers=auth_headers, json={
        "title": "Earlier Task", "due_date": "2024-01-01"
    })

    # 按截止日期排序
    response = requests.get(f"{BASE_URL}/lists/{list_id}/items?sort_by=due_date&order=asc", headers=auth_headers)
    result = response.json()

    # 验证响应
    assert response.status_code == 200
    assert result["code"] == 200
    assert len(result["data"]) == 2
    assert result["data"][0]["title"] == "Earlier Task"  # 应该按日期升序排列
