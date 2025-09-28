from typing import Optional

from src.models.user import User
from src.services.user_service import UserService


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self._user_service: UserService = user_service

    def register(self, username: str, password: str) -> User:
        pass

    def login(self, username: str, password: str) -> User:
        pass

    def change_password(
        self, user_id: int, old_password: str, new_password: str
    ) -> User:
        pass

    def is_authenticated(self, user_id: int) -> bool:
        pass

    def get_current_user(self, user_id: int) -> Optional[User]:
        pass
