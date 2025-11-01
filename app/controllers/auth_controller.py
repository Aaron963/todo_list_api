from flask_restful import Resource, Api
from flask_jwt_extended import create_access_token, create_refresh_token
from app.dto.user_dto import UserCreateDTO, UserLoginDTO
from app.services.user_service import UserService
from app.extensions.db.db_postgres import get_db
from app.utils.error_handlers import handle_exceptions
from flask import request

api = Api(prefix="/api/auth")


def init_app(app):
    api.init_app(app)


class Register(Resource):
    @handle_exceptions
    def post(self):
        """
        User Registration
        {{base_url}}/api/auth/register
        Returns:

        """
        user_service = UserService(next(get_db()))
        user = user_service.register_user(UserCreateDTO(**request.get_json()))
        access_token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.role.value}
        )
        refresh_token = create_refresh_token(identity=user.id)
        return {
            "code": 200,
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
        }, 201


class Login(Resource):
    @handle_exceptions
    def post(self):
        """
        User Login(token will be expired by 1 day)
        {{base_url}}/api/auth/login
        Returns:

        """
        # 1, transfer json to DataModel
        login_data = UserLoginDTO(**request.get_json())

        # 2, query from database
        user_service = UserService(next(get_db()))
        user = user_service.login_user(login_data)

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"role": user.role.value}
        )
        refresh_token = create_refresh_token(identity=user.id)
        return {
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
        }, 200


api.add_resource(Register, "/register")
api.add_resource(Login, "/login")
