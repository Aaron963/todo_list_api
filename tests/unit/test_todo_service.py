import pytest
from datetime import datetime
from app.services.todo_service import TodoService
from app.models.todos import TodoStatus, TodoPriority
from app.dto.todo_dto import TodoCreate
from app.utils.error_handlers import ResourceNotFoundError, ForbiddenError

def test_create_todo(db_session, test_user):
    """Test creating a TODO with tags."""
    # Arrange
    todo_service = TodoService(db_session)
    todo_create = TodoCreate(
        name="Finish API design",
        description="Complete TODO list API docs",
        due_date=datetime(2024, 12, 31),
        status=TodoStatus.IN_PROGRESS,
        priority=TodoPriority.HIGH,
        tag_names=["work", "urgent"]
    )
    # Act
    new_todo = todo_service.create_todo(todo_create, owner_id=test_user.id)
    # Assert
    assert new_todo.id is not None
    assert new_todo.name == "Finish API design"
    assert len(new_todo.tags) == 2
    assert {tag.name for tag in new_todo.tags} == {"work", "urgent"}

def test_get_todo_forbidden(db_session, test_user, another_test_user):
    """Test non-owner/non-admin cannot access a TODO."""
    # Arrange: Create a TODO owned by test_user
    todo_service = TodoService(db_session)
    todo_create = TodoCreate(name="Private TODO")
    new_todo = todo_service.create_todo(todo_create, owner_id=test_user.id)
    # Act + Assert: another_test_user (role=USER) tries to access
    with pytest.raises(ForbiddenError):
        todo_service.get_todo(
            todo_id=new_todo.id,
            user_id=another_test_user.id,
            user_role="USER"
        )