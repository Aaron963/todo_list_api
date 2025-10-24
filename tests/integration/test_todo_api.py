import pytest
from datetime import datetime
from flask import json

def test_create_todo_api(client, auth_headers):
    """Test creating a TODO via API."""
    # Arrange
    todo_data = {
        "name": "Test API TODO",
        "description": "Created via integration test",
        "due_date": "2024-12-31T00:00:00Z",
        "status": "In Progress",
        "priority": "High",
        "tag_names": ["test", "api"]
    }
    # Act
    response = client.post(
        "/api/todos",
        data=json.dumps(todo_data),
        headers=auth_headers,
        content_type="application/json"
    )
    # Assert
    assert response.status_code == 201
    data = response.json
    assert data["name"] == "Test API TODO"
    assert data["tags"] == ["test", "api"]

def test_list_todos_filter_sort_api(client, auth_headers, test_todo):
    """Test filtering and sorting TODOs via API."""
    # Act: Filter by status=Completed, sort by name (desc)
    response = client.get(
        "/api/todos?status=Completed&sort_by=name&order=desc",
        headers=auth_headers
    )
    # Assert
    assert response.status_code == 200
    data = response.json
    assert len(data) >= 1
    assert data[0]["status"] == "Completed"
    # Verify sorting (names are in descending order)
    names = [todo["name"] for todo in data]
    assert names == sorted(names, reverse=True)