from pymongo.collection import Collection
from typing import List, Optional
from datetime import datetime
from app.models.todos import TodoList, TodoItem, TodoStatus, TodoPriority
from app.utils.errors import ResourceNotFoundError
from app.extensions.db.db_redis import cache

class TodoListService:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_list(self, list_data: TodoList) -> TodoList:
        list_dict = list_data.model_dump()
        self.collection.insert_one(list_dict)
        return TodoList(**list_dict)

    def get_list(self, list_id: str) -> TodoList:
        doc = self.collection.find_one({"list_id": list_id})
        if not doc:
            raise ResourceNotFoundError(f"List {list_id} not found")
        return TodoList(**doc)

    def update_list(self, list_id: str, update_data: dict) -> TodoList:
        update_data["updated_at"] = datetime.utcnow()
        result = self.collection.find_one_and_update(
            {"list_id": list_id},
            {"$set": update_data},
            return_document=True
        )
        if not result:
            raise ResourceNotFoundError(f"List {list_id} not found")
        return TodoList(**result)

    def delete_list(self, list_id: str) -> bool:
        result = self.collection.delete_one({"list_id": list_id})
        return result.deleted_count == 1


class TodoItemService:
    def __init__(self, collection: Collection):
        self.collection = collection

    def create_item(self, item_data: TodoItem) -> TodoItem:
        item_dict = item_data.model_dump()
        self.collection.insert_one(item_dict)
        return TodoItem(**item_dict)

    def get_item(self, item_id: str, list_id: str) -> TodoItem:
        doc = self.collection.find_one({"item_id": item_id, "list_id": list_id})
        if not doc:
            raise ResourceNotFoundError(f"Item {item_id} in list {list_id} not found")
        return TodoItem(**doc)

    def list_items(
            self,
            list_id: str,
            status: Optional[TodoStatus] = None,
            due_date: Optional[datetime] = None,
            sort_by: str = "due_date",
            order: str = "asc"
    ) -> List[TodoItem]:
        query = {"list_id": list_id}

        # 过滤
        if status:
            query["status"] = status.value
        if due_date:
            query["due_date"] = {"$lte": due_date}

        # 排序
        sort_dir = 1 if order.lower() == "asc" else -1
        valid_fields = ["due_date", "status", "title", "priority", "created_at"]
        sort_field = sort_by if sort_by in valid_fields else "due_date"

        # 查询
        cursor = self.collection.find(query).sort(sort_field, sort_dir)
        return [TodoItem(**item) for item in cursor]

    def update_item(self, item_id: str, list_id: str, update_data: dict) -> TodoItem:
        update_data["updated_at"] = datetime.utcnow()
        result = self.collection.find_one_and_update(
            {"item_id": item_id, "list_id": list_id},
            {"$set": update_data},
            return_document=True
        )
        if not result:
            raise ResourceNotFoundError(f"Item {item_id} in list {list_id} not found")
        return TodoItem(**result)

    def delete_item(self, item_id: str, list_id: str) -> bool:
        result = self.collection.delete_one({"item_id": item_id, "list_id": list_id})
        return result.deleted_count == 1