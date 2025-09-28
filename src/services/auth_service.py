from typing import Optional

from src.models.user import User
from src.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self._user_service: UserService = user_service

    def register(self, username: str, password: str) -> User:
        user = User(username=username, password=password)
        return self._user_service.add(user)

    def login(self, username: str, password: str) -> User:
        user: User = self._user_service.get_by_username(username)

        if not user.is_active:
            raise ValueError("User account is deactivated")

        if user.password != password:
            raise ValueError("Invalid password")

        return user

    def change_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> User:
        user: User = self._user_service.get_by_id(user_id)

        if user.password != old_password:
            raise ValueError("Current password is incorrect")

        user.password = new_password
        return self._user_service.update(user)

    def is_authenticated(self, user_id: int) -> bool:
        try:
            user: User = self._user_service.get_by_id(user_id)
            return user.is_active
        except ValueError:
            return False

    def get_current_user(self, user_id: int) -> Optional[User]:
        try:
            return self._user_service.get_by_id(user_id)
        except ValueError:
            return None
