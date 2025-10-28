from flask import request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from pymongo.collection import Collection
from datetime import datetime
from app.dto.todo_dto import TodoItemCreateDTO, TodoItemUpdateDTO
from app.models.todos import TodoItem, TodoStatus, TodoPriority
from app.models.users import PermType
from app.services.todo_service import TodoItemService, TodoListService
from app.services.user_service import UserService
from app.extensions.db.db_postgres import get_db
from app.extensions.db.db_mongo import get_mongo_collection
from app.utils.error_handlers import handle_exceptions
from app.utils.errors import ResourceNotFoundError
from app.utils.json_encoder import process_data

api = Api(prefix="/api/lists/<string:list_id>/items")


def init_app(app):
    """初始化TDL APP"""
    api.init_app(app)


class TodoItemCollection(Resource):
    @jwt_required()
    @handle_exceptions
    def post(self, list_id: str):
        """创建TDL的Item"""
        user_id = get_jwt_identity()
        data = request.get_json()
        item_create = TodoItemCreateDTO(**data)

        # 验证权限和列表存在
        db: Session = next(get_db())
        user_service = UserService(db)
        user_service.check_list_permission(user_id, list_id, PermType.EDIT)

        list_coll: Collection = get_mongo_collection("todo_lists")
        list_service = TodoListService(list_coll)
        list_service.get_list(list_id)  # 验证列表存在

        # 创建项
        item_coll: Collection = get_mongo_collection("todo_items")
        item_service = TodoItemService(item_coll)
        new_item = item_service.create_item(TodoItem(
            list_id=list_id,
            title=item_create.title,
            description=item_create.description,
            due_date=item_create.due_date,
            status=TodoStatus(item_create.status) if item_create.status else TodoStatus.NOT_STARTED,
            priority=TodoPriority(item_create.priority) if item_create.priority else TodoPriority.MEDIUM,
            tags=item_create.tags
        ))

        return {
            "code": 200,
            "message": "Item created",
            "data": process_data(new_item.model_dump())
        }, 201

    @jwt_required()
    @handle_exceptions
    def get(self, list_id: str):
        """获取列表中的项（支持过滤排序）"""
        user_id = get_jwt_identity()
        db: Session = next(get_db())
        user_service = UserService(db)
        user_service.check_list_permission(user_id, list_id, PermType.VIEW)

        # 解析查询参数
        status = request.args.get("status")
        due_date_str = request.args.get("due_date")
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None
        sort_by = request.args.get("sort_by", "due_date")
        order = request.args.get("order", "asc")

        # 查询项
        item_coll: Collection = get_mongo_collection("todo_items")
        item_service = TodoItemService(item_coll)
        items = item_service.list_items(
            list_id=list_id,
            status=TodoStatus(status) if status else None,
            due_date=due_date,
            sort_by=sort_by,
            order=order
        )

        return {
            "code": 200,
            "data": process_data([item.model_dump() for item in items])
        }, 200


class TodoItemResource(Resource):
    @jwt_required()
    @handle_exceptions
    def get(self, list_id: str, item_id: str):
        """Get Single item by id"""
        user_id = get_jwt_identity()
        db: Session = next(get_db())
        user_service = UserService(db)
        user_service.check_list_permission(user_id, list_id, PermType.VIEW)

        item_coll: Collection = get_mongo_collection("todo_items")
        item_service = TodoItemService(item_coll)
        item = item_service.get_item(item_id, list_id)

        return {
            "code": 200,
            "data": process_data(item.model_dump())
        }, 200

    @jwt_required()
    @handle_exceptions
    def put(self, list_id: str, item_id: str):
        """更新项"""
        user_id = get_jwt_identity()
        db: Session = next(get_db())
        user_service = UserService(db)
        user_service.check_list_permission(user_id, list_id, PermType.EDIT)

        data = request.get_json()
        update_data = TodoItemUpdateDTO(**data).dict(exclude_unset=True)

        # 转换枚举类型
        if "status" in update_data:
            update_data["status"] = TodoStatus(update_data["status"])
        if "priority" in update_data:
            update_data["priority"] = TodoPriority(update_data["priority"])

        item_coll: Collection = get_mongo_collection("todo_items")
        item_service = TodoItemService(item_coll)
        updated_item = item_service.update_item(item_id, list_id, update_data)

        return {
            "code": 200,
            "message": "Item updated",
            "data": process_data(updated_item.model_dump())
        }, 200

    @jwt_required()
    @handle_exceptions
    def delete(self, list_id: str, item_id: str):
        """删除待办事项 - 检查存在性并验证删除结果"""
        user_id = get_jwt_identity()
        db: Session = next(get_db())
        user_service = UserService(db)
        user_service.check_list_permission(user_id, list_id, PermType.EDIT)

        item_coll: Collection = get_mongo_collection("todo_items")
        item_service = TodoItemService(item_coll)
        
        # 先检查待办事项是否存在
        try:
            item_service.get_item(item_id, list_id)
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"Item {item_id} in list {list_id} not found")

        # 执行删除操作
        deleted = item_service.delete_item(item_id, list_id)
        
        if not deleted:
            raise ResourceNotFoundError(f"Item {item_id} in list {list_id} not found or already deleted")

        return {
            "code": 200,
            "message": f"Item {item_id} deleted successfully"
        }, 200


api.add_resource(TodoItemCollection, "")
api.add_resource(TodoItemResource, "/<string:item_id>")
