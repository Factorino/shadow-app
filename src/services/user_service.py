from typing import List, Optional

from src.interfaces.user_repository import AbstractUserRepository
from src.models.user import User


class UserService:
    def __init__(self, user_repository: AbstractUserRepository) -> None:
        self._user_repository: AbstractUserRepository = user_repository

    def get_all(self) -> List[User]:
        pass

    def get_filtered(self, is_active: bool) -> List[User]:
        pass

    def get_active_users(self) -> List[User]:
        pass

    def get_inactive_users(self) -> List[User]:
        pass

    def get_by_id(self, user_id: int) -> User:
        pass

    def get_by_username(self, username: str) -> User:
        pass

    def add(self, user: User) -> User:
        pass

    def update(self, user: User) -> User:
        pass

    def delete(self, user_id: int) -> User:
        pass

    def activate_user(self, user_id: int) -> User:
        pass

    def deactivate_user(self, user_id: int) -> User:
        pass

    def change_password(self, user_id: int, new_password: str) -> User:
        pass

    def _validate(self, user: User) -> None:
        if user is None:
            raise ValueError("User cannot be None")

        if not user.username or not user.username.strip():
            raise ValueError("Username cannot be empty")

        if not user.password or not user.password.strip():
            raise ValueError("Password cannot be empty")

        if len(user.username) < 3 or len(user.username) > 50:
            raise ValueError("Username must be between 3 and 50 characters")

        if len(user.password) < 8 or len(user.username) > 50:
            raise ValueError("Password must be between 8 and 50 characters")

        existing_user: Optional[User] = self._user_repository.find_by_username(
            user.username
        )
        if existing_user is not None and existing_user.id != user.id:
            raise ValueError(f"User with username {user.username} already exists")
