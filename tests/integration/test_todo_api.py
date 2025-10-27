import requests

# 基础配置（替换为你的服务地址和端口）
BASE_URL = "http://localhost:5000/api"



def test_todo_list_create_success(client, auth_headers, clean_db):
    """用例LIST-CRE-001：已认证用户创建列表"""
    url = f"{BASE_URL}/lists"
    response = requests.post(
        url,
        headers=auth_headers,
        json={
        "title": "Work List",
        "description": "Daily work tasks"
        }
    )
    res_json = response.json()

    # 验证响应
    assert response.status_code == 200
    assert res_json["code"] == 200
    assert res_json["data"]["title"] == "Work List"
    assert "id" in res_json["data"]  # 确保返回列表ID


def test_todo_list_create_unauthorized(client, clean_db):
    """用例LIST-CRE-002：未认证用户创建列表"""
    data = {
        "title": "Unauth List",
        "description": "Should fail"
    }
    # 不传递auth_headers
    response = client.post("/api/lists", json=data)
    res_json = response.get_json()

    # 验证响应
    assert response.status_code == 401
    assert res_json["code"] == 401
    assert "未授权" in res_json["message"]


def test_todo_list_create_missing_title(client, auth_headers, clean_db):
    """用例LIST-CRE-003：创建列表缺少title字段"""
    data = {
        "description": "No Title List"  # 缺少title
    }
    response = client.post(
        "/api/lists",
        headers=auth_headers,
        json=data
    )
    res_json = response.get_json()

    # 验证响应
    assert response.status_code == 400
    assert res_json["code"] == 400
    assert "缺少必填字段title" in res_json["message"]


def test_todo_list_get_all(client, auth_headers, clean_db):
    """用例LIST-GET-001：查询当前用户所有列表"""
    # 先创建2个列表
    client.post(
        "/api/lists",
        headers=auth_headers,
        json={"title": "List 1", "description": "First list"}
    )
    client.post(
        "/api/lists",
        headers=auth_headers,
        json={"title": "List 2", "description": "Second list"}
    )

    # 查询所有列表
    response = client.get("/api/lists", headers=auth_headers)
    res_json = response.get_json()

    # 验证响应
    assert response.status_code == 200
    assert res_json["code"] == 200
    assert len(res_json["data"]) == 2  # 应返回2个列表


def test_todo_list_get_single_success(client, auth_headers, clean_db):
    """用例LIST-GET-002：查询指定存在的列表（本人创建）"""
    # 先创建列表
    create_res = client.post(
        "/api/lists",
        headers=auth_headers,
        json={"title": "Single List", "description": "Get single test"}
    )
    list_id = create_res.get_json()["data"]["id"]

    # 查询该列表
    response = client.get(f"/api/lists/{list_id}", headers=auth_headers)
    res_json = response.get_json()

    # 验证响应
    assert response.status_code == 200
    assert res_json["code"] == 200
    assert res_json["data"]["id"] == list_id
    assert res_json["data"]["title"] == "Single List"


def test_todo_list_get_other_user_list(client, auth_headers, other_auth_headers, clean_db):
    """用例LIST-GET-003：查询其他用户创建的列表"""
    # 其他用户创建列表
    create_res = client.post(
        "/api/lists",
        headers=other_auth_headers,  # 用其他用户的认证头
        json={"title": "Other User List", "description": "Private list"}
    )
    other_list_id = create_res.get_json()["data"]["id"]

    # 当前用户尝试查询其他用户的列表
    response = client.get(f"/api/lists/{other_list_id}", headers=auth_headers)
    res_json = response.get_json()

    # 验证响应
    assert response.status_code == 403
    assert res_json["code"] == 403
    assert "没有权限执行此操作" in res_json["message"]


def test_todo_list_get_nonexistent(client, auth_headers, clean_db):
    """用例LIST-GET-004：查询不存在的列表ID"""
    nonexistent_id = "99999"  # 不存在的列表ID
    response = client.get(f"/api/lists/{nonexistent_id}", headers=auth_headers)
    res_json = response.get_json()

    # 验证响应
    assert response.status_code == 404
    assert res_json["code"] == 404
    assert "请求的资源不存在" in res_json["message"]


def test_todo_list_update_success(client, auth_headers, clean_db):
    """用例LIST-UPD-001：本人更新列表信息"""
    # 先创建列表
    create_res = client.post(
        "/api/lists",
        headers=auth_headers,
        json={"title": "Old Title", "description": "Old desc"}
    )
    list_id = create_res.get_json()["data"]["id"]

    # 更新列表
    update_data = {
        "title": "Updated Title",
        "description": "Updated desc"
    }
    response = client.put(
        f"/api/lists/{list_id}",
        headers=auth_headers,
        json=update_data
    )
    res_json = response.get_json()

    # 验证响应
    assert response.status_code == 200
    assert res_json["code"] == 200
    assert res_json["data"]["title"] == "Updated Title"
    assert res_json["data"]["description"] == "Updated desc"


def test_todo_list_update_other_user(client, auth_headers, other_auth_headers, clean_db):
    """用例LIST-UPD-002：更新其他用户的列表"""
    # 其他用户创建列表
    create_res = client.post(
        "/api/lists",
        headers=other_auth_headers,
        json={"title": "Other User List", "description": "Cannot update"}
    )
    other_list_id = create_res.get_json()["data"]["id"]

    # 当前用户尝试更新
    update_data = {"title": "Hacked Title"}
    response = client.put(
        f"/api/lists/{other_list_id}",
        headers=auth_headers,
        json=update_data
    )
    res_json = response.get_json()

    # 验证响应
    assert response.status_code == 403
    assert res_json["code"] == 403
    assert "没有权限" in res_json["message"]


def test_todo_list_delete_success(client, auth_headers, clean_db):
    """用例LIST-DEL-001：本人删除列表"""
    # 先创建列表
    create_res = client.post(
        "/api/lists",
        headers=auth_headers,
        json={"title": "To Delete List", "description": "Delete test"}
    )
    list_id = create_res.get_json()["data"]["id"]

    # 删除列表
    response = client.delete(f"/api/lists/{list_id}", headers=auth_headers)
    res_json