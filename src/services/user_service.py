from typing import List, Optional

from src.interfaces.user_repository import AbstractUserRepository
from src.models.user import User


class UserService:
    def __init__(self, user_repository: AbstractUserRepository) -> None:
        self._user_repository: AbstractUserRepository = user_repository

    def get_all(self) -> List[User]:
        return self._user_repository.get_all()

    def get_filtered(self, is_active: bool) -> List[User]:
        return self._user_repository.get_filtered(is_active=is_active)

    def get_active_users(self) -> List[User]:
        return self._user_repository.get_filtered(is_active=True)

    def get_inactive_users(self) -> List[User]:
        return self._user_repository.get_filtered(is_active=False)

    def get_by_id(self, user_id: int) -> User:
        user: Optional[User] = self._user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} not found")
        return user

    def get_by_username(self, username: str) -> User:
        user: Optional[User] = self._user_repository.find_by_username(username)
        if user is None:
            raise ValueError(f"User with username {username} not found")
        return user

    def add(self, user: User) -> User:
        self._validate(user)
        return self._user_repository.add(user)

    def update(self, user: User) -> User:
        self._validate(user)

        if user.id is None:
            raise ValueError("Cannot update user without ID")

        existing_user: Optional[User] = self._user_repository.find_by_id(user.id)
        if existing_user is None:
            raise ValueError(f"User with ID {user.id} not found")

        updated_user: Optional[User] = self._user_repository.update(user)
        if updated_user is None:
            raise ValueError(f"Failed to update user with ID {user.id}")

        return updated_user

    def delete(self, user_id: int) -> User:
        deleted_user: Optional[User] = self._user_repository.delete(user_id)
        if deleted_user is None:
            raise ValueError(f"User with ID {user_id} not found")
        return deleted_user

    def activate_user(self, user_id: int) -> User:
        user: Optional[User] = self._user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} not found")

        user.is_active = True
        return self.update(user)

    def deactivate_user(self, user_id: int) -> User:
        user: Optional[User] = self._user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} not found")

        user.is_active = False
        return self.update(user)

    def change_password(self, user_id: int, new_password: str) -> User:
        user: Optional[User] = self._user_repository.find_by_id(user_id)
        if user is None:
            raise ValueError(f"User with ID {user_id} not found")

        user.password = new_password
        return self.update(user)

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
