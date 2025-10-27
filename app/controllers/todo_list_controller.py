from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm import Session
from pymongo.collection import Collection
from app.dto.todo_dto import TodoListCreateDTO, TodoListUpdateDTO
from app.models.todos import TodoList
from app.models.users import PermType, Permission
from app.services.todo_service import TodoListService
from app.services.user_service import UserService
from app.extensions.db.db_postgres import get_db
from app.extensions.db.db_mongo import get_mongo_collection
from app.utils.error_handlers import handle_exceptions
from app.utils.errors import ResourceNotFoundError
from flask import request, jsonify
from app.utils.json_encoder import process_data

api = Api(prefix="/api/lists")


def init_app(app):
    """初始化TODO列表API"""
    api.init_app(app)


class TodoListCollection(Resource):
    @jwt_required()
    @handle_exceptions
    def post(self):
        """
        description: Create List
        API: {{base_url}}/api/lists
        """
        user_id = get_jwt_identity()
        data = request.get_json()
        list_create = TodoListCreateDTO(**data)

        # 验证用户
        db: Session = next(get_db())
        user_service = UserService(db)
        user_service.get_user_by_id(user_id)

        # 创建列表
        list_coll: Collection = get_mongo_collection("todo_lists")
        list_service = TodoListService(list_coll)
        new_list = list_service.create_list(TodoList(
            owner_id=str(user_id),
            title=list_create.title,
            description=list_create.description
        ))
        # grant permissions to user
        user_service.grant_list_permission(
            user_id=user_id,
            list_id=new_list.list_id,
            perm_type=PermType.EDIT
        )
        return {
            "code": 200,
            "message": "List created",
            "data": process_data(new_list.model_dump())
        }, 201

    @jwt_required()
    @handle_exceptions
    def get(self):
        """
        description: Get All List
        API: {{base_url}}/api/lists
        """
        user_id = get_jwt_identity()
        db: Session = next(get_db())

        # 获取有权限的列表ID
        perms = db.query(Permission.list_id).filter(Permission.user_id == user_id).all()
        list_ids = [p.list_id for p in perms]

        # 查询列表
        list_coll: Collection = get_mongo_collection("todo_lists")
        list_service = TodoListService(list_coll)
        lists = [list_service.get_list(list_id) for list_id in list_ids]
        
        # 将Pydantic对象转换为dict
        lists_data = [list_obj.model_dump() for list_obj in lists]
        
        return {
            "code": 200,
            "data": process_data(lists_data)
        }, 200


class TodoListResource(Resource):
    @jwt_required()
    @handle_exceptions
    def get(self, list_id: str):
        """
        description: Get Single List
        API: /api/lists/{{list_id}}
        """
        user_id = get_jwt_identity()
        db: Session = next(get_db())
        user_service = UserService(db)
        user_service.check_list_permission(user_id, list_id, PermType.VIEW)

        list_coll: Collection = get_mongo_collection("todo_lists")
        list_service = TodoListService(list_coll)
        todo_list = list_service.get_list(list_id)
        return {
            "code": 200,
            "data": process_data(todo_list.model_dump())
        }, 200

    @jwt_required()
    @handle_exceptions
    def put(self, list_id: str):
        """更新列表"""
        user_id = get_jwt_identity()
        db: Session = next(get_db())
        user_service = UserService(db)
        user_service.check_list_permission(user_id, list_id, PermType.EDIT)

        data = request.get_json()
        update_data = TodoListUpdateDTO(**data).dict(exclude_unset=True)

        list_coll: Collection = get_mongo_collection("todo_lists")
        list_service = TodoListService(list_coll)
        updated_list = list_service.update_list(list_id, update_data)

        return {
            "code": 200,
            "message": "List updated",
            "data": process_data(updated_list.model_dump())
        }, 201

    @jwt_required()
    @handle_exceptions
    def delete(self, list_id: str):
        """delete list by list_id"""
        user_id = get_jwt_identity()
        db: Session = next(get_db())
        user_service = UserService(db)
        user_service.check_list_permission(user_id, list_id, PermType.EDIT)

        # check list is exist
        list_coll: Collection = get_mongo_collection("todo_lists")
        list_service = TodoListService(list_coll)
        
        try:
            # 检查列表是否存在
            list_service.get_list(list_id)
        except ResourceNotFoundError:
            raise ResourceNotFoundError(f"List {list_id} not found")

        # 删除MongoDB中的列表数据
        deleted = list_service.delete_list(list_id)
        
        if not deleted:
            raise ResourceNotFoundError(f"List {list_id} not found")

        # 删除PostgreSQL中的权限记录
        try:
            deleted_perms = user_service.revoke_list_permissions(list_id)
            return {
                "code": 200,
                "message": f"List {list_id} deleted successfully, {deleted_perms} permissions revoked"
            }, 200
        except Exception as e:
            # 如果权限删除失败，记录错误但不影响主要删除操作
            print(f"Warning: Failed to revoke permissions for list {list_id}: {e}")
            return {
                "code": 200,
                "message": f"List {list_id} deleted, but some permissions may remain"
            }, 200


api.add_resource(TodoListCollection, "")
api.add_resource(TodoListResource, "/<string:list_id>")
