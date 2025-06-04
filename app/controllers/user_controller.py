from flask import request
from controllers.base_controller import BaseController
from services.user_service import UserService

class UserController(BaseController):
    def __init__(self):
        self.user_service = UserService()

    def register(self):
        data = request.get_json()
        success, message = self.user_service.register_user(
            data.get("name"),
            data.get("email"),
            data.get("password")
        )
        if success:
            return self.success_response(message=message, status_code=201)
        return self.error_response(message=message)
    