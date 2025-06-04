from werkzeug.security import generate_password_hash
from repositories.user_repository import UserRepository
from services.base_service import BaseService


class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()


    def register_user(self, name, email, password):
        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            return False, "User already exists"

        hashed_password = generate_password_hash(password)
        user_hash = self.generate_user_hash(email)
        data = {
            'name': name,
            'email': email,
            'password': hashed_password,
            'user_id': user_hash
        }
        self.user_repository.create_user(data)
        return True, "User registered successfully"
