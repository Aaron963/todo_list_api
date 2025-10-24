from flask import request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.orm import Session
from app.dto.user_dto import UserCreateDTO, UserLoginDTO
from app.services.user_service import UserService
from app.extensions.db.db_postgres import get_db
from app.utils.error_handlers import handle_exceptions

api = Api(prefix="/api/auth")


class Register(Resource):
    @handle_exceptions
    def post(self):
        """注册新用户"""
        data = request.get_json()
        user_create = UserCreateDTO(**data)

        db: Session = next(get_db())
        user_service = UserService(db)
        user = user_service.register_user(user_create)

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.role.value}
        )
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            "code": 201,
            "message": "User registered successfully",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role.value
                }
            }
        }), 201


class Login(Resource):
    @handle_exceptions
    def post(self):
        """用户登录"""
        data = request.get_json()
        user_login = UserLoginDTO(**data)

        db: Session = next(get_db())
        user_service = UserService(db)
        user = user_service.login_user(user_login)

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.role.value}
        )
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            "code": 200,
            "message": "Login successful",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role.value
                }
            }
        })


api.add_resource(Register, "/register")
api.add_resource(Login, "/login")